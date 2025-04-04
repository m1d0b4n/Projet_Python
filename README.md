# 🐍 Projet Python 2025 — Diagnostic, Géolocalisation et Analyse de Logs

Ce projet Python interactif propose un menu terminal intuitif avec plusieurs outils intégrés. Il s’adresse à toute personne souhaitant :
- Obtenir des informations géographiques via une API publique
- Analyser un fichier de logs JSON
- Effectuer un diagnostic système distant via SSH

## 📋 Fonctionnalités disponibles

### 1️⃣ Rechercher la population par code
- Interroge l’API publique `https://geo.api.gouv.fr/communes`
- Entrée : un code département (2 chiffres) ou un code postal (5 chiffres)
- Affiche :
  - La population de la zone
  - Un lien vers une carte sur [code-postal.com](https://www.code-postal.com/)

### 2️⃣ Traiter un fichier de logs JSON
- Lecture d’un fichier JSON local
- Analyse des logs `error` et `warning`
- Résumé en console : nombre d’erreurs et avertissements
- Export possible vers un fichier `.xlsx` :
  - Colonnes : `Nom de la station`, `Niveau de l'erreur`, `Message de l'erreur`

### 3️⃣ Diagnostic système distant (via SSH)
- Connexion à une machine distante avec Fabric
- Récupération des informations suivantes :
  - OS
  - CPU (modèle, architecture, cœurs…)
  - RAM totale
  - 5 processus les plus gourmands en RAM
  - Variables d’environnement (PATH, HOME, USER…)
  - Partitions de disque
  - Espace disque disponible
  - Interfaces réseau
  - Heure du dernier démarrage
- Export Excel (.xlsx) possible, avec mise en page automatisée :
  - Cellules alignées en haut/gauche, renvoi à la ligne automatique
  - Onglet nommé : `System status`

---

## 🧱 Structure du projet

```bash
.
├── main.py                   # Menu interactif principal
├── modules/
│   ├── ascii_art.py         # Affichage ASCII d'accueil
│   ├── geo_api.py           # Requête API géographique
│   ├── log_analyzer.py      # Analyse des logs JSON
│   └── system_diag.py       # Diagnostic système via SSH
├── utils/
│   └── validators.py        # Validation des chemins fichiers
├── data/
│   └── logs.json            # Exemple de fichier log à analyser
├── requirements.txt         # Dépendances Python
└── README.md
```

---

## 🚀 Installation

1. Cloner le repo ou télécharger le zip :
```bash
git clone <url-du-repo> && cd Projet_Python
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Lancer le projet :
```bash
python main.py
```

---

## 📦 Dépendances

Liste issue de `requirements.txt` :
- `requests`
- `pandas`
- `openpyxl`
- `fabric`

---

## 🧠 Auteur

Projet réalisé dans le cadre du module Python à l'école LiveCampus (2025)  
👨‍💻 **Apprenant :** [m1d0b4n](https://github.com/m1d0b4n)   
👨‍🏫 **Enseignant :** Alexandre RASPAUD   
