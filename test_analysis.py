#!/usr/bin/env python3
"""
Test script to verify the analysis service correctly identifies different item types
"""

import asyncio
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from api.services.analysis_service import AnalysisService

async def test_analysis():
    """Test the analysis service with different mock image types"""
    
    service = AnalysisService()
    
    # Test cases with different "image" filenames
    test_cases = [
        "book_programming.jpg",
        "textbook_math.png", 
        "iphone_12_pro.jpg",
        "macbook_pro_2021.jpg",
        "apple_watch_series7.jpg",
        "canon_camera_r5.jpg",
        "unknown_item.jpg"
    ]
    
    print("🧪 Testing Analysis Service with Different Item Types\n")
    print("=" * 60)
    
    for i, test_file in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_file}")
        print("-" * 40)
        
        try:
            # Simulate analysis with mock file path
            result = await service.analyze_images([test_file])
            
            item_info = result.get('item_info', {})
            price_range = result.get('price_range', {})
            
            print(f"✅ Item: {item_info.get('name', 'Unknown')}")
            print(f"📱 Series: {item_info.get('series', 'Unknown')}")
            print(f"📅 Year: {item_info.get('year', 'Unknown')}")
            print(f"🔧 Condition: {item_info.get('condition', 'Unknown')}")
            print(f"💰 Price Range: {price_range.get('min', 0):,.0f} - {price_range.get('max', 0):,.0f} {price_range.get('currency', 'THB')}")
            print(f"💡 Suggested: {price_range.get('suggested', 0):,.0f} {price_range.get('currency', 'THB')}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Analysis Test Complete!")
    print("\n📝 Note: The system now provides intelligent mock data based on filename")
    print("📝 Books should show book prices (~280-450 THB), not iPhone prices!")

if __name__ == "__main__":
    asyncio.run(test_analysis())