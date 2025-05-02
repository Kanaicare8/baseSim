# from importation import *
# from CodageCorError import *
# from CanalDeTransmition import *
# from TypeOfModulation import *
# import tkinter as tk
# from tkinter import messagebox
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import csv
# from datetime import datetime


# class SimulatorCore:
#     def __init__(self, modulation_type="BPSK", snr_db=10, channel_type="AWGN", coder_type="HAMMING"):
#         self.snr_db = snr_db
#         self.modulation_type = modulation_type.upper()
#         self.channel_type = channel_type.upper()
#         self.coder_type = coder_type.upper()

#         # Canal
#         if self.channel_type == "AWGN":
#             self.channel = AWGNChannel(snr_db)
#         elif self.channel_type == "FADING":
#             self.channel = FadingChannel()
#         else:
#             raise ValueError("Type de canal non supporté")

#         # Codage
#         if self.coder_type == "HAMMING":
#             self.encoder = HammingEncoder()
#         elif self.coder_type == "BCH":
#             self.encoder = BCHEncoder()
#         else:
#             raise ValueError("Type de codage non supporté")

#         # Modulation
#         if self.modulation_type == "BPSK":
#             self.modulator = BPSK()
#         elif self.modulation_type == "QPSK":
#             self.modulator = QPSK()
#         elif self.modulation_type == "8PSK":
#             self.modulator = PSK8()
#         elif self.modulation_type == "16QAM":
#             self.modulator = QAM16()
#         else:
#             raise ValueError("Modulation non supportée")

#     def pad_bits(self, bits, block_size):
#         remainder = len(bits) % block_size
#         if remainder != 0:
#             padding = block_size - remainder
#             bits = np.concatenate([bits, np.zeros(padding, dtype=int)])
#         return bits

#     def run(self, bits):
#         block_size = 4 if self.coder_type == "HAMMING" else 7
#         bits = self.pad_bits(bits, block_size)

#         encoded_bits = self.encoder.encode(bits)
#         modulated_signal = self.modulator.modulate(encoded_bits)

#         if self.channel_type == "AWGN":
#             received_signal = self.channel.add_noise(modulated_signal)
#         else:
#             received_signal = self.channel.transmit(modulated_signal)

#         demodulated_bits = self.modulator.demodulate(received_signal)
#         return {
#             "transmitted_bits": bits,
#             "modulated_signal": modulated_signal,
#             "received_signal": received_signal,
#             "demodulated_bits": demodulated_bits
#         }

# class SimulationGUI:
#     def __init__(self):
#         self.root = tk.Tk()
#         self.root.title("Simulation Transmission Numérique")

#         self.setup_widgets()
#         self.root.mainloop()

#     def setup_widgets(self):
#         # Entrées utilisateur
#         input_frame = tk.Frame(self.root)
#         input_frame.pack(padx=10, pady=5)

#         self.entry_bits = self.add_labeled_entry(input_frame, "Bits (ex: 1010):", 0)
#         self.entry_modulation = self.add_labeled_entry(input_frame, "Modulation:", 1, "BPSK")
#         self.entry_channel = self.add_labeled_entry(input_frame, "Canal (AWGN/FADING):", 2, "AWGN")
#         self.entry_coder = self.add_labeled_entry(input_frame, "Codage (HAMMING/BCH):", 3, "HAMMING")
#         self.entry_snr = self.add_labeled_entry(input_frame, "SNR (dB):", 4, "10")

#         self.show_tx_bits = tk.IntVar(value=1)
#         self.show_modulated = tk.IntVar(value=1)
#         self.show_received = tk.IntVar(value=1)
#         self.show_rx_bits = tk.IntVar(value=1)

#         check_frame = tk.Frame(self.root)
#         check_frame.pack()

#         tk.Checkbutton(check_frame, text="Bits transmis", variable=self.show_tx_bits).pack(side=tk.LEFT)
#         tk.Checkbutton(check_frame, text="Signal modulé", variable=self.show_modulated).pack(side=tk.LEFT)
#         tk.Checkbutton(check_frame, text="Signal reçu", variable=self.show_received).pack(side=tk.LEFT)
#         tk.Checkbutton(check_frame, text="Bits démodulés", variable=self.show_rx_bits).pack(side=tk.LEFT)

#         # Zone d'affichage graphique
#         self.fig, self.ax = plt.subplots(figsize=(6, 3))
#         self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
#         self.canvas.get_tk_widget().pack()
    
#         # Résultats et boutons
#         result_frame = tk.Frame(self.root)
#         result_frame.pack(pady=5)

#         self.label_ber = tk.Label(result_frame, text="BER :")
#         self.label_ber.pack()

#         self.text_logs = tk.Text(result_frame, height=6, width=70)
#         self.text_logs.pack()
#         self.bits_frame = tk.Frame(self.root)
#         self.bits_frame.pack(pady=10)


#         button_frame = tk.Frame(self.root)
#         button_frame.pack(pady=5)


#         tk.Button(button_frame, text="Simuler", command=self.start_simulation).pack(side=tk.LEFT, padx=5)
#         tk.Button(button_frame, text="Exporter les courbes", command=self.export_graphs).pack(side=tk.LEFT, padx=5)

#         tk.Button(button_frame, text="Effacer les logs", command=self.clear_logs).pack(side=tk.LEFT, padx=5)
#         tk.Button(button_frame, text="Exporter le graphique", command=self.export_graph).pack(side=tk.LEFT, padx=5)

#     def add_labeled_entry(self, parent, label, row, default=""):
#         tk.Label(parent, text=label).grid(row=row, column=0, sticky="w")
#         entry = tk.Entry(parent)
#         entry.grid(row=row, column=1)
#         entry.insert(0, default)
#         return entry

#     def clear_logs(self):
#         self.text_logs.delete(1.0, tk.END)
    
#     def plot_bits(self, transmitted_bits, received_bits):
#     # Nettoyer les anciens graphiques
#         for widget in self.bits_frame.winfo_children():
#             widget.destroy()

#         fig = Figure(figsize=(7, 2.5), dpi=100)
#         ax1 = fig.add_subplot(211)
#         ax2 = fig.add_subplot(212)

#         # Bits transmis
#         ax1.bar(range(len(transmitted_bits)), transmitted_bits, color='skyblue')
#         ax1.set_title("Bits Transmis")
#         ax1.set_ylim(0, 1.2)

#         # Bits démodulés
#         ax2.bar(range(len(received_bits)), received_bits, color='lightcoral')
#         ax2.set_title("Bits Démodulés")
#         ax2.set_ylim(0, 1.2)

#         fig.tight_layout()

#         canvas = FigureCanvasTkAgg(fig, master=self.bits_frame)
#         canvas.draw()
#         canvas.get_tk_widget().pack()


#     def export_graph(self):
#         self.fig.savefig("graphique_simulation.png")
#         messagebox.showinfo("Export", "Graphique exporté en tant que graphique_simulation.png")

#     def start_simulation(self):
#         try:
#             bits_str = self.entry_bits.get().strip()
#             bits = np.array([int(b) for b in bits_str if b in '01'])
#             modulation = self.entry_modulation.get().upper()
#             channel = self.entry_channel.get().upper()
#             coder = self.entry_coder.get().upper()
#             snr_db = float(self.entry_snr.get())
#         except Exception as e:
#             messagebox.showerror("Erreur", str(e))
#             return

#         simulator = SimulatorCore(modulation, snr_db, channel, coder)
#         results = simulator.run(bits)

#         tx_bits = results["transmitted_bits"]
#         mod_signal = results["modulated_signal"]
#         rx_signal = results["received_signal"]
#         rx_bits = results["demodulated_bits"]


#         ber = np.mean(tx_bits[:len(rx_bits)] != rx_bits[:len(tx_bits)])
#         self.label_ber.config(text=f"BER : {ber:.4f}")

#         # Logs textuels
#         self.text_logs.insert(tk.END, f"Bits transmis : {''.join(map(str, tx_bits))}\n")
#         self.text_logs.insert(tk.END, f"Bits démodulés : {''.join(map(str, rx_bits))}\n")
#         self.text_logs.insert(tk.END, f"BER : {ber:.4f}\n\n")

#         # Affichage graphique
#         self.ax.clear()
#         x_tx = np.arange(len(tx_bits))
#         x_rx = np.arange(len(rx_bits))

#         if self.show_tx_bits.get():
#             self.ax.step(x_tx, tx_bits, where='mid', label="Bits transmis")
#         if self.show_modulated.get():
#             self.ax.plot(mod_signal[:100], label="Signal modulé", alpha=0.7)
#         if self.show_received.get():
#             self.ax.plot(rx_signal[:100], label="Signal reçu", alpha=0.7)
#         if self.show_rx_bits.get():
#             self.ax.step(x_rx, rx_bits, where='mid', label="Bits démodulés", linestyle='--')

#         self.ax.legend()
#         self.ax.set_title("Visualisation des signaux")
#         self.ax.set_xlabel("Échantillons")
#         self.ax.set_ylabel("Amplitude / Bit")
#         self.ax.grid(True)
#         self.canvas.draw()
#         self.plot_bits(bits.tolist(), received_bits.tolist())

#     def export_graphs(self):
#         export_dir = "exports"
#         os.makedirs(export_dir, exist_ok=True)
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
#         for i, fig in enumerate(plt.get_fignums()):
#             fig_obj = plt.figure(fig)
#             fig_obj.savefig(f"{export_dir}/graph_{i+1}_{timestamp}.png")
        
#         messagebox.showinfo("Export", f"Courbes exportées dans le dossier '{export_dir}/'.")



from importation import *
from TypeOfModulation import*
from CanalDeTransmition import *
from CodageCorError import *


# ----- Classe SimulatorCore -----
class SimulatorCore:
    def __init__(self, modulation_type="BPSK", snr_db=10, channel_type="AWGN", coder_type="HAMMING"):
        self.snr_db = snr_db
        self.modulation_type = modulation_type.upper()
        self.channel_type = channel_type.upper()
        self.coder_type = coder_type.upper()
        
        # Canal
        if self.channel_type == "AWGN":
            self.channel = AWGNChannel(snr_db)
        elif self.channel_type == "FADING":
            self.channel = FadingChannel()
        else:
            raise ValueError("Type de canal non supporté")
        
        # Codage
        if self.coder_type == "HAMMING":
            self.encoder = HammingEncoder()  # Assurez-vous que cet encodeur gère la taille de bloc souhaitée
        elif self.coder_type == "BCH":
            self.encoder = BCHEncoder()
        else:
            raise ValueError("Type de codage non supporté")
        
        # Modulation
        if self.modulation_type == "BPSK":
            self.modulator = BPSK()
        elif self.modulation_type == "QPSK":
            self.modulator = QPSK()
        elif self.modulation_type == "8PSK":
            self.modulator = PSK8()
        elif self.modulation_type == "16QAM":
            self.modulator = QAM16()
        else:
            raise ValueError("Modulation non supportée")
    
    def pad_bits(self, bits, block_size):
        remainder = len(bits) % block_size
        if remainder != 0:
            padding = block_size - remainder
            print(f"Ajout de {padding} zéro(s) pour compléter le bloc.")
            bits = np.concatenate([bits, np.zeros(padding, dtype=int)])
        return bits
    
    def run(self, bits, block_size=None):
        # Si aucun block_size n'est spécifié, on utilise 4 pour HAMMING, 7 pour BCH
        if block_size is None:
            block_size = 4 if self.coder_type == "HAMMING" else 7
        bits = self.pad_bits(bits, block_size)
        encoded_bits = self.encoder.encode(bits)
        modulated_signal = self.modulator.modulate(encoded_bits)
        
        if self.channel_type == "AWGN":
            received_signal = self.channel.add_noise(modulated_signal)
        else:
            received_signal = self.channel.transmit(modulated_signal)
        
        demodulated_bits = self.modulator.demodulate(received_signal)
        return {
            "transmitted_bits": bits,
            "encoded_bits": encoded_bits,
            "modulated_signal": modulated_signal,
            "received_signal": received_signal,
            "demodulated_bits": demodulated_bits
        }

# ----- Interface Graphique Tkinter avec thème sombre, validation, et scroll horizontal -----
class SimulationGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Plateforme de Simulation code en bande de base")
        self.root.geometry("1200x800")
        
        # --- Thème sombre personnalisé ---
        style = ttk.Style()
        style.theme_use("clam")  # Plus personnalisable que 'vista'
        
        # Couleurs de base
        background = "#2E3F4F"  # bleu foncé
        foreground = "#FFFFFF"  # texte blanc
        accent = "#4CAF50"      # vert pour les boutons ou la progression
        highlight = "#607D8B"   # gris bleuté
        
        # Appliquer le style général
        self.root.configure(bg=background)
        style.configure("TLabel", background=background, foreground=foreground, font=("Arial", 10))
        style.configure("TButton", background=accent, foreground="white", font=("Arial", 10))
        style.map("TButton", background=[("active", "#45a049")])
        style.configure("TEntry", fieldbackground="white", foreground="black", font=("Arial", 10))
        style.configure("TFrame", background=background)
        style.configure("TLabelframe", background=background, foreground=foreground)
        style.configure("TLabelframe.Label", background=background, foreground=foreground)
        style.configure("TCheckbutton", background=background, foreground=foreground)
        style.configure("TCombobox", fieldbackground="white", background="white", foreground="black")
        
        # --- Barre de progression personnalisée ---
        style.configure("Custom.Horizontal.TProgressbar",
                        troughcolor="#E0E0E0",
                        background=accent,
                        thickness=20)
        
        # --- FRAME SCROLLABLE (vertical et horizontal) ---
        container = ttk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(container, background=background, highlightthickness=0)
        v_scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        h_scrollbar = ttk.Scrollbar(container, orient="horizontal", command=canvas.xview)
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        canvas.pack(side="left", fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
        self.setup_widgets()
        self.root.mainloop()
    
    def setup_widgets(self):
        # --- Zone d'entrée ---
        input_frame = ttk.LabelFrame(self.scrollable_frame, text="Paramètres d'entrée", padding=10)
        input_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        ttk.Label(input_frame, text="Bits (ex: 1010):").grid(row=0, column=0, sticky="w")
        self.entry_bits = ttk.Entry(input_frame, width=50)
        self.entry_bits.grid(row=0, column=1, columnspan=2, padx=5)
        ttk.Button(input_frame, text="Charger fichier", command=self.load_file).grid(row=0, column=3, padx=5)
        
        ttk.Label(input_frame, text="Modulation:").grid(row=1, column=0, sticky="w")
        self.combo_mod = ttk.Combobox(input_frame, values=["BPSK", "QPSK", "8PSK", "16QAM"], state="readonly", width=15)
        self.combo_mod.set("BPSK")
        self.combo_mod.grid(row=1, column=1, sticky="w", padx=5)
        
        ttk.Label(input_frame, text="Canal:").grid(row=2, column=0, sticky="w")
        self.combo_channel = ttk.Combobox(input_frame, values=["AWGN", "FADING"], state="readonly", width=15)
        self.combo_channel.set("AWGN")
        self.combo_channel.grid(row=2, column=1, sticky="w", padx=5)
        
        ttk.Label(input_frame, text="Codage:").grid(row=3, column=0, sticky="w")
        self.combo_code = ttk.Combobox(input_frame, values=["HAMMING", "BCH"], state="readonly", width=15)
        self.combo_code.set("HAMMING")
        self.combo_code.grid(row=3, column=1, sticky="w", padx=5)
        
        ttk.Label(input_frame, text="SNR (dB):").grid(row=4, column=0, sticky="w")
        self.entry_snr = ttk.Entry(input_frame, width=10)
        self.entry_snr.insert(0, "10")
        self.entry_snr.grid(row=4, column=1, sticky="w", padx=5)
        
        # --- Zone de taille de bloc (pour Hamming) ---
        block_frame = ttk.LabelFrame(self.scrollable_frame, text="Taille de bloc (HAMMING)", padding=10)
        block_frame.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        ttk.Label(block_frame, text="Taille de bloc:").grid(row=0, column=0, sticky="w")
        self.entry_block_size = ttk.Entry(block_frame, width=10)
        self.entry_block_size.insert(0, "4")  # Par défaut pour Hamming(7,4) : 4 bits d'info
        self.entry_block_size.grid(row=0, column=1, padx=5)
        
        # --- Zone de validation des bits ---
        message_frame = ttk.Frame(self.scrollable_frame, padding=10)
        message_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self.message_label = ttk.Label(message_frame, text="", foreground="red", background="#2E3F4F")
        self.message_label.pack(side="left", padx=5)
        self.validate_button = ttk.Button(message_frame, text="Valider les bits", command=self.validate_bits)
        self.validate_button.pack(side="left", padx=5)
        self.entry_bits.bind("<Key>", lambda event: self.message_label.config(text=""))
        
        # --- Options d'affichage ---
        options_frame = ttk.LabelFrame(self.scrollable_frame, text="Options d'affichage", padding=10)
        options_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        
        self.show_tx_bits = tk.BooleanVar(value=True)
        self.show_modulated = tk.BooleanVar(value=True)
        self.show_received = tk.BooleanVar(value=True)
        self.show_rx_bits = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(options_frame, text="Afficher Bits transmis", variable=self.show_tx_bits).grid(row=0, column=0, sticky="w")
        ttk.Checkbutton(options_frame, text="Afficher Signal modulé", variable=self.show_modulated).grid(row=0, column=1, sticky="w")
        ttk.Checkbutton(options_frame, text="Afficher Signal reçu", variable=self.show_received).grid(row=0, column=2, sticky="w")
        ttk.Checkbutton(options_frame, text="Afficher Bits démodulés", variable=self.show_rx_bits).grid(row=0, column=3, sticky="w")
        
        # --- Boutons d'action ---
        action_frame = ttk.Frame(self.scrollable_frame, padding=10)
        action_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
        
        ttk.Button(action_frame, text="Simuler", command=self.start_simulation).grid(row=0, column=0, padx=5)
        ttk.Button(action_frame, text="Effacer logs", command=self.clear_logs).grid(row=0, column=1, padx=5)
        ttk.Button(action_frame, text="Exporter courbes", command=self.export_graphs).grid(row=0, column=2, padx=5)
        ttk.Button(action_frame, text="Exporter graphique", command=self.export_graph).grid(row=0, column=3, padx=5)
        
        # --- Barre de progression ---
        progress_frame = ttk.Frame(self.scrollable_frame, padding=10)
        progress_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=10)
        self.progress = ttk.Progressbar(progress_frame, mode="determinate", length=400, style="Custom.Horizontal.TProgressbar")
        self.progress.grid(row=0, column=0, pady=10)
        
        # --- Zone des logs ---
        logs_frame = ttk.LabelFrame(self.scrollable_frame, text="Logs", padding=10)
        logs_frame.grid(row=5, column=0, sticky="ew", padx=10, pady=5)
        self.text_logs = tk.Text(logs_frame, height=8, width=100)
        self.text_logs.pack(fill="both", expand=True)
        
        # --- Graphique principal (signal modulé / reçu) ---
        self.graph_frame = ttk.LabelFrame(self.scrollable_frame, text="Signal modulé / reçu", padding=10)
        self.graph_frame.grid(row=6, column=0, sticky="nsew", padx=10, pady=5)
        self.fig_main = Figure(figsize=(10, 2.5), dpi=100)
        self.ax_main = self.fig_main.add_subplot(111)
        self.canvas_main = FigureCanvasTkAgg(self.fig_main, master=self.graph_frame)
        self.canvas_main.get_tk_widget().pack(fill="both", expand=True)
        
        # --- Graphique des bits ---
        self.bits_frame = ttk.LabelFrame(self.scrollable_frame, text="Bits Transmis / Démodulés", padding=10)
        self.bits_frame.grid(row=7, column=0, sticky="nsew", padx=10, pady=5)
    
    def load_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Fichier Binaire", "*.bin *.txt")])
        if filepath:
            try:
                with open(filepath, 'r') as f:
                    content = f.read().strip()
                    valid_bits = ''.join([c for c in content if c in '01'])
                    if not valid_bits:
                        messagebox.showerror("Erreur", "Aucun bit valide trouvé.")
                        return
                    self.entry_bits.delete(0, tk.END)
                    self.entry_bits.insert(0, valid_bits)
                    self.log_message(f"Fichier chargé : {filepath}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur de lecture : {e}")
    
    def validate_bits(self):
        input_bits = self.entry_bits.get().strip()
        if not input_bits:
            self.display_message("Veuillez saisir les bits avant de valider.", "red")
            return False
        if not all(bit in ['0', '1'] for bit in input_bits):
            self.display_message("Entrée invalide : seuls les bits 0 et 1 sont autorisés.", "red")
            return False
        # Vérifier la taille par rapport à la taille de bloc (pour HAMMING)
        if self.combo_code.get() == "HAMMING":
            try:
                block_size = int(self.entry_block_size.get())
            except ValueError:
                self.display_message("La taille de bloc doit être un nombre.", "red")
                return False
            if len(input_bits) % block_size != 0:
                padding = block_size - (len(input_bits) % block_size)
                self.display_message(f"Attention : {padding} zéro(s) seront ajoutés pour compléter le bloc.", "orange")
            else:
                self.display_message("Bits valides. Vous pouvez lancer la simulation.", "green")
        else:
            self.display_message("Bits valides. Vous pouvez lancer la simulation.", "green")
        return True
    
    def display_message(self, message, color="red"):
        self.message_label.config(text=message, foreground=color)
        self.log_message(f"[MESSAGE] {message}")
    
    def start_simulation(self):
        if not self.validate_bits():
            return
        
        try:
            self.progress["value"] = 0
            self.root.update_idletasks()
            
            bits_str = self.entry_bits.get().strip()
            bits = np.array([int(b) for b in bits_str if b in '01'])
            modulation = self.combo_mod.get()
            channel = self.combo_channel.get()
            coder = self.combo_code.get()
            snr_db = float(self.entry_snr.get())
            
            # Déterminer la taille de bloc pour HAMMING, sinon utiliser 7 pour BCH
            if coder == "HAMMING":
                block_size = int(self.entry_block_size.get())
            else:
                block_size = 7
        except Exception as e:
            self.log_message(f"Erreur: {e}")
            return
        
        self.progress["value"] = 10
        self.root.update_idletasks()
        
        # Exécution de la simulation
        try:
            simulator = SimulatorCore(modulation, snr_db, channel, coder)
            results = simulator.run(bits, block_size)
        except Exception as e:
            self.log_message(f"Erreur lors de la simulation: {e}")
            return
        
        self.progress["value"] = 60
        self.root.update_idletasks()
        
        tx_bits = results["transmitted_bits"]
        mod_signal = results["modulated_signal"]
        rx_signal = results["received_signal"]
        rx_bits = results["demodulated_bits"]
        
        ber = np.mean(tx_bits[:len(rx_bits)] != rx_bits[:len(tx_bits)])
        self.log_message(f"Bits transmis : {''.join(map(str, tx_bits))}")
        self.log_message(f"Bits démodulés : {''.join(map(str, rx_bits))}")
        self.log_message(f"BER : {ber:.4f}\n")
        
        self.ax_main.clear()
        x = np.arange(len(mod_signal))
        if self.show_modulated.get():
            self.ax_main.plot(x, np.real(mod_signal), label="Signal modulé", alpha=0.7)
        if self.show_received.get():
            self.ax_main.plot(x, np.real(rx_signal), label="Signal reçu", alpha=0.7)
        self.ax_main.legend()
        self.ax_main.set_title("Visualisation du signal (partie réelle)")
        self.ax_main.set_xlabel("Échantillons")
        self.ax_main.set_ylabel("Amplitude")
        self.ax_main.grid(True)
        self.canvas_main.draw()
        
        self.plot_bits(tx_bits.tolist(), rx_bits.tolist())
        self.save_results_to_csv(modulation, channel, coder, snr_db, tx_bits, rx_bits, ber)
        
        self.progress["value"] = 100
        self.root.update_idletasks()
    
    def plot_bits(self, transmitted_bits, received_bits):
        for widget in self.bits_frame.winfo_children():
            widget.destroy()
        
        fig_bits = Figure(figsize=(7, 2.5), dpi=100)
        ax1 = fig_bits.add_subplot(121)
        ax2 = fig_bits.add_subplot(122)
        
        colors_tx = ['green' if b == 1 else 'red' for b in transmitted_bits]
        ax1.bar(range(len(transmitted_bits)), transmitted_bits, color=colors_tx)
        ax1.set_title(f"Bits Transmis ({len(transmitted_bits)} bits)")
        ax1.set_ylim(0, 1.2)
        ax1.set_xticks(range(len(transmitted_bits)))
        ax1.set_yticks([0, 1])
        ax1.grid(True, linestyle='--', alpha=0.5)
        for i, b in enumerate(transmitted_bits):
            ax1.text(i, b + 0.05, str(b), ha='center', fontsize=8)
        
        colors_rx = ['green' if b == 1 else 'red' for b in received_bits]
        ax2.bar(range(len(received_bits)), received_bits, color=colors_rx)
        ax2.set_title(f"Bits Démodulés ({len(received_bits)} bits)")
        ax2.set_ylim(0, 1.2)
        ax2.set_xticks(range(len(received_bits)))
        ax2.set_yticks([0, 1])
        ax2.grid(True, linestyle='--', alpha=0.5)
        for i, b in enumerate(received_bits):
            ax2.text(i, b + 0.05, str(b), ha='center', fontsize=8)
        
        fig_bits.tight_layout()
        bits_canvas = FigureCanvasTkAgg(fig_bits, master=self.bits_frame)
        bits_canvas.draw()
        bits_canvas.get_tk_widget().pack()
    
    def export_graphs(self):
        export_dir = "exports"
        os.makedirs(export_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        for i, fig_num in enumerate(plt.get_fignums()):
            fig_obj = plt.figure(fig_num)
            fig_obj.savefig(f"{export_dir}/graph_{i+1}_{timestamp}.png")
        messagebox.showinfo("Export", f"Courbes exportées dans le dossier '{export_dir}/'.")
    
    def export_graph(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.fig_main.savefig(file_path)
            messagebox.showinfo("Export", f"Graphique exporté sous {file_path}")
    
    def clear_logs(self):
        self.text_logs.delete(1.0, tk.END)
    
    def log_message(self, message):
        self.text_logs.insert(tk.END, message + "\n")
        self.text_logs.see(tk.END)
    
    def save_results_to_csv(self, modulation, channel, coder, snr_db, tx_bits, rx_bits, ber):
        filename = "resultats_simulation.csv"
        fieldnames = ["Date", "Modulation", "Canal", "Codage", "SNR (dB)", "Bits transmis", "Bits démodulés", "BER"]
        row = {
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Modulation": modulation,
            "Canal": channel,
            "Codage": coder,
            "SNR (dB)": snr_db,
            "Bits transmis": "".join(map(str, tx_bits)),
            "Bits démodulés": "".join(map(str, rx_bits)),
            "BER": f"{ber:.4f}"
        }
        try:
            file_exists = os.path.isfile(filename)
            with open(filename, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(row)
        except Exception as e:
            messagebox.showerror("Erreur CSV", f"Impossible de sauvegarder les résultats : {e}")