#!/bin/bash
set -e

NAMESPACE=airbnb-mlops

echo "🚀 Deploying Airbnb MLOps stack to namespace: $NAMESPACE"
kubectl config use-context minikube

kubectl apply -f k8s/00-namespace.yaml

kubectl apply -n $NAMESPACE -f k8s/01-secret.yaml
kubectl apply -n $NAMESPACE -f k8s/02-configmap.yaml

kubectl apply -n $NAMESPACE -f k8s/03-postgres.yaml
kubectl rollout status deployment/airbnb-db -n $NAMESPACE || true

kubectl apply -n $NAMESPACE -f k8s/04-api.yaml
kubectl rollout status deployment/airbnb-api -n $NAMESPACE

kubectl apply -n $NAMESPACE -f k8s/06-ui.yaml
kubectl apply -n $NAMESPACE -f k8s/07-ui-service.yaml
kubectl rollout status deployment/airbnb-ui -n $NAMESPACE

kubectl apply -n $NAMESPACE -f k8s/05-ingress.yaml

echo "🔎 Pods:"
kubectl get pods -n $NAMESPACE

echo "🌐 Ingress:"
kubectl get ingress -n $NAMESPACE

echo "✅ Deployment completed successfully"
