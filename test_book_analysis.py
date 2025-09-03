#!/usr/bin/env python3
"""
Test script to verify that book images now return book analysis instead of iPhone analysis
"""

import requests
import json

def test_analysis():
    """Test the analysis endpoint"""
    
    print("Testing analysis service...")
    
    # Test the test endpoint
    response = requests.get("http://localhost:8001/api/test-analysis")
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ Analysis Service Test Results:")
        print(f"Success: {result['success']}")
        
        if result['success']:
            analysis = result['result']
            item_info = analysis['item_info']
            price_range = analysis['price_range']
            
            print(f"\n📋 Item Information:")
            print(f"  Name: {item_info['name']}")
            print(f"  Series: {item_info['series']}")
            print(f"  Year: {item_info['year']}")
            print(f"  Condition: {item_info['condition']}")
            
            print(f"\n💰 Price Analysis:")
            print(f"  Min Price: {price_range['min']} {price_range['currency']}")
            print(f"  Max Price: {price_range['max']} {price_range['currency']}")
            print(f"  Suggested: {price_range['suggested']} {price_range['currency']}")
            print(f"  Confidence: {analysis['confidence']}%")
            
            # Check if it's book-related
            if 'book' in item_info['name'].lower() and price_range['max'] < 1000:
                print("\n🎉 SUCCESS: Analysis correctly identifies books with book pricing!")
                print("📚 No more iPhone results for book images!")
            else:
                print("\n⚠️  WARNING: Still returning non-book results")
        else:
            print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
    else:
        print(f"❌ Request failed with status code: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    test_analysis()