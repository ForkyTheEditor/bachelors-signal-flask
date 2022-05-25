import base64
import io

import numpy as np
from matplotlib.figure import Figure
from scipy.signal import find_peaks

from app.dft_calculation import calculate_fft, plot_dft


def granular_dft(signal, sample_rate, start_freq, end_freq):
    # Calculate real and imaginary part
    # then calculate magnitude of the vector

    # Calculate the variables
    N = signal.shape[1]
    t = N / sample_rate
    delta_f = 1 / t

    signal = signal[0]

    if end_freq > N or end_freq <= start_freq:
        raise Exception("Invalid start and end frequencies!")

    # Initialize arrays
    k = [i for i in range(end_freq-start_freq)]
    imaginary_values = [0 for i in range(end_freq-start_freq)]
    real_values = [0 for i in range(end_freq-start_freq)]

    for i in range(N):
        for j in range(end_freq - start_freq):
            imaginary_part = -signal[i] * np.sin(2 * np.pi * k[j] * i / N)
            real_part = signal[i] * np.cos(2 * np.pi * k[j] * i / N)

            # Sum the imaginary and real parts for the respective spectral line
            imaginary_values[j] += imaginary_part
            real_values[j] += real_part


    amplitudes = [np.sqrt(imaginary_values[i] ** 2 + real_values[i] ** 2) for i in range(end_freq - start_freq)]
    frequencies = [i * delta_f for i in range(start_freq, end_freq)]



    return frequencies, amplitudes


def estimate_initial_frequency(signal, start_freq, end_freq):
    # First calculate the DFT of the signal
    dft = granular_dft(signal[2], signal[3], start_freq, end_freq)

    x_dft = np.array(dft[0])
    y_dft = np.array(dft[1])

    # Find the peaks
    peaks = find_peaks(y_dft, height=0.1, prominence=0.15, wlen=5)

    # ======= DRAW PLOT ====== #
    fig = Figure(figsize=(10, 6))
    ax = fig.subplots()

    ax.plot(dft[0], dft[1])

    peaks = peaks[0]


    if peaks is not None:

        # Add the text for each peak
        for index, peak in enumerate(peaks):
            ax.scatter(x_dft[peak], y_dft[peak])

            text = "Peak " + str(index) + " - Freq: " + str(x_dft[peak]) \
                   + " / DFT Amplitude: " + str(round(y_dft[peak], 4))

            ax.annotate(text, (peak - 0.05, y_dft[peak] + 0.01))


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


def signal_crop_estimation(signal, chosen_peak):
    pass
