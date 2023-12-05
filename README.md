# k8s-files

https://helm.sh/docs/intro/quickstart/
helm install rabbitmq bitnami/rabbitmq
minikube service rabbitmq
#get user and password through the way written in the stdout and replace in the python files



eval $(minikube -p minikube docker-env)

for flask app:

 - docker build -t flask-app:latest . 
 - kubectl apply -f flask-deployment.yaml 
 - kubectl apply -f flask-service.yaml 
 - minikube service flask-app-service

for rabbit-app

 - docker build -t rabbit-app:latest .
 - kubectl apply -f pika-deployment.yaml
 - kubectl apply -f rabbit-app-service.yaml
 - minikube service rabbit-app
