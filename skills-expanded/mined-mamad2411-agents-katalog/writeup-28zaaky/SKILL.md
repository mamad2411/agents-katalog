<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-28zaaky
description: CTF writeups and security challenges by 28Zaaky.
---

# Writeups by 28Zaaky

Source repository: `/repos/28Zaaky`

## Repository Index

- Pwn-Tool-XVX/README.md

## Writeup Content


### File: Pwn-Tool-XVX/README.md

# Binary Vulnerability Scanner PwnToolXVX

## Objectif du Projet

Outil de pentesting pour l'analyse approfondie de fichiers binaires, spécialisé dans la détection et l'exploitation de vulnérabilités de sécurité.

## Fonctionnalités Principales

### Analyse des Binaires
- Inspection statique avec Radare2
- Détection de vulnérabilités potentielles
- Génération de shellcode d'exploitation
- Vérification des mécanismes de sécurité (ASLR, DEP, etc.)

### Formats Supportés
- Binaires ELF (Linux)
- Fichiers exécutables Windows (EXE)
- Support progressif pour d'autres formats

## Architecture Technique

### Composants Clés
- **Radare2** : Analyse statique et désassemblage
- **Checksec** : Vérification des protections de sécurité 
- **Pwntools** : Génération et manipulation de shellcode

### Workflow d'Analyse
1. Chargement et inspection du binaire
2. Identification des vulnérabilités potentielles
3. Génération de payloads d'exploitation
4. Production d'un rapport détaillé

## Limitations Actuelles
- Prototype en développement
- Couverture limitée des types de vulnérabilités
- Nécessite des connaissances avancées en sécurité

## Cas d'Usage
- Audit de sécurité
- Éducation en cybersécurité

## Principes Éthiques
- Utilisation strictement légale et autorisée
- Confidentialité et responsabilité
- Respect des bonnes pratiques de sécurité

