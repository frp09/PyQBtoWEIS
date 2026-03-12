import matplotlib.pyplot as plt
from mappings import qblade_to_openfast_map, qblade_nodes_map
from data_utils import load_and_map_stats, load_DELs
from plotting import plot_stat_vs_wind, add_shared_legend, plot_spanwise_comparison, plot_DEL_vs_wind, plot_spanwise_aero
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd
from plot_max_clcd_distribution import get_interpolated_max_efficiency


#%% USER INPUTS ------------------------------------------------------------------------

ss_names = [
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.11_BOPTSTR/mout_MED15-308_v30.2.12/iteration_0/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.8_BOPTNSS/iteration_0/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.17/iteration_0/summary_stats.p',
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.7_BOPSTD/mout_MED15-308_v30.2.16/iteration_0/summary_stats.p',
    ]

lables = [
'30.3.2_1.6',
'30.3.2_1.1',
#'blblbl'
          ]


savewind = False
savespan = False
savedel = False
outn_wnd = r'/home/papi/FLOATFARM/REPORTS/compareSpar_wind_R1R2.svg'
outn_spn = r'/home/papi/FLOATFARM/REPORTS/compareSpar_span_R1R2_9ms.svg'
outn_del = r'/home/papi/FLOATFARM/REPORTS/compareSpar_del_R1R2.svg'

# Plotting: Spanwise comparisons
sim_index = [
 [2, 6, 9, 14, 18, ],
 [0,4,8, 12,14,] ,
 #[0,4,12,14, 16] 
]

title = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']
title = ['3 m/s', '5 m/s', '7 m/s', '9 m/s', '10 m/s']

channels = ['BldPitch1',
            #'RtAeroCp',
            # 'RtAeroCt',
            #'GenPwr',
            #'RtAeroPwr', 
            #'GenTq',
            'RotSpeed',
            'RtAeroTh',
            'TipDxc1',
            'TipDyc1',
            'RDzb1_0.950',
            #'PtfmSurge',
            #'PtfmPitch',
            #'RootMyc1',
            #'TwrBsMyt',
            #'NcIMUTAxn', 
            ]

labels = ['BldPitch1',
            #'RtAeroCp',
            # 'RtAeroCt',
            #'GenPwr',
            #'RtAeroPwr', 
            #'GenTq',
            'RotSpeed',
            'RtAeroTh',
            'TipDxc1',
            'TipDyc1',
            'RDzb1_0.950',
            #'PtfmSurge',
            #'PtfmPitch',
            #'RootMyc1',
            #'TwrBsMyt',
            #'NcIMUTAxn', 
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

# Load data
stats_raw, stats = load_and_map_stats(ss_names, qblade_to_openfast_map, drop_unmapped=True, verbose=False)
del_paths = [ss_names[i].replace('summary_stats.p', 'DELs.p') for i in range(len(ss_names))]
DELs = load_DELs(del_paths)


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

n_models  = len(sim_index)            # i‑dimension
n_runs    = len(sim_index[0])         # assume all lists same length
wsds = pd.DataFrame(index=range(n_models),
                    columns=range(n_runs),
                    dtype=float)      # or fill later

for i, idi in enumerate(sim_index):
    for j, idj in enumerate(sim_index[i]):
        # locate the row label corresponding to the selected wind speed
        speed = sim_index[i][j]
        token1 = f'_{speed}_'
        token2 = f'_{speed:02}_' if 0 <= speed < 10 else None
        lbl = None
        for elm in stats[i].index:
            if token1 in elm or (token2 and token2 in elm):
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

    figs, axss = plt.subplots(1, len(sim_index[0]), figsize=(3.5 * len(sim_index[0]), 5))

    for i,idi in enumerate(sim_index):   #loop through various cases

        # wsds already filled above; do not recreate here
        for j,idj in enumerate(sim_index[i]):   #loop through various wind speeds

            plot_spanwise_comparison({i: stats[i]}, [channel], lables, colors, linestyles, figs, axss[j], sim_label=idj, title_prefix="Spanwise: ", show_extrema=True)
   
            axss[j].set_ylabel(label_map.get(channel, channel))
            axss[j].set_title(title[j])
    
    figs.tight_layout()
        
#
    #axss[5].set_ylim(0,14)
    ##axss[2].set_ylim(-1250, 250)
#
    #figs.tight_layout()
    #handles, labels = axss[0].get_legend_handles_labels()
    #add_shared_legend(fig, handles, labels, margin = 0.9)
    ##plt.show()

if savespan:
    figs.savefig(outn_spn, dpi = 300)

## ---------------------------------------------------------------------------#
## Plotting: qblade aero  spanwise quantites such as Cl, Cd, Induction
#
#spanwise_aero_channels = [    
#          'B1AxInd',
#          #'B1Cl',
#          #'B1Alpha', 
#          'B1ClCd',
#          #'B1Cd',
#          'B1Re']
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
##print('MEAN WIND SPEED: ', stats[0].loc[:,('Wind1VelX', 'mean')].iloc[sim_index_to_plot])
#fig, axs = plt.subplots(1, len(spanwise_aero_channels), figsize=(3.5 * len(spanwise_aero_channels), 4))
#Re, spn = plot_spanwise_aero(stats, spanwise_aero_channels, qblade_nodes_map, labels, colors, linestyles, fig, axs, sim_label=sim_index_to_plot, title_prefix="", show_extrema=True)
#
#axs[0].plot([0,1], [0.33, 0.33], color = 'black', linestyle = '--')
#
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
