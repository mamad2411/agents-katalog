<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-gregoriovinti
description: CTF writeups and security challenges by GregorioVinti.
---

# Writeups by GregorioVinti

Source repository: `/repos/GregorioVinti`

## Repository Index

- AUTO_ZAP/README.md

## Writeup Content


### File: AUTO_ZAP/README.md

# scan-zap

Script Bash per lanciare rapidamente scansioni ZAP su una lista di URL.

## Avvertenza legale
Esegui questo script SOLO su asset per cui hai autorizzazione esplicita.

## Requisiti
- zaproxy (`zap.sh`)
- curl, getent/dig/ping
- (opzionale) weasyprint

## Uso
1. Inserisci una URL per riga in `url_list.txt` (vedi `url_list.txt.example`).
2. Rendi eseguibile lo script:  
   ```bash
   chmod +x scripts/AUTO_ZAP.sh
   ./scripts/AUTO_ZAP.sh
   ```
3. I report saranno salvati in `full-dirs/`.

## Licenza
MIT

