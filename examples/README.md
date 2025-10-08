# BKRCast Example Scripts

This directory contains practical example scripts demonstrating how to use BKRCast and the Emme Python API.

## 📁 Available Examples

### 1. Highway Network Analysis
**File**: `example_highway_analysis.py`

Demonstrates:
- Loading and analyzing highway network data
- Calculating V/C ratios and VMT
- Identifying congested links
- Exporting results to CSV

**Usage**:
```python
python examples/example_highway_analysis.py
```

### 2. Transit Network Analysis
**File**: `example_transit_analysis.py`

Demonstrates:
- Analyzing transit boardings and alightings
- Route-level performance metrics
- Stop-level analysis
- Daily transit aggregation

**Usage**:
```python
python examples/example_transit_analysis.py
```

## 🚀 Running the Examples

### Prerequisites
1. BKRCast model must be installed and configured
2. Emme Python API must be available
3. A completed model run with results in the databanks

### Basic Usage

```python
import sys
import os
sys.path.append(os.getcwd())

# Import and run
from examples.example_highway_analysis import analyze_highway_network

# Analyze AM period
project_path = 'projects/LoadTripTables/LoadTripTables.emp'
results = analyze_highway_network(project_path, 'am')
```

### Customization

Each example script can be customized by modifying:
- **Time period**: Change `tod='am'` to 'md', 'pm', or 'ni'
- **Output directory**: Modify `output_dir` variable
- **Metrics calculated**: Add your own calculations
- **Export format**: Change from CSV to Excel, JSON, etc.

## 📊 Output Files

Results are saved to `outputs/examples/`:

### Highway Analysis
- `highway_analysis_{tod}.csv` - All link data with V/C ratios
- `congested_links_{tod}.csv` - Links with V/C > 1.0

### Transit Analysis
- `transit_routes_{tod}.csv` - Route-level performance
- `transit_stops_{tod}.csv` - Stop-level boardings/alightings
- `transit_segments_{tod}.csv` - Segment-level data
- `daily_route_boardings.csv` - Daily totals by route
- `daily_stop_boardings.csv` - Daily totals by stop

## 🔧 Modifying Examples

### Add Custom Metrics

```python
# In example_highway_analysis.py, add to performance metrics section:

# Calculate VHT (Vehicle-Hours-Traveled)
df['travel_time'] = df['length'] / df['speed']  # hours
vht = (df['volume'] * df['travel_time']).sum()
print(f"   Total VHT: {vht:,.0f} vehicle-hours")
```

### Filter by Geographic Area

```python
# Filter links in BKR area only
if '@bkrlink' in link.get_extra_attributes():
    if link['@bkrlink'] == 1:
        link_data.append({...})
```

### Add Visualization

```python
import matplotlib.pyplot as plt

# Plot V/C distribution
df['vc_ratio'].hist(bins=20)
plt.xlabel('V/C Ratio')
plt.ylabel('Number of Links')
plt.title('V/C Ratio Distribution')
plt.savefig('outputs/examples/vc_distribution.png')
```

## 📚 Additional Resources

For detailed documentation, see:
- `BKRCast_코드리뷰_활용가이드.md` - Comprehensive Korean guide
- `EMME_PYTHON_GUIDE.md` - English summary guide
- `QUICK_REFERENCE.md` - Quick reference cheat sheet

## 🆘 Troubleshooting

### Common Issues

**Error: "No module named 'EmmeProject'"**
```python
# Make sure to add scripts directory to path
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'scripts'))
```

**Error: "Emme desktop not found"**
- Ensure Emme is installed and licensed
- Check that `input_configuration.py` has correct paths
- Try running from the BKRCast root directory

**Error: "Scenario not found"**
- Make sure the model has been run and databanks exist
- Check that Banks/{tod}/emmebank directories are populated
- Verify scenario ID (usually 1002) exists

### Getting Help

1. Check the main documentation files
2. Review the BKRCast Wiki: https://github.com/Bellevuewa/BKRCast/wiki
3. Look at `scripts/EmmeProject.py` for available methods
4. Contact: City of Bellevue Transportation Department

## 🎓 Learning Path

Recommended order for learning:
1. Read `QUICK_REFERENCE.md` for syntax
2. Run `example_highway_analysis.py`
3. Run `example_transit_analysis.py`
4. Modify examples for your specific needs
5. Read full documentation in Korean or English guides

## 💡 Tips

- Always start with a completed model run
- Test on one time period (e.g., 'am') before running all periods
- Use small output samples first to verify your code works
- Keep the original examples as reference - make copies to modify
- Add print statements to understand what's happening

---

*For questions or contributions, please create an issue on GitHub.*
