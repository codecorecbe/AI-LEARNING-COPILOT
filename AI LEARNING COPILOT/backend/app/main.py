"""
FastAPI Main Application Entry Point
CodeCore AI Backend - Educational Content Generation API

This is the core application file that initializes FastAPI,
configures middleware, and registers all routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import subject_routes

# Initialize FastAPI app with metadata
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc documentation
)


# Configure CORS (Cross-Origin Resource Sharing)
# Allows frontend to communicate with backend from different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # Which origins can access the API
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Register API routes
app.include_router(
    subject_routes.router,
    prefix="/api",  # All routes will be prefixed with /api
    tags=["AI Generation"]  # Group routes in documentation
)


@app.get("/")
async def root():
    """
    Root endpoint - Health check and API information.
    """
    return {
        "message": "CodeCore AI Backend is running! 🚀",
        "status": "active",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "endpoints": {
            "generate": "/api/generate"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and deployment.
    """
    return {
        "status": "healthy",
        "api_version": settings.API_VERSION
    }


# Run the application (for development)
if __name__ == "__main__":
    import uvicorn
    
    print(f"""
    ╔══════════════════════════════════════════╗
    ║   CodeCore AI Backend Starting...        ║
    ║   Port: {settings.PORT}                           ║
    ║   Docs: http://localhost:{settings.PORT}/docs    ║
    ╚══════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG  # Auto-reload on code changes in debug mode
    )
