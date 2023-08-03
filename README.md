# ECS scaling with Step Functions

For applications that notify their user base of certain events, they may experience a rapid increase in traffic. If this increase is not accounted for, it can cause your users to experience slowness.
This repository contains sample code that uses Step Functions to pause the scale-down of an ECS Fargate Service via SNS notifications. The infrastructure is deployed utilizing AWS CDK.
Once a message is sent to the SNS topic, a subscribed Lambda function will invoke the Step Functions state machine. 

The state machine will:

1. Pause the scale-down of tasks within the ECS service.
2. Scale up the ECS service to its maximum configured task count.
3. wait for a specified duration of time.
4. Resume the scale-down process. 

## Prerequisite

* Set up your AWS CLI. 
* Install the latest version of AWS CDK. We used Version 2.54.0 AWS CDK
* Python3  

## Deploy 

Set required environment variables
```shell
export ACCOUNT_ID=$(aws sts get-caller-identity --output text --query Account)
export AWS_REGION=$(aws configure get region)
```

clone code repository and deploy infrastructure
```shell
git clone https://github.com/aws-samples/ecs-suspend-scaling-with-stepfunctions.git
cd ecs-suspend-scaling-with-stepfunctions/infra
pip install -r requirements.txt
cdk deploy --auto-approve
```
Prior to sending a message to the SNS topic, review the configuration of the scalable targets
```shell
aws application-autoscaling describe-scalable-targets --service-namespace ecs | jq '.ScalableTargets[].SuspendedState'
```
Publish a notification to SNS
```shell
aws sns publish --message file://./message.txt --subject Test \
--topic-arn arn:aws:sns:$AWS_REGION:$ACCOUNT_ID\:customer_topic
```

Review paused scalable targets 
```shell
aws application-autoscaling describe-scalable-targets --service-namespace ecs | jq '.ScalableTargets[].SuspendedState'
```
clean up
```shell
cdk destroy
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
