from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import uuid
import os
import json
from datetime import datetime
import asyncio
from pathlib import Path

from .models import AnalysisResponse, AnalysisResult, ItemInfo, PriceRange, MarketResult
from .services.analysis_service import AnalysisService
from .services.storage_service import StorageService

app = FastAPI(
    title="2nd Hand Price Checker API",
    description="AI-powered price analysis for second-hand items",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
analysis_service = AnalysisService()
storage_service = StorageService()

# In-memory storage for demo (replace with database in production)
analyses_db = {}

@app.get("/")
async def root():
    return {"message": "2nd Hand Price Checker API", "version": "1.0.0"}

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_images(
    background_tasks: BackgroundTasks,
    images: List[UploadFile] = File(...),
    user_id: Optional[str] = None
):
    """Upload images and start analysis process"""
    
    # Validate images
    if len(images) > 5:
        raise HTTPException(status_code=400, detail="Maximum 5 images allowed")
    
    for image in images:
        print(f"DEBUG: Received file - filename: {image.filename}, content_type: {image.content_type}")
        if not image.content_type or not image.content_type.startswith('image/'):
            print(f"DEBUG: Rejecting file with content_type: {image.content_type}")
            raise HTTPException(status_code=400, detail="Only image files are allowed")
        
        # Check file size (10MB limit)
        content = await image.read()
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Image size must be less than 10MB")
        
        # Reset file pointer
        await image.seek(0)
    
    # Generate analysis ID
    analysis_id = str(uuid.uuid4())
    
    # Save images
    image_paths = []
    for i, image in enumerate(images):
        content = await image.read()
        file_path = await storage_service.save_image(analysis_id, f"image_{i}.jpg", content)
        image_paths.append(file_path)
    
    # Initialize analysis record
    analyses_db[analysis_id] = {
        "analysis_id": analysis_id,
        "user_id": user_id,
        "status": "pending",
        "image_paths": image_paths,
        "created_at": datetime.now().isoformat(),
        "estimated_time": 30
    }
    
    # Start background analysis
    background_tasks.add_task(process_analysis, analysis_id, image_paths)
    print(f"DEBUG: Background task added for analysis {analysis_id}")
    
    return AnalysisResponse(
        analysis_id=analysis_id,
        status="processing",
        estimated_time=30
    )

@app.get("/api/analysis/{analysis_id}", response_model=AnalysisResult)
async def get_analysis(analysis_id: str):
    """Get analysis results by ID"""
    
    if analysis_id not in analyses_db:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    analysis = analyses_db[analysis_id]
    print(f"DEBUG: Getting analysis {analysis_id}, current data: {analysis}")
    
    if analysis["status"] == "completed":
        result = AnalysisResult(
            analysis_id=analysis["analysis_id"],
            status=analysis["status"],
            item_info=analysis.get("item_info"),
            price_range=analysis.get("price_range"),
            confidence=analysis.get("confidence"),
            market_data=analysis.get("market_data", []),
            created_at=analysis["created_at"]
        )
        print(f"DEBUG: Returning completed analysis: {result}")
        return result
    else:
        result = AnalysisResult(
            analysis_id=analysis["analysis_id"],
            status=analysis["status"],
            created_at=analysis["created_at"]
        )
        print(f"DEBUG: Returning processing analysis: {result}")
        return result

@app.get("/api/history/{user_id}")
async def get_user_history(user_id: str, page: int = 1, limit: int = 20):
    """Get user's analysis history"""
    
    user_analyses = [
        analysis for analysis in analyses_db.values() 
        if analysis.get("user_id") == user_id
    ]
    
    # Sort by creation date (newest first)
    user_analyses.sort(key=lambda x: x["created_at"], reverse=True)
    
    # Pagination
    start = (page - 1) * limit
    end = start + limit
    paginated_analyses = user_analyses[start:end]
    
    return {
        "analyses": paginated_analyses,
        "total_count": len(user_analyses),
        "page": page,
        "limit": limit
    }

@app.delete("/api/analysis/{analysis_id}")
async def delete_analysis(analysis_id: str):
    """Delete an analysis"""
    
    if analysis_id not in analyses_db:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    analysis = analyses_db[analysis_id]
    
    # Clean up stored images
    for image_path in analysis.get("image_paths", []):
        await storage_service.delete_image(image_path)
    
    # Remove from database
    del analyses_db[analysis_id]
    
    return {"message": "Analysis deleted successfully"}

@app.get("/api/test-analysis")
async def test_analysis():
    """Test endpoint to verify analysis service works"""
    try:
        result = await analysis_service.analyze_images(["test_path"])
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/complete-analysis/{analysis_id}")
async def complete_analysis_manually(analysis_id: str):
    """Manually complete an analysis for testing"""
    if analysis_id not in analyses_db:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    try:
        await process_analysis(analysis_id, analyses_db[analysis_id].get("image_paths", []))
        return {"success": True, "message": "Analysis completed"}
    except Exception as e:
        return {"success": False, "error": str(e)}

async def process_analysis(analysis_id: str, image_paths: List[str]):
    """Background task to process image analysis"""
    
    try:
        print(f"DEBUG: Starting analysis for {analysis_id}")
        # Update status to processing
        analyses_db[analysis_id]["status"] = "processing"
        print(f"DEBUG: Status updated to processing for {analysis_id}")
        
        # Simulate processing time
        await asyncio.sleep(2)
        print(f"DEBUG: Processing delay completed for {analysis_id}")
        
        # Use the analysis service to process images
        result = await analysis_service.analyze_images(image_paths)
        print(f"DEBUG: Analysis service returned: {result}")
        
        # Update analysis with results
        analyses_db[analysis_id].update({
            "status": "completed",
            "item_info": result["item_info"],
            "price_range": result["price_range"],
            "confidence": result["confidence"],
            "market_data": result["market_data"],
            "completed_at": datetime.now().isoformat()
        })
        print(f"DEBUG: Analysis completed successfully for {analysis_id}")
        print(f"DEBUG: Final analysis data: {analyses_db[analysis_id]}")
        
    except Exception as e:
        print(f"DEBUG: Analysis failed for {analysis_id}: {str(e)}")
        # Handle errors
        analyses_db[analysis_id].update({
            "status": "error",
            "error_message": str(e),
            "completed_at": datetime.now().isoformat()
        })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)