import numpy as np
from scipy.signal import find_peaks

from app.dft_calculation import calculate_fft, plot_dft


def granular_dft(signal, sample_rate, start_freq, end_freq):
    # Calculate real and imaginary part
    # then calculate magnitude of the vector

    # Calculate the variables
    N = signal.shape[1]
    t = N / sample_rate
    delta_f = 1 / t

    if end_freq > N or end_freq <= start_freq:
        raise Exception("Invalid start and end frequencies!")

    k = np.zeros((1, end_freq - start_freq))

    imaginary_values = np.zeros((1, end_freq - start_freq))
    real_values = np.zeros((1, end_freq - start_freq))

    for i in range(N):
        for j in range(end_freq - start_freq):
            imaginary_part = -signal[i] * np.sin(2 * np.pi * k[j] * i / N)
            real_part = signal[i] * np.cos(2 * np.pi * k[j] * i / N)

            # Sum the imaginary and real parts for the respective spectral line
            imaginary_values[j] += imaginary_part
            real_values[j] += real_part

    amplitudes = [np.sqrt(imaginary_values[i] ^ 2 + real_values[i] ^ 2) * 2/N for i in range(end_freq - start_freq)]
    frequencies = [i * delta_f for i in range(start_freq, end_freq)]

    return zip(frequencies, amplitudes)


def estimate_initial_frequency(signal, start_freq, end_freq):
    # First calculate the DFT of the signal
    dft = granular_dft(signal[2], signal[3], start_freq, end_freq)

    # Only use half
    N = dft.shape[1]
    half_point = N // 2

    dft_half = dft[0][:half_point] / half_point

    # Find the peaks
    peaks = find_peaks(dft_half, height=0.1, prominence=0.15, wlen=5)

    return plot_dft(dft, signal[3], peaks=peaks[0]), peaks[0]


def signal_crop_estimation(signal, chosen_peak):
    pass
