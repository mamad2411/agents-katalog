<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-coded-roger
description: CTF writeups and security challenges by CodeD-Roger.
---

# Writeups by CodeD-Roger

Source repository: `/repos/CodeD-Roger`

## Repository Index

- Pentest-Toolkit/README.md

## Writeup Content


### File: Pentest-Toolkit/README.md

# Pentest Toolkit
---
Le script **install.sh** prépare l’environnement nécessaire pour exécuter **main.sh**, l’outil principal.

Il effectue les actions suivantes :

- **📦 Installation des dépendances essentielles pour l’exécution des outils de pentesting.**
- **🔄 Mise à jour et configuration du système pour optimiser la compatibilité.**
- **🛡 Vérification des installations et réinstallation en cas de besoin.**
- **🔗 Création des répertoires et permissions nécessaires pour stocker les résultats des scans et des rapports.** 

---

## 🎯 Menu interactif permettant :

- **📡 Scans réseau avec nmap (SYN, UDP, ACK, IPv6, etc.)**
- **📜 Génération de rapports en HTML, XML, CSV et JSON.**
- **🚀 Exécution de Metasploit, Nikto, SQLmap, Wireshark, etc.**
- **⚡ Configurations avancées (fragmentation, spoofing, bande passante).**
- **🔔 Système d'alertes sur les vulnérabilités détectées.**
- **🚀 Installation et Utilisation**

### 1️⃣ Cloner le dépôt

 ```bash
git clone https://github.com/CodeD-Roger/Pentest-Toolkit.git
cd Pentest-Toolkit
```

### 2️⃣ Exécuter le script d'installation
 ```bash
sudo chmod +x install.sh
sudo ./install.sh
```

### 3️⃣ Lancer l'outil principal
 ```bash

chmod +x main.sh
./main.sh
```
---
## 📜 Fonctionnalités détaillées
🔍 Scans disponibles
- **Type de scan	Description**
- **SYN Scan	Scan furtif (par défaut)**
- **DP Scan	Détection des services UDP ouverts**
- **ACK Scan	Détection des règles de firewall**
- **IPv6 Scan	Scan de réseaux IPv6**
- **Scan Agressif	Collecte maximale d’informations**
- **Scan Ultra Discret	Techniques avancées d’évasion**

#### 📊 Rapports et exports
#### 🔄 Génération de rapports détaillés en HTML, XML, CSV, et JSON.
#### 📑 Affichage et analyse des résultats de scan.
#### 📉 Statistiques et tendances des vulnérabilités.

---
## 🛠️ Outils complémentaires
Metasploit : Framework d’exploitation.
Nikto : Scanner web.
SQLmap : Détection et exploitation de vulnérabilités SQLi.
Wireshark : Analyse du trafic réseau.

## 📷 Captures d’écran  

Voici un aperçu de l'outil **Pentest Toolkit** :

| **Menu principal** | **Visualisation des scans** |
|-------------------|---------------------------|
| ![image](https://github.com/user-attachments/assets/4ab775d8-77e7-454d-a4a6-5fc89632a05f) | ![image](https://github.com/user-attachments/assets/857345bb-ad97-47b3-a4c2-0b582ed53868) |

| **Scan NSE** | **Monitoring** |
|-------------|--------------|
| ![image](https://github.com/user-attachments/assets/f8694f60-79ab-46fc-a166-13cb45b13858) | ![image](https://github.com/user-attachments/assets/605ac2f1-9ea4-4323-becc-666642e75ce2) |

---
## 🛠 Prérequis  
✅ **Système** : Debian / Ubuntu  

## ⚠️ Avertissement  
⚠ **À utiliser uniquement sur des réseaux et systèmes autorisés !**  
L’usage de cet outil sur des systèmes tiers **sans consentement explicite** peut être **illégal**.

