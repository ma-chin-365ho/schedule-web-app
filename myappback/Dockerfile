FROM cimg/base:2022.09

# exists: python3
RUN sudo apt-get update && \
    sudo apt-get install npm && \
    sudo npm install -g serverless && \
    mkdir co && \
    mkdir ci && \
    cd ci && \
    sudo sudo serverless create -t aws-python3 -n ci && \
    sudo serverless plugin install -n serverless-python-requirements && \
    sudo serverless plugin install -n serverless-wsgi && \
    sudo serverless plugin install -n serverless-dynamodb-local && \
    sed -i -e "s/http:/https:/" node_modules/dynamodb-localhost/dynamodb/config.json && \
    sed -i -e "s/\"http\"/\"https\"/" node_modules/dynamodb-localhost/dynamodb/installer.js && \
    sudo apt-get install default-jdk && \
    sudo serverless dynamodb install && \
    sudo apt-get install python3-venv && \
    python3 -m venv venv && \
    source venv/bin/activate && \
    pip install flask && \
    pip install boto3 && \
    pip install pytest && \
    pip install requests