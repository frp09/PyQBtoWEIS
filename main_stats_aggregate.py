import matplotlib.pyplot as plt
from mappings import qblade_to_openfast_map, qblade_nodes_map
from data_utils import load_and_map_stats, load_DELs
from plotting import plot_stat_vs_wind, add_shared_legend, plot_spanwise_comparison, plot_DEL_vs_wind, plot_spanwise_aero, bin_sims_by_mean_wind_speed_pd
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd
import scipy as sc


#%% USER INPUTS ------------------------------------------------------------------------

## MED STEADY vs DLC1.1
ss_names = [
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.8_BOPTNSS/iteration_0/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.17/iteration_0/summary_stats.p',
]

lables = [
    'DLC 1.1',
    'STEADY',
]

## MED CLD1.6 vs DLC1.1 vs IEA 22  DLC 1.6
ss_names = [
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/IEA22_RWT/mout_DLC_1.6/iteration_0/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.3.0_BOPTSTR/mout_MED15-308_v30.3.1/iteration_0/summary_stats.p', 
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.3.2_BOPTNSS/mout_MED15-308_v30.3.4/iteration_0/summary_stats.p',
]

lables = [
    'IEA 22',
    'DLC THIN DLC 1.6',
    'MED THIN DLC 1.1'
]

### MED STEADY vs DLC1.1
#ss_names = [
#    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.8_BOPTNSS/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.17/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.16/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.16/iteration_272/summary_stats.p',
#]
#
#lables = [
#    'STEADY THICK START',
#    'STEADY THIN START',
#    'STEADY THIN END',
#]

cmap_custom_green = LinearSegmentedColormap.from_list(
    "gray_to_teal", 
    #["#FAAA0A", "#006BA6"]  # Warm gray to teal
    #[ #"#A9A9A9", 
    # '#4682b4', 
    # "#003f5c", 
    # '#78c2ad'
    # ]
     [
    #"#0072B2",  # Strong blue
    #"#009E73",  # Bluish green
    ##"#56B4E9",  # Light sky blue
    #"#17BECF",  # cyan

    "#1F77B4",  # blue
    "#2CA02C",  # green
    "#D62728",
    #"#BCBD22",  # olive / yellow-green

     ]
)

#cmap_custom_green = LinearSegmentedColormap.from_list(
#    "gray_to_teal", 
#    [  
#    # '#e97451', 
#    # "#CC79A7",
#    # "#8a4b7d", 
#    # '#800020',
#    "#D62728",  # red
#    "#FF7F0E",  # orange
#    "#9467BD",  # purple
#     ]
#)

savewind = False
savespan = False
outn_wnd = r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.6.1_OPT/R2/compare_wind_R1R2.svg'
outn_spn = r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.6.1_OPT/R2/compare_span_R1R2_7ms.svg'

# Plotting: Spanwise comparisons
sim_index_to_plot = 10

title = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)', '(g)', '(h)', '(i)', '(l)']

channels = [#'BldPitch1',
            #'RtAeroCp',
            # 'RtAeroCt',
            'GenPwr', 
            #'GenTq',
            #'RotSpeed',
            'RtAeroTh',
            #'TipDxc1',
            #'TipDyc1',
            'RDzb1_0.950',
            'PtfmSurge',
            'PtfmPitch',
            #'RootMyc1',
            #'TwrBsMyt',
            #'NcIMUTAxn', 
            ]

#channels = [
#            'RtAeroCp',
#            # 'RtAeroCt',
#            #'GenPwr', 
#            #'GenTq',
#            #'RotSpeed',
#            'RtAeroTh',
#            'BldPitch1',
#            'TipDxc1',
#            #'TipDyc1',
#            'RDzb1_0.950',
#            #'PtfmSurge',
#            #'PtfmPitch',
#            #'RootMyc1',
#            #'TwrBsMyt',
#            #'NcIMUTAxn', 
#            ]

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
        gap_factor=0.8,
        tol = 0.3
    )

fig, axs = plt.subplots(2, 5, figsize=(14, 6))#, sharex=True)
axs = axs.flatten()

for i, chan in enumerate(channels):
    for j in range(len(binned_stats)):
        
        axs[i].fill_between(binned_stats[j]['Wind1VelX']['mean'], binned_stats[j][chan]["min"], binned_stats[j][chan]["max"], color = colors[j], alpha = 0.15)
        axs[i].plot(binned_stats[j]['Wind1VelX']['mean'], binned_stats[j][chan]["mean"], marker='.', linestyle = linestyles[j], color = colors[j], label = lables[j])
        #axs[i].scatter(binned_stats[j]['Wind1VelX']['mean'], binned_stats[j][chan]["max"], marker='^', edgecolors = colors[j], facecolor = "None", sizes = [10])
        #axs[i].scatter(binned_stats[j]['Wind1VelX']['mean'], binned_stats[j][chan]["min"], marker='v', edgecolors = colors[j], facecolor = "None", sizes = [10])

        axs[i].plot(binned_stats[j]['Wind1VelX']['mean'], binned_stats[j][chan]["max"], linestyle = ':', lw = 0.75,  color = colors[j])
        axs[i].plot(binned_stats[j]['Wind1VelX']['mean'], binned_stats[j][chan]["min"], linestyle = ':', lw = 0.75, color = colors[j])

        axs[i+5].plot(binned_stats[j]['Wind1VelX']['mean'], binned_stats[j][chan]["std"], marker='.', linestyle = '', color = colors[j])
    
    axs[i].set_title(title[i], fontsize='large')
    axs[i+5].set_title(title[i+5], fontsize='large')
    axs[i].set_ylabel(label_map.get(chan, chan))
    axs[i+5].set_xlabel("Mean Wind Speed (m/s)")
    axs[i].grid(linestyle=':')
    axs[i+5].grid(linestyle=':')

    axs[i+5].set_ylabel(label_map.get(chan, chan). replace('(', 'STD ('))
    axs[i].ticklabel_format(axis='y', style='sci', scilimits=(-3, 3))
    axs[i+5].ticklabel_format(axis='y', style='sci', scilimits=(-3, 3))
    axs[i+5].set_xticks([2, 6, 10, 14, 18, 22, 26])

axs[0].set_ylim([0.4, 0.6])
axs[0].set_xlim([3, 10])
axs[1].set_ylim([2000, 2600])
axs[1].set_xlim([3, 10])
axs[2].set_xlim([3, 10])
axs[2].set_ylim([-5, 5])

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
#
#axt.plot(x,w,color = 'black', linestyle ='--')
##axt.plot(x,w1,color = 'black', linestyle =':')
#axt.ticklabel_format(axis='y', style='sci', scilimits=(-1, 3))
#
#axt.set_ylabel('Wind speed probability (-)')

fig.tight_layout()

handles, labels = axs[0].get_legend_handles_labels()
add_shared_legend(fig, handles, labels, upper_margin = 0.925)


plt.show()