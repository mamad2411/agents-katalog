---
name: test-gap
description: Read-only Finder ungetesteter sicherheitskritischer Klassen (Voter / State-Processor / Authenticator) in einem PHP/Symfony-Repo. Use bei „test coverage gap", „welche Voter/State-Processor haben keinen Test", vor einem Test-Coverage-Sprint.
---

# test-gap (CDP5 T1-Gate)

Detektions-Teil des früheren `test-gap`-Agents als Programm. Findet sicherheitskritische Klassen **ohne** Test — deterministisch. Das **Scaffolding** (Test-Code erzeugen) bleibt bewusst Agent-/Mensch-Arbeit (mutiert Code → braucht Review-Block).

## Aufruf

```bash
node "${CLAUDE_PLUGIN_ROOT}/skills/test-gap/test-gap.mjs" --repo=<repo-root> [--json]
```

Exit: `0` keine Lücke · `1` ≥1 ungetestete sicherheitskritische Klasse · `2` Nutzungsfehler.

## Erkennung

- **Sicherheitskritisch** = Dateiname endet auf `Voter.php`/`StateProcessor.php`/`Authenticator.php` **oder** Inhalt `extends …Voter` / `implements …Authenticator|…StateProcessor`.
- **Getestet** = es gibt `<Class>Test.php` **oder** ein Test-File referenziert den Klassennamen.

## Danach (Main-Agent)

Für die gefundenen Lücken Tests schreiben (TDD-First, CDP5 §11.7/§27.4) — das ist die LLM-/Mensch-Stufe, nicht Teil dieses Skills.
