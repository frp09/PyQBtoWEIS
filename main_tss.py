from plotting import plot_psd, plot_fft, plot_tss, add_shared_legend
import pandas as pd
from data_utils import get_mapped_columns, read_df, load_and_map_timeseries
from mappings import qblade_to_openfast_map
import matplotlib.pyplot as plt

# set inputs -----------------------------------------------------------

#files = [
#    # r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.4.0_OPT/mout_MED15-308_v20.4.0/iteration_0/timeseries/MED15-308_v20.4.0_45.p',
#    # r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.4.0_OPT_II/mout_MED15-308_v20.4.0/iteration_8/timeseries/MED15-308_v20.4.0_47.p',
#    # r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.5.0_OPT/mout_MED15-308_v20.5.0/iteration_0/timeseries/MED15-308_v20.5.0_40.p',
#    # r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.5.0_OPT_II/iteration_0/timeseries/MED15-308_v20.5.0_40.p',
#
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.6.0_OPT/R1/mout_MED15-308_v20.7.0/iteration_318/timeseries/MED15-308_v20.7.0_46.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.6.1_OPT/R1/mout_MED15-308_v20.7.1/iteration_324/timeseries/MED15-308_v20.7.1_46.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.6.2_OPT/R1/mout_MED15-308_v20.7.2/iteration_329/timeseries/MED15-308_v20.7.0_46.p',
#
#    ]
#
#lables = [
#   
#    'middle',
#    'forward', 
#    'back',
#
#    ]
#
#files = [
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/00_QBTOWEIS_VERIFICATION_IEA22/VALIDATE_RADIANS_DEGREES/mout_SONATA_deg/iteration_0/timeseries/IEA22_turbine_deg_4.p',
#    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/00_QBTOWEIS_VERIFICATION_IEA22/VALIDATE_RADIANS_DEGREES/mout_SONATA_rad/iteration_0/timeseries/IEA22_turbine_rad_4.p',
#
#    ]
#
#lables = [
#   
#    'rad',
#    'deg', 
#
#    ]

files = [
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.6.1_OPT/R1/mout_MED15-308_v20.7.1/iteration_0/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_CtrlOpt/R2/mout_MED15-308_v30.1.1/iteration_0/timeseries/MED15-308_v30.1.1_26.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_CtrlOpt/R2/mout_MED15-308_v30.1.1/iteration_115/timeseries/MED15-308_v30.1.1_26.p',

]

lables = [

        'iter_0', 
        'iter_115'
          
          ]

files = [
    #r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v20.6.1_OPT/R1/mout_MED15-308_v20.7.1/iteration_0/summary_stats.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_BOPT/mout_MED15-308_v30.1.2/iteration_0/timeseries/MED15-308_v30.1.2_26.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_BOPT/mout_MED15-308_v30.1.2/iteration_79/timeseries/MED15-308_v30.1.2_26.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_BOPTNSS/mout_MED15-308_v30.1.3/iteration_0/timeseries/MED15-308_v30.1.3_26.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_BOPTNSS/mout_MED15-308_v30.1.3/iteration_208/timeseries/MED15-308_v30.1.3_26.p',
    r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.1.0_BOPTNSS/mout_MED15-308_v30.1.3/iteration_193/timeseries/MED15-308_v30.1.3_26.p',

]

lables = [

        'BOPT_it0', 
        'BOPT_it79',
        'BOPTNSS_it0',  
        'BOPTNSS_it208',
        'BOPTNSS_it193',
          ]

colors = ['red', 'black', 'red', 'green', 'orange', 'purple','blue', 'black', 'red', 'green', 'orange', 'purple']
#colors = ['#e05252', 'royalblue',]# '#4ca64c']
linestyles = ['-','--','-.',':', '-']
channels = ['NcIMUTAxn', 'BldPitch1', 'TwrBsMyt', 'RotSpeed', 'GenPwr']#, 'PtfmPitch']# 'TDxb1_1.000', 'RDzb1_1.000']
#channels = ['TwrBsMyt', 'Wind1VelX', 'BldPitch1', 'RotSpeed', 'GenPwr', 'TipDyc1']
titles = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']

label_map = {
'NcIMUTAxn' : 'Nacelle Acceleration', 
'TwrBsMyt': 'Tower NBase OOP moment',
'TipDyc1': 'Blade tip IP deflection', 
'TipDxc1': 'Blade tip OOP deflection',
'RDzb1_0.950': 'Blade tip torsional deflection',
'PtfmPitch': 'Plartform Pitch'
}

# process data ---------------------------------------------------------

# Load data
ts_raw, tss = load_and_map_timeseries(files, qblade_to_openfast_map, drop_unmapped=True, verbose=True)

# Plotting: PSD
fig_psd, axs_psd = plt.subplots(3, 2, figsize=(10, 7))
axs_psd = axs_psd.flatten()
for i, chan in enumerate(channels):
    for j in range(len(tss)):
        fs = 1 / tss[j].Time.diff().dropna().mean()
        plot_psd(
            axs_psd[i], tss[j], chan, fs,
            style={'color': colors[j], 'linestyle': linestyles[j]},
            label=lables[j],
            label_map=label_map
        )
    axs_psd[i].set_title(titles[i], fontsize='large')
    axs_psd[i].set_xlabel("Frequency [Hz]")
    #axs_psd[i].semilogy()
handles, labels = axs_psd[0].get_legend_handles_labels()
add_shared_legend(fig_psd, handles, labels)
plt.show()
#
## Plotting: FFT
fig_fft, axs_fft = plt.subplots(3, 2, figsize=(10, 7))
axs_fft = axs_fft.flatten()
for i, chan in enumerate(channels):
    for j in range(len(tss)):
        fs = 1 / tss[j].Time.diff().dropna().mean()
        plot_fft(
            axs_fft[i], tss[j], chan, fs,
            style={'color': colors[j], 'linestyle': linestyles[j]},
            label=lables[j],
            label_map=label_map
        )
    axs_fft[i].set_title(titles[i], fontsize='large')
    axs_fft[i].set_xlabel("Frequency [Hz]")
handles, labels = axs_fft[0].get_legend_handles_labels()
add_shared_legend(fig_fft, handles, labels)
plt.show()

# Plotting: TSS
fig_tss, axs_tss = plt.subplots(3, 2, figsize=(10, 7), sharex=True)
axs_tss = axs_tss.flatten()
for i, chan in enumerate(channels):
    for j in range(len(tss)):
        plot_tss(
            axs_tss[i], tss[j], chan,
            style={'color': colors[j], 'linestyle': linestyles[j]},
            label=lables[j],
            label_map=label_map
        )
    axs_tss[i].set_title(titles[i], fontsize='large')
    axs_tss[i].set_xlabel("Time [s]")
handles, labels = axs_tss[0].get_legend_handles_labels()
add_shared_legend(fig_tss, handles, labels)
plt.show()

