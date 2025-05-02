from importation import *


class BPSK:
    def modulate(self, bits):
        return 2 * bits - 1

    def demodulate(self, signal):
        return (signal >= 0).astype(int)

    def plot_signal(self, signal, title="BPSK Signal"):
        plt.figure(figsize=(8, 4))
        plt.stem(signal, linefmt='b-', markerfmt='bo', basefmt='r-')
        plt.title(title)
        plt.xlabel("Temps")
        plt.ylabel("Amplitude")
        plt.grid()
        plt.show()

class QPSK:
    def modulate(self, bits):
        mapping = {
            (0,0): 1 + 1j, (0,1): -1 + 1j,
            (1,0): 1 - 1j, (1,1): -1 - 1j
        }
        symbols = np.array([mapping[tuple(bits[i:i+2])] for i in range(0, len(bits), 2)])
        return symbols

    def demodulate(self, signal):
        bits = []
        for s in signal:
            bits.extend([int(s.real > 0), int(s.imag > 0)])
        return np.array(bits)

    def plot_signal(self, signal, title="QPSK Signal"):
        plt.figure(figsize=(6, 6))
        plt.scatter(signal.real, signal.imag, c='b', marker='o')
        plt.title(title)
        plt.xlabel("In-Phase")
        plt.ylabel("Quadrature")
        plt.grid()
        plt.show()

class PSK8:
    def modulate(self, bits):
        bits = bits[:len(bits) - len(bits) % 3]  # Assure un multiple de 3
        symbols = []
        for i in range(0, len(bits), 3):
            index = bits[i] * 4 + bits[i+1] * 2 + bits[i+2]
            angle = 2 * np.pi * index / 8
            symbols.append(np.exp(1j * angle))
        return np.array(symbols)

    def demodulate(self, signal):
        bits = []
        for s in signal:
            angle = np.angle(s)
            index = int(np.round((angle % (2 * np.pi)) / (2 * np.pi / 8))) % 8
            bits.extend([int(index >> 2) & 1, int(index >> 1) & 1, int(index) & 1])
        return np.array(bits)

    def plot_signal(self, signal, title="8-PSK Signal"):
        plt.figure(figsize=(6, 6))
        plt.scatter(np.real(signal), np.imag(signal), c='purple', marker='o')
        plt.title(title)
        plt.xlabel("In-Phase")
        plt.ylabel("Quadrature")
        plt.grid()
        plt.axis('equal')
        plt.show()

class QAM16:
    def modulate(self, bits):
        bits = bits[:len(bits) - len(bits) % 4]  # Assure un multiple de 4
        mapping = {
            (0, 0): -3, (0, 1): -1, (1, 1): 1, (1, 0): 3
        }
        symbols = []
        for i in range(0, len(bits), 4):
            i_part = mapping[(bits[i], bits[i+1])]
            q_part = mapping[(bits[i+2], bits[i+3])]
            symbols.append(complex(i_part, q_part))
        return np.array(symbols)

    def demodulate(self, signal):
        def nearest_level(val):
            if val < -2: return (0, 0)
            elif val < 0: return (0, 1)
            elif val < 2: return (1, 1)
            else: return (1, 0)

        bits = []
        for s in signal:
            i_bits = nearest_level(s.real)
            q_bits = nearest_level(s.imag)
            bits.extend(i_bits + q_bits)
        return np.array(bits)

    def plot_signal(self, signal, title="16-QAM Signal"):
        plt.figure(figsize=(6, 6))
        plt.scatter(signal.real, signal.imag, c='green', marker='o')
        plt.title(title)
        plt.xlabel("In-Phase")
        plt.ylabel("Quadrature")
        plt.grid()
        plt.axis('equal')
        plt.show()

