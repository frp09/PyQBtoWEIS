import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import re
import numpy as np
import scipy.signal as signal

def plot_stat_vs_wind(ax, data, x_col, y_col, style, label):
    x = data[x_col]['mean']
    y_mean = data[y_col]['mean']
    y_max = data[y_col]['max']
    y_min = data[y_col]['min']

    ax.plot(x, y_mean, label=label, **style)
    ax.scatter(x, y_max, edgecolor=style['color'], color='none', marker='^', s = 14)
    ax.scatter(x, y_min, edgecolor=style['color'], color='none', marker='v', s = 14)
    ax.grid(linestyle =':', color = 'gray')

def plot_DEL_vs_wind(ax, data_st, data_DEL, x_col, y_col, style, label):
    x = data_st[x_col]['mean']
    y_mean = data_DEL[y_col]

    ax.plot(x, y_mean, label=label, **style)
    ax.grid(linestyle =':', color = 'gray')

def plot_spanwise_comparison(stats_mapped, spanwise_channels, labels, colors, linestyles, fig, axs, sim_label, title_prefix="", show_extrema=False):
    
    if len(spanwise_channels) == 1:
        axs = [axs]

    for i, chan in enumerate(spanwise_channels):
        ax = axs[i]

        for j, df in stats_mapped.items():
            try:
                # Extract mean, max and min slices from multi-index DataFrame
                df_mean = df.xs('mean', axis=1, level=1)
                df_max = df.xs('max', axis=1, level=1) if show_extrema else None
                df_min = df.xs('min', axis=1, level=1) if show_extrema else None

                # Construct row label from simulation index, zero-padded
                row_label = str(sim_label).zfill(2)
                lbl = False
                for elm in df_mean.index:
                    if '_'+row_label+'_' in elm: 
                        lbl = elm

                if not lbl:
                    raise ValueError(f"Row label {row_label} not found in index")

                matching_cols = []  # holds column names matching current channel
                spans = []          # holds corresponding spanwise positions

                for col in df_mean.columns:
                    if chan in col:
                        match = re.search(r'(\d+\.\d+)', col)
                        if match:
                            matching_cols.append(col)
                            spans.append(float(match.group(1)))

                if not matching_cols:
                    raise ValueError("No valid spanwise data columns found")

                # Sort columns by their spanwise numeric values
                sorted_pairs = sorted(zip(spans, matching_cols))
                spans, matching_cols = zip(*sorted_pairs)

                # Extract mean values along span for selected row and columns
                values = df_mean.loc[lbl, list(matching_cols)].values

                ax.plot(spans, values, label=labels[j], color=colors[j], linestyle=linestyles[j])

                if show_extrema and df_max is not None and df_min is not None:
                    y_max = df_max.loc[lbl, list(matching_cols)].values
                    y_min = df_min.loc[lbl, list(matching_cols)].values
                    ax.scatter(spans, y_max, edgecolor=colors[j], color='none', marker='^')
                    ax.scatter(spans, y_min, edgecolor=colors[j], color='none', marker='v')

            except Exception as e:
                print(f"Failed to plot {chan} for dataset {j}: {e}")
                continue

        ax.set_title(f"{title_prefix}{chan}")
        ax.set_xlabel("Spanwise position (r/R)")
        ax.set_ylabel(chan)
        ax.grid(linestyle =':', color = 'gray')

    handles, labels = axs[0].get_legend_handles_labels()
    add_shared_legend(fig, handles, labels)

def plot_spanwise_aero(stats_mapped, spanwise_channels, span_map, labels, colors, linestyles, fig, axs, sim_label, title_prefix="", show_extrema=False):
    
    if len(spanwise_channels) == 1:
        axs = [axs]

    for i, chan in enumerate(spanwise_channels):
        ax = axs[i]

        for j, df in stats_mapped.items():
            try:
                # Extract mean, max and min slices from multi-index DataFrame
                df_mean = df.xs('mean', axis=1, level=1)
                df_max = df.xs('max', axis=1, level=1) if show_extrema else None
                df_min = df.xs('min', axis=1, level=1) if show_extrema else None

                # Construct row label from simulation index, zero-padded
                row_label = str(sim_label).zfill(2)
                lbl = False
                for elm in df_mean.index:
                    if '_'+row_label+'_' in elm: 
                        lbl = elm

                if not lbl:
                    raise ValueError(f"Row label {row_label} not found in index")

                matching_cols = []  # holds column names matching current channel
                spans = []          # holds corresponding spanwise positions

                for col in df_mean.columns:
                    if chan in col:
                        match = re.search(r'_n(\d)', col)
                        node =float(col.split('_n')[-1])
                        if match:
                            matching_cols.append(col)
                            spans.append(span_map[node])

                if not matching_cols:
                    raise ValueError("No valid spanwise data columns found")

                # Sort columns by their spanwise numeric values
                sorted_pairs = sorted(zip(spans, matching_cols))
                spans, matching_cols = zip(*sorted_pairs)

                # Extract mean values along span for selected row and columns
                values = df_mean.loc[lbl, list(matching_cols)].values

                ax.plot(spans, values, label=labels[j], color=colors[j], linestyle=linestyles[j])

                if show_extrema and df_max is not None and df_min is not None:
                    y_max = df_max.loc[lbl, list(matching_cols)].values
                    y_min = df_min.loc[lbl, list(matching_cols)].values
                    #ax.scatter(spans, y_max, edgecolor=colors[j], color='none', marker='^')
                    #ax.scatter(spans, y_min, edgecolor=colors[j], color='none', marker='v')

            except Exception as e:
                print(f"Failed to plot {chan} for dataset {j}: {e}")
                continue

        ax.set_title(f"{title_prefix}{chan}")
        ax.set_xlabel("Spanwise position (r/R)")
        ax.set_ylabel(chan)
        ax.grid(linestyle =':', color = 'gray')

    handles, labels = axs[0].get_legend_handles_labels()
    add_shared_legend(fig, handles, labels)

def add_shared_legend(fig, handles, labels):
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0.98), ncol=3, fontsize='large')
    fig.tight_layout(rect=[0, 0, 1, 0.85])

def calcPSD(channel, samplingfreq, nperseg, noverlap):
    f, PSD=signal.welch(channel, samplingfreq, nperseg=nperseg, noverlap=noverlap)
    return f, PSD

def plot_psd(ax, df, channel, fs, style, label, label_map=None):
    
    # compute psd
    signal = df[channel].dropna().values
    freqs, psd = calcPSD(signal, fs, nperseg=int(len(signal)/2), noverlap=0.5)

    ax.plot(freqs, psd, label=label, **style, linewidth=1)
    ax.set_xlim([0.0, 5.0])
    ax.set_ylabel(label_map.get(channel, channel) if label_map else channel)
    ax.tick_params(axis='both', labelsize='large')
    ax.grid(linestyle=':', color='gray')
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.get_major_formatter().set_powerlimits((3, 4))
    

def plot_fft(ax, df, channel, fs, style, label, label_map=None):
    
    # clean signal and remove mean
    signal = df[channel].dropna().values
    signal -= np.mean(signal)
    n = len(signal)

    # compute fft
    freqs = np.fft.rfftfreq(n, d=1/fs)
    fft_vals = np.fft.rfft(signal)
    fft_mag = np.abs(fft_vals)
    
    # alternatively compute PSD as square of fft
    # freqs_fft = np.fft.rfftfreq(n, d=1/fs)
    # fft_values = np.fft.rfft(signal - np.mean(signal))
    # psd = (np.abs(fft_values) ** 2) / (n * fs)

    # plot data
    ax.plot(freqs, fft_mag, label=label, **style, linewidth=1)
    ax.set_xlim([0.0, 0.5])
    ax.set_ylabel(label_map.get(channel, channel) if label_map else channel)
    ax.tick_params(axis='both', labelsize='large')
    ax.grid(linestyle=':', color='gray')
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.get_major_formatter().set_powerlimits((3, 4))
    

def plot_tss(ax, df, channel, style, label, label_map=None):
    
    ax.plot(df['Time'], df[channel], label=label, **style, linewidth=1)
    ax.set_ylabel(label_map.get(channel, channel) if label_map else channel)
    ax.grid(linestyle=':', color='gray')
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.get_major_formatter().set_powerlimits((0, 3))
    
