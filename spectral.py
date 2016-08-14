from scipy.fftpack import fft
from scipy.io import wavfile

(sample_rate, data) = wavfile.read('output.wav')
samples = data.T[0]

# Sample data from a 0.1-second block in the middle of the file.
window = sample_rate / 10
start = len(samples - window)/2
fragment = samples[start:start + window]
frequencies = map(abs, fft(fragment)[:window/2])

plot_frequencies = True
if plot_frequencies:
    import matplotlib.pyplot as plot
    plot.plot(frequencies)
    plot.show()
