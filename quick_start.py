#!/usr/bin/env python3
"""
Quick start script for Brickset analysis.

This script helps users get started quickly with the Brickset analyzer.
It provides options to run a demo or set up for real API usage.
"""

import os
import sys
from pathlib import Path

def print_banner():
    """Print welcome banner"""
    print("=" * 60)
    print(" BRICKSET ANALYSIS TOOL")
    print("=" * 60)
    print("Analyze LEGO set dimensions and weight data from Brickset API")
    print()

def check_requirements():
    """Check if requirements are installed"""
    try:
        import pandas
        import matplotlib
        import seaborn
        import requests
        return True
    except ImportError as e:
        print(f"✗ Missing required packages: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def run_demo():
    """Run the demo with synthetic data"""
    print("Running demo with synthetic data...")
    print("-" * 40)
    os.system("python3 demo_analyzer.py")

def setup_api():
    """Help user set up API configuration"""
    print("API Setup Guide")
    print("-" * 20)
    print("1. Go to: https://brickset.com/tools/webservices/v3")
    print("2. Register for a free API key")
    print("3. Copy the API key you receive")
    print()
    
    api_key = input("Enter your API key (or press Enter to skip): ").strip()
    
    if api_key:
        # Create .env file
        env_content = f"""# Brickset API Configuration
BRICKSET_API_KEY={api_key}

# Optional: For full API access
# BRICKSET_USERNAME=your_username
# BRICKSET_PASSWORD=your_password
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✓ API key saved to .env file")
        return True
    else:
        print("Skipping API setup. You can manually create .env file later.")
        return False

def run_real_analysis():
    """Run analysis with real Brickset data"""
    if not os.path.exists('.env'):
        print("✗ No .env file found. Please set up API first.")
        return False
    
    print("Running analysis with real Brickset data...")
    print("-" * 40)
    os.system("python3 brickset_analyzer.py")
    return True

def main():
    """Main menu"""
    print_banner()
    
    # Check requirements
    if not check_requirements():
        return 1
    
    while True:
        print("Choose an option:")
        print("1. Run demo with sample data")
        print("2. Set up API and run real analysis")
        print("3. Run real analysis (if already configured)")
        print("4. Run tests")
        print("5. Exit")
        print()
        
        choice = input("Enter your choice (1-5): ").strip()
        print()
        
        if choice == '1':
            run_demo()
            
        elif choice == '2':
            if setup_api():
                print("\nNow running real analysis...")
                run_real_analysis()
            
        elif choice == '3':
            if not run_real_analysis():
                print("Use option 2 to set up API first.")
            
        elif choice == '4':
            print("Running tests...")
            print("-" * 20)
            os.system("python3 test_analyzer.py")
            
        elif choice == '5':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")
        
        print("\n" + "=" * 60 + "\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())