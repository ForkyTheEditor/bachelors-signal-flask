import base64
import io

import numpy as np
from matplotlib.figure import Figure


def plot_dft(DFT, sample_rate):

    N = DFT.shape[1]
    n = np.arange(N)
    T = N / sample_rate
    frequency = n / T

    DFT = DFT[0]

    # The plot is symmetric from the half point ( Nyquist frequency )
    # => only use one half
    half_point = N // 2
    frequency_half = frequency[:half_point]

    DFT_half = DFT[:half_point]/half_point
    print(DFT_half)
    print(DFT)
    # ======= DRAW PLOT ====== #
    fig = Figure(figsize=(10, 6))
    ax = fig.subplots()


    ax.plot(frequency_half, abs(DFT_half))

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
