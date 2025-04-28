# Azure AI Chatbot on AKS

## Project Overview
This project demonstrates the implementation of an AI-powered chatbot using Azure OpenAI's GPT-4 model, deployed on Azure Kubernetes Service (AKS). The chatbot provides real-time responses to user queries through a modern web interface.

## Purpose
This project serves as a practical demonstration of:
- Cloud-native application development
- Kubernetes orchestration and deployment
- AI/ML integration in production environments
- Modern web application architecture
- DevOps best practices

## Key Learning Outcomes
1. **Cloud Infrastructure**
   - Azure Kubernetes Service (AKS) deployment
   - Azure Container Registry (ACR) integration
   - Azure OpenAI API integration

2. **Container Orchestration**
   - Kubernetes deployment management
   - Service and ingress configuration
   - Pod lifecycle management

3. **AI Integration**
   - Azure OpenAI API implementation
   - Real-time chat processing
   - Error handling and logging

4. **Web Development**
   - FastAPI backend implementation
   - Modern web interface
   - CORS and security best practices

## Architecture Diagram
```
External User                 Azure Kubernetes Service (AKS)                     Azure Services
     │                                │
     │                                │
     │                                │
     │    ┌──────────────────────────────────────────┐
     │    │                          │               │
     │    │     ┌─────────────┐      │               │
     └────┼────▶│   Ingress   │      │               │
          │     │  Controller  │      │               │
          │     └──────┬──────┘      │               │
          │            │             │               │
          │            │             │               │
          │     ┌──────┴──────┐      │               │         ┌──────────────┐
          │     │ Service     │      │               │         │              │
          │     │(ClusterIP)  │      │               │         │              │
          │     └──────┬──────┘      │               │    ┌────▶  Azure      │
          │            │             │               │    │    │  OpenAI      │
          │    ┌───────┴───────┐     │               │    │    │  (GPT-4)    │
          │    │   Pod         │     │               │    │    │              │
          │    │ ┌───────────┐ │     │               │    │    └──────────────┘
          │    │ │  FastAPI  ├─┼─────┼───────────────┼────┘
          │    │ │           │ │     │               │         ┌──────────────┐
          │    │ └───────────┘ │     │               │         │   Azure      │
          │    └───────────────┘     │               │         │  Container   │
          │                          │               │         │  Registry    │
          └──────────────────────────────────────────┘         └──────────────┘


Flow:
1. User sends request to public IP
2. NGINX Ingress Controller routes request
3. Kubernetes Service directs to Pod
4. FastAPI app in Pod processes request
5. Azure OpenAI API generates response
6. Response returns through same path
```

## Technical Stack
- **Backend**: FastAPI (Python 3.9)
- **AI Model**: Azure OpenAI GPT-4
- **Container Runtime**: Docker
- **Orchestration**: Azure Kubernetes Service (AKS)
- **Registry**: Azure Container Registry (ACR)
- **API Version**: Azure OpenAI API 2024-02-15-preview

## Project Structure
```
chatbot/fastapi-app/
├── app/
│   └── main.py          # FastAPI application
├── kubernetes/
│   ├── deployment.yaml  # Kubernetes deployment
│   ├── service.yaml     # Service configuration
│   ├── ingress.yaml    # Ingress rules
│   └── secrets.yaml     # OpenAI credentials
├── static/
│   ├── index.html      # Web interface
│   └── favicon.ico     # Site favicon
├── Dockerfile          # Container image definition
├── requirements.txt    # Python dependencies
└── start.sh           # Application startup script
```

## Key Features
- Real-time chat interface with Azure OpenAI integration
- Kubernetes-native deployment with proper resource management
- CORS-enabled API endpoints for web client integration
- Comprehensive error handling and logging
- Health check endpoints for Kubernetes probes

## Dependencies
```python
fastapi==0.109.2
uvicorn==0.27.1
openai==0.28.1
python-multipart==0.0.9
python-jose==3.3.0
passlib==1.7.4
python-dotenv==1.0.1
aiofiles==23.2.1
```

## Setup Instructions

### Prerequisites
- Azure subscription
- Azure CLI installed
- kubectl installed
- Docker installed
- Python 3.9+

### 1. Azure OpenAI Setup
```bash
# Create a .env file with your credentials
OPENAI_API_KEY="your-api-key"
AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
```

### 2. Build and Push Docker Image
```bash
# Build image
docker build -t your-acr-name.azurecr.io/chatbot:latest .

# Push to ACR
docker push your-acr-name.azurecr.io/chatbot:latest
```

### 3. Deploy to Kubernetes
```bash
# Apply configurations
kubectl apply -f kubernetes/secrets.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/ingress.yaml

# Verify deployment
kubectl get pods,services,ingress
```

## API Endpoints

### Chat Endpoint
- **URL**: `/chat`
- **Method**: `POST`
- **Request Body**:
```json
{
    "message": "Your message here"
}
```
- **Response**:
```json
{
    "response": "AI-generated response"
}
```

### Health Check
- **URL**: `/`
- **Method**: `GET`
- **Response**: HTML interface

## Monitoring and Logs
```bash
# View pod logs
kubectl logs -f deployment/chatbot-deployment

# Check pod status
kubectl get pods -l app=chatbot
```

## Troubleshooting
1. If pods are in `ImagePullBackOff`:
   - Verify ACR credentials
   - Check image name and tag

2. If pods are in `CrashLoopBackOff`:
   - Check logs with `kubectl logs`
   - Verify environment variables

3. If ingress isn't working:
   - Verify ingress controller is running
   - Check ingress configuration

## Security Considerations
- All sensitive data (API keys, endpoints) are stored as Kubernetes secrets
- CORS is configured to restrict access to specific origins
- Ingress rules are implemented for traffic management
- No sensitive data is logged or exposed in responses
- Environment variables are properly managed

## Future Improvements
1. Add authentication layer
2. Implement rate limiting
3. Add message history persistence
4. Enhance error handling
5. Add monitoring with Prometheus/Grafana
6. Implement CI/CD pipeline with GitHub Actions
7. Add automated testing
8. Implement chat history and user sessions

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
MIT License - feel free to use this project for learning and development!

## Acknowledgments
- Azure OpenAI for providing the GPT-4 model
- FastAPI team for the excellent web framework
- Kubernetes community for container orchestration tools
  
