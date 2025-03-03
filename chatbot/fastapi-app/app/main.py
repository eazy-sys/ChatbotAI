import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import openai
import json
import os

# Configure detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_openai_client():
    """Initialize and return the OpenAI client."""
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        
        if not api_key or not azure_endpoint:
            raise ValueError("Missing required environment variables: OPENAI_API_KEY or AZURE_OPENAI_ENDPOINT")
        
        logger.info(f"Initializing Azure OpenAI client with endpoint: {azure_endpoint}")
        logger.info(f"API Key (first 5 chars): {api_key[:5]}...")
        
        # Configure OpenAI for Azure
        openai.api_type = "azure"
        openai.api_base = azure_endpoint
        openai.api_version = "2024-02-15-preview"
        openai.api_key = api_key
        
        # Test the connection by listing models
        try:
            models = openai.Model.list()
            logger.info("Successfully connected to Azure OpenAI")
            logger.info("Available models:")
            for model in models['data']:
                logger.info(f"- {model['id']}")
        except Exception as e:
            logger.error(f"Failed to list models: {str(e)}")
            raise Exception(f"Failed to connect to Azure OpenAI: {str(e)}")
            
        return openai
    except Exception as e:
        logger.error(f"Failed to initialize Azure OpenAI client: {str(e)}")
        raise Exception(f"Failed to initialize Azure OpenAI client: {str(e)}")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    logger.info(f"Headers: {dict(request.headers)}")
    
    response = await call_next(request)
    
    logger.info(f"Response status: {response.status_code}")
    return response

@app.get("/")
async def root():
    logger.info("Serving index.html")
    try:
        return FileResponse("static/index.html")
    except Exception as e:
        logger.error(f"Error serving index.html: {str(e)}")
        raise HTTPException(status_code=500, detail="Error serving index.html")

@app.get("/favicon.ico")
async def favicon():
    logger.info("Serving favicon.ico")
    try:
        return FileResponse("static/favicon.ico")
    except Exception as e:
        logger.error(f"Error serving favicon.ico: {str(e)}")
        return JSONResponse(status_code=404, content={})

@app.options("/chat")
async def chat_options():
    logger.info("Handling OPTIONS request for /chat")
    return JSONResponse(content={})

@app.post("/chat")
async def chat(request: Request):
    try:
        logger.info("Received chat request")
        body = await request.json()
        logger.info(f"Request body: {body}")
        
        if "message" not in body:
            logger.error("Missing 'message' field")
            raise HTTPException(status_code=400, detail="Message field is required")
        
        try:
            client = get_openai_client()
        except Exception as e:
            logger.error(f"Failed to get OpenAI client: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
            
        # Use the correct GPT-4 deployment name
        deployment_name = "gpt-4"  # This matches your Azure OpenAI deployment
        logger.info(f"Creating chat completion with deployment: {deployment_name}")
        
        try:
            completion = client.ChatCompletion.create(
                engine=deployment_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": body["message"]}
                ],
                max_tokens=800
            )
            
            response = {"response": completion.choices[0].message.content}
            logger.info(f"Chat completion successful")
            return response
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"OpenAI API error: {error_msg}")
            if "model not found" in error_msg.lower():
                logger.error("Model not found. Available deployments:")
                try:
                    models = client.Model.list()
                    for model in models['data']:
                        logger.error(f"- {model['id']}")
                except Exception as list_error:
                    logger.error(f"Failed to list models: {str(list_error)}")
            return JSONResponse(
                status_code=500,
                content={
                    "error": "OpenAI API error",
                    "detail": error_msg
                }
            )
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "detail": str(e)
            }
        ) 