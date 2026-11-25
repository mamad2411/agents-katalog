<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-esneyder-rojas
description: CTF writeups and security challenges by esneyder-rojas.
---

# Writeups by esneyder-rojas

Source repository: `/repos/esneyder-rojas`

## Repository Index

- fuzzer/README.md

## Writeup Content


### File: fuzzer/README.md

# 🚀 Fuzzer - Automated Web Fuzzing Tool

**Fuzzer** es una herramienta de pentesting automatizado que realiza fuzzing web completo desde el escaneo de puertos hasta la generación de reportes.

## ✨ Características Principales

- 🔍 **Escaneo inteligente**: Detección automática de puertos y servicios
- 🛠️ **Multi-herramienta**: Soporte para FFUF, Gobuster, Feroxbuster, Dirb y Wfuzz
- 📊 **Reportes HTML**: Genera reportes visuales con estadísticas completas
- ⚙️ **Configuración adaptativa**: Ajustes automáticos según la herramienta
- 📁 **Gestión de diccionarios**: Detecta automáticamente wordlists comunes

# Ejecutar
python3 fuzzer.py

📊 Flujo de Ejecución
Escaneo de puertos → Nmap completo

Detección de servicios → Versiones y tecnologías

Identificación web → HTTP/HTTPS detectados automáticamente

Configuración → Selección de herramienta y ajustes

Fuzzing → Ejecución contra servicios web identificados

Reporte → Generación de HTML con resultados

