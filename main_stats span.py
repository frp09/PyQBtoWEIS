import matplotlib.pyplot as plt
from mappings import qblade_to_openfast_map, qblade_nodes_map
from data_utils import load_and_map_stats, load_DELs
from plotting import plot_stat_vs_wind, add_shared_legend, plot_spanwise_comparison, plot_DEL_vs_wind, plot_spanwise_aero, extract_reynolds_distribution
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd
#from plot_max_clcd_distribution import get_interpolated_max_efficiency

#%% USER INPUTS ------------------------------------------------------------------------

# MED CLD1.6 vs DLC1.1 vs IEA 22  DLC 1.6
ss_names = [
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/LATEST_MED_v1/UNIFORM/iteration_0/summary_stats.p', 
]

lables = [
    'IEA 22',
    'DLC THIN DLC 1.6',
    'MED THIN DLC 1.1'
]


# Plotting: Spanwise comparisons
sim_index = [
  [0,4,8, 12,14,],
  [0,4,8, 12,14,],
 # [0,4,8, 12,14,],
]

savewind = False
savespan = False
savedel = False
outn_wnd = r'/home/papi/FLOATFARM/REPORTS/compareSpar_wind_R1R2.svg'
outn_spn = r'/home/papi/FLOATFARM/REPORTS/compareSpar_span_R1R2_9ms.svg'
outn_del = r'/home/papi/FLOATFARM/REPORTS/compareSpar_del_R1R2.svg'

title = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']
title = ['3 m/s', '5 m/s', '7 m/s', '9 m/s', '10 m/s']

label_map = {
    'BldPitch1': 'Blade pitch (°)',
    'RtAeroCp': 'Aero Cp (-)',
    'RtAeroCt': 'Aero Ct (-)',
    'RotSpeed': 'Rotor speed (rpm)',
    'TipDxc1': 'Tip deflection (OOP)',
    'TipDyc1': 'Tip deflection (IP)',
    'RDzb1_0.800': 'Tip torsional deflection (°)',
    'RtAeroTh': 'Aerodynamic Thrust (kN)',
    'RootMyc1': 'Blade Root OOP BM (kNm)', 
    'GenPwr': 'Generator Power (kW)',
    'RootMc1': 'Blade Root BM (kNm)', 
    'LSShftAxMyza': 'Low Speed shaft torque (kNm)',
    'TwrBsAxMomXYt': 'Tower Base BM (kNm)',
    'RDzb1': 'Torsional deformation (°)',
    'TDxb1': 'OOP deformation (m)', 
    'TDyb1': 'IP deformation (m)',
    'AeroFyb1': 'Tangential force (kN)',
    'AeroFxb1': 'OOP force (kN)', 
    'B1Alpha': 'Angle of Attack Blade 1 (°)'

}

cmap_custom_green = LinearSegmentedColormap.from_list(
    "gray_to_teal", 
    [ #"#A9A9A9",
       "royalblue",  
     '#e05252', 
     '#4ca64c'
     ]
)

colors = cmap_custom_green(np.linspace(0, 1, len(ss_names)))
linestyles = ['-.', '--', ':', '-', '-.', '--', ':', '-']

# Load data
stats_raw, stats = load_and_map_stats(ss_names, qblade_to_openfast_map, drop_unmapped=True, verbose=False)
del_paths = [ss_names[i].replace('summary_stats.p', 'DELs.p') for i in range(len(ss_names))]
DELs = load_DELs(del_paths)

model_keys = list(stats.keys())
active_sim_index = sim_index[:len(model_keys)]

if len(active_sim_index) != len(model_keys):
    print(f"warning: sim_index defines {len(sim_index)} model rows, but loaded {len(model_keys)} datasets; trimming to loaded datasets")


# ---------------------------------------------------------------------------#
# Plotting: qblade struct spanwise quantities

spanwise_channels = [    
          'RDzb1',
        #   'TDxb1',
        #   'TDyb1',
          'AeroFyb1',  
          'AeroFxb1',
          'B1Alpha',
          #'B1AxInd',
          #'TDyb1',
          #'TDxb1'
          ]

n_models  = len(model_keys)
n_runs    = len(active_sim_index[0])
wsds = pd.DataFrame(index=range(n_models),
                    columns=range(n_runs),
                    dtype=float)      # or fill later

for i in model_keys:
    for j, idj in enumerate(active_sim_index[i]):
        # locate the row label corresponding to the selected wind speed
        speed = active_sim_index[i][j]
        token1 = f'_{speed}_'
        token2 = f'_{speed:02}_' if 0 <= speed < 10 else None
        token3 = f'_{speed:03}_' if 0 <= speed < 10 else (f'_{speed:03}_' if speed < 100 else None)
        lbl = None
        for elm in stats[i].index:
            if token1 in elm or (token2 and token2 in elm) or (token3 and token3 in elm):

                lbl = elm
                break
        if lbl is None:
            # nothing matched; warn and skip this entry
            print(f"warning: no stats row found for speed {speed} (i={i}, j={j})")
            continue

        # grab the mean wind speed value now that lbl is valid
        val = stats[i].loc[lbl, ('Wind1VelX', 'mean')]
        if isinstance(val, pd.Series):       # guard against a 1‑elem
            val = val.iloc[0]
        wsds.at[i, j] = val

print("mean wind speeds matrix (models x runs):")
print(wsds)

for channel in spanwise_channels:

    figs, axss = plt.subplots(1, n_runs, figsize=(3.5 * n_runs, 5))

    if n_runs == 1:
        axss = np.array([axss])
    else:
        axss = np.array(axss)

    for j, wind_speed_idx in enumerate(active_sim_index[0]):
        plot_spanwise_comparison(
            stats,
            [channel],
            lables[:len(model_keys)],
            colors[:len(model_keys)],
            linestyles[:len(model_keys)],
            figs,
            axss[j],
            sim_label=wind_speed_idx,
            title_prefix="Spanwise: ",
            show_extrema=True,
        )

        axss[j].set_ylabel(label_map.get(channel, channel))
        axss[j].set_title(title[j])

        if 'B1Alpha' in channel:

            axss[j].set_ylim(0,25)
    
if savespan:
    figs.savefig(outn_spn, dpi = 300)


# ============== AERODYNAMIC SPANWISE PLOTTING ==============
# Plot aero quantities (Cl, Cd, Induction) across wind speeds
# One figure per quantity, with subplots for each wind speed, showing all models

aero_channels = ['B1Cl', 'B1ClCd', 'B1AxInd', 'B1Re']

if 'B1ClCd' in aero_channels:
    for i in range(len(stats)):

        # Use negative lookahead to match B1Cl but not B1ClCd
        num = stats[i].filter(regex=r"B1Cl(?!Cd)")
        den = stats[i].filter(regex="B1Cd")

        # Make sure they have the same shape
        if len(num.columns) > 0 and len(den.columns) > 0:
            result = pd.DataFrame(
                np.divide(num.to_numpy(), den.to_numpy()),
                index=stats[i].index,
                columns=pd.MultiIndex.from_tuples([
                (c[0].replace("B1Cl", "B1ClCd"), c[1]) for c in num.columns
                    ])
                )
            # Directly assign instead of join to avoid column name conflicts
            for col in result.columns:
                stats[i][col] = result[col]

# GET MAXIMUM EFFICIENCY FOR A CERTAIN ROTOR DESIGN
#Example: Extract Reynolds distribution and compute optimal efficiency for a specific wind speed

from aero_efficiency import compute_optimal_efficiency_distribution

yaml_path = r"/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.3.2_BOPTNSS/MED15-308_v30.3.2.yaml"
sim_label = 12       # Wind speed index (row label) to analyze
model_idx = 1        # Which model from ss_names

# Method 1: Extract Reynolds from QB format columns (recommended)
spans, re_vals = extract_reynolds_distribution(
    stats_raw[model_idx],           # Use raw stats (has B1Re_n* columns)
    sim_label=sim_label,
    span_map=qblade_nodes_map,      # For accurate span positions
    blade=1
)

# Compute optimal efficiency at each span
eff_results = compute_optimal_efficiency_distribution(
    yaml_path,
    reynolds_numbers=re_vals,
    span_positions=spans,
    aoa_range=(-5, 25)
)

# eff_results DataFrame has columns:
# ['span', 'reynolds', 'optimal_aoa', 'max_efficiency', 'cl_opt', 'cd_opt']

## Overlay optimal AoA on your existing B1Al pha plots:
#axss[j].plot(eff_results['span'], eff_results['optimal_aoa'], 
#             label='Optimal AoA', linewidth=2, color='red', marker='o')

for aero_channel in aero_channels:
    print(f"\nPlotting {aero_channel} across wind speeds...")
    # One figure per aero quantity with subplots for each wind speed
    fig, axss = plt.subplots(1, len(sim_index[0]), figsize=(3.5 * len(sim_index[0]), 5))
    
    # Ensure axss is always iterable
    if len(sim_index[0]) == 1:
        axss = np.array([axss])
    else:
        axss = np.array(axss)
    
    # For each wind speed
    for j, wind_speed_idx in enumerate(sim_index[0]):
        # Use plot_spanwise_aero to plot this aero quantity at this wind speed for all models
        # Pass the single axis directly (not wrapped in array)
        plot_spanwise_aero(stats, [aero_channel], qblade_nodes_map, lables, colors, linestyles,
                          fig, axss[j], sim_label=wind_speed_idx, title_prefix="", show_extrema=False)
        
        if aero_channel == 'B1ClCd':
            axss[j].plot(eff_results['span'], eff_results['max_efficiency'], linestyle = ':', color = 'black')
        # Set wind speed as subplot title
        #if j < wsds.shape[1]:
        #    wind_speed = wsds.iloc[0, j]
        #    axss[j].set_title(f'{wind_speed:.1f} m/s', fontsize=10)
        #else:
        #    axss[j].set_title(f'Run {j}', fontsize=10)

        axss[j].set_title(title[j])
    

plt.show()
