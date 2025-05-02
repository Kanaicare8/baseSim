# BaseSim : Plateforme de simulation de transmission numérique en bande de base

BaseSim est une application Python destinée aux ingénieurs et étudiants en télécommunications pour simuler des chaînes de transmission numérique en bande de base. Elle permet de convertir une séquence binaire en signal modulé (par exemple BPSK, QPSK, QAM), d’y ajouter du bruit (AWGN) ou d’autres perturbations, puis de démoduler et de décoder le signal pour comparer les bits reçus aux bits envoyés. Cette plateforme pédagogique illustre comment la modulation, les caractéristiques du canal et les codes correcteurs influencent la qualité de la transmission.

---

## Fonctionnalités principales

* **Modulations numériques** : schémas courants (PAM, PSK – BPSK, QPSK, 8-PSK –, QAM16, QAM64, etc.) transformant des bits en symboles numériques.
* **Canaux de transmission** : canal AWGN paramétrable via le SNR (Additive White Gaussian Noise). Possibilité d’ajouter d’autres modèles simples (BSC binaire, fading, etc.).
* **Codage de canal** : codes correcteurs (Hamming, Reed–Solomon, convolutionnel + Viterbi) pour étudier la correction d’erreurs.
* **Analyse des performances** : calcul du taux d’erreur binaire (BER) en comparant bits émis / bits reçus.
* **Affichage graphique** : tracés Matplotlib (constellations, diagramme de l’œil, évolution temporelle du signal).

---

## Technologies utilisées

* **Python 3.8+**
* **Tkinter** pour l’interface graphique
* **NumPy** pour les calculs numériques
* **SciPy** pour les algorithmes scientifiques (filtres, transformées, etc.)
* **Matplotlib** pour la visualisation (courbes, constellations, diagrammes de l’œil)
* **csv**, **pandas** (optionnel) pour l’export des résultats

> **Remarque** : sous Linux, installez le paquet `python3-tk` si Tkinter manque.

---

## Installation

1. **Installer Python 3.8+**

   ```bash
   python3 --version
   ```
2. **Créer et activer un environnement virtuel** (recommandé)

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate    # Windows
   ```
3. **Installer les dépendances**

   ```bash
   pip install numpy scipy matplotlib
   ```
4. **Cloner le projet**

   ```bash
   git clone https://.../BaseSim.git
   cd BaseSim
   ```
5. **Vérifier Tkinter**

   ```bash
   python -m tkinter
   ```

---

## Exécution

```bash
# Dans le dossier du projet
python main.py   # ou basesim.py selon votre configuration
```

L’interface Tkinter s’ouvre, proposant les champs de saisie et menus pour configurer la simulation.

---

## Exemple de simulation

1. **Saisie des bits** : entrez une trame binaire (ex. `10110011`).
2. **Paramètres** :

   * Modulation : BPSK
   * Canal : AWGN
   * Codage : Aucun (ou Hamming)
   * SNR : 10 dB
3. **Démarrer** la simulation.
4. **Résultats** : affichage du signal modulé, du diagramme de l’œil, bits reçus et BER.
5. **Varier** les paramètres (QAM16, convolutionnel, SNR faible) pour observer l’évolution du BER.

---

## Guide utilisateur (interface graphique)

1. **Saisie des bits** : champ texte, uniquement `0` et `1`.
2. **Menus déroulants** :

   * **Modulation** : choix du schéma (BPSK, QPSK, 8-PSK, 16-QAM, ...)
   * **Canal** : AWGN (SNR), fading...
   * **Codage** : Aucun, Hamming, BCH, convolutionnel...
3. **Champ SNR** : valeur en dB.
4. **Boutons** : `Démarrer` / `Exporter` / `Effacer logs`.
5. **Affichages** : courbes Matplotlib intégrées, logs textuels, BER.
6. **Export** : CSV des résultats, PNG/PDF des graphes.

---

## Liens utiles

* Documentation Python : [https://docs.python.org/3/](https://docs.python.org/3/)
* Tkinter (FR) : [https://docs.python.org/fr/3/library/tkinter.html](https://docs.python.org/fr/3/library/tkinter.html)
* NumPy : [https://numpy.org/](https://numpy.org/)
* SciPy : [https://scipy.org/](https://scipy.org/)
* Matplotlib : [https://matplotlib.org/](https://matplotlib.org/)
* Pandoc : convertir README.md en PDF :

  ```bash
  pandoc -s -o BaseSim.pdf README.md
  ```

---

*© 2025 BaseSim – Projet pédagogique en télécommunications*
