import os
import aiofiles
from pathlib import Path
from typing import Optional
import uuid

class StorageService:
    def __init__(self, base_path: str = "uploads"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
    
    async def save_image(self, analysis_id: str, filename: str, content: bytes) -> str:
        """Save uploaded image to local storage"""
        
        # Create directory for this analysis
        analysis_dir = self.base_path / analysis_id
        analysis_dir.mkdir(exist_ok=True)
        
        # Generate unique filename
        file_extension = Path(filename).suffix or '.jpg'
        unique_filename = f"{uuid.uuid4().hex}{file_extension}"
        file_path = analysis_dir / unique_filename
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        return str(file_path)
    
    async def get_image(self, file_path: str) -> Optional[bytes]:
        """Retrieve image from storage"""
        
        try:
            async with aiofiles.open(file_path, 'rb') as f:
                return await f.read()
        except FileNotFoundError:
            return None
    
    async def delete_image(self, file_path: str) -> bool:
        """Delete image from storage"""
        
        try:
            os.remove(file_path)
            return True
        except FileNotFoundError:
            return False
    
    async def delete_analysis_images(self, analysis_id: str) -> bool:
        """Delete all images for an analysis"""
        
        analysis_dir = self.base_path / analysis_id
        
        if not analysis_dir.exists():
            return False
        
        try:
            # Remove all files in the directory
            for file_path in analysis_dir.iterdir():
                if file_path.is_file():
                    file_path.unlink()
            
            # Remove the directory
            analysis_dir.rmdir()
            return True
        except Exception:
            return False
    
    def get_image_url(self, file_path: str, base_url: str = "http://localhost:8000") -> str:
        """Generate URL for accessing stored image"""
        
        # Convert absolute path to relative path from base_path
        relative_path = Path(file_path).relative_to(self.base_path)
        return f"{base_url}/uploads/{relative_path}"