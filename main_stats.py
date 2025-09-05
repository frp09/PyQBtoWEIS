import matplotlib.pyplot as plt
from mappings import qblade_to_openfast_map, qblade_nodes_map
from data_utils import load_and_map_stats, load_DELs
from plotting import plot_stat_vs_wind, add_shared_legend, plot_spanwise_comparison, plot_DEL_vs_wind, plot_spanwise_aero
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


#%% USER INPUTS ------------------------------------------------------------------------

ss_names = [

    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.0_OPT/R1/mout_MED15-308_v20.7.0/iteration_0/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.0_OPT/R1/mout_MED15-308_v20.7.0/iteration_318/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.1_OPT/R1/mout_MED15-308_v20.7.1/iteration_324/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.2_OPT/R1/mout_MED15-308_v20.7.2/iteration_329/summary_stats.p',
]

#ss_names = [
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.6.1_OPT/R1/mout_MED15-308_v20.7.1/iteration_0/summary_stats.p',
#    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.6.1_OPT/R1/mout_MED15-308_v20.7.1/iteration_324/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.6.1_OPT/R2/mout_MED15-308_v20.7.1/iteration_159/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.6.1_OPT/R3/iteration_0/summary_stats.p',
#
#]

lables = [

        'start',
        'middle', 
        'forward', 
        'back'
          
          ]


#ss_names = [
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/00_QBTOWEIS_VERIFICATION_IEA22/VALIDATE_RADIANS_DEGREES/mout_SONATA_deg/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/00_QBTOWEIS_VERIFICATION_IEA22/VALIDATE_RADIANS_DEGREES/mout_SONATA_rad/iteration_0/summary_stats.p',
#]
#
#lables = [
#
#        'deg',
#        'red', 
#          
#          ]
#
#ss_names = [
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.6.1_OPT/R2/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v31.1.0_OPT/iteration_0/summary_stats.p',
#]
#
#lables = [
#
#        '2 shear webs',
#        '3 shear webs', 
#          
#          ]

#ss_names = [
#    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.6.1_OPT/R1/mout_MED15-308_v20.7.1/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.1_RUN/mout_MED15-308_v20.6.1_LD1/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.1_RUN/mout_MED15-308_v20.6.1_LD2/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.1_RUN/mout_MED15-308_v20.6.1_LD3/iteration_0/summary_stats.p',
#
#]
#
#lables = [
#        #'1-2%% crit',
#        '0.5-1% crit',
#        '0.25-0.5%crit', 
#        '0%c crit'
#          
#          ]
#
# ---------------------------------------------------------------------------------------


#ss_names = [
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v31.1.0_OPT_II/mout_MED15-308_v31.1.2/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v31.1.0_OPT_III/mout_MED15-308_v31.1.3/iteration_0/summary_stats.p',
#
#]
#
#lables = [
#
#        '31.1.0_II_it0',
#        '31.1.0_III_it0', 
#          
#          ]

# ------------------------------------------------------------------------------------------
ss_names = [

    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_CtrlOpt/R1/mout_MED15-308_v30.1.1/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_CtrlOpt/mout_MED15-308_v30.1.1/iteration_84/summary_stats.p',

]

lables = [

        'iter_0', 
        'iter_84'
          
          ]

savewind = False
savespan = False
outn_wnd = r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.6.1_OPT/R2/compare_wind_R1R2.svg'
outn_spn = r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.6.1_OPT/R2/compare_span_R1R2_7ms.svg'

# Plotting: Spanwise comparisons
sim_index_to_plot = 10



title = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']

channels = ['BldPitch1',
            'RtAeroCp',
            # 'RtAeroCt',
            #'GenPwr', 
            # 'GenTq',
            #'RotSpeed',
            'RtAeroTh',
            #'TipDxc1',
            'TipDyc1',
            'RDzb1_1.000',
            'RootMyc1'
            ]

DELchannels = [
    'X_b RootBend. Mom. BLD_1',
    'Y_b RootBend. Mom. BLD_2',
    'Z_b RootBend. Mom. BLD_3',
    'RootMc1', 
    'RootMc2', 
    'RootMc3'


]

label_map = {
    'BldPitch1': 'Blade pitch (°)',
    'RtAeroCp': 'Aero Cp (-)',
    'RtAeroCt': 'Aero Ct (-)',
    'RotSpeed': 'Rotor speed (rpm)',
    'TipDxc1': 'Tip deflection (OOP)',
    'RDzb1_0.800': 'Tip torsional deflection (°)',
    'RtAeroTh': 'Aerodynamic Thrust (kN)',
    'RootMyc1': 'Blade Root OOP BM (kNm)'
}

cmap_custom_green = LinearSegmentedColormap.from_list(
    "gray_to_teal", 
    #["#FAAA0A", "#006BA6"]  # Warm gray to teal
    [ "#A9A9A9", 
     '#e05252', 
     "royalblue", 
     '#4ca64c'
     ]
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
# Plotting: DELs as function of wind speed 
fig, axs = plt.subplots(2, 3, figsize=(10, 7))
axs = axs.flatten()

for i, chan in enumerate(DELchannels):
    for j in range(len(stats)):
        
        plot_DEL_vs_wind(            
            axs[i],
            stats[j], 
            DELs[j], 
            x_col='Wind1VelX',
            y_col=chan,
            style={'color': colors[j], 'linestyle': '', 'marker': '.'},
            label=lables[j]
            )
        
    axs[i].set_title(title[i], fontsize='large')
    axs[i].set_ylabel(label_map.get(chan, chan))
    axs[i].set_xlabel("Mean Wind Speed (m/s)")

handles, labels = axs[0].get_legend_handles_labels()
add_shared_legend(fig, handles, labels)
plt.show()

# ---------------------------------------------------------------------------#
# Plotting: qblade struct spanwise quantities

spanwise_channels = [    
          'RDzb1',
          #'AeroFyb1',  
          #'AeroFxb1',
          'B1Alpha',
          #'B1AxInd',
          'TDyb1',
          'TDxb1']

fig, axs = plt.subplots(1, len(spanwise_channels), figsize=(3.5 * len(spanwise_channels), 4))
plot_spanwise_comparison(stats, spanwise_channels, lables, colors, linestyles, fig, axs, sim_label=sim_index_to_plot, title_prefix="Spanwise: ", show_extrema=True)
plt.show()

if savespan:
    fig.savefig(outn_spn, dpi = 300)

# ---------------------------------------------------------------------------#
# Plotting: qblade aero  spanwise quantites such as Cl, Cd, Induction

spanwise_aero_channels = [    
          'B1AxInd', 
          'B1Cl',
          'B1Cd',]

fig, axs = plt.subplots(1, len(spanwise_aero_channels), figsize=(3.5 * len(spanwise_aero_channels), 4))
plot_spanwise_aero(stats, spanwise_aero_channels, qblade_nodes_map, labels, colors, linestyles, fig, axs, sim_label=sim_index_to_plot, title_prefix="", show_extrema=True)
plt.show()

