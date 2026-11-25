---
name: rag-vuln-triage
description: Consulta el RAG local de vulnerabilidades (KEV + exploit público + EPSS + CVSS de CVE 5.0) para priorizar por explotación real. Úsala cuando tengas un producto/servicio/versión y quieras saber qué CVEs accionables tiene.
---

# Triage de vulnerabilidades con el RAG local

Esta skill prioriza vulnerabilidades por **explotación real**, no solo por CVSS. Orden:
**KEV (explotado de verdad) → exploit público → EPSS → CVSS**.

## Cuándo usarla
Tras enumerar un activo (producto + versión), para decidir qué explotar primero.

## Cómo usarla
Ejecuta el retrieval local (offline, apto para la zona E2 aislada):

```bash
python rag/query_vulns.py --query "<vendor producto>" --json
# opcionales: --version "<versión>"  --kev-only  --min-epss 0.5  --limit 15
```

Si el store está vacío, puéblalo primero:
```bash
python rag/refresh.py --epss-all
```

## Cómo interpretar la salida
Cada resultado trae `severity` (tier ya calculado), `in_kev`, `exploit_public` +
`exploit_sources` (ExploitDB/Metasploit/Nuclei), `epss`, `cvss` + `cvss_vector` (de CVE 5.0,
no del NVD degradado), `ssvc` (decisión de CISA) y `source_refs`.

Reglas:
- `in_kev: true` o `exploit_public: true` ⇒ es lo más accionable: empújalo a explotación primero.
- Mapea cada resultado a un `finding` (esquema `contracts/finding.schema.json`): copia
  `cvss`, `cvss_vector`, `epss`, `exploit_public`, `exploit_sources`, `ssvc`, `cve`,
  `source_refs`, `status: "candidate"`.
- **Nunca inventes un CVE**: si no hay `source_refs`, es hipótesis, no finding.

## Alcance
Solo activos en scope (`contracts/scope.json`). El hook de alcance bloquea lo demás.
