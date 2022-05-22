from scipy.signal import find_peaks

from app.dft_calculation import calculate_dft, plot_dft


def estimate_frequency(signal):
    # First calculate the DFT of the signal
    dft = calculate_dft(signal)

    # Only use half
    N = dft.shape[1]
    half_point = N // 2

    dft_half = dft[0][:half_point] / half_point


    # Find the peaks
    peaks = find_peaks(dft_half, height=0.1, prominence=0.2)


    return plot_dft(dft, signal[3], peaks=peaks[0])
