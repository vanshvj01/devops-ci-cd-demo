pipeline {
    agent any
    triggers {
        pollSCM('* * * * *')          // check GitHub every minute; a new commit starts the pipeline
    }
    environment {
        IMAGE = "devops-ci-cd-demo"
        TAG   = "${env.BUILD_NUMBER}"
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/vanshvj01/devops-ci-cd-demo.git'
            }
        }
        stage('Install & Test') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -q -r requirements.txt
                    python app.py
                    pytest -v --junitxml=test-results.xml
                '''
            }
            post { always { junit 'test-results.xml' } }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build --build-arg BASE_IMAGE=ubuntu-local:noble -t $IMAGE:$TAG -t $IMAGE:latest .'
                sh 'docker images $IMAGE'
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f k8s/
                    kubectl set image deployment/student-result student-result=$IMAGE:$TAG
                    kubectl rollout status deployment/student-result --timeout=120s
                    kubectl get pods,svc -l app=student-result -o wide
                '''
            }
        }
        stage('Verify') {
            steps {
                sh '''
                    NODE_IP=$(kubectl get nodes -o jsonpath="{.items[0].status.addresses[0].address}")
                    sleep 3
                    curl -s --noproxy "*" http://$NODE_IP:30080/health
                '''
            }
        }
    }
    post {
        success { echo "Deployed ${IMAGE}:${TAG} to Kubernetes" }
        failure { echo 'Pipeline failed - check the stage logs' }
    }
}
