---
name: konzept-model-api
description: Read-only Modell↔API-Drift-Detektor. Diff von PHP-Enum-Cases gegen OpenAPI-enum-Arrays und PHP-Entity-Properties gegen OpenAPI-Schema-Properties (gleichen Namens). Use bei „enum drift", „Modell gegen OpenAPI prüfen", „API-Konsistenz", Sprint-Ende.
---

# konzept-model-api (CDP5 T1-Gate)

Deterministischer Diff-Teil des früheren `konzept-model-api`-Agents als Programm (CDP5 §32.8(1) nennt Enum-Drift + Modell↔OpenAPI-Diff explizit als deterministisch). Die semantische **Konzept-Vokabular-Drift**-Wertung (gleicher Begriff, andere Bedeutung) bleibt LLM-/Mensch-Arbeit.

## Aufruf

```bash
node "${CLAUDE_PLUGIN_ROOT}/skills/konzept-model-api/model-api-drift.mjs" \
  --repo=<repo-root> --openapi=<pfad/openapi.yaml> [--json]
```

Exit: `0` kein Drift · `1` Drift gefunden · `2` Nutzungsfehler.

## Checks (Name-Match, normalisiert)

- **Enum-Drift** — PHP `enum X { case … }` (Backing-Value oder Case-Name) ↔ OpenAPI `enum: […]` gleichen Namens; meldet fehlendes Pendant + abweichende Wertemengen.
- **Property-Drift** — PHP-Entity-Properties (`private/protected/public … $x`) ↔ OpenAPI-Schema-`properties:` gleichen Namens; meldet „nur OpenAPI" / „nur Entity".

## Grenzen (dependency-frei)

Der OpenAPI-Parser ist ein kompakter Zeilen-Scanner (kein voller YAML-Parser): er erfasst `components.schemas.*.properties` und `enum`-Blöcke/Inline-Arrays. Für exotische YAML-Konstrukte ggf. ungenau — Befunde sind Hinweise, die der Main-Agent verifiziert (CDP5 §10.6).
