import boto3

app_auto_scaling = boto3.client('application-autoscaling')
ecs = boto3.client('ecs')

def lambda_handler(event, context):
    
    response = app_auto_scaling.register_scalable_target(
        ServiceNamespace='ecs',
        ResourceId='service/ecs-scaling-example/service_1',
        ScalableDimension='ecs:service:DesiredCount',
        SuspendedState={
            'DynamicScalingInSuspended': True
        }
    )
    
    describe_target = app_auto_scaling.describe_scalable_targets(
        ServiceNamespace='ecs',
    )
    
    scale_service = ecs.update_service(
        cluster='ecs-scaling-example',
        service='service_1',
        desiredCount=describe_target["ScalableTargets"][0]["MaxCapacity"]
    )
