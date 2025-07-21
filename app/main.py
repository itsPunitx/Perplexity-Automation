import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.automator import PerplexityAutomator
from .config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Global automator instance
automator = PerplexityAutomator()

# Lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up Perplexity Automation API")
    try:
        await automator.setup_browser()
        logger.info("Browser setup completed")
    except Exception as e:
        logger.error(f"Failed to setup browser: {str(e)}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Perplexity Automation API")
    await automator.cleanup()

# FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Automate searches on Perplexity.AI without using the official API",
    version="1.0.0",
    docs_url="/docs" if settings.environment == "development" else None,
    redoc_url="/redoc" if settings.environment == "development" else None,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class SearchRequest(BaseModel):
    prompt: str
    timeout: Optional[int] = 30

class SearchResponse(BaseModel):
    success: bool
    answer: Optional[str] = None
    sources: Optional[List[Dict[str, str]]] = None
    execution_time: Optional[float] = None
    error: Optional[str] = None
    prompt: str

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Perplexity Automation API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "perplexity-automation-api"}

# GET endpoint for search (for simple testing)
@app.get("/search", response_model=SearchResponse)
async def search_get(
    prompt: str = Query(..., description="The search query to send to Perplexity"),
    timeout: int = Query(30, description="Timeout in seconds for the search")
):
    """
    Search Perplexity.AI with a GET request
    
    Example: GET /search?prompt=What is artificial intelligence?
    """
    try:
        result = await automator.search_perplexity(prompt, timeout)
        return SearchResponse(**result)
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )

# POST endpoint for search (more robust)
@app.post("/search", response_model=SearchResponse)
async def search_post(request: SearchRequest):
    """
    Search Perplexity.AI with a POST request
    
    Body:
    {
        "prompt": "What is artificial intelligence?",
        "timeout": 30
    }
    """
    try:
        result = await automator.search_perplexity(request.prompt, request.timeout)
        return SearchResponse(**result)
    except Exception as e:
        logger.error(f"Search failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )

# Batch search endpoint
@app.post("/batch-search")
async def batch_search(prompts: List[str], timeout: int = 30):
    """
    Search multiple prompts in sequence
    """
    results = []
    for prompt in prompts:
        try:
            result = await automator.search_perplexity(prompt, timeout)
            results.append(result)
        except Exception as e:
            results.append({
                "success": False,
                "error": str(e),
                "prompt": prompt
            })
    
    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)