#!/usr/bin/env python3
"""
Brickset API Analysis Script

This script connects to the Brickset API to fetch LEGO set data including dimensions
and weight, then performs various analyses on the data.

Requirements:
- Brickset API key (get from https://brickset.com/tools/webservices/v3)
- Python packages listed in requirements.txt

Usage:
    python brickset_analyzer.py

Author: Brickset Analysis Project
"""

import os
import sys
import json
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BricksetAPI:
    """Class to handle Brickset API interactions"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('BRICKSET_API_KEY')
        self.base_url = "https://brickset.com/api/v3.asmx"
        self.session = requests.Session()
        self.user_hash = None
        
        if not self.api_key:
            raise ValueError("API key is required. Set BRICKSET_API_KEY environment variable or pass it to the constructor.")
        
        # Set up logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
    
    def login(self, username: str = None, password: str = None) -> bool:
        """Login to Brickset API to get user hash"""
        username = username or os.getenv('BRICKSET_USERNAME')
        password = password or os.getenv('BRICKSET_PASSWORD')
        
        if not username or not password:
            self.logger.info("No username/password provided. Using anonymous access (limited functionality).")
            return False
        
        url = f"{self.base_url}/login"
        params = {
            'apiKey': self.api_key,
            'username': username,
            'password': password
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            self.user_hash = response.text.strip('"')
            self.logger.info("Successfully logged in to Brickset API")
            return True
        except Exception as e:
            self.logger.error(f"Login failed: {e}")
            return False
    
    def get_sets(self, params: Dict[str, Any] = None) -> List[Dict]:
        """Fetch sets from Brickset API"""
        url = f"{self.base_url}/getSets"
        
        default_params = {
            'apiKey': self.api_key,
            'userHash': self.user_hash or '',
            'query': '',
            'theme': '',
            'subtheme': '',
            'setNumber': '',
            'year': '',
            'owned': '',
            'wanted': '',
            'orderBy': 'Number',
            'pageSize': '500'
        }
        
        if params:
            default_params.update(params)
        
        try:
            response = self.session.get(url, params=default_params)
            response.raise_for_status()
            data = response.json()
            
            if 'sets' in data:
                return data['sets']
            else:
                self.logger.error(f"Unexpected API response: {data}")
                return []
        except Exception as e:
            self.logger.error(f"Error fetching sets: {e}")
            return []
    
    def get_themes(self) -> List[Dict]:
        """Fetch available themes from Brickset API"""
        url = f"{self.base_url}/getThemes"
        params = {'apiKey': self.api_key}
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('themes', [])
        except Exception as e:
            self.logger.error(f"Error fetching themes: {e}")
            return []


class BricksetAnalyzer:
    """Class to analyze LEGO set data"""
    
    def __init__(self):
        self.data = None
        self.logger = logging.getLogger(__name__)
        
        # Set up plotting style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def load_data(self, sets_data: List[Dict]):
        """Load and preprocess the sets data"""
        if not sets_data:
            raise ValueError("No data provided")
        
        self.data = pd.DataFrame(sets_data)
        self.logger.info(f"Loaded {len(self.data)} sets")
        
        # Clean and convert data types
        self._preprocess_data()
    
    def _preprocess_data(self):
        """Preprocess the data for analysis"""
        # Convert dimensions to numeric
        if 'dimensions' in self.data.columns:
            self.data['dimensions_parsed'] = self.data['dimensions'].apply(self._parse_dimensions)
        
        # Convert weight to numeric
        if 'weight' in self.data.columns:
            self.data['weight_kg'] = self.data['weight'].apply(self._parse_weight)
        
        # Convert other numeric fields
        numeric_fields = ['pieces', 'minifigs', 'year', 'USRetailPrice', 'UKRetailPrice']
        for field in numeric_fields:
            if field in self.data.columns:
                self.data[field] = pd.to_numeric(self.data[field], errors='coerce')
        
        # Extract length, width, height from dimensions
        if 'dimensions_parsed' in self.data.columns:
            dims_df = pd.json_normalize(self.data['dimensions_parsed'])
            self.data = pd.concat([self.data, dims_df], axis=1)
        
        self.logger.info("Data preprocessing completed")
    
    def _parse_dimensions(self, dim_str: str) -> Dict[str, float]:
        """Parse dimension string to extract length, width, height in cm"""
        if not dim_str or pd.isna(dim_str):
            return {'length_cm': None, 'width_cm': None, 'height_cm': None}
        
        try:
            # Remove units and split
            clean_str = dim_str.replace('cm', '').replace('mm', '').replace('"', '').strip()
            parts = [p.strip() for p in clean_str.split('x') if p.strip()]
            
            if len(parts) >= 3:
                return {
                    'length_cm': float(parts[0]),
                    'width_cm': float(parts[1]),
                    'height_cm': float(parts[2])
                }
            elif len(parts) == 2:
                return {
                    'length_cm': float(parts[0]),
                    'width_cm': float(parts[1]),
                    'height_cm': None
                }
        except (ValueError, IndexError):
            pass
        
        return {'length_cm': None, 'width_cm': None, 'height_cm': None}
    
    def _parse_weight(self, weight_str: str) -> Optional[float]:
        """Parse weight string to extract weight in kg"""
        if not weight_str or pd.isna(weight_str):
            return None
        
        try:
            # Extract numeric value and convert to kg
            clean_str = str(weight_str).replace('kg', '').replace('g', '').replace('lbs', '').strip()
            weight = float(clean_str)
            
            # Convert grams to kg if the value seems to be in grams
            if 'g' in str(weight_str) and 'kg' not in str(weight_str):
                weight = weight / 1000
            # Convert pounds to kg
            elif 'lbs' in str(weight_str):
                weight = weight * 0.453592
            
            return weight
        except ValueError:
            return None
    
    def basic_statistics(self) -> Dict[str, Any]:
        """Generate basic statistics about the dataset"""
        if self.data is None:
            raise ValueError("No data loaded")
        
        stats = {
            'total_sets': len(self.data),
            'date_range': {
                'earliest': self.data['year'].min() if 'year' in self.data.columns else None,
                'latest': self.data['year'].max() if 'year' in self.data.columns else None
            },
            'themes': self.data['theme'].nunique() if 'theme' in self.data.columns else None,
            'sets_with_dimensions': self.data['length_cm'].notna().sum() if 'length_cm' in self.data.columns else 0,
            'sets_with_weight': self.data['weight_kg'].notna().sum() if 'weight_kg' in self.data.columns else 0
        }
        
        return stats
    
    def dimension_analysis(self) -> Dict[str, Any]:
        """Analyze dimensions data"""
        if self.data is None:
            raise ValueError("No data loaded")
        
        dim_cols = ['length_cm', 'width_cm', 'height_cm']
        available_dims = [col for col in dim_cols if col in self.data.columns]
        
        if not available_dims:
            return {'error': 'No dimension data available'}
        
        analysis = {}
        
        for dim in available_dims:
            valid_data = self.data[dim].dropna()
            if len(valid_data) > 0:
                analysis[dim] = {
                    'count': len(valid_data),
                    'mean': valid_data.mean(),
                    'median': valid_data.median(),
                    'std': valid_data.std(),
                    'min': valid_data.min(),
                    'max': valid_data.max(),
                    'quartiles': valid_data.quantile([0.25, 0.75]).to_dict()
                }
        
        # Calculate volume if all dimensions are available
        if all(col in self.data.columns for col in dim_cols):
            volume_data = (self.data['length_cm'] * self.data['width_cm'] * self.data['height_cm']).dropna()
            if len(volume_data) > 0:
                analysis['volume_cm3'] = {
                    'count': len(volume_data),
                    'mean': volume_data.mean(),
                    'median': volume_data.median(),
                    'std': volume_data.std(),
                    'min': volume_data.min(),
                    'max': volume_data.max()
                }
        
        return analysis
    
    def weight_analysis(self) -> Dict[str, Any]:
        """Analyze weight data"""
        if self.data is None or 'weight_kg' not in self.data.columns:
            return {'error': 'No weight data available'}
        
        valid_data = self.data['weight_kg'].dropna()
        
        if len(valid_data) == 0:
            return {'error': 'No valid weight data found'}
        
        return {
            'count': len(valid_data),
            'mean': valid_data.mean(),
            'median': valid_data.median(),
            'std': valid_data.std(),
            'min': valid_data.min(),
            'max': valid_data.max(),
            'quartiles': valid_data.quantile([0.25, 0.5, 0.75]).to_dict()
        }
    
    def create_visualizations(self, output_dir: str = 'plots'):
        """Create various visualizations of the data"""
        if self.data is None:
            raise ValueError("No data loaded")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Dimension distributions
        self._plot_dimension_distributions(output_dir)
        
        # Weight distribution
        self._plot_weight_distribution(output_dir)
        
        # Correlations
        self._plot_correlations(output_dir)
        
        # Time series
        self._plot_time_series(output_dir)
        
        self.logger.info(f"Visualizations saved to {output_dir}/")
    
    def _plot_dimension_distributions(self, output_dir: str):
        """Plot dimension distributions"""
        dim_cols = ['length_cm', 'width_cm', 'height_cm']
        available_dims = [col for col in dim_cols if col in self.data.columns and self.data[col].notna().sum() > 0]
        
        if not available_dims:
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('LEGO Set Dimensions Analysis', fontsize=16)
        
        # Individual dimension histograms
        for i, dim in enumerate(available_dims):
            row, col = divmod(i, 2)
            if i < 3:  # Only plot first 3 dimensions
                axes[row, col].hist(self.data[dim].dropna(), bins=30, alpha=0.7, edgecolor='black')
                axes[row, col].set_title(f'{dim.replace("_", " ").title()} Distribution')
                axes[row, col].set_xlabel(f'{dim.replace("_", " ").title()}')
                axes[row, col].set_ylabel('Frequency')
        
        # Box plot for all dimensions
        if len(available_dims) > 1:
            axes[1, 1].boxplot([self.data[dim].dropna() for dim in available_dims], 
                              labels=[dim.replace('_cm', '').title() for dim in available_dims])
            axes[1, 1].set_title('Dimensions Box Plot')
            axes[1, 1].set_ylabel('Size (cm)')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/dimension_distributions.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_weight_distribution(self, output_dir: str):
        """Plot weight distribution"""
        if 'weight_kg' not in self.data.columns:
            return
        
        weight_data = self.data['weight_kg'].dropna()
        if len(weight_data) == 0:
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Histogram
        ax1.hist(weight_data, bins=30, alpha=0.7, edgecolor='black')
        ax1.set_title('Weight Distribution')
        ax1.set_xlabel('Weight (kg)')
        ax1.set_ylabel('Frequency')
        
        # Box plot
        ax2.boxplot(weight_data)
        ax2.set_title('Weight Box Plot')
        ax2.set_ylabel('Weight (kg)')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/weight_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_correlations(self, output_dir: str):
        """Plot correlation matrix"""
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            return
        
        correlation_matrix = self.data[numeric_cols].corr()
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                   square=True, fmt='.2f')
        plt.title('Correlation Matrix of Numeric Variables')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/correlations.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_time_series(self, output_dir: str):
        """Plot time series of dimensions and weight"""
        if 'year' not in self.data.columns:
            return
        
        # Group by year and calculate means
        yearly_stats = self.data.groupby('year').agg({
            col: 'mean' for col in ['length_cm', 'width_cm', 'height_cm', 'weight_kg'] 
            if col in self.data.columns
        }).reset_index()
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Temporal Trends in LEGO Set Dimensions and Weight', fontsize=16)
        
        plots = [
            ('length_cm', 'Average Length (cm)'),
            ('width_cm', 'Average Width (cm)'),
            ('height_cm', 'Average Height (cm)'),
            ('weight_kg', 'Average Weight (kg)')
        ]
        
        for i, (col, title) in enumerate(plots):
            row, col_idx = divmod(i, 2)
            if col in yearly_stats.columns:
                axes[row, col_idx].plot(yearly_stats['year'], yearly_stats[col], marker='o')
                axes[row, col_idx].set_title(title)
                axes[row, col_idx].set_xlabel('Year')
                axes[row, col_idx].set_ylabel(title)
                axes[row, col_idx].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/time_series.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def generate_report(self, output_file: str = 'brickset_analysis_report.txt'):
        """Generate a comprehensive text report"""
        if self.data is None:
            raise ValueError("No data loaded")
        
        with open(output_file, 'w') as f:
            f.write("BRICKSET ANALYSIS REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Basic statistics
            basic_stats = self.basic_statistics()
            f.write("BASIC STATISTICS\n")
            f.write("-" * 20 + "\n")
            for key, value in basic_stats.items():
                f.write(f"{key}: {value}\n")
            f.write("\n")
            
            # Dimension analysis
            dim_analysis = self.dimension_analysis()
            if 'error' not in dim_analysis:
                f.write("DIMENSION ANALYSIS\n")
                f.write("-" * 20 + "\n")
                for dim, stats in dim_analysis.items():
                    f.write(f"\n{dim.upper()}:\n")
                    for stat, value in stats.items():
                        if isinstance(value, dict):
                            f.write(f"  {stat}: {value}\n")
                        else:
                            f.write(f"  {stat}: {value:.2f}\n")
                f.write("\n")
            
            # Weight analysis
            weight_analysis = self.weight_analysis()
            if 'error' not in weight_analysis:
                f.write("WEIGHT ANALYSIS\n")
                f.write("-" * 20 + "\n")
                for stat, value in weight_analysis.items():
                    if isinstance(value, dict):
                        f.write(f"{stat}: {value}\n")
                    else:
                        f.write(f"{stat}: {value:.2f}\n")
        
        self.logger.info(f"Report saved to {output_file}")


def main():
    """Main function to run the analysis"""
    print("Brickset API Analysis Tool")
    print("=" * 40)
    
    # Initialize API client
    try:
        api = BricksetAPI()
        print("✓ API client initialized")
    except ValueError as e:
        print(f"✗ Error: {e}")
        print("\nTo use this script, you need a Brickset API key.")
        print("1. Get an API key from: https://brickset.com/tools/webservices/v3")
        print("2. Create a .env file with: BRICKSET_API_KEY=your_key_here")
        print("3. Optionally add BRICKSET_USERNAME and BRICKSET_PASSWORD for full access")
        return
    
    # Try to login (optional)
    api.login()
    
    # Fetch themes to show available options
    print("\nFetching available themes...")
    themes = api.get_themes()
    if themes:
        print(f"Found {len(themes)} themes available")
        popular_themes = ['Star Wars', 'City', 'Creator', 'Technic', 'Architecture']
        available_popular = [t for t in themes if t.get('theme') in popular_themes]
        if available_popular:
            print("Popular themes available:", [t['theme'] for t in available_popular[:5]])
    
    # Fetch data
    print("\nFetching LEGO set data...")
    print("This may take a moment...")
    
    # Start with a specific theme or year to get meaningful data
    sets_data = api.get_sets({
        'theme': 'Star Wars',  # Focus on a popular theme
        'pageSize': '200'      # Limit for demonstration
    })
    
    if not sets_data:
        print("No data retrieved. Trying with different parameters...")
        # Try without theme filter
        sets_data = api.get_sets({'pageSize': '100'})
    
    if not sets_data:
        print("✗ No data could be retrieved from the API.")
        print("This might be due to API limits or connection issues.")
        return
    
    print(f"✓ Retrieved data for {len(sets_data)} sets")
    
    # Initialize analyzer
    analyzer = BricksetAnalyzer()
    analyzer.load_data(sets_data)
    
    # Generate basic statistics
    print("\nGenerating analysis...")
    basic_stats = analyzer.basic_statistics()
    print(f"✓ Analysis complete!")
    print(f"  - Total sets: {basic_stats['total_sets']}")
    print(f"  - Sets with dimensions: {basic_stats['sets_with_dimensions']}")
    print(f"  - Sets with weight: {basic_stats['sets_with_weight']}")
    
    # Generate visualizations
    print("\nCreating visualizations...")
    try:
        analyzer.create_visualizations()
        print("✓ Visualizations saved to 'plots/' directory")
    except Exception as e:
        print(f"✗ Error creating visualizations: {e}")
    
    # Generate report
    print("\nGenerating report...")
    try:
        analyzer.generate_report()
        print("✓ Analysis report saved as 'brickset_analysis_report.txt'")
    except Exception as e:
        print(f"✗ Error generating report: {e}")
    
    print("\n" + "=" * 40)
    print("Analysis complete!")
    print("Check the generated files:")
    print("- brickset_analysis_report.txt (detailed analysis)")
    print("- plots/ directory (visualizations)")


if __name__ == "__main__":
    main()