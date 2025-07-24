import matplotlib.pyplot as plt
from mappings import qblade_to_openfast_map
from data_utils import load_and_map_stats
from plotting import plot_stat_vs_wind, add_shared_legend, plot_spanwise_comparison
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

ss_names = [

    # r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.1.0/mout_MED15-300_v20.0.0_OPT/iteration_0/summary_stats.p',
    # r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.1.0/mout_MED15-300_v20.0.0_OPT/iteration_46/summary_stats.p',
    # r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.1.0_OPT_II/mout_MED15-308_v20.3.0_OPT/iteration_0/summary_stats.p'
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.1.0_OPT_III/mout_MED15-308_v20.3.0_OPT/iteration_0/summary_stats.p',
    # r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.1.0_OPT_III/mout_MED15-308_v20.3.0_OPT/iteration_120/summary_stats.p',
    # r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.1.0_OPT_III/mout_MED15-308_v20.3.0_OPT/iteration_121/summary_stats.p',
    # r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.1.0_OPT_III/mout_MED15-308_v20.3.0_OPT/iteration_122/summary_stats.p',
    # r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.1.0_OPT_III/mout_MED15-308_v20.3.0_OPT/iteration_123/summary_stats.p',
    # r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.1.0_OPT_III/mout_MED15-308_v20.3.0_OPT/iteration_124/summary_stats.p',
    # r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.1.0_OPT_III/mout_MED15-308_v20.3.0_OPT/iteration_125/summary_stats.p',
    # r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.1.0_OPT_III/mout_MED15-308_v20.3.0_OPT/iteration_126/summary_stats.p',
    # r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.1.0_OPT_III/mout_MED15-308_v20.3.0_OPT/iteration_127/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.1.0_OPT_III/mout_MED15-308_v20.3.0/iteration_0/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.4.0/mout_MED15-308_v20.4.0/iteration_0/summary_stats.p',

]

lables = [
          'v20.3.0_ITER1',
          # 'v20.3.0_ITER120',
          # 'v20.3.0_ITER121',
          # 'v20.3.0_ITER122',
          # 'v20.3.0_ITER123',
          # 'v20.3.0_ITER124',
          # 'v20.3.0_ITER125',
          # 'v20.3.0_ITER126',
          # 'v20.3.0_ITER127',
          'v20.3.0_lowdamp',
          'v20.4.0_ITER0',
          
          ]

title = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']

channels = ['BldPitch1',
            'RtAeroCp',
            # 'RtAeroCt',
            # 'GenPwr', 
            # 'GenTq',
            'RotSpeed',
            'RtAeroTh',
            'TipDxc1',
            #'RDzb1_0.800',
            'RootMyc1'
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
    ["#FAAA0A", "#006BA6"]  # Warm gray to teal
)

colors = cmap_custom_green(np.linspace(0, 1, len(ss_names)))
linestyles = ['-.', '--', ':', '-', '-.', '--', ':', '-']

# Load data
stats_raw, stats = load_and_map_stats(ss_names, qblade_to_openfast_map, drop_unmapped=True, verbose=True)

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


# Plotting: Spanwise comparisons
sim_index_to_plot = 15

spanwise_channels = [    
          'RDzb1',
          'AeroFyb1',  
          'AeroFxb1',
          'TDxb1']

plot_spanwise_comparison(stats, spanwise_channels, lables, colors, linestyles, sim_label=sim_index_to_plot, title_prefix="Spanwise: ", show_extrema=True)