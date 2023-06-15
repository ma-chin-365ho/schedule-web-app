#!/bin/bash
source setup.sh
docker run -p 8001:8001 -e DYNAMO_ENDPOINT=http://host.docker.internal:8000 -e AWS_REGION=localhost aaronshaf/dynamodb-admin:latest