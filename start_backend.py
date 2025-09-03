#!/usr/bin/env python3
"""
Startup script for the 2nd Hand Price Checker FastAPI backend
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Start the FastAPI server"""
    
    # Check for required environment variables
    required_env_vars = ['ARK_API_KEY', 'SERPAPI_API_KEY']
    missing_vars = []
    
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("Warning: Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nNote: The API will work with mock data, but won't perform real analysis.")
        print("   To enable full functionality, set these environment variables:")
        print("   export ARK_API_KEY='your_ark_api_key'")
        print("   export SERPAPI_API_KEY='your_serpapi_key'")
        print()
    
    # Import and run the FastAPI app
    try:
        import uvicorn
        from api.main import app
        
        print("Starting 2nd Hand Price Checker API...")
        print("Server will be available at: http://localhost:8000")
        print("API documentation: http://localhost:8000/docs")
        print("\nStarting server...")
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except ImportError as e:
        print(f"Error importing required modules: {e}")
        print("\nPlease install the required dependencies:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()