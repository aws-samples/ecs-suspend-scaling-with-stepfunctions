export ACCOUNT_ID=$(aws sts get-caller-identity --output text --query Account)
export AWS_REGION=$(curl -s 169.254.169.254/latest/dynamic/instance-identity/document | jq -r '.region')

cd infra/
cdk deploy --auto-approve

cd ..
aws sns publish --message file://../message.txt --subject Test \
--topic-arn arn:aws:sns:$AWS_REGION:$ACCOUNT_ID\:customer_topic