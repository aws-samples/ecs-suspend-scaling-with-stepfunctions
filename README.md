This is a sample application demo setup of ECS, Step Functions and Lambda using AWS CDK.

Python is used as language runtime to set up both the cdk application and needed lambda functions.

```shell
export ACCOUNT_ID=$(aws sts get-caller-identity --output text --query Account)
export AWS_REGION=$(curl -s 169.254.169.254/latest/dynamic/instance-identity/document | jq -r '.region')
```

```shell
git clone https://gitlab.aws.dev/hansnesb/ecs_scaling_with_step_functions.git
cd ecs_scaling_with_step_functions/infra
cdk deploy --auto-approve
```

```shell
cd ..
aws sns publish --message file://../message.txt --subject Test \
--topic-arn arn:aws:sns:$AWS_REGION:$ACCOUNT_ID\:customer_topic
```