from scipy.io import wavfile
import numpy as np
from scipy.signal import resample_poly, bilinear, lfilter
import matplotlib.pyplot as plt
from rtlsdr import RtlSdr

# RTL-SDR setup
sdr = RtlSdr()
sdr.sample_rate = 2.048e6  # Hz
sdr.center_freq = 90.6e6     # Hz
sdr.freq_correction = 60   # PPM
sdr.gain = 'auto'

# Recording
samples = np.array([])
for i in range(100):
    samples = np.append(samples, sdr.read_samples(256*1024))

sdr.close()

# Resample to 250 kHz
x = resample_poly(samples, 5, 48)

# Read in signal
sample_rate = 250e3
center_freq = 774.41875e6

# Demodulation (Works)
# x = np.diff(np.unwrap(np.angle(x)))

# P25 demodulation (In-Testing)
x = x[1:] * np.conj(x[:-1])
x = np.angle(x)

# De-emphasis filter, H(s) = 1/(RC*s + 1), implemented as IIR via bilinear transform
bz, az = bilinear(1, [75e-6, 1], fs=sample_rate)
x = lfilter(bz, az, x)

# decimate by 6 to get mono audio
x = x[::6]
sample_rate_audio = sample_rate/6

# normalize volume so its between -1 and +1
x /= np.max(np.abs(x))

# some machines want int16s
x *= 32767
x = x.astype(np.int16)

# Save to wav file, you can open this in Audacity for example
wavfile.write('fm.wav', int(sample_rate_audio), x)
