# devops-ci-cd-demo

Student Result Service used for the DevOps lab (Batch A3, K. J. Somaiya School of Engineering).

- `app.py` - small Python web service (`python app.py serve` on port 8000)
- `test_app.py` - pytest unit tests
- `Dockerfile` - container image
- `k8s/` - Kubernetes Deployment and NodePort Service
- `Jenkinsfile` - CI/CD pipeline: checkout, test, build image, deploy to Kubernetes
