import matplotlib.pyplot as plt
from mappings import qblade_to_openfast_map, qblade_nodes_map
from data_utils import load_and_map_stats, load_DELs
from plotting import plot_stat_vs_wind, add_shared_legend, plot_spanwise_comparison, plot_DEL_vs_wind, plot_spanwise_aero, bin_sims_by_mean_wind_speed_pd
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd


#%% USER INPUTS ------------------------------------------------------------------------

## 22MW DERATED 4 DRIVETRAIN SIZING
#ss_names = [
#    r"C:\Users\FP\Downloads\summary_stats_IEA22MW.p",
#    r"C:\Users\FP\Downloads\summary_stats_IEA22MWD15.p",
#    r"C:\Users\FP\Downloads\summary_stats_IEA22MWD10.p",
#    r"C:\Users\FP\Downloads\summary_stats_IEA22MWD8.p",
#    ]
#
#lables = [
#
#        'IEA22',
#        'IEA22_D15',
#        'IEA22_D10',
#        'IEA22_D8'
#        
#          ]

## 15MW DERATED 4 DRIVETRAIN SIZING
#ss_names = [
#    r"C:\Users\FP\Downloads\summary_stats_IEA15MW.p",
#    r"C:\Users\FP\Downloads\summary_stats_IEA15MWD10.p",
#    r"C:\Users\FP\Downloads\summary_stats_IEA15MWD8.p",
#    ]
#
#lables = [
#
#        'IEA15',
#        'IEA15_D10',
#        'IEA15_D8'
#        
#          ]

## 22MW DERATED LOAD ANALYSIS
ss_names = [
    r"C:\Users\FP\Downloads\Load_analysis_results_22MW\22MW_stiff_stiff\summary_stats.p",
    r"C:\Users\FP\Downloads\Load_analysis_results_22MW\D15\summary_stats.p",
    r"C:\Users\FP\Downloads\Load_analysis_results_22MW\D10\summary_stats.p",
]

lables = [
    'IEA22',
    'IEA22-15',
    'IEA22-10',
]


savewind = False
savespan = False
outn_wnd = r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.6.1_OPT/R2/compare_wind_R1R2.svg'
outn_spn = r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.6.1_OPT/R2/compare_span_R1R2_7ms.svg'

# Plotting: Spanwise comparisons
sim_index_to_plot = 10

title = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']

channels = ['BldPitch1',
            #'RtAeroCp',
            # 'RtAeroCt',
            #'GenPwr', 
            #'GenTq',
            'RotSpeed',
            'RtAeroTh',
            #'TipDxc1',
            #'TipDyc1',
            #'RDzb1_0.950',
            #'PtfmSurge',
            'PtfmPitch',
            #'RootMyc1',
            'TwrBsMyt',
            #'NcIMUTAxn', 
            ]

#channels = [
#
#    'LSShftFxh',
#    'LSShftFys',
#    'LSShftFzs',
#    'LSShftMxs',
#    'LSShftMys',
#    'LSShftMzs',
#
#]

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
    'RDzb1_0.800': 'Tip torsional deflection (°)',
    'RtAeroTh': 'Aerodynamic Thrust (kN)',
    'RootMyc1': 'Blade Root OOP BM (kNm)',
    'TwrBsMyt': 'Tower Base F-A BM (kNm)'
}

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

colors = cmap_custom_green(np.linspace(0, 1, len(ss_names)))
linestyles = ['-.', '--', ':', '-', '-.', '--', ':', '-']

# Load data
stats_raw, stats = load_and_map_stats(ss_names, qblade_to_openfast_map, drop_unmapped=True, verbose=False)
del_paths = [ss_names[i].replace('summary_stats.p', 'DELs.p') for i in range(len(ss_names))]
DELs = load_DELs(del_paths)

# %%---------------------------------------------------------------------------#
# Plotting: mean/min/max as function of wind speed 
fig, axs = plt.subplots(2, 3, figsize=(10, 7))
axs = axs.flatten()

for i, chan in enumerate(channels):
    for j in range(len(stats)):
        plot_stat_vs_wind(
            axs[i],
            stats[j],
            x_col='Wind1VelX',
            y_col=chan,
            style={'color': colors[j], 'linestyle': linestyles[j]},
            label=lables[j]
        )
    axs[i].set_title(title[i], fontsize='large')
    axs[i].set_ylabel(label_map.get(chan, chan))
    axs[i].set_xlabel("Mean Wind Speed (m/s)")

handles, labels = axs[0].get_legend_handles_labels()
add_shared_legend(fig, handles, labels)
plt.show()

if savewind: 
    fig.savefig(outn_wnd, dpi = 300)

# ---------------------------------------------------------------------------#
# Plotting: Binned stats

df_bins = bin_sims_by_mean_wind_speed_pd(
    stats[j],
    wind_speed_channel='Wind1VelX',
    value_channel="GenPwr",
    #bin_width=0.75,
    min_count=1,
    gap_factor=0.1,
    tol = 0.3
)

plt.plot(df_bins['Wind1VelX']['mean'], df_bins["GenPwr"]["mean"], marker='o')
#plt.fill_between(df_bins.ws_center, df_bins.min, df_bins.max, alpha=0.3)

## ---------------------------------------------------------------------------#
## Plotting: DELs as function of wind speed 
#fig, axs = plt.subplots(2, 3, figsize=(10, 7))
#axs = axs.flatten()
#
#for i, chan in enumerate(DELchannels):
#    for j in range(len(stats)):
#        
#        plot_DEL_vs_wind(            
#            axs[i],
#            stats[j], 
#            DELs[j], 
#            x_col='Wind1VelX',
#            y_col=chan,
#            style={'color': colors[j], 'linestyle': '', 'marker': '.'},
#            label=lables[j]
#            )
#        
#    axs[i].set_title(title[i], fontsize='large')
#    axs[i].set_ylabel(label_map.get(chan, chan))
#    axs[i].set_xlabel("Mean Wind Speed (m/s)")
#
#handles, labels = axs[0].get_legend_handles_labels()
#add_shared_legend(fig, handles, labels)
#plt.show()

# ---------------------------------------------------------------------------#
## Plotting: qblade struct spanwise quantities
#
#spanwise_channels = [    
#          'RDzb1',
#          'AeroFyb1',  
#          'AeroFxb1',
#          'B1Alpha',
#          #'B1AxInd',
#          #'TDyb1',
#          #'TDxb1'
#          ]
#
#fig, axs = plt.subplots(1, len(spanwise_channels), figsize=(3.5 * len(spanwise_channels), 4))
#plot_spanwise_comparison(stats, spanwise_channels, lables, colors, linestyles, fig, axs, sim_label=sim_index_to_plot, title_prefix="Spanwise: ", show_extrema=True)
#axs[3].set_ylim(-5,15)
#axs[1].set_ylim(-1250, 250)
#plt.show()
#
#if savespan:
#    fig.savefig(outn_spn, dpi = 300)

# ---------------------------------------------------------------------------#
## Plotting: qblade aero  spanwise quantites such as Cl, Cd, Induction
#
#spanwise_aero_channels = [    
#          'B1AxInd', 
#          #'B1ClCd',
#          'B1Cd',]
#
#
#if 'B1ClCd' in spanwise_aero_channels:
#    for i in range(len(stats)):
#
#        num = stats[i].filter(regex="B1Cl")
#        den = stats[i].filter(regex="B1Cd")
#
#        # Make sure they have the same shape
#        result = pd.DataFrame(
#            np.divide(num.to_numpy(), den.to_numpy()),
#            index=stats[i].index,
#            columns=pd.MultiIndex.from_tuples([
#            (c[0].replace("B1Cl", "B1ClCd"), c[1]) for c in num.columns
#                ])
#            )
#        # Add it back
#        stats[i] = stats[i].join(result)
#
#print('MEAN WIND SPEED: ', stats[0].loc[:,('Wind1VelX', 'mean')].iloc[sim_index_to_plot])
#fig, axs = plt.subplots(1, len(spanwise_aero_channels), figsize=(3.5 * len(spanwise_aero_channels), 4))
#plot_spanwise_aero(stats, spanwise_aero_channels, qblade_nodes_map, labels, colors, linestyles, fig, axs, sim_label=sim_index_to_plot, title_prefix="", show_extrema=True)
#plt.show()
#

# %%
