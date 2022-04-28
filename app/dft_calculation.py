import base64
import io

import numpy as np
from matplotlib.figure import Figure


def calculate_dft(signal):
    """
    N = total number of samples;
    n = current sample;
    k = current frequency, where k∈[0,N−1];

    """
    N = len(signal)
    n = np.arange(N)
    k = n.reshape((N, 1))
    e = np.exp(-2j * np.pi * k * n / N)

    DFT = np.dot(e, signal)

    return DFT


def plot_dft(DFT, sample_rate):

    N = len(DFT)
    n = np.arange(N)
    T = N / sample_rate
    frequency = n / T

    # ======= DRAW PLOT ====== #
    fig = Figure(figsize=(10, 6))
    ax = fig.subplots()
    ax.stem(frequency, abs(DFT))

    ax.grid(visible=True)

    ax.set_xlabel('Frequency Domain (Hz)')
    ax.set_ylabel('DFT Amplitude')


    # Save it to a temporary buffer.
    buf = io.BytesIO()


    fig.savefig(buf, format="png")


    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    embedded_image = f"data:image/png;base64,{data}"
    # ======= DRAW PLOT ====== #

    return embedded_image
