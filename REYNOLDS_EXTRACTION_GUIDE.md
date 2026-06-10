# Reynolds Number Extraction & Optimal Efficiency Computation

## Overview
This guide shows how to extract spanwise Reynolds numbers from simulations and compute optimal aerodynamic efficiency.

## Key Functions

### 1. `extract_reynolds_distribution()` (in `plotting.py`)
Extracts Reynolds numbers from QB simulation stats.

**Usage:**
```python
from plotting import extract_reynolds_distribution
from mappings import qblade_nodes_map

# Extract Reynolds for a specific simulation
spans, reynolds = extract_reynolds_distribution(
    stats_raw[model_idx],           # Use raw stats (has B1Re_n* columns)
    sim_label=9,                    # Row label for the simulation
    span_map=qblade_nodes_map,      # Optional: for accurate span positions
    blade=1                         # Blade number (default: 1)
)
```

**Returns:**
- `spans`: Array of spanwise positions (0-1), sorted
- `reynolds`: Array of Reynolds numbers at each span

**Notes:**
- Use `stats_raw` not `stats` (mapped stats drop unmapped columns)
- `span_map` optional - if not provided, infers position as node_i / max_node
- Works with QB format columns (`B1Re_n*`)

---

### 2. `compute_optimal_efficiency_distribution()` (in `aero_efficiency.py`)
Computes optimal AoA and L/D for each span position.

**Usage:**
```python
from aero_efficiency import compute_optimal_efficiency_distribution

yaml_path = "/path/to/turbine.yaml"

# Compute optimal operating points
results = compute_optimal_efficiency_distribution(
    yaml_path,
    reynolds_numbers=reynolds,      # From extract_reynolds_distribution()
    span_positions=spans,           # From extract_reynolds_distribution()
    aoa_range=(-5, 25)              # Search range for optimal AoA
)
```

**Returns DataFrame with columns:**
- `span`: Spanwise position (0-1)
- `reynolds`: Reynolds number at that position
- `optimal_aoa`: Angle of attack that maximizes L/D (degrees)
- `max_efficiency`: Maximum L/D ratio (Cl/Cd)
- `cl_opt`: Lift coefficient at optimal point
- `cd_opt`: Drag coefficient at optimal point

---

## Complete Example

```python
from mappings import qblade_to_openfast_map, qblade_nodes_map
from data_utils import load_and_map_stats
from plotting import extract_reynolds_distribution
from aero_efficiency import compute_optimal_efficiency_distribution
import matplotlib.pyplot as plt

# 1. Load simulation data
ss_names = ['/path/to/summary_stats.p']
stats_raw, stats = load_and_map_stats(ss_names, qblade_to_openfast_map, 
                                       drop_unmapped=True, verbose=False)

# 2. Extract Reynolds for a specific wind speed
sim_label = 9  # Row label for 9 m/s wind
model_idx = 0
spans, reynolds = extract_reynolds_distribution(
    stats_raw[model_idx], 
    sim_label=sim_label,
    span_map=qblade_nodes_map
)

# 3. Compute optimal efficiency
yaml_path = "/path/to/MED15-308_v30.3.2.yaml"
eff_results = compute_optimal_efficiency_distribution(
    yaml_path,
    reynolds_numbers=reynolds,
    span_positions=spans,
    aoa_range=(-5, 25)
)

# 4. Plot optimal AoA
fig, ax = plt.subplots()
ax.plot(eff_results['span'], eff_results['optimal_aoa'], 
        marker='o', label='Optimal AoA', linewidth=2)
ax.set_xlabel('Span position (r/R)')
ax.set_ylabel('Optimal AoA (degrees)')
ax.grid(True)
ax.legend()
plt.show()

# 5. Save results
eff_results.to_csv('optimal_efficiency.csv', index=False)
```

---

## Key Design Choices

### Why `extract_spanwise_data()`?
Generic helper function that extracts any spanwise channel (B1Cl, B1Cd, B1Re, etc.)
- Handles QB naming convention (`{channel}_n{node}`)
- Returns sorted arrays by span position
- Used internally by `plot_spanwise_aero()` and `extract_reynolds_distribution()`

### Why separate functions?
1. **Modularity**: Reynolds extraction decoupled from plotting
2. **Flexibility**: Can use for any analysis, not just plotting
3. **Cleanness**: Each function does one thing well

### Reynolds Number Extraction
- Prefers QB format (`B1Re_n*`) which preserves node information
- Auto-detects format and handles missing mappings gracefully
- Provides accurate span positions when `span_map` provided

---

## Troubleshooting

**Error: "No Reynolds columns found"**
- Ensure you're using `stats_raw` not `stats` (mapped stats drop B1Re columns)
- Check the sim_label matches an index in stats

**Error: "Row label not found"**
- sim_label must exist in stats index (usually 0-47 for 48 sims)
- Use `.zfill(2)` logic: label is zero-padded

**Unexpected optimal AoA values**
- Check Reynolds range is realistic (typically 3e6 to 12e6 for wind turbines)
- Verify YAML has polar data for relevant Re numbers
- Check aoa_range covers the airfoil data

---

## Performance Notes

- Expects accurate Reynolds numbers from simulations
- Interpolation is robust but requires sufficient airfoil polar data
- Skips problematic airfoils (e.g., 'circular', 'generic') automatically
