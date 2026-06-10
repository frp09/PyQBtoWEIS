import matplotlib.pyplot as plt
from mappings import qblade_to_openfast_map, qblade_nodes_map
from data_utils import load_and_map_stats, load_DELs
from plotting import plot_stat_vs_wind, add_shared_legend, plot_spanwise_comparison, plot_DEL_vs_wind, plot_spanwise_aero
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd
#from plot_max_clcd_distribution import get_interpolated_max_efficiency


'''
PLOT PER-SIMULATION STATISTICS OF DATA
F.Papi - 2026
Università degli Studi di Firenze 

This script loads summary statistics from multiple simulations, and plots the mean, min, 
max, and std of selected channels vs wind speed for each simulation. It is designed to 
use QBtoWEIS outputs but can be adapted to other data sources with similar structure.
Optionally Damage Equivalent loads can also be plotted vs wind speed. Finally, 
it can plot spanwise distributions of selected channels.

'''

#%% USER INPUTS ------------------------------------------------------------------------

## MED CLD1.6 vs DLC1.1 vs IEA 22  DLC 1.6
ss_names = [
    r'/mnt/c/Users/utente/Desktop/TORQUEPAPER/QBSim/280-D18/iteration_0/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/LATEST_MED_v1/DLC16/iteration_0/summary_stats.p'
]

lables = [
    'IEA 22 derated 18',
    'MED 15-308'
]

savewind = True
savespan = True
savedel = True
outn_wnd = r'/home/papi/FLOATFARM/REPORTS/compareSpar_wind_R1R2.svg'
outn_spn = r'/home/papi/FLOATFARM/REPORTS/compareSpar_span_R1R2_9ms.svg'
outn_del = r'/home/papi/FLOATFARM/REPORTS/compareSpar_del_R1R2.svg'

# Plotting: Spanwise comparisons
sim_index_to_plot = 14

title = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']

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

DELchannels = [
    'X_b RootBend. Mom. BLD_1',
    'Y_b RootBend. Mom. BLD_2',
    'Z_b RootBend. Mom. BLD_3',
    #'TwrBsMyt',
    #'RootMc1', 
    #'RootMc2', 
    #'RootMc3',

    'RootMc1',
    'LSShftAxMyza',
    'TwrBsAxMomXYt',

]

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
    'AeroFyb1': 'Tangential force (kN)',
    'AeroFxb1': 'OOP force (kN)', 
    'B1Alpha': 'Angle of Attack Blade 1 (°)'

}

cmap_custom_green = LinearSegmentedColormap.from_list(
    "gray_to_teal", 
    [ #"#A9A9A9", 
     '#e05252', 
     "royalblue", 
     '#4ca64c'
     ]
)

colors = cmap_custom_green(np.linspace(0, 1, len(ss_names)))
linestyles = ['-.', '--', ':', '-', '-.', '--', ':', '-']

#%% Load data ----------------------------------------------------------------#
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
add_shared_legend(fig, handles, labels, upper_margin = 0.9)
plt.show()

if savewind: 
    fig.savefig(outn_wnd, dpi = 300)

# ## ---------------------------------------------------------------------------#
# # Plotting: DELs as function of wind speed 
# fig, axs = plt.subplots(2, 3, figsize=(10, 6.5))
# axs = axs.flatten()

# p = [ 0.03647182951511005, 0.03647182951511005, 0.03647182951511005, 0.03647182951511005,
#        0.048717647407173936, 0.048717647407173936, 0.048717647407173936, 0.048717647407173936,
#        0.04893650559845322, 0.04893650559845322, 0.04893650559845322, 0.04893650559845322,
#        0.03138968495811706, 0.03138968495811706, 0.03138968495811706, 0.03138968495811706,
#        0.017275956869181958, 0.017275956869181958, 0.017275956869181958, 0.017275956869181958,
#        0.02015206291537472, 0.02015206291537472, 0.02015206291537472, 0.02015206291537472,
#        0.017280100716439983, 0.017280100716439983, 0.017280100716439983, 0.017280100716439983,
#        0.009188510044123022, 0.009188510044123022, 0.009188510044123022, 0.009188510044123022,
#        0.00429614195483774, 0.00429614195483774, 0.00429614195483774, 0.00429614195483774,
#        0.0017732904969850194, 0.0017732904969850194, 0.0017732904969850194, 0.0017732904969850194,
#        0.0008580092583828081, 0.0008580092583828081, 0.0008580092583828081, 0.0008580092583828081,
#        6.0482736759737143e-05, 6.0482736759737143e-05, 6.0482736759737143e-05, 6.0482736759737143e-05 
#        ]

# for i, chan in enumerate(DELchannels):

#    pt = 0

#    for j in range(len(stats)):
       
#        plot_DEL_vs_wind(            
#            axs[i],
#            stats[j], 
#            DELs[j], 
#            x_col='Wind1VelX',
#            y_col=chan,
#            style={'color': colors[j], 'linestyle': '', 'marker': '.'},
#            label=lables[j]
#            )
       
#        pt = np.sum(DELs[j][chan]*p)
#        pt = pt*(25*365*24*60/900)
#        #print('LifetimeDEL ', stats[j], pt)
       
#    axs[i].set_title(title[i], fontsize='large')
#    axs[i].set_ylabel(label_map.get(chan, chan))
#    axs[i].set_xlabel("Mean Wind Speed (m/s)")
   
# handles, labels = axs[0].get_legend_handles_labels()
# add_shared_legend(fig, handles, labels, upper_margin = 0.9)
# plt.show()

# if savedel: 
#    fig.savefig(outn_del, dpi = 300)

# ---------------------------------------------------------------------------#
# Plotting: qblade struct spanwise quantities

spanwise_channels = [    
          'RDzb1',
          'TDxb1',
          'TDyb1',
          'AeroFyb1',  
          'AeroFxb1',
          'B1Alpha',
          #'B1AxInd',
          #'TDyb1',
          #'TDxb1'
          ]

figs, axss = plt.subplots(1, len(spanwise_channels), figsize=(3.5 * len(spanwise_channels), 5))
plot_spanwise_comparison(stats, spanwise_channels, lables, colors, linestyles, figs, axss, sim_label=sim_index_to_plot, title_prefix="Spanwise: ", show_extrema=True)

for i, chan in enumerate(spanwise_channels):
    axss[i].set_ylabel(label_map.get(chan, chan))
    axss[i].set_title(title[i])

axss[5].set_ylim(0,14)
#axss[2].set_ylim(-1250, 250)

figs.tight_layout()
handles, labels = axss[0].get_legend_handles_labels()
add_shared_legend(fig, handles, labels, upper_margin= 0.9)
#plt.show()

if savespan:
    figs.savefig(outn_spn, dpi = 300)

# ---------------------------------------------------------------------------#
# Plotting: qblade aero  spanwise quantites such as Cl, Cd, Induction

spanwise_aero_channels = [    
          'B1AxInd',
          #'B1Cl',
          #'B1Alpha', 
          'B1ClCd',
          #'B1Cd',
          'B1Re']


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

#print('MEAN WIND SPEED: ', stats[0].loc[:,('Wind1VelX', 'mean')].iloc[sim_index_to_plot])
fig, axs = plt.subplots(1, len(spanwise_aero_channels), figsize=(3.5 * len(spanwise_aero_channels), 4))
plot_spanwise_aero(stats, spanwise_aero_channels, qblade_nodes_map, labels, colors, linestyles, fig, axs, sim_label=sim_index_to_plot, title_prefix="", show_extrema=True)

axs[0].plot([0,1], [0.33, 0.33], color = 'black', linestyle = '--')

##plot maximum spanwise distribution of aerodynamic efficiency
#BLADE_FILE = '/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.8_BOPTNSS/DLC1.1_0_MED15-308_v30.2.10_02/Aero/DLC1.1_0_MED15-308_v30.2.10_02.bld'
#example_target_spans = np.array(spn)*150
#example_target_reynolds = np.array(Re)
#
#print(example_target_reynolds)
#print(example_target_spans)
#print(type(example_target_reynolds))
#print(type(example_target_spans))
#print("Calculating max efficiency distribution...")
#
#try:
#    max_cl_cd_dist, max_cl_cd_aoa = get_interpolated_max_efficiency(
#        example_target_spans,
#        example_target_reynolds,
#        BLADE_FILE
#    )
#    print("Calculation complete.")
#except Exception as e:
#        print(f"An error occurred during calculation: {e}")
#
#    
#
#axs[1].plot(spn, max_cl_cd_dist, color = 'black', linestyle = '--')
#axss[4].plot(spn, max_cl_cd_aoa, color = 'black', linestyle = '--')

plt.show()


# %%
