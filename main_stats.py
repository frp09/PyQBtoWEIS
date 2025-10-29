import matplotlib.pyplot as plt
from mappings import qblade_to_openfast_map, qblade_nodes_map
from data_utils import load_and_map_stats, load_DELs
from plotting import plot_stat_vs_wind, add_shared_legend, plot_spanwise_comparison, plot_DEL_vs_wind, plot_spanwise_aero
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd


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

        'start (mid)',
        'middle', 
        'forward', 
        'back'
          
          ]

ss_names = [

    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.0_OPT/R1/mout_MED15-308_v20.7.0/iteration_0/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.1_OPT/R1/mout_MED15-308_v20.7.1/iteration_0/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.2_OPT/R1/mout_MED15-308_v20.7.2/iteration_0/summary_stats.p',
]

lables = [

        'start (mid)',
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
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.1_OPT/R2/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v31.1.0_OPT/iteration_0/summary_stats.p',
#]
#
#lables = [
#
#        '2 shear webs',
#        '3 shear webs', 
#          
#          ]
#
ss_names = [
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.6.1_OPT/R1/mout_MED15-308_v20.7.1/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.2_RUN/mout_MED15-308_v20.6.2_LD1/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.0_RUN/mout_MED15-308_v20.6.0_LD2/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.1_RUN/mout_MED15-308_v20.6.1_LD1/iteration_0/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.1_RUN/mout_MED15-308_v20.6.1_LD2/iteration_0/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.7.0_RUN/mout_MED15-308_v20.7.2_LD3/iteration_0/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.7.1_RUN/mout_MED15-308_v20.7.1_LD2/iteration_0/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.7.2_RUN/mout_MED15-308_v20.7.2_LD2/iteration_0/summary_stats.p',
    

#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.6.1_RUN/mout_MED15-308_v20.6.1_LD3/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.7.1_RUN/mout_MED15-308_v20.7.1_LD1/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/COMPARE_SPAR_POS/MED15-308_v20.7.1_RUN/mout_MED15-308_v20.7.1_LD4/iteration_0/summary_stats.p'    
]

lables = [

        'start (forw)',
        'middle', 
        'forward', 
        'back'
          
          ]
#
#lables = [
#        '1-2%% crit',
##        '0.5-1% crit',
##        '0.25-0.5% crit', 
#        '0.0% crit'
##          
#          ]
##
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
#
# ------------------------------------------------------------------------------------------
#ss_names = [
#
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_CtrlOpt/R2/mout_MED15-308_v30.1.1/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_CtrlOpt/R2/mout_MED15-308_v30.1.1/iteration_71/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_CtrlOpt/R2/mout_MED15-308_v30.1.1/iteration_115/summary_stats.p',
#
#]
#
#lables = [
#
#        'iter_0', 
#        'iter_71',
#        'iter_115',
#          
#          ]

# ------------------------------------------------------------------------------------------
#ss_names = [
#    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.6.1_OPT/R1/mout_MED15-308_v20.7.1/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/06_bladeOpt/mout_MED15-308_v31.1.2/iteration_0/summary_stats.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/06_bladeOpt/mout_MED15-308_v31.1.2/iteration_1/summary_stats.p',
#
#]
#
#lables = [
#
#        'iter_0', 
#        'iter_1'
#          
#          ]

ss_names = [
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.6.1_OPT/R1/mout_MED15-308_v20.7.1/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_BOPT/mout_MED15-308_v30.1.2/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_BOPT/mout_MED15-308_v30.1.2/iteration_79/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_BOPTNSS/mout_MED15-308_v30.1.3/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_BOPTNSS/mout_MED15-308_v30.1.3/iteration_208/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_BOPTNSS/mout_MED15-308_v30.1.3/iteration_400/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_BOPTNSS/mout_MED15-308_v30.1.4/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_BOPTNSS/mout_MED15-308_v30.1.4/iteration_33/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_BOPTNSS/mout_MED15-308_v30.1.4/iteration_200/summary_stats.p',
    #r'/mnt/d/RUN/AGSM/IEA_15MW/IEA15MW_RWT_out/iteration_0/summary_stats.p',
    #r'/mnt/d/RUN/AGSM/IEA_15MW copy/iteration_0/summary_stats.p',
    ]

lables = [

        'BOPT_TSR',
        'BOPT'
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
            'GenTq',
            'RotSpeed',
            'RtAeroTh',
            'TipDxc1',
            #'TipDyc1',
            #'RDzb1_0.950',
            #'PtfmSurge',
            #'PtfmPitch',
            #'RootMyc1',
            #'TwrBsMyt',
            #'NcIMUTAxn', 
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
    'RDzb1_0.800': 'Tip torsional deflection (°)',
    'RtAeroTh': 'Aerodynamic Thrust (kN)',
    'RootMyc1': 'Blade Root OOP BM (kNm)'
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

## ---------------------------------------------------------------------------#
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
          'AeroFyb1',  
          'AeroFxb1',
          'B1Alpha',
          #'B1AxInd',
          #'TDyb1',
          #'TDxb1'
          ]

fig, axs = plt.subplots(1, len(spanwise_channels), figsize=(3.5 * len(spanwise_channels), 4))
plot_spanwise_comparison(stats, spanwise_channels, lables, colors, linestyles, fig, axs, sim_label=sim_index_to_plot, title_prefix="Spanwise: ", show_extrema=True)
axs[3].set_ylim(-5,15)
axs[1].set_ylim(-1250, 250)
plt.show()

if savespan:
    fig.savefig(outn_spn, dpi = 300)

# ---------------------------------------------------------------------------#
# Plotting: qblade aero  spanwise quantites such as Cl, Cd, Induction

spanwise_aero_channels = [    
          'B1AxInd', 
          #'B1ClCd',
          'B1Cd',]


if 'B1ClCd' in spanwise_aero_channels:
    for i in range(len(stats)):

        num = stats[i].filter(regex="B1Cl")
        den = stats[i].filter(regex="B1Cd")

        # Make sure they have the same shape
        result = pd.DataFrame(
            np.divide(num.to_numpy(), den.to_numpy()),
            index=stats[i].index,
            columns=pd.MultiIndex.from_tuples([
            (c[0].replace("B1Cl", "B1ClCd"), c[1]) for c in num.columns
                ])
            )
        # Add it back
        stats[i] = stats[i].join(result)

print('MEAN WIND SPEED: ', stats[0].loc[:,('Wind1VelX', 'mean')].iloc[sim_index_to_plot])
fig, axs = plt.subplots(1, len(spanwise_aero_channels), figsize=(3.5 * len(spanwise_aero_channels), 4))
plot_spanwise_aero(stats, spanwise_aero_channels, qblade_nodes_map, labels, colors, linestyles, fig, axs, sim_label=sim_index_to_plot, title_prefix="", show_extrema=True)
plt.show()


# %%
