# Medical Insurance Analysis - API Documentation

## 📚 Module Reference

### `data_loader.py` - MedicalInsuranceDataLoader

#### Class Overview
```python
class MedicalInsuranceDataLoader:
    """Handles data loading, cleaning, and preprocessing."""
```

#### Constructor
```python
__init__(self, url=None, local_path=None)
```
**Parameters:**
- `url` (str, optional): URL to download dataset
- `local_path` (str, optional): Path to local dataset file

#### Methods

##### `download_data(save_path='/tmp/medical_insurance.csv')`
Downloads dataset from URL.

**Parameters:**
- `save_path` (str): Where to save downloaded file

**Returns:**
- `bool`: Success status

**Example:**
```python
loader = MedicalInsuranceDataLoader(url="http://example.com/data.csv")
success = loader.download_data("/path/to/save.csv")
```

##### `load_data()`
Loads dataset from local file.

**Returns:**
- `pd.DataFrame`: Raw dataset

**Example:**
```python
raw_data = loader.load_data()
print(f"Dataset shape: {raw_data.shape}")
```

##### `clean_data()`
Cleans and preprocesses the dataset.

**Returns:**
- `pd.DataFrame`: Cleaned dataset

**Features:**
- Handles missing values using median/mode imputation
- Converts data types appropriately
- Validates data integrity

##### `create_labeled_data()`
Creates human-readable labeled version.

**Returns:**
- `pd.DataFrame`: Dataset with readable category labels

**Label Mappings:**
```python
{
    'sex': {1: 'male', 2: 'female'},
    'smoker': {0: 'no', 1: 'yes'},
    'region': {1: 'northeast', 2: 'northwest', 3: 'southeast', 4: 'southwest'}
}
```

##### `get_data_summary()`
Generates comprehensive data summary.

**Returns:**
- `dict`: Summary statistics and metadata

---

### `data_analyzer.py` - MedicalInsuranceAnalyzer

#### Class Overview
```python
class MedicalInsuranceAnalyzer:
    """Performs comprehensive statistical analysis."""
```

#### Constructor
```python
__init__(self, df_clean, df_labeled=None)
```
**Parameters:**
- `df_clean` (pd.DataFrame): Cleaned numerical dataset
- `df_labeled` (pd.DataFrame, optional): Labeled dataset

#### Methods

##### `basic_statistics()`
Calculates descriptive statistics.

**Returns:**
- `dict`: Basic statistics summary

**Includes:**
- Descriptive stats (mean, std, min, max, quartiles)
- Additional measures (median, mode, skewness, kurtosis)

##### `correlation_analysis()`
Performs correlation analysis between variables.

**Returns:**
- `dict`: Correlation results including matrix and strongest predictors

##### `group_analysis()`
Analyzes groups based on categorical variables.

**Returns:**
- `dict`: Group statistics for each categorical variable

##### `statistical_tests()`
Performs hypothesis testing for group differences.

**Returns:**
- `dict`: Test statistics and p-values

**Tests Performed:**
- T-tests for binary comparisons
- ANOVA for multi-group comparisons

##### `generate_insights()`
Generates business insights from analysis.

**Returns:**
- `dict`: Key insights and interpretations

##### `run_full_analysis()`
Executes complete analysis pipeline.

**Returns:**
- `dict`: All analysis results

##### `export_results(output_path)`
Exports results to JSON file.

**Parameters:**
- `output_path` (str): Path to save results

---

### `data_visualizer.py` - MedicalInsuranceVisualizer

#### Class Overview
```python
class MedicalInsuranceVisualizer:
    """Creates comprehensive data visualizations."""
```

#### Constructor
```python
__init__(self, df_clean, df_labeled=None)
```
**Parameters:**
- `df_clean` (pd.DataFrame): Cleaned numerical dataset  
- `df_labeled` (pd.DataFrame, optional): Labeled dataset

#### Visualization Methods

##### `create_line_chart(x_col='age', y_col='charges', save_path=None)`
Creates line chart showing trends.

**Parameters:**
- `x_col` (str): Column for x-axis
- `y_col` (str): Column for y-axis
- `save_path` (str, optional): Path to save plot

**Returns:**
- `matplotlib.figure.Figure`: Created figure

##### `create_bar_chart(x_col='region_label', y_col='charges', save_path=None)`
Creates bar chart for categorical comparisons.

**Parameters:**
- `x_col` (str): Categorical column
- `y_col` (str): Numerical column
- `save_path` (str, optional): Path to save plot

##### `create_histogram(col='bmi', bins=30, save_path=None)`
Creates histogram for distribution analysis.

**Parameters:**
- `col` (str): Column to plot
- `bins` (int): Number of histogram bins
- `save_path` (str, optional): Path to save plot

##### `create_scatter_plot(x_col='bmi', y_col='charges', hue_col='smoker_label', save_path=None)`
Creates scatter plot with optional color coding.

**Parameters:**
- `x_col` (str): X-axis column
- `y_col` (str): Y-axis column  
- `hue_col` (str, optional): Color coding column
- `save_path` (str, optional): Path to save plot

##### `create_correlation_heatmap(save_path=None)`
Creates correlation matrix heatmap.

##### `create_box_plots(save_path=None)`
Creates box plots for categorical comparisons.

##### `create_all_required_plots(output_dir='/home/user/output/')`
Creates all required visualizations and saves them.

**Parameters:**
- `output_dir` (str): Directory to save all plots

**Returns:**
- `dict`: Dictionary of created figures

---

## 🛠️ Usage Patterns

### Quick Analysis Pipeline
```python
# Import modules
from data_loader import MedicalInsuranceDataLoader
from data_analyzer import MedicalInsuranceAnalyzer  
from data_visualizer import MedicalInsuranceVisualizer

# Load and clean data
loader = MedicalInsuranceDataLoader(url="your_url")
loader.download_data()
clean_data = loader.clean_data()
labeled_data = loader.create_labeled_data()

# Analyze data
analyzer = MedicalInsuranceAnalyzer(clean_data, labeled_data)
results = analyzer.run_full_analysis()

# Create visualizations
visualizer = MedicalInsuranceVisualizer(clean_data, labeled_data)
figures = visualizer.create_all_required_plots()
```

### Custom Analysis Example
```python
# Custom correlation analysis
analyzer = MedicalInsuranceAnalyzer(df_clean, df_labeled)
correlations = analyzer.correlation_analysis()

strongest_predictor = correlations['strongest_predictor']
correlation_value = correlations['strongest_correlation']

print(f"Strongest predictor: {strongest_predictor}")
print(f"Correlation: {correlation_value:.3f}")
```

### Custom Visualization Example
```python
# Custom scatter plot with different variables
visualizer = MedicalInsuranceVisualizer(df_clean, df_labeled)

fig = visualizer.create_scatter_plot(
    x_col='age',
    y_col='charges', 
    hue_col='sex_label',
    save_path='custom_age_charges_by_sex.png'
)
```

## 🔧 Configuration Options

### Matplotlib Styling
```python
# Default style configuration in visualizer
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
```

### Customizing Plot Appearance
```python
# Example: Custom color palette
custom_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']

# Example: Custom figure size
plt.rcParams['figure.figsize'] = (15, 10)
```

## 🐛 Error Handling

### Common Errors and Solutions

#### ImportError
```python
# Error: ModuleNotFoundError: No module named 'pandas'
# Solution: Install dependencies
pip install -r requirements.txt
```

#### FileNotFoundError  
```python
# Error: [Errno 2] No such file or directory
# Solution: Check file paths and ensure download completed
loader.download_data()  # Re-download if needed
```

#### ValueError in Data Processing
```python
# Error: Cannot convert string to float
# Solution: Check for non-numeric data in numeric columns
# The cleaner handles this automatically
```

## 📊 Performance Considerations

### Memory Usage
- **Dataset Size**: ~380 KB in memory
- **Visualization Memory**: ~50-100 MB per complex plot
- **Total Memory**: <500 MB for complete analysis

### Processing Time
- **Data Loading**: <5 seconds
- **Statistical Analysis**: <10 seconds
- **Visualization Creation**: <15 seconds
- **Total Pipeline**: <30 seconds

### Optimization Tips
```python
# For large datasets, consider:
# 1. Chunked processing
df_chunks = pd.read_csv('large_file.csv', chunksize=1000)

# 2. Memory-efficient data types
df['category'] = df['category'].astype('category')

# 3. Selective column loading
df = pd.read_csv('file.csv', usecols=['col1', 'col2'])
```

---

This API documentation provides comprehensive guidance for using and extending the medical insurance analysis modules. Each class and method is designed for modularity and reusability across different datasets and analysis scenarios.
