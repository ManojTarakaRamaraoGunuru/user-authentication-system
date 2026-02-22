import logging
import time
import os
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Create logs directory
os.makedirs("logs", exist_ok=True)

# Configure custom logger for file output
logger = logging.getLogger("custom.api")
logger.setLevel(logging.INFO)
logger.propagate = False
logger.handlers.clear()

# Add file handler
file_handler = logging.FileHandler("logs/custom_api.log", encoding='utf-8')
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s | %(levelname)-8s | %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S'
))
logger.addHandler(file_handler)


def register_middlewares(app:FastAPI):
    
    @app.middleware("http")
    async def comprehensive_logging(request: Request, call_next):
        start_time = time.time()
        
        # Log request start
        logger.info(f"→ {request.method} {request.url.path} starting...")
        
        # Get client info
        client = f"{request.client.host}:{request.client.port}"
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Status emoji based on response code
            if response.status_code < 300:
                emoji = "✅"
            elif response.status_code < 400:
                emoji = "⚠️"
            else:
                emoji = "❌"
            
            # Readable log message
            log_message = (
                f"{emoji} {client} | "
                f"{request.method:4} {request.url.path} | "
                f"Status: {response.status_code} | "
                f"Time: {process_time*1000:.1f}ms | "
                f"Size: {response.headers.get('content-length', '-')}B"
            )
                
            # Log at different levels based on status
            if response.status_code >= 500:
                logger.error(log_message)
            elif response.status_code >= 400:
                logger.warning(log_message)
            else:
                logger.info(log_message)
                
            # Add response header with processing time
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            # Log exceptions
            logger.exception(
                f"💥 {client} | {request.method} {request.url.path} | "
                f"Error: {str(e)}"
            )
            raise
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1"],
    )