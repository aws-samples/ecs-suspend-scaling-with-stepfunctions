import boto3

client = boto3.client('application-autoscaling')

def lambda_handler(event, context):
    
    response = client.register_scalable_target(
        ServiceNamespace='ecs',
        ResourceId='service/ecs-scaling-example/service_1',
        ScalableDimension='ecs:service:DesiredCount',
        SuspendedState={
            'DynamicScalingInSuspended': False
        }
    )
