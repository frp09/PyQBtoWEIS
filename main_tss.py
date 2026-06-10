from plotting import plot_psd, plot_fft, plot_tss, add_shared_legend
import pandas as pd
from data_utils import get_mapped_columns, read_df, load_and_map_timeseries
from mappings import qblade_to_openfast_map
import matplotlib.pyplot as plt

# set inputs -----------------------------------------------------------

files = [
r'/home/papi/FLOATFARM/QB-WEIS-COUPLE/NEW_MED_OPTIMIZATION/MED15-308_v30.2.24_RUN/DLC16_MED15-308_v30.2.24/iteration_0/timeseries/MED15-308_v30.2.24_20.p',
    ]

lables = [

        'DLC16', 
          
          ]


colors = ['red', 'black', 'red', 'green', 'orange', 'purple','blue', 'black', 'red', 'green', 'orange', 'purple']
#colors = ['#e05252', 'royalblue',]# '#4ca64c']
linestyles = ['-','--','-.',':', '-']
channels = ['NcIMUTAxn', 'BldPitch1', 'TwrBsMyt', 'RotSpeed', 'GenPwr']#, 'PtfmPitch']# 'TDxb1_1.000', 'RDzb1_1.000']
#channels = ['TwrBsMyt', 'Wind1VelX', 'BldPitch1', 'RotSpeed', 'GenPwr', 'TipDyc1']
channels = ['TipDxc1', 'TipDyc1','TwrBsMyt', 'RootMxc1', 'RootMyc1', 'RootMzc1']
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

