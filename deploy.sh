#!/bin/sh

if [ -z ${LAMBDA_TAG+x} ]; then
    echo "LAMBDA_TAG is unset";
else
    aws s3 cp lambda.zip s3://bazwilliams.lambdas/pollen-count-${LAMBDA_TAG}.zip
    aws cloudformation deploy --stack-name=pollen-count-backend --template-file=./lambda.yaml --parameter-overrides LambdaTag=${LAMBDA_TAG} --capabilities=CAPABILITY_IAM
fi
