# BKRCast Quick Reference Cheat Sheet

## 🚀 Quick Start

```python
from scripts.EmmeProject import EmmeProject

# Initialize project
project = EmmeProject('projects/LoadTripTables/LoadTripTables.emp')

# Switch time period
project.change_active_database('am')  # am, md, pm, ni

# Get network
network = project.current_scenario.get_network()
```

## 📊 Common Operations

### Network Access
```python
# Links
for link in network.links():
    print(f"{link.i_node} → {link.j_node}: volume={link['@tveh']}")

# Nodes
for node in network.nodes():
    print(f"Node {node.id}: x={node.x}, y={node.y}")

# Transit lines
for line in network.transit_lines():
    print(f"Line {line.id}: {line.description}")
```

### Create Extra Attributes
```python
# Link attribute
project.create_extra_attribute('LINK', '@volume', 'Traffic volume', True)

# Node attribute
project.create_extra_attribute('NODE', '@boarding', 'Boardings', True)

# Transit segment attribute
project.create_extra_attribute('TRANSIT_SEGMENT', '@tboard', 'Boardings', True)
```

### Network Calculator
```python
# Simple calculation
project.network_calculator(
    "link_calculation",
    result='@tveh',
    expression='@svol + @hvol2 + @hvol3'
)

# With selection
project.network_calculator(
    "link_calculation",
    result='@arterial',
    expression='1',
    selections_by_link='@class=2,3'
)
```

### Matrix Operations
```python
# Create matrix
project.create_matrix('sov_am', 'AM SOV trips', 'FULL')

# Numpy → Emme
project.matrix_to_emme(numpy_array, 'sov_am', 'Description', 'FULL')

# Emme → Numpy
data = project.emmeMatrix_to_numpyMatrix('sov_am', 'float32', 1.0)
```

## 🛣️ Highway Analysis

### Calculate V/C Ratio
```python
project.network_calculator(
    "link_calculation",
    result='@vc_ratio',
    expression='@tveh / ul2'
)

# Find congested links
congested = [link for link in network.links() if link['@vc_ratio'] > 1.0]
```

### Calculate VMT
```python
network = project.current_scenario.get_network()
vmt = sum(link['@tveh'] * link.length for link in network.links())
print(f"Total VMT: {vmt:,.0f} miles")
```

### HOT Lane Revenue
```python
total_revenue = 0
for link in network.links():
    if link['@tolllane'] > 0:
        revenue = link['@svol'] * link['@stoll'] / 100
        total_revenue += revenue
```

## 🚌 Transit Analysis

### Transit Summary
```python
df_line, df_node, df_segment = project.transit_summary()

# Daily boardings by stop
daily_boarding = df_node.groupby('node_id')['total_boarding'].sum()
top_stops = daily_boarding.nlargest(10)
```

### Transit Segment Attributes
```python
# Available attributes
'@tboard'       # Total boardings
'@iboard'       # Initial boardings
'@trsboard'     # Transfer boardings
'@talight'      # Total alightings
'@finalight'    # Final alightings
'@transalight'  # Transfer alightings
```

### Calculate Transit Performance
```python
# PMT (Person-Miles-Traveled)
pmt = df_segment['segment_volume'] * df_segment['length']

# Route-level boardings
route_boardings = df_line.groupby('route_code')['boardings'].sum()
```

## 📋 Extra Attributes Reference

### Common Link Attributes
```python
'@tveh'      # Total vehicles
'@svol'      # SOV volume
'@hvol2'     # HOV2 volume
'@hvol3'     # HOV3 volume
'@lttrk'     # Light truck volume
'@metrk'     # Medium truck volume
'@hvtrk'     # Heavy truck volume
'@bvol'      # Bus volume
'@vc_ratio'  # V/C ratio
'@tolllane'  # HOT lane ID
'@stoll'     # SOV toll (cents)
'@htoll'     # HOV toll (cents)
```

### Common Node Attributes
```python
'@bkrnode'   # BKR area flag
'@elevation' # Elevation
'@tboard_nde'   # Total boarding at node
'@talight_nde'  # Total alighting at node
```

### Common Transit Line Attributes
```python
'@board'     # Total boardings
'@timtr'     # Travel time
```

## 🔧 Useful Functions

### Network Import
```python
# Import network elements
project.process_modes('inputs/modes.txt')
project.process_base_network('inputs/am_roadway.in')
project.process_turn('inputs/am_turns.in')
project.process_transit('inputs/am_transit.in')
project.process_vehicles('inputs/vehicles.txt')
```

### Import Attribute Values
```python
project.import_attribute_values(
    file_path='inputs/extra_attributes/@count.txt',
    revert_on_error=False
)
```

### Export Results
```python
# Export to OMX
project.export_omx_matrices('outputs/matrices.omx')

# Export dataframe
df.to_csv('outputs/results.csv', index=False)
```

## 🔄 Time of Day (TOD)

```python
tod_dict = {
    'am': '6to9',           # 6:00 - 9:00 AM
    'md': '9to1530',        # 9:00 AM - 3:30 PM
    'pm': '1530to1830',     # 3:30 PM - 6:30 PM
    'ni': '1830to6'         # 6:30 PM - 6:00 AM
}
```

## 💡 Common Patterns

### Iterate Through All TODs
```python
for tod in ['am', 'md', 'pm', 'ni']:
    project.change_active_database(tod)
    # Do analysis
```

### Access Specific Link
```python
network = project.current_scenario.get_network()
link = network.link(i_node_id, j_node_id)
if link:
    volume = link['@tveh']
```

### Filter Links by Criteria
```python
# Functional class 2 or 3 (arterials)
arterials = [link for link in network.links() 
             if link['@class'] in [2, 3]]

# High volume links
high_vol = [link for link in network.links() 
            if link['@tveh'] > 5000]
```

### Compare Scenarios
```python
project.set_primary_scenario(1002)  # Base
network_base = project.current_scenario.get_network()

project.set_primary_scenario(1003)  # Alternative
network_alt = project.current_scenario.get_network()

# Compare volumes
for link_base in network_base.links():
    link_alt = network_alt.link(link_base.i_node.id, link_base.j_node.id)
    if link_alt:
        diff = link_alt['@tveh'] - link_base['@tveh']
```

## 📐 PCE (Passenger Car Equivalent)

```python
# Standard PCE values
PCE = {
    'SOV': 1.0,
    'HOV2': 1.0,
    'HOV3': 1.0,
    'Light Truck': 1.0,
    'Medium Truck': 1.5,
    'Heavy Truck': 2.0,
    'Bus': 2.0
}

# Calculate equivalent vehicles
project.network_calculator("link_calculation", 
    result='@mveh', expression='@metrk/1.5')
project.network_calculator("link_calculation", 
    result='@hveh', expression='@hvtrk/2.0')
```

## 🎯 Performance Metrics

### Highway
- **VMT**: Vehicle-Miles-Traveled
- **VHT**: Vehicle-Hours-Traveled
- **V/C**: Volume/Capacity ratio
- **Delay**: Congested time - Free flow time

### Transit
- **PMT**: Person-Miles-Traveled
- **VHD**: Vehicle-Hours-Delay
- **Boardings**: By stop, route, agency
- **Load Factor**: Volume / Capacity

## 🔗 Emme Namespaces

```python
# Common tools
"inro.emme.network_calculation.network_calculator"
"inro.emme.traffic_assignment.sola_traffic_assignment"
"inro.emme.transit_assignment.extended_transit_assignment"
"inro.emme.matrix_calculation.matrix_calculator"
"inro.emme.data.extra_attribute.create_extra_attribute"
```

## 📚 File Locations

```
inputs/
  ├── skim_params/        # JSON configuration files
  ├── extra_attributes/   # Attribute value files
  ├── observed/           # Counts and validation data
  └── model/              # Model parameters

outputs/
  ├── network/            # Network summaries
  ├── transit/            # Transit performance
  └── supplemental/       # Additional outputs

scripts/
  ├── EmmeProject.py      # Main wrapper class
  ├── skimming/           # Assignment and skims
  ├── modeller/           # Emme Modeller tools
  └── summarize/          # Results processing
```

## 🆘 Troubleshooting

### Common Issues

**Desktop instance error**:
```python
# Ensure only one Emme desktop instance is running
# Or use dedicated desktop
desktop = app.start_dedicated(True, modeller_initial, filepath)
```

**Missing attribute**:
```python
# Check if attribute exists
if scenario.extra_attribute('@volume'):
    # Use it
else:
    # Create it first
    project.create_extra_attribute('LINK', '@volume', 'Volume', True)
```

**Matrix not found**:
```python
# List all matrices
for matrix in project.bank.matrices():
    print(f"{matrix.id}: {matrix.name}")
```

---

**For detailed documentation see:**
- `BKRCast_코드리뷰_활용가이드.md` (Korean)
- `EMME_PYTHON_GUIDE.md` (English)
