This is a sample application demo setup of ECS, Step Functions and Lambda using AWS CDK.

Python is used as language runtime to set up both the cdk application and needed lambda functions.

```shell
export ACCOUNT_ID=$(aws sts get-caller-identity --output text --query Account)
export AWS_REGION=$(aws configure get region)
```

```shell
git clone https://gitlab.aws.dev/hansnesb/ecs_scaling_with_step_functions.git
cd ecs_scaling_with_step_functions/infra
cdk deploy --auto-approve
```

```shell
aws application-autoscaling describe-scalable-targets --service-namespace ecs | jq '.ScalableTargets[].SuspendedState'
```

```shell
cd ..
aws sns publish --message file://../message.txt --subject Test \
--topic-arn arn:aws:sns:$AWS_REGION:$ACCOUNT_ID\:customer_topic
```

```shell
cdk destroy
```