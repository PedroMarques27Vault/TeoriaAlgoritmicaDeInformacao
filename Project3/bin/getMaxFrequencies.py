import numpy as np
import wave
from scipy import signal
from matplotlib import pyplot as plt
from pydub import AudioSegment


def get_signature_from_audio(filename, output_file):
    raw = wave.open(filename)

    # reads all the frames
    # -1 indicates all or max frames
    (n_channels, samp_width, frame_rate, n_frames, comp_type, comp_name) = raw.getparams()
    _signal = raw.readframes(n_frames * n_channels)
    _signal = np.frombuffer(_signal, dtype="int16")

    stereo_audio = AudioSegment.from_file(filename,  format="wav")

    mono_audios = stereo_audio.split_to_mono()

    left, right = np.fromstring(mono_audios[0]._data, np.int16), np.fromstring(mono_audios[1]._data, np.int16)
    _signal = [(left[i]/2 + right[i]/2) for i in range(len(left))]
    # plt.plot(list(range(n_frames))[:1000], _signal[:1000])
    # plt.show()

    f_rate = raw.getframerate()

    output_data = []
    n_windows_needed = int(len(_signal) / f_rate)
    windows = []

    for i in range(n_windows_needed):
        if i * f_rate + f_rate > len(_signal):
            windows.append((i * f_rate, len(_signal)))
        else:
            windows.append((i*f_rate, i*f_rate+f_rate))

    for i in windows:
        h_x = abs(np.fft.rfft(_signal[i[0]:i[1]]))
        freq_x = abs(np.fft.fftfreq(len(h_x), 1 / f_rate))
        points_per_freq = len(freq_x) / (1 / f_rate)
        target_idx = int(points_per_freq * 4000)
        h_x[target_idx - 1: target_idx + 2] = 0

        max_amplitude = max(h_x)
        indexes = min([i for i in range(len(h_x)) if h_x[i] == max_amplitude])
        freq_x = freq_x[indexes:]
        h_x = h_x[indexes:]
        plt.plot(freq_x, h_x)

        _max, _min = max(h_x), min(h_x)

        abv_index = [i for i in range(1, len(h_x)-1, 2) if h_x[i-1] < h_x[i] and h_x[i] > h_x[i+1] and h_x[i] > _max/2]

        abv_frequencies = [(freq_x[i], h_x[i], i) for i in abv_index]
        output_data.extend(abv_frequencies)
        # plt.show()

    f = open(f"{output_file}", 'w')
    _str = ''.join([str(i) for i in output_data])
    f.write(_str)
    f.close()
    print(f"Generated {filename} Signature")

    return output_file
