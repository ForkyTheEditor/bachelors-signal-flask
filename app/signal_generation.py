import base64
import io

import numpy as np
from matplotlib.figure import Figure


def generate_signal(sample_rate, frequency, duration, useCos):
    """
        Generates a sin signal with the given sample rate, frequency and duration.
        Make useCos True to generate a cos signal.
    """

    sample_rate = int(sample_rate)

    nr_time_samples = int(sample_rate * duration)
    time_range = np.arange(0, nr_time_samples) / sample_rate * duration

    signal = 0
    if useCos:
        signal = np.cos(2 * np.pi * frequency * time_range)
    else:
        signal = np.sin(2 * np.pi * frequency * time_range)

    return signal, time_range


def create_plot(signal, time):
    # ======= DRAW PLOT ====== #
    fig = Figure()
    ax = fig.subplots()
    ax.plot(time, signal)

    ax.grid(visible=True)

    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')

    # Save it to a temporary buffer.
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    embedded_image = f"data:image/png;base64,{data}"
    # ======= DRAW PLOT ====== #

    return embedded_image
