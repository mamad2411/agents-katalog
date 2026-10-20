---
name: profile-check
description: Read-only Konformitäts-Check eines Konzepts + Repos gegen ein einmal deklariertes project-profile.md (YAML-Frontmatter). Verifiziert deklarierte Defaults statt sie neu zu erfragen — EU-AI-Act-Klasse/security_level im Konzept, Runtime + Test-Framework im Repo, freie Pflicht-Tokens. Use bei „passt das Projekt zum Profil", „profile check", als CI-Gate nach Setup-Änderungen.
---

# profile-check (CDP5 T1-Gate, §1.9/§22)

Setzt die Doktrin **„Default einmal setzen, danach nur noch Konformitäts-Checks"** um: ein Projekt deklariert seine Vorgaben einmal in `project-profile.md` (Architekt-Entscheidung, z. B. EU-AI-Act-Klasse, Sicherheits-Level, Runtime, Test-Framework); dieser Skill prüft **deterministisch** (0 Modell-Token), ob Konzept und Repo dazu konform sind — statt die Fragen pro Schritt neu zu stellen.

## Aufruf

```bash
node "${CLAUDE_PLUGIN_ROOT}/skills/profile-check/profile-check.mjs" \
  --profile=<project-profile.md> [--konzept=<konzept.md>] [--repo=<root>] [--json]
```

Mindestens `--konzept` oder `--repo` angeben. Exit: `0` konform · `1` Profil-Drift · `2` Nutzungsfehler.

## Profil-Felder (YAML-Frontmatter)

| Feld | Wirkung |
|---|---|
| `eu_ai_act_class` | Konzept muss die Klasse + „AI-Act" deklarieren (Architekt setzt die Klasse einmal). |
| `security_level` | `elevated` → Konzept muss Threat-Modeling (§33.4) enthalten; `standard` → kein Check. |
| `runtime` | `node`/`php`/`python` — erwartete Runtime-Marker (package.json/composer.json/… oder passende Datei-Endungen) im Repo. |
| `test_framework` | `node:test`/`phpunit`/`jest`/`vitest`/`pytest` — mind. eine Test-Datei mit passender Signatur. |
| `require_in_concept` | Freie Liste von Pflicht-Tokens, die im Konzept-Text vorkommen müssen (projektspezifische Pflicht-Sektionen). |

Vorlage: [`project-profile.template.md`](project-profile.template.md) (kopieren, ausfüllen, in das Zielprojekt legen).

## Grenzen

Deterministischer Detektor: prüft **Präsenz/Signatur**, nicht Semantik. Ob die deklarierte EU-AI-Act-Klasse regulatorisch *korrekt* ist, bleibt Architekt-Entscheidung (§1.9/§23) — der Skill prüft nur, dass sie deklariert und konsistent ist.
