# BKRCast - Emme Python Integration Guide

## Overview

This document provides a comprehensive guide to understanding and using the **BKRCast** (Bellevue-Kirkland-Redmond Cast) travel demand model, with a focus on:
- **Emme Python API** integration
- **Highway (roadway) demand analysis**
- **Transit demand analysis**

## Quick Reference

### Key Files
- `scripts/EmmeProject.py` - Core Emme API wrapper class
- `scripts/skimming/SkimsAndPaths.py` - Skim and assignment module
- `emme_configuration.py` - Emme configuration parameters
- `run_bkrcast.py` - Main model runner

### Key Concepts
- **TOD (Time of Day)**: am, md, pm, ni (6-9, 9-15:30, 15:30-18:30, 18:30-6)
- **Extra Attributes**: User-defined network attributes (prefix with @)
- **Matrix Types**: FULL (OD), ORIGIN, DESTINATION, SCALAR
- **Emmebank**: Database containing scenarios, networks, and matrices

## EmmeProject Class - Core Methods

### Network Operations
```python
# Initialize project
project = EmmeProject('projects/LoadTripTables/LoadTripTables.emp')

# Import network elements
project.process_base_network(network_file)    # Road network
project.process_transit(transit_file)          # Transit lines
project.process_turn(turn_file)                # Turn restrictions
```

### Extra Attributes
```python
# Create link attribute
project.create_extra_attribute(
    type='LINK',           # NODE, LINK, TURN, TRANSIT_LINE, TRANSIT_SEGMENT
    name='@volume',
    description='Traffic volume',
    overwrite=True,
    default_value=0
)

# Network calculator
project.network_calculator(
    "link_calculation",
    result='@tveh',        # Target attribute
    expression='@svol + @hvol2 + @hvol3'  # Calculation
)
```

### Matrix Operations
```python
# Create matrix
project.create_matrix('sov_am', 'AM SOV trips', 'FULL')

# Convert numpy to Emme matrix
project.matrix_to_emme(numpy_array, 'sov_am', 'AM SOV trips', 'FULL')

# Convert Emme matrix to numpy
data = project.emmeMatrix_to_numpyMatrix('sov_am', 'float32', 1.0)
```

## Highway (Roadway) Demand Analysis

### Process Flow
1. **Network Import** → Load road network, modes, attributes
2. **VDF Setup** → Volume-Delay Functions (BPR functions)
3. **Load Trip Tables** → Import demand matrices by vehicle class
4. **Traffic Assignment** → SOLA or Path-based assignment
5. **Skim Generation** → Travel time, distance, cost matrices
6. **Convergence Check** → Iterate until equilibrium

### Multi-Class Assignment
```python
classes = [
    {'mode': 's', 'demand': 'mfSOV',    'results': {'link_volumes': '@svol'}},
    {'mode': 'h', 'demand': 'mfHOV2',   'results': {'link_volumes': '@hvol2'}},
    {'mode': 'h', 'demand': 'mfHOV3',   'results': {'link_volumes': '@hvol3'}},
    {'mode': 'c', 'demand': 'mfLTruck', 'results': {'link_volumes': '@lttrk'}},
    {'mode': 'c', 'demand': 'mfMTruck', 'results': {'link_volumes': '@metrk'}},
    {'mode': 'c', 'demand': 'mfHTruck', 'results': {'link_volumes': '@hvtrk'}}
]
```

### Vehicle Equivalency (PCE)
```python
# Medium trucks: PCE = 1.5
project.network_calculator("link_calculation", result='@mveh', expression='@metrk/1.5')

# Heavy trucks: PCE = 2.0
project.network_calculator("link_calculation", result='@hveh', expression='@hvtrk/2.0')

# Buses: PCE = 2.0
project.network_calculator("link_calculation", result='@bveh', expression='@trnv3/2.0')

# Total vehicles
expression = '@svol + @hvol2 + @hvol3 + @lttrk + @mveh + @hveh + @bveh'
project.network_calculator("link_calculation", result='@tveh', expression=expression)
```

## Transit Demand Analysis

### Process Flow
1. **Transit Network Load** → Import transit lines, stops, vehicles
2. **Node Attributes Setup** → Perception factors, headway fractions
3. **Extended Transit Assignment** → Multi-class transit assignment
4. **Boarding/Alighting Calculation** → By segment and by node
5. **Transit Skims** → In-vehicle time, wait time, fare
6. **Performance Metrics** → PMT, boardings, route performance

### Extended Transit Assignment
```python
spec = {
    "type": "EXTENDED_TRANSIT_ASSIGNMENT",
    "modes": ["b", "r", "p", "f", "l"],  # bus, rail, premium, ferry, light rail
    "demand": "mfTransit",
    
    "waiting_time": {
        "headway_fraction": "@headway_fraction",
        "perception_factor": "@wait_time"
    },
    "in_vehicle_time": {
        "perception_factor": "@in_vehicle_time"
    },
    
    "od_results": {
        "transit_times": "mfTransitTime",
        "total_impedance": "mfTransitImpedance"
    }
}
```

### Boarding/Alighting Calculation
```python
# Transit segment attributes
segment_attrs = {
    '@tboard': 'Total boardings',
    '@iboard': 'Initial boardings',
    '@trsboard': 'Transfer boardings',
    '@talight': 'Total alightings',
    '@finalight': 'Final alightings',
    '@transalight': 'Transfer alightings'
}

# Calculate using network results tool
network_results = project.m.tool("inro.emme.transit_assignment.extended.network_results")
spec = {
    "on_segments": {
        "total_boardings": "@tboard",
        "total_alightings": "@talight"
    }
}
network_results(spec, class_name='trnst')
```

### Transit Performance Metrics
```python
# PMT (Person-Miles-Traveled)
df_segment['PMT'] = df_segment['segment_volume'] * df_segment['length']

# VHD (Vehicle-Hours-Delay)
df_segment['VHD'] = df_segment['bus_vehicles'] * \
    (df_segment['transit_travel_time'] - df_segment['free_flow_time']) / 60
```

## Practical Examples

### Example 1: Basic Traffic Assignment
```python
from scripts.EmmeProject import EmmeProject

project = EmmeProject('projects/LoadTripTables/LoadTripTables.emp')
project.change_active_database('am')

# Run assignment
from scripts.skimming.SkimsAndPaths import run_sola_assignment
run_sola_assignment(project, max_iterations=50)

# Calculate VMT
network = project.current_scenario.get_network()
total_vmt = sum(link['@svol'] * link.length for link in network.links())
print(f"Total VMT: {total_vmt:,.0f} miles")
```

### Example 2: Transit Stop Analysis
```python
project = EmmeProject('projects/LoadTripTables/LoadTripTables.emp')

# Analyze all time periods
tod_list = ['am', 'md', 'pm', 'ni']
all_data = []

for tod in tod_list:
    project.change_active_database(tod)
    df_line, df_node, df_segment = project.transit_summary()
    all_data.append(df_node)

# Daily boardings by stop
df_daily = pd.concat(all_data, ignore_index=True)
daily_boarding = df_daily.groupby('node_id')['total_boarding'].sum()
top_10_stops = daily_boarding.nlargest(10)
```

### Example 3: V/C Ratio Analysis
```python
project = EmmeProject('projects/LoadTripTables/LoadTripTables.emp')

# Calculate V/C ratio
project.network_calculator(
    "link_calculation",
    result='@vc_ratio',
    expression='@tveh / ul2'
)

# Find congested links (V/C > 1.0)
network = project.current_scenario.get_network()
congested = [link for link in network.links() if link['@vc_ratio'] > 1.0]
print(f"Found {len(congested)} congested links")
```

### Example 4: HOT Lane Revenue
```python
project = EmmeProject('projects/LoadTripTables/LoadTripTables.emp')
project.change_active_database('am')

network = project.current_scenario.get_network()
total_revenue = 0

for link in network.links():
    if link['@tolllane'] > 0:
        sov_revenue = link['@svol'] * link['@stoll'] / 100
        hov_revenue = (link['@hvol2'] + link['@hvol3']) * link['@htoll'] / 100
        total_revenue += sov_revenue + hov_revenue

print(f"Total AM HOT Lane Revenue: ${total_revenue:,.2f}")
```

## Configuration Files

### emme_configuration.py
- Network parameters (modes, units, TOD definitions)
- Extra attributes definitions
- Assignment parameters (max_iter, relative_gap)
- HOT lane toll rates by TOD
- Transit node perception factors

### input_configuration.py
- File paths and directories
- Model switches (run_daysim, run_skims, etc.)
- Population sampling parameters
- Convergence criteria
- Output specifications

## Key Namespaces (Emme Tools)

```python
# Traffic Assignment
"inro.emme.traffic_assignment.sola_traffic_assignment"
"inro.emme.traffic_assignment.path_based_traffic_assignment"

# Transit Assignment
"inro.emme.transit_assignment.extended_transit_assignment"
"inro.emme.transit_assignment.extended.matrix_results"
"inro.emme.transit_assignment.extended.network_results"

# Network Operations
"inro.emme.network_calculation.network_calculator"
"inro.emme.data.network.base.base_network_transaction"
"inro.emme.data.network.transit.transit_line_transaction"

# Matrix Operations
"inro.emme.matrix_calculation.matrix_calculator"
"inro.emme.data.matrix.create_matrix"
"inro.emme.data.matrix.export_to_omx"

# Extra Attributes
"inro.emme.data.extra_attribute.create_extra_attribute"
"inro.emme.data.extra_attribute.delete_extra_attribute"
```

## Use Cases

### 1. Traffic Impact Analysis
- Forecast trip generation from new developments
- Analyze impacts on surrounding road network
- Evaluate signal timing improvements

### 2. Transit Planning
- Design new bus routes
- Optimize headways
- Evaluate BRT systems

### 3. Roadway Improvement Projects
- Analyze lane addition benefits
- Evaluate HOV/HOT lane implementation
- Assess intersection improvements

### 4. Policy Scenario Analysis
- VMT reduction policies
- Toll pricing strategies
- Transportation Demand Management (TDM) effects

### 5. Performance Monitoring
- V/C ratio analysis
- Level of Service (LOS) evaluation
- Bottleneck identification

## Model Integration

BKRCast integrates multiple components:
1. **Daysim** - Activity-based travel demand model
2. **Emme** - Network assignment and skimming
3. **Truck Model** - Commercial vehicle trips
4. **Supplemental Trips** - External, airport, special generators
5. **Bike Model** - Bicycle mode choice and routing

## Data Flow

```
Synthetic Population (H5)
    ↓
Daysim → Trip Tables
    ↓
Emme Assignment → Skims
    ↓
← Feedback Loop (iterate until convergence)
    ↓
Summary & Reporting
```

## Learning Resources

- **Korean Guide**: `BKRCast_코드리뷰_활용가이드.md` (detailed Korean documentation)
- **Emme Documentation**: Official Inro Emme Python API reference
- **BKRCast Wiki**: https://github.com/Bellevuewa/BKRCast/wiki
- **Four-Step Model Theory**: Traditional travel demand forecasting
- **Activity-Based Models**: Daysim framework

## Contact

- **GitHub**: https://github.com/traffic7/BKRCast
- **Organization**: City of Bellevue Transportation Department

---

*Document Version: 2024*
*For detailed Korean documentation, see: BKRCast_코드리뷰_활용가이드.md*
