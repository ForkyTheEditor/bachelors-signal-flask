import base64
import io
import math

import numpy as np
from app import generated_signals_history
from matplotlib.figure import Figure


def generate_signal(sample_rate, frequencies, duration, amplitudes, phases, use_cos=False, normalize=True, save=False):
    """
        Generates a sin signal with the given sample rate, frequency and duration.
        Make useCos True to generate a cos signal.
        Formula for signal generation: y(t)=A*sin(ωt+ϕ), where
        A - amplitude
        ω - angular frequency, and ω = 2πT = 2πf
        ϕ - phase

    """

    # Convert to numpy array for more flexibility
    frequencies = np.array(frequencies)



    # Sample rate should be an integer
    sample_rate = int(sample_rate)

    nr_time_samples = int(sample_rate * duration)

    # Define variable
    signal = np.zeros((1, nr_time_samples))

    t = np.linspace(0, duration, nr_time_samples, endpoint=False)

    # Add all the frequencies together to get the resulting signal
    for i in range(0, frequencies.shape[0]):
        if use_cos:
            signal += amplitudes[i] * np.cos(2 * np.pi * frequencies[i] * t + phases[i])
        else:
            signal += amplitudes[i] * np.sin(2 * np.pi * frequencies[i] * t + phases[i])

        if normalize:
            maxA = np.repeat(signal.max()[np.newaxis], nr_time_samples)
            minA = np.repeat(signal.min()[np.newaxis], nr_time_samples)
            signal = (2 * (signal - minA) / (maxA - minA)) - 1


    if save:

        # Create id so you don't save same signal twice
        signal_id = ""
        for f in frequencies:
            signal_id += str(f)
        for a in amplitudes:
            signal_id += str(a)
        for p in phases:
            signal_id += str(p)
        signal_id += str(duration)
        signal_id += str(sample_rate)

        # Only save if id is unique
        if signal_id not in [i[0] for i in generated_signals_history]:

            # Give the signal a name (TODO: Let the user decide on the name)
            name = "Signal " + str(len(generated_signals_history))

            # Save the signal to the history
            generated_signals_history.append((signal_id, name, signal, sample_rate))


    return signal, t


def create_plot(signal, time):
    """
    Creates a plot of the given signal and returns it as an image.

    """


    # ======= DRAW PLOT ====== #

    # Dynamically resize the plot depending on the size of the signal
    fig_x_size = 8 + int(math.log(len(time), 3))

    fig = Figure(figsize=(fig_x_size, 6))
    ax = fig.subplots()
    ax.plot(time, signal.T)

    ax.grid(visible=True)

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')


    # Save it to a temporary buffer.
    buf = io.BytesIO()


    fig.savefig(buf, format="png")


    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    embedded_image = f"data:image/png;base64,{data}"
    # ======= DRAW PLOT ====== #

    return embedded_image
