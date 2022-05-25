import base64
import io

import numpy as np
from matplotlib.figure import Figure
from scipy.fftpack import fft, fftfreq


def calculate_fft(signal):
    return fft(signal[2])



def plot_dft(DFT, sample_rate, peaks=None):

    N = DFT.shape[1]
    frequencies = fftfreq(N, 1/sample_rate)

    DFT = DFT[0]

    # The plot is symmetric from the half point ( Nyquist frequency )
    # => only use one half
    half_point = N // 2

    DFT_half = DFT[:half_point]/half_point

    # ======= DRAW PLOT ====== #
    fig = Figure(figsize=(10, 6))
    ax = fig.subplots()

    ax.plot(frequencies[:half_point], abs(DFT_half))

    if peaks is not None:
        ax.scatter(frequencies[peaks], abs(DFT_half[peaks]))

        # Add the text for each peak
        for index, peak in enumerate(peaks):

            text = "Peak " + str(index) + " - Freq: " + str(frequencies[peak]) \
                   + " / DFT Amplitude: " + str(round(abs(DFT_half[peak]), 4))

            ax.annotate(text, (peak - 0.05, DFT_half[peak] + 0.01))


    # Show precise grid
    ax.minorticks_on()
    ax.grid(which='major', color='b')
    ax.grid(which='minor', color='g', linestyle='--')

    ax.set_xlabel('Frequency Domain (Hz)')
    ax.set_ylabel('DFT Amplitude')


    # Save it to a temporary buffer.
    buf = io.BytesIO()


    fig.savefig(buf, format="png", bbox_inches="tight")


    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    embedded_image = f"data:image/png;base64,{data}"
    # ======= DRAW PLOT ====== #

    return embedded_image
