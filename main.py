from matplotlib import get_backend
import matplotlib.pyplot as plt
import math
import numpy as np

# frequencies = list(range(1, 6))
frequencies = np.arange(1, 6, 0.1)
r = 50          # Given transmission line impedance
res_freq = 3e9  # Given resonance frequency for antenna


def get_load_impedance(freq):
    q = 20         # antenna quality factor
    x_0 = 20       # input reactance

    real_part = r / (1 + complex(2 * q * ((freq/res_freq) - 1)))
    img_part = complex(0, x_0 * (freq/res_freq))

    return real_part + img_part


def get_transformer_input_impedance(load_impedence):

    tao = (load_impedence - r) / (load_impedence + r)
    return (1 + abs(tao)) / (1 - abs(tao))


def get_transformer_impedance(input_impedance):
    return math.sqrt((abs(input_impedance) * r) * r)


def get_swr(impedance):
    return max((impedance / r), (r/impedance))


bandwith = []
res = []

f1 = (0, 10000)
f2 = (0, -1)
for freq in frequencies:
    load_impedance = get_load_impedance(freq * 1000000000)
    input_impeance = get_transformer_input_impedance(load_impedance)
    transformer_impedance = get_transformer_impedance(input_impeance)
    swr = get_swr(transformer_impedance)

    if math.floor(swr) == 2:
        if swr < f1[1] and f1[0]:
            f1 = (freq, swr)
        if swr > f2[1]:
            f2 = (freq, swr)
    print(swr)
    res.append(swr)


def get_bandwith(freq1, freq2):
    return (abs((freq2 - freq1)) / res_freq) * 100


print(get_bandwith(f1[0] * 1000000000, f2[0] * 1000000000))

#             x        y
plt.plot(frequencies, res)
plt.xlabel("Frequency [GHz]")
plt.ylabel("SWR")
plt.title("SWR x Frequency")


plt.show()
