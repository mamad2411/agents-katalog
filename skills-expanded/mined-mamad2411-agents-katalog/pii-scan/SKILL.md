---
name: pii-scan
description: Read-only, dependency-freier Klartext-PII-Detektor für ein Repo/Testdaten/Traces (E-Mail, IBAN, Telefon, Kreditkarte mit Luhn). Use bei „PII scan", „keine personenbezogenen Daten im Repo/Testdaten", Datenschutz-Check vor Commit/Release, als CI-Gate (speist den Sicher-Gate).
---

# pii-scan (CDP5 T1-Gate, §15.6/§15.7/§2.7)

Findet Klartext-PII (deterministisch, redacted Output, nur `node:`-Builtins). Adressiert die Pflicht „keine personenbezogenen Produktivdaten in Repo/Testdaten/Traces".

## Aufruf

```bash
node "${CLAUDE_PLUGIN_ROOT}/skills/pii-scan/pii-scan.mjs" --repo=<root> [--json]
```

Exit: `0` sauber · `1` ≥1 Fund · `2` Nutzungsfehler.

## Erkennung

E-Mail · IBAN · Telefon (intl.) · Kreditkarte (mit **Luhn**-Prüfung gegen False-Positives). Platzhalter (`${…}`, `your_…`, `example.com`, `<…>`, `changeme`) werden ignoriert; Funde **redacted**; `node_modules`/`vendor` etc. übersprungen, Dateien > 1 MB ausgelassen.

## Hybrid (wichtig)

Der Regex-Teil ist deterministisch, die **semantische** Einstufung (echter Name vs. Zufallsstring, Kontext) gehört in ein `review-verify`-Overlay — `pii-scan` ist ein **Hinweis-Gate**, kein finaler Wahrheits-Entscheid (CDP5 §10.6).
