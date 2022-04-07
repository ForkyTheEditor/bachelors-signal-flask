import numpy as np



def generate_signal(sample_rate, frequency, duration, useCos):
    """
        Generates a sin signal with the given sample rate, frequency and duration.
        Make useCos True to generate a cos signal.
    """
    nr_time_samples = sample_rate * duration
    time_range = np.arange(0, nr_time_samples) / sample_rate

    signal = 0
    if useCos:
        signal = np.cos(2 * np.pi * frequency * time_range)
    else:
        signal = np.sin(2 * np.pi * frequency * time_range)

    return signal
