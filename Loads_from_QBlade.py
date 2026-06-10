import sys
sys.path.append(r"D:\Giuliani\Projects\PyQBtoWEIS-main_FP")
import matplotlib.pyplot as plt
from mappings import qblade_to_openfast_map, qblade_nodes_map
from data_utils import load_and_map_stats, load_DELs
from plotting import plot_stat_vs_wind, add_shared_legend, plot_spanwise_comparison, plot_DEL_vs_wind, plot_spanwise_aero, bin_sims_by_mean_wind_speed_pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import ScalarFormatter
import numpy as np
import pandas as pd

#%% USER INPUTS ------------------------------------------------------------------------

ss_names = [ #derating
    
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.24_RUN/DLC16_MED15-308_v30.2.24/iteration_0/summary_stats.p',
    

    ]

lables = [
    '240-D8',

    ]


# Plotting: Spanwise comparisons
sim_index_to_plot = 10

title = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)', '(g)', '(h)', '(i)', '(l)', '(m)', '(n)', '(o)', '(p)', '(q)', '(r)']
# title = ['(f)', '(g)', '(h)', '(i)', '(j)']



channels = ['BldPitch1',
            #'RtAeroCp',
            # 'RtAeroCt',
            'GenPwr',
            #'RtAeroPwr', 
            #'GenTq',
            'RotSpeed',
            'RtAeroTh',
            'TipDxc1',
            'LSShftMxs',
            #'TipDyc1',
            # 'RDzb1_0.950',
            #'PtfmSurge',
            #'PtfmPitch',
            #'RootMyc1',
            #'TwrBsMyt',
            #'NcIMUTAxn', 
            ]

label_map = {   #TOWER
'TwrBsMyt': 'TwrBsMyt',
'TwrTop X Def.': 'TwrTop X Def.',
'TwrTop Y Def.': 'TwrTop Y Def.',
'TwrTop. Rot. Z Def.': 'TwrTop. Rot. Z Def.', 
"Wave1Elev": "Wave1Elev",
'Wind1VelX': 'Wind1VelX'}



# DELchannels = [ #BLADE
#     'X_b RootBend. Mom. BLD_1',
#     'Y_b RootBend. Mom. BLD_2',
#     'Z_b RootBend. Mom. BLD_3',
#     'RootMc1', 
#     'RootMc2', 
#     'RootMc3',
# ]

DELchannels = [ #TOWER
    'TwrBsShForZt',
    # 'X_tb Mom. TWR Bot. Constr.',
    # 'YtbMom',
    'TwrBsM',
    'TwrBsShMomXYt',
    'TwrBsAxForXYt']

cmap_custom_green = LinearSegmentedColormap.from_list(
    "gray_to_teal", 
    #["#FAAA0A", "#006BA6"]  # Warm gray to teal
    [ #"#A9A9A9", 
     '#e05252', 
     "royalblue", 
     #'#4ca64c'
     ]

   # [ #"#A9A9A9", 
   #  '#e05252', 
   #  "royalblue", 
   # # '#4ca64c'
   #  ]
)



colors = [

    '#266433', #'#026452', #'#ECEF0C',
    '#82C10A',
    # 'blue',
    '#B81BC9',
    '#FF8C25',
    # 'red',
    '#2F52E0',
    '#B81BC9',
    '#FF8C25',
    '#DA3833',
    ]




linestyles = [':',  '-.',  '-', '-', '-', '-.', '--', ':', '-']

# Load data
stats_raw, stats = load_and_map_stats(ss_names, qblade_to_openfast_map, drop_unmapped=True, verbose=False)
del_paths = [ss_names[i].replace('summary_stats', 'DELs') for i in range(len(ss_names))]
DELs = load_DELs(del_paths)

n_plots = len(channels)
n_cols = 5  # Fixed number of columns
n_rows = (n_plots + n_cols - 1) // n_cols  # Calculate rows needed

#%%
import numpy as np
import pandas as pd


def _get_stat_series_1d(df, channel, stat):
    """
    Estrae una singola Series 1D da un DataFrame con colonne MultiIndex.
    Solleva errore se la selezione restituisce zero o più di una colonna.
    """
    col = (channel, stat)

    if col not in df.columns:
        raise KeyError(f"Colonna {col} non trovata")

    # selezione robusta
    out = df.loc[:, col]

    # Se per qualche motivo torna un DataFrame, verificare che abbia una sola colonna
    if isinstance(out, pd.DataFrame):
        if out.shape[1] != 1:
            raise ValueError(
                f"La selezione della colonna {col} non è univoca: "
                f"restituite {out.shape[1]} colonne"
            )
        out = out.iloc[:, 0]

    return out


def _build_ws_cluster_labels(
    ws,
    gap_factor=4.0,
    tol=0.1,
):
    """
    Costruisce gli indici di cluster a partire da una Series 1D di wind speed.
    Usa la stessa logica di gap detection del tuo binning adattivo.
    """
    if ws.empty:
        raise ValueError("No valid simulations found")

    ws_values = ws.to_numpy(dtype=float)

    order = np.argsort(ws_values)
    ws_sorted = ws_values[order]

    gaps = np.diff(ws_sorted)
    gaps_m = gaps[gaps > tol]

    if len(gaps_m) == 0:
        median_gap = np.nan
    else:
        median_gap = np.median(gaps_m)

    # Caso degenere: un solo cluster
    if (not np.isfinite(median_gap)) or (median_gap == 0):
        return np.zeros(len(ws_values), dtype=int)

    split_idx = np.where(gaps > gap_factor * median_gap)[0]

    cluster_labels_sorted = np.zeros(len(ws_sorted), dtype=int)
    cluster_id = 0
    start = 0

    for idx in split_idx:
        end = idx + 1
        cluster_labels_sorted[start:end] = cluster_id
        cluster_id += 1
        start = end

    cluster_labels_sorted[start:] = cluster_id

    cluster_labels = np.empty_like(cluster_labels_sorted)
    cluster_labels[order] = cluster_labels_sorted

    return cluster_labels


def get_binned_max_over_seeds_by_wind(
    stats,
    lables,
    key,
    wind_speed_channel='Wind1VelX',
    wind_stat='mean',
    value_stat='max',
    min_count=1,
    gap_factor=4.0,
    tol=0.1,
    return_counts=False,
):
    """
    Per ogni label:
    - clusterizza le simulazioni sulla base della wind speed mean
    - in ciascun cluster prende il massimo della key con statistica value_stat

    Output:
    {
        '240-D8': {
            'wind_speeds': np.array([...]),
            'values': np.array([...]),
            'counts': np.array([...])   # solo se return_counts=True
        },
        ...
    }
    """
    out = {}

    for i, label in enumerate(lables):
        df = stats[i]

        # **ordinare le colonne riduce i PerformanceWarning**
        if isinstance(df.columns, pd.MultiIndex) and not df.columns.is_monotonic_increasing:
            df = df.sort_index(axis=1)

        ws = _get_stat_series_1d(df, wind_speed_channel, wind_stat)
        val = _get_stat_series_1d(df, key, value_stat)

        cluster_labels = _build_ws_cluster_labels(
            ws,
            gap_factor=gap_factor,
            tol=tol,
        )

        tmp = pd.DataFrame({
            'wind': ws.to_numpy(dtype=float),
            'value': val.to_numpy(dtype=float),
            'ws_cluster': cluster_labels.astype(int),
        })

        tmp = tmp.dropna(subset=['wind', 'value'])

        if tmp.empty:
            entry = {
                'wind_speeds': np.array([], dtype=float),
                'values': np.array([], dtype=float),
            }
            if return_counts:
                entry['counts'] = np.array([], dtype=int)
            out[label] = entry
            continue

        grouped = (
            tmp.groupby('ws_cluster', observed=True)
               .agg(
                   wind_speed=('wind', 'mean'),
                   value_max=('value', value_stat),
                   count=('value', 'size'),
               )
               .reset_index(drop=True)
               .sort_values('wind_speed')
        )

        grouped = grouped[grouped['count'] >= min_count]

        entry = {
            'wind_speeds': grouped['wind_speed'].to_numpy(dtype=float),
            'values': grouped['value_max'].to_numpy(dtype=float),
        }

        if return_counts:
            entry['counts'] = grouped['count'].to_numpy(dtype=int)

        out[label] = entry

    return out

max_thrust_binned = get_binned_max_over_seeds_by_wind(
    stats=stats,
    lables=lables,
    key='RtAeroTh',
    wind_speed_channel='YawBrFxh',
    wind_stat='mean',
    value_stat='max',
    min_count=1,
    gap_factor=0.4,
    tol = 0.35,
    return_counts=True,
)

fig, axs = plt.subplots()
plt.plot(max_thrust_binned['240-D8']['wind_speeds'], max_thrust_binned['240-D8']['values'], marker='o', linestyle='-')
plt.show()