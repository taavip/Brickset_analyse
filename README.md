# Brickset Analysis Tool

A Python script that connects to the Brickset API, fetches LEGO set dimensions and weight data, and performs comprehensive analysis.

## Features

- **API Integration**: Connects to the Brickset API to fetch LEGO set data
- **Data Analysis**: Analyzes dimensions (length, width, height) and weight data
- **Visualizations**: Creates charts and plots showing data distributions and trends
- **Statistical Reports**: Generates comprehensive text reports with statistics
- **Error Handling**: Robust error handling for API calls and data processing

## Quick Start

For the fastest way to get started, use the interactive quick start script:

```bash
python quick_start.py
```

This script provides an interactive menu to:
- Run a demo with sample data
- Set up your API key
- Run analysis with real Brickset data
- Run tests to verify functionality

## Manual Setup

1. **Get API Key**: Register at [Brickset Web Services](https://brickset.com/tools/webservices/v3) to get your API key

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key**:
   - Copy `.env.example` to `.env`
   - Replace `your_api_key_here` with your actual API key
   ```bash
   cp .env.example .env
   # Edit .env with your API key
   ```

## Available Scripts

- **`brickset_analyzer.py`**: Main analysis script for real Brickset data
- **`demo_analyzer.py`**: Demo script with synthetic data (no API key needed)
- **`quick_start.py`**: Interactive menu for easy setup and usage
- **`test_analyzer.py`**: Test script to verify functionality

## Demo Mode

Try the analyzer without an API key using synthetic data:

```bash
python demo_analyzer.py
```

## Usage

Run the main analysis script:

```bash
python brickset_analyzer.py
```

The script will:
- Connect to the Brickset API
- Fetch LEGO set data (dimensions, weight, etc.)
- Perform statistical analysis
- Generate visualizations in the `plots/` directory
- Create a detailed report file `brickset_analysis_report.txt`

## Output Files

- **`brickset_analysis_report.txt`**: Comprehensive analysis report with statistics
- **`plots/dimension_distributions.png`**: Histograms and box plots of set dimensions
- **`plots/weight_distribution.png`**: Weight distribution analysis
- **`plots/correlations.png`**: Correlation matrix of numeric variables
- **`plots/time_series.png`**: Temporal trends in dimensions and weight

## Data Analysis Features

### Dimensions Analysis
- Length, width, height distributions
- Volume calculations
- Statistical summaries (mean, median, std dev, quartiles)
- Box plots and histograms

### Weight Analysis
- Weight distribution analysis
- Statistical summaries
- Correlation with other variables

### Visualizations
- Dimension distributions
- Weight distributions
- Correlation heatmaps
- Time series trends
- Box plots for comparative analysis

## API Configuration

The script supports both anonymous and authenticated access:

- **Anonymous**: Limited functionality, no user-specific data
- **Authenticated**: Full API access (add username/password to .env)

## Requirements

- Python 3.8+
- Brickset API key
- Internet connection for API access

## Dependencies

See `requirements.txt` for full list:
- requests (API calls)
- pandas (data manipulation)
- matplotlib (plotting)
- seaborn (statistical visualization)
- numpy (numerical operations)
- python-dotenv (environment variables)

## License

MIT License - see LICENSE file for details