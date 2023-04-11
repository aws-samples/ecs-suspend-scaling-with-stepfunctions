import aws_cdk as cdk
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_ecs_patterns as ecs_patterns

from constructs import Construct

class InfraStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        notification_topic = cdk.aws_sns.Topic(self, "Topic",
            display_name="Customer notification topic",
            topic_name="customer_topic"
        )
        
        cluster = ecs.Cluster(self, "FargateCluster", 
            cluster_name = "ecs-scaling-example"
        )
        
        load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
            cluster = cluster,
            service_name = "service_1",
            memory_limit_mib=512,
            desired_count=1,
            cpu=256,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
            )
        )
        
        scalable_target = load_balanced_fargate_service.service.auto_scale_task_count(
            min_capacity=1,
            max_capacity=5
        )
        
        scalable_target.scale_on_cpu_utilization("CpuScaling",
            target_utilization_percent=50
        )
        
        
        stop_scaling_lambda = cdk.aws_lambda.Function(
            self, 'stopscaling',
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_9,
            code=cdk.aws_lambda.Code.from_asset('stopscaling'),
            handler='stopscaling.lambda_handler',
        )

        stop_scaling_lambda.role.attach_inline_policy(cdk.aws_iam.Policy(self, "stop_scaling_lambda_policy",
            statements=[cdk.aws_iam.PolicyStatement(
                actions=[
                    "application-autoscaling:RegisterScalableTarget",
                    "application-autoscaling:DescribeScalableTargets",
                    "ecs:UpdateService"
                ],
                resources=["*"]
            )]
        ))
        
        start_scaling_lambda = cdk.aws_lambda.Function(
            self, 'startscaling',
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_9,
            code=cdk.aws_lambda.Code.from_asset('startscaling'),
            handler='startscaling.lambda_handler',
        )
        
        start_scaling_lambda.role.attach_inline_policy(cdk.aws_iam.Policy(self, "start_scaling_lambda_policy",
            statements=[cdk.aws_iam.PolicyStatement(
                actions=[
                    "application-autoscaling:RegisterScalableTarget",
                    "application-autoscaling:DescribeScalableTargets",
                    "ecs:UpdateService"
                ],
                resources=["*"]
            )]
        ))
        
        stop_scaling_task = cdk.aws_stepfunctions_tasks.LambdaInvoke(self, "InvokeStopScalingLambda",
            lambda_function=stop_scaling_lambda
        )
        
        start_scaling_task = cdk.aws_stepfunctions_tasks.LambdaInvoke(self, "InvokeStartScalingLambda",
            lambda_function=start_scaling_lambda
        )
        
        wait = cdk.aws_stepfunctions.Wait(self, "Wait",
            time=cdk.aws_stepfunctions.WaitTime.duration(cdk.Duration.seconds(500))
        )

        start_state = cdk.aws_stepfunctions.Pass(self, "StartState")

        scaling_state_machine = cdk.aws_stepfunctions.StateMachine(self, "StateMachine",
            definition=start_state.next(stop_scaling_task).next(wait).next(start_scaling_task)
        )

        invoke_state_machine_lambda = cdk.aws_lambda.Function(self, 'invokestatemachine',
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_9,
            code=cdk.aws_lambda.Code.from_asset('invokesfn'),
            handler='invokestepfunction.lambda_handler',
            environment={ 
                "sfn_arn": scaling_state_machine.state_machine_arn
            },
        )

        invoke_state_machine_lambda.role.attach_inline_policy(cdk.aws_iam.Policy(self, "invoke_state_machine_lambda_policy",
            statements=[cdk.aws_iam.PolicyStatement(
                actions=[
                    "states:*"
                ],
                resources=[scaling_state_machine.state_machine_arn]
            )]
        ))
        
        notification_topic.add_subscription(
            cdk.aws_sns_subscriptions.LambdaSubscription(invoke_state_machine_lambda)
            
        )