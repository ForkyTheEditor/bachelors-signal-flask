import base64
import io
from math import floor, ceil

import numpy as np
from matplotlib.figure import Figure
from scipy.signal import find_peaks


def granular_dft(signal, sample_rate, start_freq, end_freq):

    # Calculate real and imaginary part
    # then calculate magnitude of the vector

    # Calculate the variables
    N = signal.shape[0]
    t = N / sample_rate
    delta_f = 1 / t

    if end_freq > N or end_freq <= start_freq:
        raise Exception("Invalid start and end frequencies!")

    # Initialize arrays
    k = [i for i in range(end_freq-start_freq)]
    imaginary_values = [0 for _ in range(end_freq - start_freq)]
    real_values = [0 for _ in range(end_freq-start_freq)]

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


def estimate_initial_frequency(signal_object, start_freq, end_freq):
    # First calculate the DFT of the signal
    dft = granular_dft(signal_object[2][0], signal_object[3], start_freq, end_freq)

    x_dft = np.array(dft[0])
    y_dft = np.array(dft[1])

    # Find the peaks
    peaks = find_peaks(y_dft, height=0.1, prominence=0.15, wlen=5)[0]

    # ======= DRAW PLOT ====== #
    fig = Figure(figsize=(10, 6))
    ax = fig.subplots()

    ax.plot(dft[0], dft[1])

    if peaks is not None:

        # Add the text for each peak
        for index, peak in enumerate(peaks):
            ax.scatter(x_dft[peak], y_dft[peak])

            text = "Peak " + str(index) + " - Freq: " + str(round(x_dft[peak], 3)) \
                   + " / DFT Amplitude: " + str(round(y_dft[peak], 3))

            ax.annotate(text, (peak - 0.05, y_dft[peak] - 0.01))


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
    return embedded_image, [(x_dft[i], y_dft[i]) for i in peaks]


def signal_crop_estimation(signal, sample_rate, chosen_peak):


    # Calculate the DFT in a small range around the peak
    start_frequency = floor(chosen_peak[0]) - 4
    end_frequency = ceil(chosen_peak[0]) + 4


    N = signal.shape[0]
    ts = N / sample_rate
    frequency = chosen_peak[0]
    period = 1/frequency

    # The time (in seconds) the signal will have when the algorithm has finished running
    final_time = ts - 1.9 * period

    # The time (in nr of samples) the signal will blah blah
    final_nr_samples = final_time * sample_rate

    # The period in nr of samples
    period_nr_sample = int(period * sample_rate)


    peak_curve_1 = []
    peak_curve_2 = []
    peak_curve_3 = []

    # Find the initial whole number of cycles
    last_whole_nr_cycles = floor(frequency * (signal.shape[0] / sample_rate))


    unseparated_peak_curve = []

    # Repetitively crop 2 samples from the signal until t = ts - 1.9*period, where ts is the original
    # signal length
    while signal.shape[0] > final_nr_samples:

        # Crop two samples
        signal = signal[:-2]

        # Re-run the algorithm
        dft = granular_dft(signal, sample_rate, start_frequency, end_frequency)

        x_dft = np.array(dft[0])
        y_dft = np.array(dft[1])

        new_peak_index = find_peaks(y_dft, height=0.1, prominence=0.15, wlen=5)[0]
        new_peak = (x_dft[new_peak_index][0], y_dft[new_peak_index][0])

        nr_of_whole_cycles_left = floor(frequency * (signal.shape[0] / sample_rate))
        unseparated_peak_curve.append(new_peak)

        if last_whole_nr_cycles > nr_of_whole_cycles_left:
            last_whole_nr_cycles = nr_of_whole_cycles_left


    threshold = 0.5
    x_whole_curve, _ = zip(*unseparated_peak_curve)
    discontinuities = np.where(abs(np.diff(x_whole_curve)) > threshold)[0] + 1


    peak_curve_1 = unseparated_peak_curve[:discontinuities[0]]
    peak_curve_2 = unseparated_peak_curve[discontinuities[0]:discontinuities[1]]
    peak_curve_3 = unseparated_peak_curve[discontinuities[1]:]



    # ======= DRAW PLOT ====== #
    fig = Figure(figsize=(10, 6))
    ax = fig.subplots()
    if len(peak_curve_1) > 0:
        x_1, y_1 = zip(*peak_curve_1)
        ax.scatter(x_1, y_1, color='red', label='Cycle ' + str(last_whole_nr_cycles + 2))

    x_2, y_2 = zip(*peak_curve_2)

    ax.scatter(x_2, y_2, color='black', label='Cycle ' + str(last_whole_nr_cycles + 1))

    if len(peak_curve_3) > 0:
        x_3, y_3 = zip(*peak_curve_3)
        ax.scatter(x_3, y_3, color='purple', label='Cycle ' + str(last_whole_nr_cycles))



    ax.legend()

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
