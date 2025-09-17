#!/usr/bin/env python3
"""
Demo script to show Brickset analyzer functionality with sample data.

This script demonstrates the analysis capabilities without requiring an API key.
It uses synthetic LEGO set data to show how the analysis works.

Usage:
    python demo_analyzer.py
"""

from brickset_analyzer import BricksetAnalyzer
import random
import json

def generate_sample_data(num_sets=100):
    """Generate sample LEGO set data for demonstration"""
    themes = ['Star Wars', 'City', 'Creator', 'Technic', 'Architecture', 'Friends', 'Ninjago']
    sample_data = []
    
    for i in range(num_sets):
        # Generate realistic dimensions and weights
        length = round(random.uniform(5, 50), 1)
        width = round(random.uniform(5, 30), 1)
        height = round(random.uniform(3, 25), 1)
        weight = round(random.uniform(0.1, 5.0), 2)
        
        set_data = {
            'setID': f'set_{i}',
            'number': f'{random.randint(1000, 99999)}',
            'name': f'Sample LEGO Set {i+1}',
            'theme': random.choice(themes),
            'year': random.randint(2010, 2024),
            'pieces': random.randint(50, 5000),
            'minifigs': random.randint(0, 10),
            'dimensions': f'{length} x {width} x {height}cm',
            'weight': f'{weight}kg',
            'USRetailPrice': round(random.uniform(10, 500), 2),
            'UKRetailPrice': round(random.uniform(8, 400), 2)
        }
        sample_data.append(set_data)
    
    return sample_data

def main():
    """Run the demo analysis"""
    print("Brickset Analyzer Demo")
    print("=" * 30)
    print("This demo uses synthetic data to show analysis capabilities.\n")
    
    # Generate sample data
    print("Generating sample data...")
    sample_data = generate_sample_data(150)
    print(f"✓ Generated {len(sample_data)} sample LEGO sets\n")
    
    # Initialize analyzer with sample data
    print("Initializing analyzer...")
    analyzer = BricksetAnalyzer()
    analyzer.load_data(sample_data)
    print("✓ Data loaded and preprocessed\n")
    
    # Show basic statistics
    print("Basic Statistics:")
    print("-" * 20)
    basic_stats = analyzer.basic_statistics()
    for key, value in basic_stats.items():
        print(f"  {key}: {value}")
    print()
    
    # Show dimension analysis
    print("Dimension Analysis:")
    print("-" * 20)
    dim_analysis = analyzer.dimension_analysis()
    if 'error' not in dim_analysis:
        for dim, stats in dim_analysis.items():
            if isinstance(stats, dict) and 'mean' in stats:
                print(f"  {dim.replace('_', ' ').title()}:")
                print(f"    Mean: {stats['mean']:.2f}")
                print(f"    Median: {stats['median']:.2f}")
                print(f"    Range: {stats['min']:.2f} - {stats['max']:.2f}")
                print()
    
    # Show weight analysis
    print("Weight Analysis:")
    print("-" * 20)
    weight_analysis = analyzer.weight_analysis()
    if 'error' not in weight_analysis:
        print(f"  Count: {weight_analysis['count']}")
        print(f"  Mean: {weight_analysis['mean']:.2f} kg")
        print(f"  Median: {weight_analysis['median']:.2f} kg")
        print(f"  Range: {weight_analysis['min']:.2f} - {weight_analysis['max']:.2f} kg")
    print()
    
    # Generate visualizations
    print("Creating visualizations...")
    try:
        analyzer.create_visualizations('demo_plots')
        print("✓ Visualizations saved to 'demo_plots/' directory")
    except Exception as e:
        print(f"✗ Error creating visualizations: {e}")
    
    # Generate report
    print("Generating report...")
    try:
        analyzer.generate_report('demo_analysis_report.txt')
        print("✓ Demo analysis report saved as 'demo_analysis_report.txt'")
    except Exception as e:
        print(f"✗ Error generating report: {e}")
    
    print("\n" + "=" * 30)
    print("Demo complete!")
    print("\nThis demonstrates the analysis capabilities.")
    print("To analyze real Brickset data:")
    print("1. Get an API key from https://brickset.com/tools/webservices/v3")
    print("2. Create a .env file with your API key")
    print("3. Run: python brickset_analyzer.py")

if __name__ == "__main__":
    main()