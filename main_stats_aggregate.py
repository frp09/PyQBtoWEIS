import matplotlib.pyplot as plt
from mappings import qblade_to_openfast_map, qblade_nodes_map
from data_utils import load_and_map_stats, load_DELs
from plotting import plot_stat_vs_wind, add_shared_legend, plot_spanwise_comparison, plot_DEL_vs_wind, plot_spanwise_aero, bin_sims_by_mean_wind_speed_pd, export_binned_stats_to_dataframes, save_binned_stats_export
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd
import scipy as sc


'''
PLOT BINNED-AVERAGES AND STATISTICS OF DATA
F.Papi - 2026
Univerità degli Studi di Firenze 

This script loads summary statistics from multiple simulations, bins them by mean wind speed, 
and plots the mean, min, max, and std of selected channels vs wind speed. It also supports 
exporting the binned statistics to Excel or other formats. It is designed to use QBtoWEIS 
outputs but can be adapted to other data sources with similar structure.

'''
#%% USER INPUTS ------------------------------------------------------------------------

ss_names = [
r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/IEA15_RWT/mout_DLC_AEP/iteration_0/summary_stats.p',
r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/IEA22_RWT/mout_DLC_AEP/iteration_0/summary_stats.p',
r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/LATEST_MED/DLC_AEP_MED15-308_v30.2.25/iteration_0/summary_stats.p',
]  

lables = [
'IEA-15',
'IEA-22',
'MED-15'
]

cmap_custom_green = LinearSegmentedColormap.from_list(
    "gray_to_teal", 
     [
    "#1F77B4",  # blue
    "#2CA02C",  # green
    "#D62728",
    #"#BCBD22",  # olive / yellow-green
     ]
)

savewind = False
savespan = False
outn_wnd = r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/LATEST_MED_v1/UNIFORM/MED-15-300-RWT_v1.0.0/R2/compare_wind.svg'
outn_spn = r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/LATEST_MED_v1/UNIFORM/MED-15-300-RWT_v1.0.0/R2/compare_span_7ms.svg'

# Export binned statistics
export_binned = True # Set to True to export binned stats as dictionary of DataFrames
# export_channels = ['GenPwr', 'RtAeroTh', 'RDzb1_0.950', 'RootMyc1', 'TwrBsMyt']  # Channels to export
export_channels = ['GenPwr', 'RtAeroTh', 'RtAeroCp', 'RtAeroCt', 'TwrBsMyt']  # Channels to export
export_channels = [
    r'AeroFxb1_0.000',
    r'AeroFyb1_0.000',
    r'Fzb1_0.000',
    r'AeroFxb1_0.100',
    r'AeroFyb1_0.100',
    r'Fzb1_0.100',
    r'AeroFxb1_0.200',
    r'AeroFyb1_0.200',
    r'Fzb1_0.200',
    r'AeroFxb1_0.300',
    r'AeroFyb1_0.300',
    r'Fzb1_0.300',
    r'AeroFxb1_0.400',
    r'AeroFyb1_0.400',
    r'Fzb1_0.400',
    r'AeroFxb1_0.500',
    r'AeroFyb1_0.500',
    r'Fzb1_0.500',
    r'AeroFxb1_0.600',
    r'AeroFyb1_0.600',
    r'Fzb1_0.600',
    r'AeroFxb1_0.700',
    r'AeroFyb1_0.700',
    r'Fzb1_0.700',
    r'AeroFxb1_0.800',
    r'AeroFyb1_0.800',
    r'Fzb1_0.800',
    r'AeroFxb1_0.900',
    r'AeroFyb1_0.900',
    r'Fzb1_0.900',
    r'AeroFxb1_1.000',
    r'AeroFyb1_1.000',
    r'Fzb1_1.000',
    r'TDxb1_0.000',
    r'TDyb1_0.000',
    r'TDzb1_0.000',
    r'RDxb1_0.000',
    r'RDyb1_0.000',
    r'RDzb1_0.000',
    r'TDxb1_0.100',
    r'TDyb1_0.100',
    r'TDzb1_0.100',
    r'RDxb1_0.100',
    r'RDyb1_0.100',
    r'RDzb1_0.100',
    r'TDxb1_0.200',
    r'TDyb1_0.200',
    r'TDzb1_0.200',
    r'RDxb1_0.200',
    r'RDyb1_0.200',
    r'RDzb1_0.200',
    r'TDxb1_0.300',
    r'TDyb1_0.300',
    r'TDzb1_0.300',
    r'RDxb1_0.300',
    r'RDyb1_0.300',
    r'RDzb1_0.300',
    r'TDxb1_0.400',
    r'TDyb1_0.400',
    r'TDzb1_0.400',
    r'RDxb1_0.400',
    r'RDyb1_0.400',
    r'RDzb1_0.400',
    r'TDxb1_0.500',
    r'TDyb1_0.500',
    r'TDzb1_0.500',
    r'RDxb1_0.500',
    r'RDyb1_0.500',
    r'RDzb1_0.500',
    r'TDxb1_0.600',
    r'TDyb1_0.600',
    r'TDzb1_0.600',
    r'RDxb1_0.600',
    r'RDyb1_0.600',
    r'RDzb1_0.600',
    r'TDxb1_0.700',
    r'TDyb1_0.700',
    r'TDzb1_0.700',
    r'RDxb1_0.700',
    r'RDyb1_0.700',
    r'RDzb1_0.700',
    r'TDxb1_0.800',
    r'TDyb1_0.800',
    r'TDzb1_0.800',
    r'RDxb1_0.800',
    r'RDyb1_0.800',
    r'RDzb1_0.800',
    r'TDxb1_0.900',
    r'TDyb1_0.900',
    r'TDzb1_0.900',
    r'RDxb1_0.900',
    r'RDyb1_0.900',
    r'RDzb1_0.900',
    r'TDxb1_1.000',
    r'TDyb1_1.000',
    r'TDzb1_1.000',
    r'RDxb1_1.000',
    r'RDyb1_1.000',
    r'TipRzb1',
]
export_output_paths = None  # Set to a list of file paths to save exports (e.g., ['export.xlsx', 'export.pkl'])
                             # Supports: .xlsx (Excel - one sheet per simulation), .pkl (pickle), .csv (CSV), .h5/.hdf5 (HDF5)
                             # Sheet names in Excel match the labels list
                             # If None, exported dict stays in memory only as binned_stats_export
# export_output_paths = [r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/LATEST_MED/AEPCompare.xlsx']
export_output_paths = [r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/LATEST_MED_v1/UNIFORM/loads_out.xlsx']

# Plotting: Spanwise comparisons
sim_index_to_plot = 10

title = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)', '(g)', '(h)', '(i)', '(l)', '(m)', '(n)']

channels = [
    r'TDxb1_0.000',
    r'TDyb1_0.000',
    r'TDzb1_0.000',
    r'RDxb1_0.000',
    r'RDyb1_0.000',
    r'RDzb1_0.000',
            ]

channels = [
    'GenPwr', 'RotSpeed', 'RtAeroTh', 'TwrBsMyt', 'NcIMUTAxn', 'PtfmPitch', #'RtAeroCp', 'RtAeroCt', 
]

DELchannels = [
    'X_b RootBend. Mom. BLD_1',
    'Y_b RootBend. Mom. BLD_2',
    'Z_b RootBend. Mom. BLD_3',
    #'TwrBsMyt',
    'RootMc1', 
    'RootMc2', 
    'RootMc3',
]

label_map = {
    'BldPitch1': 'Blade pitch (°)',
    'RtAeroCp': 'Aero Cp (-)',
    'RtAeroCt': 'Aero Ct (-)',
    'RotSpeed': 'Rotor speed (rpm)',
    'TipDxc1': 'Tip deflection (OOP)',
    'TipRzb1': 'Tip torsional deflection (°)',
    'RtAeroTh': 'Aerodynamic Thrust (kN)',
    'RootMyc1': 'Blade Root OOP BM (kNm)',
    'TwrBsMyt': 'Tower Base F-A BM (kNm)',
    'PtfmPitch': 'Platform Pitch (°)', 
    'GenPwr': 'Generated Power (kW)',
    'NcIMUTAxn': 'Nacelle F-A acceleration ($m/s^2$)'
}

colors = cmap_custom_green(np.linspace(0, 1, len(ss_names)))
linestyles = ['-', '--', '-.', '-', '-.', '--', ':', '-']

# Load data
stats_raw, stats = load_and_map_stats(ss_names, qblade_to_openfast_map, drop_unmapped=True, verbose=False)
del_paths = [ss_names[i].replace('summary_stats.p', 'DELs.p') for i in range(len(ss_names))]
DELs = load_DELs(del_paths)

# ---------------------------------------------------------------------------#
# Plotting: Binned stats
binned_stats = {}
for j in range(len(stats)):
    binned_stats[j] = bin_sims_by_mean_wind_speed_pd(
        stats[j],
        wind_speed_channel='Wind1VelX',
        value_channel="GenPwr",
        #bin_width=0.75,
        min_count=1,
        gap_factor=0.45,
        tol = 0.35
    )

# Export binned statistics if requested
if export_binned:
    print(f"\nExporting binned statistics for {len(export_channels)} channels...")
    binned_stats_export = export_binned_stats_to_dataframes(
        binned_stats, 
        labels=lables, 
        export_channels=export_channels
    )
    print(f"✓ Exported binned stats for {len(binned_stats_export) - 1} simulations")
    print(f"  Metadata available in binned_stats_export['_metadata']")
    print("\nAccess exported data via:")
    print("  binned_stats_export[simulation_label][(channel_name, stat_type)]")
    print("  where stat_type ∈ {'mean', 'min', 'max', 'std'}")
    
    # Save to files if paths specified
    if export_output_paths is not None:
        save_binned_stats_export(binned_stats_export, export_output_paths)
else:
    print("Binned statistics export is disabled (set export_binned=True to enable)")

fig, axs = plt.subplots(2, 6, figsize=(16, 6))#, sharex=True)
axs = axs.flatten()

for i, chan in enumerate(channels):
    for j in range(len(binned_stats)):
        
        axs[i].fill_between(binned_stats[j]['Wind1VelX']['mean'], binned_stats[j][chan]["min"], binned_stats[j][chan]["max"], color = colors[j], alpha = 0.15)
        axs[i].plot(binned_stats[j]['Wind1VelX']['mean'], binned_stats[j][chan]["mean"], marker='.', linestyle = linestyles[j], color = colors[j], label = lables[j])
        #axs[i].scatter(binned_stats[j]['Wind1VelX']['mean'], binned_stats[j][chan]["max"], marker='^', edgecolors = colors[j], facecolor = "None", sizes = [10])
        #axs[i].scatter(binned_stats[j]['Wind1VelX']['mean'], binned_stats[j][chan]["min"], marker='v', edgecolors = colors[j], facecolor = "None", sizes = [10])

        axs[i].plot(binned_stats[j]['Wind1VelX']['mean'], binned_stats[j][chan]["max"], linestyle = ':', lw = 0.75,  color = colors[j])
        axs[i].plot(binned_stats[j]['Wind1VelX']['mean'], binned_stats[j][chan]["min"], linestyle = ':', lw = 0.75, color = colors[j])

        axs[i+6].plot(binned_stats[j]['Wind1VelX']['mean'], binned_stats[j][chan]["std"], marker='.', linestyle = '', color = colors[j])
    
    axs[i].set_title(title[i], fontsize='large')
    axs[i+6].set_title(title[i+6], fontsize='large')
    axs[i].set_ylabel(label_map.get(chan, chan))
    axs[i+6].set_xlabel("Mean Wind Speed (m/s)")
    axs[i].grid(linestyle=':')
    axs[i+6].grid(linestyle=':')

    axs[i+6].set_ylabel(label_map.get(chan, chan). replace('(', 'STD ('))
    axs[i].ticklabel_format(axis='y', style='sci', scilimits=(-3, 3))
    axs[i+6].ticklabel_format(axis='y', style='sci', scilimits=(-3, 3))
    axs[i+6].set_xticks([2, 6, 10, 14, 18, 22, 26])

# axs[0].set_ylim([0.4, 0.6])
# axs[0].set_xlim([3, 10])
# axs[1].set_ylim([2000, 2600])
# axs[1].set_xlim([3, 10])
# axs[2].set_xlim([3, 10])
# axs[2].set_ylim([-5, 5])

shape = 2
mean = 7.5
mean1 = 10

scale = mean/sc.special.gamma(1+1/shape)
scale1 = mean1/sc.special.gamma(1+1/shape)

def weib_pdf(x,scale,shape):

    w = (shape/scale)*((x/scale)**(shape-1))*np.exp(-(x/scale)**shape)

    return w

x = np.linspace(3,25,23)
w = weib_pdf(x,scale,shape)
w1 = weib_pdf(x,scale1,shape)

#axt = axs[0].twinx()
#axt.plot(x,w,color = 'black', linestyle ='--')
#axt.plot(x,w1,color = 'black', linestyle =':')
#axt.ticklabel_format(axis='y', style='sci', scilimits=(-1, 3))
#
#axt.set_ylabel('Wind speed probability (-)')

fig.tight_layout()

handles, labels = axs[0].get_legend_handles_labels()
add_shared_legend(fig, handles, labels, upper_margin = 0.925)


plt.show()