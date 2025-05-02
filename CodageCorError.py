from importation import*

class HammingEncoder:
    def encode(self, bits):
        G = np.array([[1, 1, 0, 1],
                      [1, 0, 1, 1],
                      [1, 0, 0, 0],
                      [0, 1, 1, 1],
                      [0, 1, 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])
        return (np.dot(G, bits) % 2).astype(int)

class BCHEncoder:
    def encode(self, bits):
        return np.concatenate((bits, np.random.randint(0, 2, size=3)))