pipeline {
    agent any
    options {
        skipDefaultCheckout(true)     // checkout is done in our own Checkout stage
    }
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
                checkout scm              // same repository and branch as the job (GitHub, main)
                sh 'git log -1 --oneline'
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
            post {
                always  { junit 'test-results.xml' }
                success { archiveArtifacts artifacts: 'app.py, Dockerfile, k8s/*.yaml, test-results.xml', fingerprint: true }
            }
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
                    kubectl get deployment,pods -l app=student-result -o wide
                    kubectl get service student-result-svc
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
