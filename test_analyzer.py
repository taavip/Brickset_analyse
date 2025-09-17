#!/usr/bin/env python3
"""
Test script for Brickset analyzer functionality.

This script performs basic tests to ensure the analyzer works correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from brickset_analyzer import BricksetAPI, BricksetAnalyzer

def test_analyzer_with_sample_data():
    """Test analyzer with sample data"""
    print("Testing BricksetAnalyzer with sample data...")
    
    # Create sample data
    sample_data = [
        {
            'setID': '1',
            'number': '75001',
            'name': 'Republic Troopers vs. Sith Troopers',
            'theme': 'Star Wars',
            'year': 2013,
            'pieces': 63,
            'minifigs': 4,
            'dimensions': '15.7 x 14.1 x 4.6cm',
            'weight': '0.12kg',
            'USRetailPrice': 12.99,
            'UKRetailPrice': 9.99
        },
        {
            'setID': '2',
            'number': '10244',
            'name': 'Fairground Mixer',
            'theme': 'Creator',
            'year': 2014,
            'pieces': 1746,
            'minifigs': 8,
            'dimensions': '38.4 x 25.9 x 32.0cm',
            'weight': '2.1kg',
            'USRetailPrice': 149.99,
            'UKRetailPrice': 119.99
        }
    ]
    
    try:
        # Initialize analyzer
        analyzer = BricksetAnalyzer()
        analyzer.load_data(sample_data)
        
        # Test basic statistics
        stats = analyzer.basic_statistics()
        assert stats['total_sets'] == 2
        assert stats['sets_with_dimensions'] == 2
        assert stats['sets_with_weight'] == 2
        print("✓ Basic statistics test passed")
        
        # Test dimension analysis
        dim_analysis = analyzer.dimension_analysis()
        assert 'length_cm' in dim_analysis
        assert dim_analysis['length_cm']['count'] == 2
        print("✓ Dimension analysis test passed")
        
        # Test weight analysis
        weight_analysis = analyzer.weight_analysis()
        assert weight_analysis['count'] == 2
        assert weight_analysis['mean'] > 0
        print("✓ Weight analysis test passed")
        
        print("✓ All analyzer tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Analyzer test failed: {e}")
        return False

def test_api_initialization():
    """Test API initialization without actual API calls"""
    print("Testing BricksetAPI initialization...")
    
    try:
        # Test without API key (should raise ValueError)
        try:
            api = BricksetAPI()
            print("✗ Should have raised ValueError for missing API key")
            return False
        except ValueError:
            print("✓ Correctly handles missing API key")
        
        # Test with API key
        api = BricksetAPI(api_key="test_key")
        assert api.api_key == "test_key"
        assert api.base_url == "https://brickset.com/api/v3.asmx"
        print("✓ API initialization test passed")
        
        return True
        
    except Exception as e:
        print(f"✗ API test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Running Brickset Analyzer Tests")
    print("=" * 40)
    
    tests = [
        test_api_initialization,
        test_analyzer_with_sample_data
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())