name: Deploy to AKS

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:

    - name: Checkout Repository
      uses: actions/checkout@v4

    - name: Log in to Azure
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}

    - name: Set up Docker
      run: |
        az acr login --name juniochatbotacr

    - name: Build and Push Docker Image
      run: |
        cd chatbot/fastapi-app
        docker build -t juniochatbotacr.azurecr.io/fastapi-app:latest .
        docker push juniochatbotacr.azurecr.io/fastapi-app:latest

    - name: Get AKS Credentials
      run: |
        az aks get-credentials --resource-group OpenAI-RG --name OpenAI-AKS

    - name: Create OpenAI secret
      run: |
        kubectl create secret generic openai-secret \
          --from-literal=OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }} \
          --dry-run=client -o yaml | kubectl apply -f -

    - name: Deploy to AKS
      run: |
        cd chatbot/fastapi-app/kubernetes
        kubectl apply -f deployment.yaml
        kubectl apply -f service.yaml
        kubectl apply -f ingress.yaml

    - name: Verify Deployment
      run: kubectl get pods -o wide
