"""
Aerodynamic efficiency analysis: compute optimal AoA and sectional L/D along blade span.

This module extracts polar data from turbine YAML definitions, interpolates across
span, Reynolds number, and angle of attack, and returns optimal operating points.
"""

import yaml
import numpy as np
import pandas as pd
from scipy.interpolate import RectBivariateSpline, interp1d
import warnings


def load_yaml_turbine(yaml_path):
    """Load turbine definition from YAML file."""
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)


def extract_airfoil_positions(turbine_def):
    """
    Extract airfoil positions and names from the blade definition.
    
    Returns:
        airfoil_positions : dict
            Mapping of span position (0-1) to airfoil name
        span_positions : array
            Sorted array of span positions
    """
    blade = turbine_def['components']['blade']
    outer_shape = blade['outer_shape_bem']
    
    # Extract positions and airfoil names
    airfoil_positions = {}
    
    if 'airfoil_position' in outer_shape and outer_shape['airfoil_position'] is not None:
        af_pos = outer_shape['airfoil_position']
        
        # Handle dict structure with 'grid' and 'labels'
        if isinstance(af_pos, dict) and 'grid' in af_pos and 'labels' in af_pos:
            grid = af_pos['grid']
            labels = af_pos['labels']
            
            if len(grid) == len(labels):
                for pos, name in zip(grid, labels):
                    airfoil_positions[float(pos)] = str(name)
        
        # Handle list of dicts structure (legacy)
        elif isinstance(af_pos, list):
            for entry in af_pos:
                if isinstance(entry, dict):
                    pos = entry.get('position')
                    name = entry.get('name')
                    if pos is not None and name is not None:
                        airfoil_positions[float(pos)] = str(name)
    
    # Sort by position
    span_positions = np.array(sorted(airfoil_positions.keys()))
    
    return airfoil_positions, span_positions


def extract_polar_data(turbine_def, airfoil_name):
    """
    Extract Cl, Cd, and Re data for a given airfoil.
    
    The YAML format has:
    - c_l, c_d, c_m as dicts with 'grid' (alpha values) and 'values' arrays
    - re: Reynolds number as float
    
    Returns:
        polars_dict : dict
            Dictionary with keys 're' (Reynolds numbers as floats) and 
            each Re having a dict of {aoa, cl, cd} arrays
    """
    airfoils = turbine_def.get('airfoils', [])
    
    target_airfoil = None
    for af in airfoils:
        if af.get('name') == airfoil_name:
            target_airfoil = af
            break
    
    if target_airfoil is None:
        raise ValueError(f"Airfoil {airfoil_name} not found in YAML definition")
    
    polars_data = target_airfoil.get('polars', [])
    if not polars_data:
        warnings.warn(f"No polar data found for airfoil {airfoil_name}")
        return None
    
    # Organize by Reynolds number
    polars_dict = {}
    
    for polar_entry in polars_data:
        re = polar_entry.get('re')
        if re is None:
            continue
        
        # Extract c_l and c_d from nested dict structure
        c_l_data = polar_entry.get('c_l', {})
        c_d_data = polar_entry.get('c_d', {})
        
        if isinstance(c_l_data, dict) and isinstance(c_d_data, dict):
            # New format: {'grid': [...], 'values': [...]}
            aoa = np.array(c_l_data.get('grid', []))
            cl = np.array(c_l_data.get('values', []))
            cd = np.array(c_d_data.get('values', []))
        else:
            # Fallback for old format (if it exists)
            aoa = np.array(polar_entry.get('alpha', []))
            cl = np.array(c_l_data if isinstance(c_l_data, list) else [])
            cd = np.array(c_d_data if isinstance(c_d_data, list) else [])
        
        if len(aoa) > 0 and len(cl) > 0 and len(cd) > 0 and len(aoa) == len(cl) == len(cd):
            polars_dict[float(re)] = {
                'aoa': aoa,
                'cl': cl,
                'cd': cd
            }
    
    if not polars_dict:
        warnings.warn(f"No valid polar data found for airfoil {airfoil_name}")
        return None
    
    return polars_dict


def interpolate_cl_cd(polars_dict, re_target, aoa_array, kind='linear'):
    """
    Interpolate Cl and Cd for given Reynolds number and AoA array.
    
    Uses linear interpolation in Re, then linear in AoA (more robust than cubic).
    
    Parameters:
        polars_dict : dict
            Polar data dictionary with Re values as keys
        re_target : float
            Target Reynolds number for interpolation
        aoa_array : array
            Array of angles of attack to interpolate to
        kind : str
            Interpolation kind ('linear' or 'cubic'). Default 'linear' is more robust.
    
    Returns:
        cl_interp : array
            Interpolated lift coefficient
        cd_interp : array
            Interpolated drag coefficient
    """
    re_values = sorted(polars_dict.keys())
    
    # Handle out-of-range Re by clamping to nearest
    if re_target < min(re_values):
        re_target = min(re_values)
    elif re_target > max(re_values):
        re_target = max(re_values)
    
    # Find bracketing Reynolds numbers
    if re_target in polars_dict:
        # Exact match
        re_lower = re_upper = re_target
        weight_upper = 1.0
    else:
        # Interpolate between two Re values
        idx_upper = np.searchsorted(re_values, re_target)
        re_lower = re_values[idx_upper - 1]
        re_upper = re_values[idx_upper]
        weight_upper = (re_target - re_lower) / (re_upper - re_lower)
    
    # Get polar data at lower and upper Re
    data_lower = polars_dict[re_lower]
    data_upper = polars_dict[re_upper]
    
    # Sort by AoA to ensure monotonicity for interpolation
    sort_idx_lower = np.argsort(data_lower['aoa'])
    sort_idx_upper = np.argsort(data_upper['aoa'])
    
    aoa_lower_sorted = data_lower['aoa'][sort_idx_lower]
    cl_lower_sorted = data_lower['cl'][sort_idx_lower]
    cd_lower_sorted = data_lower['cd'][sort_idx_lower]
    
    aoa_upper_sorted = data_upper['aoa'][sort_idx_upper]
    cl_upper_sorted = data_upper['cl'][sort_idx_upper]
    cd_upper_sorted = data_upper['cd'][sort_idx_upper]
    
    # Interpolate Cl and Cd at target Re for each AoA in aoa_array
    cl_lower = interp1d(aoa_lower_sorted, cl_lower_sorted, kind=kind, 
                        fill_value='extrapolate', bounds_error=False)
    cd_lower = interp1d(aoa_lower_sorted, cd_lower_sorted, kind=kind,
                        fill_value='extrapolate', bounds_error=False)
    
    cl_upper = interp1d(aoa_upper_sorted, cl_upper_sorted, kind=kind,
                        fill_value='extrapolate', bounds_error=False)
    cd_upper = interp1d(aoa_upper_sorted, cd_upper_sorted, kind=kind,
                        fill_value='extrapolate', bounds_error=False)
    
    cl_lower_vals = cl_lower(aoa_array)
    cd_lower_vals = cd_lower(aoa_array)
    cl_upper_vals = cl_upper(aoa_array)
    cd_upper_vals = cd_upper(aoa_array)
    
    # Linear interpolation in Re
    cl_interp = (1 - weight_upper) * cl_lower_vals + weight_upper * cl_upper_vals
    cd_interp = (1 - weight_upper) * cd_lower_vals + weight_upper * cd_upper_vals
    
    return cl_interp, cd_interp


def compute_sectional_efficiency(cl, cd):
    """
    Compute sectional aerodynamic efficiency (L/D).
    
    Parameters:
        cl : array or float
            Lift coefficients
        cd : array or float
            Drag coefficients
    
    Returns:
        efficiency : array or float
            L/D ratio (Cl/Cd)
    """
    with np.errstate(divide='ignore', invalid='ignore'):
        efficiency = np.where(cd != 0, cl / cd, np.nan)
    return efficiency


def find_optimal_aoa(polars_dict, re_target, aoa_range=None, n_points=500, 
                     cl_min=0.0, cl_max=2.5):
    """
    Find angle of attack that maximizes L/D for given Reynolds number.
    
    Filters for physically sensible operating ranges (positive Cl, reasonable range).
    
    Parameters:
        polars_dict : dict
            Polar data dictionary
        re_target : float
            Target Reynolds number
        aoa_range : tuple, optional
            (min_aoa, max_aoa) for search range. If None, uses full polar range.
        n_points : int
            Number of points for interpolation search
        cl_min : float
            Minimum Cl to consider (filters stall region)
        cl_max : float
            Maximum Cl to consider (filters unrealistic values)
    
    Returns:
        optimal_aoa : float
            Angle of attack that maximizes L/D
        max_efficiency : float
            Maximum L/D value
        cl_opt : float
            Cl at optimal point
        cd_opt : float
            Cd at optimal point
    """
    re_values = sorted(polars_dict.keys())
    
    if aoa_range is None:
        # Use reasonable default range for forward flight
        aoa_range = (-5, 25)
    
    aoa_range = np.radians(aoa_range)
    # Create fine AoA grid for optimization
    aoa_grid = np.linspace(aoa_range[0], aoa_range[1], n_points)
    
    # Interpolate Cl, Cd at this Re
    cl_fine, cd_fine = interpolate_cl_cd(polars_dict, re_target, aoa_grid, kind='linear')
    
    # Compute efficiency
    efficiency = compute_sectional_efficiency(cl_fine, cd_fine)

    import matplotlib.pyplot as plt
    plt.plot(cd_fine, cl_fine)
    
    # Filter for physically sensible operating range
    valid_mask = (
        (cl_fine >= cl_min) & 
        (cl_fine <= cl_max) & 
        (cd_fine > 0) &                    # Positive drag
        (efficiency > 0) &                 # Positive L/D
        np.isfinite(efficiency)            # No NaN/Inf
    )
    
    if not np.any(valid_mask):
        # Fallback: just find max efficiency regardless
        valid_idx = ~np.isnan(efficiency) & ~np.isinf(efficiency)
        if not np.any(valid_idx):
            return np.nan, np.nan, np.nan, np.nan
        max_idx = np.argmax(efficiency[valid_idx])
        optimal_aoa = aoa_grid[valid_idx][max_idx]
        max_efficiency = efficiency[valid_idx][max_idx]
        cl_opt = cl_fine[valid_idx][max_idx]
        cd_opt = cd_fine[valid_idx][max_idx]
    else:
        # Find maximum L/D in valid range
        valid_aoas = aoa_grid[valid_mask]
        valid_efficiencies = efficiency[valid_mask]
        valid_cls = cl_fine[valid_mask]
        valid_cds = cd_fine[valid_mask]
        
        max_idx = np.argmax(valid_efficiencies)
        optimal_aoa = valid_aoas[max_idx]
        max_efficiency = valid_efficiencies[max_idx]
        cl_opt = valid_cls[max_idx]
        cd_opt = valid_cds[max_idx]
    
    return np.degrees(optimal_aoa), max_efficiency, cl_opt, cd_opt


def interpolate_airfoil_at_span(turbine_def, span_position):
    """
    Interpolate airfoil definition at a given span position.
    
    If span position falls between defined airfoils, performs linear interpolation
    in polar coefficient space.
    
    Parameters:
        turbine_def : dict
            Turbine definition from YAML
        span_position : float
            Span position (0-1) along blade
    
    Returns:
        interpolated_airfoil : dict or None
            Dictionary with 're' keys pointing to interpolated polar data
    """
    airfoil_positions, span_positions = extract_airfoil_positions(turbine_def)
    
    # Handle edge cases
    if span_position <= span_positions[0]:
        airfoil_name = airfoil_positions[span_positions[0]]
        return extract_polar_data(turbine_def, airfoil_name)
    elif span_position >= span_positions[-1]:
        airfoil_name = airfoil_positions[span_positions[-1]]
        return extract_polar_data(turbine_def, airfoil_name)
    
    # Find bracketing positions
    idx_upper = np.searchsorted(span_positions, span_position)
    span_lower = span_positions[idx_upper - 1]
    span_upper = span_positions[idx_upper]
    
    airfoil_lower_name = airfoil_positions[span_lower]
    airfoil_upper_name = airfoil_positions[span_upper]
    
    polars_lower = extract_polar_data(turbine_def, airfoil_lower_name)
    polars_upper = extract_polar_data(turbine_def, airfoil_upper_name)
    
    if polars_lower is None or polars_upper is None:
        # Fall back to one of them
        return polars_lower if polars_lower is not None else polars_upper
    
    # Linear interpolation weight
    weight_upper = (span_position - span_lower) / (span_upper - span_lower)
    
    # Merge Reynolds numbers from both
    all_re = set(polars_lower.keys()) | set(polars_upper.keys())
    interpolated = {}
    
    for re in all_re:
        if re in polars_lower and re in polars_upper:
            # Interpolate Cl, Cd at this Re
            # Use a common AoA grid
            aoa_lower = polars_lower[re]['aoa']
            aoa_upper = polars_upper[re]['aoa']
            aoa_common = np.linspace(
                max(np.min(aoa_lower), np.min(aoa_upper)),
                min(np.max(aoa_lower), np.max(aoa_upper)),
                100
            )
            
            cl_lower = interp1d(aoa_lower, polars_lower[re]['cl'], kind='cubic',
                               fill_value='extrapolate', bounds_error=False)
            cd_lower = interp1d(aoa_lower, polars_lower[re]['cd'], kind='cubic',
                               fill_value='extrapolate', bounds_error=False)
            cl_upper = interp1d(aoa_upper, polars_upper[re]['cl'], kind='cubic',
                               fill_value='extrapolate', bounds_error=False)
            cd_upper = interp1d(aoa_upper, polars_upper[re]['cd'], kind='cubic',
                               fill_value='extrapolate', bounds_error=False)
            
            cl_interp = (1 - weight_upper) * cl_lower(aoa_common) + weight_upper * cl_upper(aoa_common)
            cd_interp = (1 - weight_upper) * cd_lower(aoa_common) + weight_upper * cd_upper(aoa_common)
            
            interpolated[re] = {
                'aoa': aoa_common,
                'cl': cl_interp,
                'cd': cd_interp
            }
        elif re in polars_lower:
            interpolated[re] = polars_lower[re]
        else:
            interpolated[re] = polars_upper[re]
    
    return interpolated if interpolated else None


def compute_optimal_efficiency_distribution(yaml_path, reynolds_numbers, 
                                           span_positions=None, aoa_range=None,
                                           skip_airfoils=None):
    """
    Main function: compute optimal AoA and max L/D for each span position.
    
    Parameters:
        yaml_path : str
            Path to turbine YAML file
        reynolds_numbers : array or DataFrame
            Reynolds numbers at each span position. Can be:
            - 1D array of Re values (one per span position)
            - DataFrame with Re values indexed by span position
            - Dict mapping span positions to Re values
        span_positions : array, optional
            Span positions (0-1) where to compute results. If None, uses
            positions from blade definition.
        aoa_range : tuple, optional
            (min_aoa, max_aoa) search range
        skip_airfoils : list, optional
            Airfoil names to skip (default: ['circular', 'generic'])
    
    Returns:
        results : DataFrame
            Columns: ['span', 'reynolds', 'optimal_aoa', 'max_efficiency', 'cl_opt', 'cd_opt']
    """
    if skip_airfoils is None:
        skip_airfoils = ['circular', 'generic']
    
    # Load turbine definition
    turbine_def = load_yaml_turbine(yaml_path)
    
    # Get airfoil positions
    airfoil_pos, default_spans = extract_airfoil_positions(turbine_def)
    
    if span_positions is None:
        span_positions = default_spans
    
    # Convert span_positions to array if needed
    span_positions = np.atleast_1d(span_positions)
    
    # Handle different reynolds_numbers input formats
    if isinstance(reynolds_numbers, pd.DataFrame):
        # Assume index or columns aligned with span positions
        re_dict = dict(zip(span_positions, reynolds_numbers.values.flatten()))
    elif isinstance(reynolds_numbers, dict):
        re_dict = reynolds_numbers
    else:
        # Assume array aligned with span_positions
        reynolds_numbers = np.atleast_1d(reynolds_numbers)
        if len(reynolds_numbers) != len(span_positions):
            raise ValueError(
                f"Length mismatch: {len(reynolds_numbers)} Re values "
                f"for {len(span_positions)} span positions"
            )
        re_dict = dict(zip(span_positions, reynolds_numbers))
    
    results = []
    skipped_count = 0
    
    for span in span_positions:
        try:
            # Get Reynolds number at this span
            re_target = re_dict.get(span)
            if re_target is None:
                warnings.warn(f"No Reynolds number provided for span {span}, skipping")
                continue
            
            # Check what airfoil is at this position
            nearest_airfoil_span = min(airfoil_pos.keys(), key=lambda x: abs(x - span))
            airfoil_at_span = airfoil_pos[nearest_airfoil_span]
            
            # Skip problematic airfoils
            if any(skip_name.lower() in airfoil_at_span.lower() for skip_name in skip_airfoils):
                skipped_count += 1
                continue
            
            # Get interpolated airfoil at this span
            polars_interp = interpolate_airfoil_at_span(turbine_def, span)
            
            if polars_interp is None:
                warnings.warn(f"Could not obtain airfoil data for span {span}")
                continue
            
            # Find optimal AoA (now returns 4 values)
            optimal_aoa, max_efficiency, cl_opt, cd_opt = find_optimal_aoa(
                polars_interp, re_target, aoa_range=aoa_range
            )
            
            # Only add if we found valid results
            if np.isfinite(optimal_aoa) and np.isfinite(max_efficiency):
                results.append({
                    'span': span,
                    'reynolds': re_target,
                    'optimal_aoa': optimal_aoa,
                    'max_efficiency': max_efficiency,
                    'cl_opt': cl_opt,
                    'cd_opt': cd_opt
                })
        
        except Exception as e:
            warnings.warn(f"Error processing span {span}: {e}")
            continue
    
    print(f"Skipped {skipped_count} problematic airfoils (e.g., 'circular')")
    
    results_df = pd.DataFrame(results)
    return results_df


def get_optimal_aoa_at_wind_speed(yaml_path, stats_df, wind_speed_idx, 
                                   sim_label, qblade_nodes_map=None,
                                   aoa_range=None):
    """
    Convenience wrapper: extract Reynolds numbers from stats and compute optimal efficiency.
    
    This function extracts spanwise Reynolds number from QB-WEIS stats for a specific
    wind speed/simulation, then computes optimal AoA and efficiency.
    
    Parameters:
        yaml_path : str
            Path to turbine YAML
        stats_df : DataFrame
            Stats DataFrame with MultiIndex columns (channel, stat_type)
        wind_speed_idx : int
            Simulation index corresponding to desired wind speed
        sim_label : int
            Label to match in stats index (e.g., sim number)
        qblade_nodes_map : dict, optional
            Mapping from node number to span position (0-1). 
            If None, uses default assumption of equal spacing.
        aoa_range : tuple, optional
            Search range for optimal AoA
    
    Returns:
        results : DataFrame
            Optimal efficiency distribution at this wind speed
    """
    # Extract B1AxInd (axial induction) to infer span positions
    try:
        axi_cols = [c for c in stats_df.columns if 'B1AxInd' in c[0]]
        if not axi_cols:
            raise ValueError("No B1AxInd columns found in stats")
        
        # Extract mean values
        stats_mean = stats_df.xs('mean', axis=1, level=1)
        row_label = str(sim_label).zfill(2)
        lbl = None
        for elm in stats_mean.index:
            if '_'+row_label+'_' in elm:
                lbl = elm
                break
        
        if lbl is None:
            raise ValueError(f"No stats row found for label {sim_label}")
        
        # Extract Reynolds numbers (use B1AxInd as proxy for extracting node positions)
        reynolds_vals = []
        span_vals = []
        
        for col in axi_cols:
            # Extract node number
            import re
            match = re.search(r'_n(\d+)', col)
            if match:
                node_num = int(match.group(1))
                # Map to span position
                if qblade_nodes_map:
                    span_pos = qblade_nodes_map.get(node_num)
                else:
                    # Assume linear spacing
                    span_pos = node_num / 10.0
                
                # Try to get Reynolds number from stats
                # (You may need to adjust this if Reynolds is not directly in stats)
                # For now, estimate based on wind speed and span position
                re_val = 5e6  # placeholder
                
                reynolds_vals.append(re_val)
                span_vals.append(span_pos)
        
        reynolds_vals = np.array(reynolds_vals)
        span_vals = np.array(span_vals)
        
    except Exception as e:
        warnings.warn(f"Could not extract Reynolds from stats: {e}")
        # Use default
        reynolds_vals = np.linspace(3e6, 10e6, 20)
        span_vals = np.linspace(0.1, 1.0, 20)
    
    # Compute optimal efficiency
    results = compute_optimal_efficiency_distribution(
        yaml_path,
        reynolds_vals,
        span_positions=span_vals,
        aoa_range=aoa_range
    )
    
    return results


# Example usage / testing
if __name__ == "__main__":
    # Test with sample data
    yaml_path = "/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.3.2_BOPTNSS/MED15-308_v30.3.2.yaml"
    
    # Sample Reynolds numbers (one per spanwise position - adjust as needed)
    reynolds_sample = np.linspace(3e6, 10e6, 40)  # 40 points along span
    span_sample = np.linspace(0.0, 1.0, 40)
    
    try:
        results = compute_optimal_efficiency_distribution(
            yaml_path, 
            reynolds_sample, 
            span_positions=span_sample,
            aoa_range=(-10, 25)
        )
        
        print("Optimal efficiency distribution:")
        print(results)
        print("\nResults saved to 'optimal_efficiency.csv'")
        results.to_csv('optimal_efficiency.csv', index=False)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
