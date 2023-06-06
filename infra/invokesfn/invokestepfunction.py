import boto3
import datetime
import os
import json

client = boto3.client('stepfunctions')

stateMachineArn = os.environ['sfn_arn']

def is_state_machine_running(stateMachineArn):
    
    state_machine_executions = client.list_executions(
        stateMachineArn=stateMachineArn,
        statusFilter='RUNNING',
        maxResults=100
    )
    
    try:
        if state_machine_executions['executions'][0]['status'] == 'RUNNING':
            return True
    except:
        return False

def start_state_machine(stateMachineArn):

    datetime_now = datetime.datetime.now()
    
    input_data = {
        'wait_seconds': 500
    }

    response = client.start_execution(
        stateMachineArn=stateMachineArn,
        name = 'ecs-pause-scaling' + '-' + datetime_now.strftime("%m-%d-%Y-%H-%M-%S"),
        input=json.dumps(input_data)
    )

def lambda_handler(event, context):
    
    if is_state_machine_running(stateMachineArn) == False:
        start_state_machine(stateMachineArn)