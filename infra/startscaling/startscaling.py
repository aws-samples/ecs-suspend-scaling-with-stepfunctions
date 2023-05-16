import boto3

app_auto_scaling = boto3.client('application-autoscaling')

def lambda_handler(event, context):
    
    response = app_auto_scaling.register_scalable_target(
        ServiceNamespace='ecs',
        ResourceId='service/ecs-scaling-example/service_1',
        ScalableDimension='ecs:service:DesiredCount',
        SuspendedState={
            'DynamicScalingInSuspended': False
        }
    )
