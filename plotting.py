import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import re
import numpy as np
import scipy.signal as signal
import pandas as pd

def extract_spanwise_data(df_mean, channel_prefix, sim_label, span_map):
    """
    Extract spanwise data for a given channel and simulation.
    
    Searches for columns matching the pattern: {channel_prefix}_n{node_number}
    Returns sorted arrays of spanwise positions and corresponding values.
    
    Parameters:
        df_mean : DataFrame
            Mean values slice of stats DataFrame (already extracted with .xs('mean', axis=1, level=1))
        channel_prefix : str
            Channel prefix to match (e.g., 'B1Re', 'B1Cl', 'B1AxInd')
        sim_label : int
            Simulation label to match in index
        span_map : dict
            Mapping from node number to span position (0-1)
    
    Returns:
        spans : array
            Sorted spanwise positions (0-1)
        values : array
            Sorted values corresponding to spans
        matching_cols : list
            Column names that matched (for reference)
    
    Raises:
        ValueError if no matching columns found or sim_label not found in index
    """
    # Construct row label from simulation index, zero-padded
    row_label = str(sim_label).zfill(2)
    lbl = False
    for elm in df_mean.index:
        if '_' + row_label + '_' in elm:
            lbl = elm
            break
    
    if not lbl:
        raise ValueError(f"Row label {row_label} not found in stats index")
    
    matching_cols = []  # Column names matching the channel
    spans = []          # Corresponding spanwise positions
    
    for col in df_mean.columns:
        # Match pattern: {channel_prefix}_n{digits}
        match = re.search(r'^' + re.escape(channel_prefix) + r'_n(\d+)', col)
        if match:
            node = float(match.group(1))
            if node in span_map:
                matching_cols.append(col)
                spans.append(span_map[node])
    
    if not matching_cols:
        raise ValueError(
            f"No spanwise columns found for channel '{channel_prefix}' "
            f"with pattern '{channel_prefix}_n*'"
        )
    
    # Sort by span position
    sorted_pairs = sorted(zip(spans, matching_cols))
    spans, matching_cols = zip(*sorted_pairs)
    spans = np.array(spans)
    
    # Extract values
    values = df_mean.loc[lbl, list(matching_cols)].values
    
    return spans, values, list(matching_cols)


def plot_stat_vs_wind(ax, data, x_col, y_col, style, label):
    x = data[x_col]['mean']
    y_mean = data[y_col]['mean']
    y_max = data[y_col]['max']
    y_min = data[y_col]['min']

    ax.plot(x, y_mean, label=label, **style)
    ax.scatter(x, y_max, edgecolor=style['color'], color='none', marker='^', s = 14)
    ax.scatter(x, y_min, edgecolor=style['color'], color='none', marker='v', s = 14)
    ax.grid(linestyle =':', color = 'gray')

def plot_DEL_vs_wind(ax, data_st, data_DEL, x_col, y_col, style, label):
    x = data_st[x_col]['mean']
    y_mean = data_DEL[y_col]

    ax.plot(x, y_mean, label=label, **style)
    ax.grid(linestyle =':', color = 'gray')

import numpy as np
import pandas as pd


def bin_sims_by_mean_wind_speed_pd(
    data,
    wind_speed_channel,
    value_channel,
    min_count=1,
    gap_factor=4.0,
    tol = 0.1,
):
    """
    Cluster simulations by mean wind speed using adaptive gap detection.

    This replaces fixed-width binning and is robust to uneven wind-speed spacing.

    Parameters
    ----------
    data : pandas.DataFrame
        Stats dataframe (rows = simulations).
    wind_speed_channel : str
        Channel name used to compute mean wind speed per simulation.
    value_channel : str
        Channel name whose mean value is aggregated per cluster.
    min_count : int, optional
        Minimum number of simulations required per cluster.
    gap_factor : float, optional
        Multiplier for median gap used to detect cluster boundaries.

    Returns
    -------
    pandas.DataFrame
        Clustered statistics (mean of means).
    """

    # --- Extract data ---
    ws = data[wind_speed_channel]["mean"]
    val = data[value_channel]["mean"]

    if ws.empty:
        raise ValueError("No valid simulations found")

    # --- Sort wind speeds ---
    order = np.argsort(ws.values)
    ws_sorted = ws.values[order]

    # --- Compute gaps ---
    gaps = np.diff(ws_sorted)
    gaps_m = gaps[(gaps > tol)]
    median_gap = np.median(gaps_m)

    print(f"Median gap: {median_gap}")
    print(gaps)

    # --- Handle degenerate cases ---
    if median_gap == 0 or not np.isfinite(median_gap):
        data = data.copy()
        data["ws_cluster"] = ws.mean()
    else:
        # --- Detect cluster boundaries ---
        split_idx = np.where(gaps > gap_factor * median_gap)[0]

        cluster_labels = np.zeros(len(ws_sorted), dtype=int)
        cluster_id = 0
        start = 0

        for idx in split_idx:
            end = idx + 1
            cluster_labels[start:end] = cluster_id
            cluster_id += 1
            start = end

        cluster_labels[start:] = cluster_id

        # --- Map back to original order ---
        labels = np.empty_like(cluster_labels)
        labels[order] = cluster_labels

        data = data.copy()
        data["ws_cluster"] = labels

    # --- Aggregate ---
    grouped = (
        data.groupby("ws_cluster", observed=True)
        .mean()
        .reset_index(drop=True)
    )

    # --- Optional: enforce minimum count ---
    if min_count > 1:
        counts = data.groupby("ws_cluster").size().values
        grouped = grouped[counts >= min_count]

    return grouped



def plot_spanwise_comparison(stats_mapped, spanwise_channels, labels, colors, linestyles, fig, axs, sim_label, title_prefix="", show_extrema=False):
    
    if len(spanwise_channels) == 1:
        axs = [axs]

    for i, chan in enumerate(spanwise_channels):
        ax = axs[i]

        for j, df in stats_mapped.items():
            try:
                # Extract mean, max and min slices from multi-index DataFrame
                df_mean = df.xs('mean', axis=1, level=1)
                df_max = df.xs('max', axis=1, level=1) if show_extrema else None
                df_min = df.xs('min', axis=1, level=1) if show_extrema else None

                # Construct row label from simulation index, zero-padded
                row_label = str(sim_label).zfill(2)
                lbl = False
                for elm in df_mean.index:
                    if '_'+row_label+'_' in elm: 
                        lbl = elm

                if not lbl:
                    raise ValueError(f"Row label {row_label} not found in index")

                matching_cols = []  # holds column names matching current channel
                spans = []          # holds corresponding spanwise positions

                for col in df_mean.columns:
                    if chan in col:
                        match = re.search(r'(\d+\.\d+)', col)
                        if match:
                            matching_cols.append(col)
                            spans.append(float(match.group(1)))

                if not matching_cols:
                    raise ValueError("No valid spanwise data columns found")

                # Sort columns by their spanwise numeric values
                sorted_pairs = sorted(zip(spans, matching_cols))
                spans, matching_cols = zip(*sorted_pairs)

                # Extract mean values along span for selected row and columns
                values = df_mean.loc[lbl, list(matching_cols)].values

                ax.plot(spans, values, label=labels[j], color=colors[j], linestyle=linestyles[j])

                if show_extrema and df_max is not None and df_min is not None:
                    y_max = df_max.loc[lbl, list(matching_cols)].values
                    y_min = df_min.loc[lbl, list(matching_cols)].values
                    ax.scatter(spans, y_max, edgecolor=colors[j], color='none', marker='^')
                    ax.scatter(spans, y_min, edgecolor=colors[j], color='none', marker='v')

            except Exception as e:
                print(f"Failed to plot {chan} for dataset {j}: {e}")
                continue

        ax.set_title(f"{title_prefix}{chan}")
        ax.set_xlabel("Spanwise position (r/R)")
        ax.set_ylabel(chan)
        ax.grid(linestyle =':', color = 'gray')

    handles, labels = axs[0].get_legend_handles_labels()
    add_shared_legend(fig, handles, labels)

def plot_spanwise_aero(stats_mapped, spanwise_channels, span_map, labels, colors, linestyles, fig, axs, sim_label, title_prefix="", show_extrema=False):
    
    if len(spanwise_channels) == 1:
        axs = [axs]

    for i, chan in enumerate(spanwise_channels):
        ax = axs[i]

        for j, df in stats_mapped.items():
            try:
                # Extract mean, max and min slices from multi-index DataFrame
                df_mean = df.xs('mean', axis=1, level=1)
                df_max = df.xs('max', axis=1, level=1) if show_extrema else None
                df_min = df.xs('min', axis=1, level=1) if show_extrema else None

                # Use helper to extract spanwise data
                spans, values, _ = extract_spanwise_data(df_mean, chan, sim_label, span_map)

                ax.plot(spans, values, label=labels[j], color=colors[j], linestyle=linestyles[j])

                if show_extrema and df_max is not None and df_min is not None:
                    # Extract extrema using same method
                    _, y_max, _ = extract_spanwise_data(df_max, chan, sim_label, span_map)
                    _, y_min, _ = extract_spanwise_data(df_min, chan, sim_label, span_map)
                    ax.fill_between(spans, y_max, y_min, color=colors[j], alpha=0.2)

            except Exception as e:
                print(f"Failed to plot {chan} for dataset {j}: {e}")
                continue

        ax.set_title(f"{title_prefix}{chan}")
        ax.set_xlabel("Spanwise position (r/R)")
        ax.set_ylabel(chan)
        ax.grid(linestyle =':', color = 'gray')

    handles, labels = axs[0].get_legend_handles_labels()
    add_shared_legend(fig, handles, labels)

def extract_reynolds_distribution(stats_df, sim_label, span_map=None, blade=1, 
                                   from_raw=False):
    """
    Extract spanwise Reynolds number distribution for a given simulation.
    
    Prioritizes QB format (B1Re_n*) which works with raw or mapped stats.
    
    Parameters:
        stats_df : DataFrame
            Stats DataFrame with MultiIndex columns (channel, stat_type).
            Can be either raw QB format or mapped FAST format (both have B1Re_n cols).
        sim_label : int
            Simulation label (e.g., wind speed index)
        span_map : dict, optional
            Mapping from node number to span position (0-1). 
            If None, infers positions as node_i / max_node.
        blade : int, optional
            Blade number (default 1, for B1Re)
        from_raw : bool, optional
            Kept for backward compatibility. Function now auto-detects format.
    
    Returns:
        span_positions : array
            Spanwise positions (0-1), sorted
        reynolds_numbers : array
            Reynolds numbers at each span position, sorted by position
    
    Example:
        >>> # Extract Reynolds from any stats format
        >>> spans, re_vals = extract_reynolds_distribution(stats[0], sim_label=9, 
        ...                                                 span_map=qblade_nodes_map)
        >>> results = compute_optimal_efficiency_distribution(yaml_path, re_vals, spans)
    """
    df_mean = stats_df.xs('mean', axis=1, level=1)
    
    # Construct row label from simulation index, zero-padded
    row_label = str(sim_label).zfill(2)
    lbl = False
    for elm in df_mean.index:
        if '_' + row_label + '_' in elm:
            lbl = elm
            break
    
    if not lbl:
        raise ValueError(f"Row label {row_label} not found in stats index")
    
    # Try QB format first: B1Re_n*
    channel_prefix = f'B{blade}Re'
    reynolds_cols = [c for c in df_mean.columns if re.match(r'^' + re.escape(channel_prefix) + r'_n\d+', c)]
    
    if reynolds_cols:
        # Extract node numbers and match to span positions
        node_data = []
        for col in reynolds_cols:
            match = re.search(r'_n(\d+)', col)
            if match:
                node_num = int(match.group(1))
                node_data.append((node_num, col))
        
        node_data.sort(key=lambda x: x[0])
        node_nums, sorted_cols = zip(*node_data)
        
        # Map to span positions
        if span_map:
            try:
                span_positions = np.array([span_map[n] for n in node_nums])
            except KeyError:
                # If not all nodes in map, use numeric spacing
                max_node = max(node_nums)
                span_positions = np.array(node_nums) / max_node if max_node > 0 else np.array(node_nums)
        else:
            # Use numeric node number as proxy for span
            max_node = max(node_nums)
            span_positions = np.array(node_nums) / max_node if max_node > 0 else np.array(node_nums)
        
        # Extract values
        reynolds_values = df_mean.loc[lbl, list(sorted_cols)].values
        return span_positions, reynolds_values
    
    # Fallback: FAST mapped format (Reynolds Number BLD_1 PAN_*)
    pattern = f'Reynolds Number BLD_{blade}'
    reynolds_cols = [c for c in df_mean.columns if pattern in c]
    
    if reynolds_cols:
        # Extract PAN numbers and sort
        pan_data = []
        for col in reynolds_cols:
            match = re.search(r'PAN_(\d+)', col)
            if match:
                pan_num = int(match.group(1))
                pan_data.append((pan_num, col))
        
        pan_data.sort(key=lambda x: x[0])
        max_pan = max(p[0] for p in pan_data) if pan_data else 1
        
        pan_nums, sorted_cols = zip(*pan_data)
        span_positions = np.array(pan_nums) / max_pan
        reynolds_values = df_mean.loc[lbl, list(sorted_cols)].values
        return span_positions, reynolds_values
    
    raise ValueError(
        f"No Reynolds Number columns found. Expected 'B{blade}Re_n*' or "
        f"'Reynolds Number BLD_{blade} PAN_*' pattern."
    )


def add_shared_legend(fig, handles, labels, upper_margin = 0.85):
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0.98), ncol=3, fontsize='large')
    fig.tight_layout(rect=[0, 0, 1, upper_margin])

def calcPSD(channel, samplingfreq, nperseg, noverlap):
    f, PSD=signal.welch(channel, samplingfreq, nperseg=nperseg, noverlap=noverlap)
    return f, PSD

def plot_psd(ax, df, channel, fs, style, label, label_map=None):
    
    # compute psd
    signal = df[channel].dropna().values
    freqs, psd = calcPSD(signal, fs, nperseg=int(len(signal)/2), noverlap=0.5)

    ax.plot(freqs, psd, label=label, **style, linewidth=1)
    ax.set_xlim([0.0, 1.0])
    ax.set_ylabel(label_map.get(channel, channel) if label_map else channel)
    ax.tick_params(axis='both', labelsize='large')
    ax.grid(linestyle=':', color='gray')
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.get_major_formatter().set_powerlimits((3, 4))
    

def plot_fft(ax, df, channel, fs, style, label, label_map=None):
    
    # clean signal and remove mean
    signal = df[channel].dropna().values
    signal -= np.mean(signal)
    n = len(signal)

    # compute fft
    freqs = np.fft.rfftfreq(n, d=1/fs)
    fft_vals = np.fft.rfft(signal)
    fft_mag = np.abs(fft_vals)
    
    # alternatively compute PSD as square of fft
    # freqs_fft = np.fft.rfftfreq(n, d=1/fs)
    # fft_values = np.fft.rfft(signal - np.mean(signal))
    # psd = (np.abs(fft_values) ** 2) / (n * fs)

    # plot data
    ax.plot(freqs, fft_mag, label=label, **style, linewidth=1)
    ax.set_xlim([0.0, 0.5])
    ax.set_ylabel(label_map.get(channel, channel) if label_map else channel)
    ax.tick_params(axis='both', labelsize='large')
    ax.grid(linestyle=':', color='gray')
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.get_major_formatter().set_powerlimits((3, 4))
    

def plot_tss(ax, df, channel, style, label, label_map=None):
    
    ax.plot(df['Time'], df[channel], label=label, **style, linewidth=1)
    ax.set_ylabel(label_map.get(channel, channel) if label_map else channel)
    ax.grid(linestyle=':', color='gray')
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.get_major_formatter().set_powerlimits((0, 3))


def export_binned_stats_to_dataframes(binned_stats, labels, export_channels):
    """
    Export binned statistics to a dictionary of DataFrames.
    
    Converts binned statistics from bin_sims_by_mean_wind_speed_pd() into a user-friendly
    dictionary structure where each simulation is mapped to a DataFrame containing all
    requested channels binned by wind speed.
    
    Parameters
    ----------
    binned_stats : dict
        Dictionary of binned DataFrames from bin_sims_by_mean_wind_speed_pd().
        Keys are integer indices (0, 1, 2, ...), values are DataFrames with MultiIndex
        columns (channel_name, stat_type) where stat_type ∈ {'mean', 'min', 'max', 'std'}.
    
    labels : list
        List of simulation labels corresponding to binned_stats keys.
        Must have same length as number of keys in binned_stats.
    
    export_channels : list
        List of channel names to include in export (e.g., ['GenPwr', 'RtAeroTh', 'RootMyc1']).
        If a channel is not found in binned_stats, it is skipped with a warning.
    
    Returns
    -------
    exported_dict : dict
        Dictionary with structure:
        {
            'label_0': DataFrame with columns MultiIndex (channel, stat_type),
            'label_1': DataFrame with columns MultiIndex (channel, stat_type),
            ...
            '_metadata': DataFrame with bin statistics (count, wind_speed_min/max per bin)
        }
        
        Each DataFrame has:
        - Index: wind speed values (bins)
        - MultiIndex columns: (channel, stat_type) where stat_type ∈ {'mean', 'min', 'max', 'std'}
        - Values: corresponding statistics for each channel and bin
    
    Example
    -------
    >>> exported_dict = export_binned_stats_to_dataframes(
    ...     binned_stats, 
    ...     labels=['Design A', 'Design B'], 
    ...     export_channels=['GenPwr', 'RootMyc1']
    ... )
    >>> 
    >>> # Access binned power for first design
    >>> power_data = exported_dict['Design A'][('GenPwr', 'mean')]
    >>> 
    >>> # Access metadata about bins
    >>> metadata = exported_dict['_metadata']
    >>> print(metadata)
    """
    
    exported_dict = {}
    stat_types = ['mean', 'min', 'max', 'std']
    
    # Process each simulation
    for j, binned_df in binned_stats.items():
        if j >= len(labels):
            print(f"Warning: More simulations ({j+1}) than labels ({len(labels)}). Skipping index {j}.")
            continue
        
        label = labels[j]
        
        # Extract wind speed bin centers
        wind_speeds = binned_df['Wind1VelX']['mean'].values
        
        # Build the exported DataFrame
        data_dict = {}
        missing_channels = []
        
        for channel in export_channels:
            # Check if channel exists in binned_df
            channel_cols = [col for col in binned_df.columns if col[0] == channel]
            
            if not channel_cols:
                missing_channels.append(channel)
                continue
            
            # Extract all stat types for this channel
            for stat_type in stat_types:
                try:
                    values = binned_df[channel][stat_type].values
                    data_dict[(channel, stat_type)] = values
                except KeyError:
                    pass
        
        if missing_channels:
            print(f"  Warning: Channels {missing_channels} not found in simulation '{label}'")
        
        # Create DataFrame with MultiIndex columns
        df_export = pd.DataFrame(data_dict, index=wind_speeds)
        df_export.index.name = 'Wind Speed (m/s)'
        
        exported_dict[label] = df_export
    
    # Generate metadata
    metadata = {
        'num_simulations': len(binned_stats),
        'num_bins_per_sim': {},
        'wind_speed_range': {},
        'num_channels_exported': len(export_channels),
        'channels_requested': export_channels,
    }
    
    for j, binned_df in binned_stats.items():
        if j >= len(labels):
            continue
        label = labels[j]
        wind_speeds = binned_df['Wind1VelX']['mean'].values
        metadata['num_bins_per_sim'][label] = len(wind_speeds)
        metadata['wind_speed_range'][label] = (wind_speeds.min(), wind_speeds.max())
    
    # Convert metadata to DataFrame for easier inspection
    metadata_df = pd.DataFrame({
        'key': list(metadata.keys()),
        'value': [str(v) for v in metadata.values()]
    }).set_index('key')
    
    exported_dict['_metadata'] = metadata_df
    
    return exported_dict


def save_binned_stats_export(exported_dict, output_paths):
    """
    Save exported binned statistics to specified file formats.
    
    Supports multiple output formats and can save to multiple files simultaneously.
    Automatically detects format from file extension.
    
    Parameters
    ----------
    exported_dict : dict
        Dictionary returned by export_binned_stats_to_dataframes().
        Structure: {label: DataFrame, ..., '_metadata': metadata_df}
    
    output_paths : str or list
        Path(s) to save files to. Can be:
        - Single string: saves to one file
        - List of strings: saves to multiple files with different formats
        
        Supported formats (auto-detected from extension):
        - .pkl, .pickle : Binary pickle format (preserves MultiIndex)
        - .csv : Comma-separated values (one file per simulation + metadata)
        - .xlsx : Excel workbook (one sheet per simulation + metadata sheet)
        - .h5, .hdf5 : HDF5 hierarchical format (requires tables library)
    
    Returns
    -------
    None
    
    Examples
    --------
    >>> # Save to single pickle file
    >>> save_binned_stats_export(binned_stats_export, 'export.pkl')
    
    >>> # Save to multiple formats
    >>> save_binned_stats_export(binned_stats_export, ['export.pkl', 'export_data.csv'])
    
    >>> # Save to HDF5
    >>> save_binned_stats_export(binned_stats_export, 'export.h5')
    
    >>> # Save to Excel (each simulation as a sheet)
    >>> save_binned_stats_export(binned_stats_export, 'export.xlsx')
    """
    
    # Convert single path to list
    if isinstance(output_paths, str):
        output_paths = [output_paths]
    
    for output_path in output_paths:
        ext = output_path.lower().split('.')[-1]
        
        try:
            if ext in ['pkl', 'pickle']:
                # Save as pickle (preserves MultiIndex columns perfectly)
                import pickle
                with open(output_path, 'wb') as f:
                    pickle.dump(exported_dict, f)
                print(f"✓ Saved to {output_path} (pickle format)")
            
            elif ext == 'csv':
                # Save each DataFrame to CSV (one per simulation + metadata)
                import os
                base_dir = os.path.dirname(output_path) or '.'
                base_name = os.path.splitext(os.path.basename(output_path))[0]
                
                # Save each simulation's data
                for label, df in exported_dict.items():
                    if label != '_metadata':
                        csv_path = os.path.join(base_dir, f"{base_name}_{label}.csv")
                        df.to_csv(csv_path)
                        print(f"✓ Saved to {csv_path}")
                
                # Save metadata
                metadata_path = os.path.join(base_dir, f"{base_name}_metadata.csv")
                exported_dict['_metadata'].to_csv(metadata_path)
                print(f"✓ Saved metadata to {metadata_path}")
            
            elif ext == 'xlsx':
                # Save to Excel with one sheet per simulation + metadata sheet
                with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                    for label, df in exported_dict.items():
                        if label != '_metadata':
                            # Use label as sheet name (max 31 chars for Excel)
                            sheet_name = str(label)[:31]
                            df.to_excel(writer, sheet_name=sheet_name)
                            print(f"✓ Saved '{label}' to sheet in {output_path}")
                        else:
                            # Save metadata in separate sheet
                            exported_dict['_metadata'].to_excel(writer, sheet_name='Metadata')
                            print(f"✓ Saved metadata to 'Metadata' sheet in {output_path}")
                print(f"✓ Successfully created Excel workbook: {output_path}")
            
            elif ext in ['h5', 'hdf5']:
                # Save as HDF5 store
                with pd.HDFStore(output_path, mode='w') as store:
                    for label, df in exported_dict.items():
                        # HDF5 doesn't support MultiIndex columns the same way
                        # Flatten them for storage
                        if label != '_metadata':
                            # Store with flattened column names
                            df_flat = df.copy()
                            df_flat.columns = [f"{col[0]}_{col[1]}" if isinstance(col, tuple) else col 
                                              for col in df_flat.columns]
                            store.put(label.replace(' ', '_'), df_flat, format='table')
                            print(f"✓ Stored '{label}' in {output_path}")
                        else:
                            store.put('_metadata', df, format='table')
                            print(f"✓ Stored metadata in {output_path}")
            
            else:
                print(f"✗ Unsupported file format: .{ext}")
                print(f"  Supported formats: .pkl, .csv, .xlsx, .h5, .hdf5")
        
        except Exception as e:
            print(f"✗ Error saving to {output_path}: {str(e)}")
            import traceback
            traceback.print_exc()
    
