from importation import*

class AWGNChannel:
    def __init__(self, snr_db):
        self.snr_db = snr_db

    def add_noise(self, signal):
        snr_linear = 10 ** (self.snr_db / 10)
        noise_std = np.sqrt(1 / (2 * snr_linear))
        noise = noise_std * (np.random.randn(*signal.shape) + 1j * np.random.randn(*signal.shape))
        noisy_signal = signal + noise
        self.plot_signal(noisy_signal)
        return noisy_signal

    def plot_signal(self, signal, title="Signal Bruité (AWGN)"):
        plt.figure(figsize=(6, 6))
        plt.scatter(signal.real, signal.imag, c='r', marker='x')
        plt.title(title)
        plt.xlabel("In-Phase")
        plt.ylabel("Quadrature")
        plt.grid()
        plt.show()

class FadingChannel:
    def transmit(self, signal):
        fading = np.random.uniform(0.5, 1.5, size=signal.shape)
        faded_signal = signal * fading
        self.plot_signal(faded_signal)
        return faded_signal

    def plot_signal(self, signal, title="Signal Transmis (Fading)"):
        plt.figure(figsize=(6, 6))
        plt.scatter(signal.real, signal.imag, c='g', marker='s')
        plt.title(title)
        plt.xlabel("In-Phase")
        plt.ylabel("Quadrature")
        plt.grid()
        plt.show()

        