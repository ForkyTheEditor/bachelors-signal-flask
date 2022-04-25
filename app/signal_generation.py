import base64
import io

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure


def generate_signal(sample_rate, frequencies, duration, useCos):
    """
        Generates a sin signal with the given sample rate, frequency and duration.
        Make useCos True to generate a cos signal.
    """

    # Convert to numpy array for more flexibility
    frequencies = np.array(frequencies)


    # Sample rate should be an integer
    sample_rate = int(sample_rate)

    nr_time_samples = int(sample_rate * duration)

    # The time range (if put in pyplot plots with number of seconds)
    time_range = np.arange(0, nr_time_samples) / sample_rate

    # Define variable
    signal = np.zeros((frequencies.shape[0], nr_time_samples))


    for i in range(0, frequencies.shape[0]):
        for f in frequencies:
            if useCos:
                signal[i] += np.cos(2 * np.pi * f * time_range)
            else:
                signal[i] += np.sin(2 * np.pi * f * time_range)


        max = np.repeat(signal[i].max()[np.newaxis], nr_time_samples)
        min = np.repeat(signal[i].min()[np.newaxis], nr_time_samples)
        signal[i] = (2 * (signal[i] - min) / (max - min)) - 1

    return signal, time_range


def create_plot(signal, time):
    # ======= DRAW PLOT ====== #

    fig = Figure(figsize=(10,6))
    ax = fig.subplots()
    ax.plot(time, signal.T)

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
