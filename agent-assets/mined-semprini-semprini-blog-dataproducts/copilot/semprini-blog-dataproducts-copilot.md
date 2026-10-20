# semprini-blog-dataproducts

This project uses the [MD-DDL standard](https://github.com/Semprini/md-ddl) for
data domain modelling. MD-DDL is installed from PyPI (`pip install md-ddl`) and
unpacked into `.md-ddl/` by `md-ddl init`.

## Agents

MD-DDL provides AI agents for every stage of the modelling lifecycle.
Use the custom agents in `.github/agents/` via GitHub Copilot Chat:

Agent | Purpose
--- | ---
`agent-guide` | Learning, navigation, concept explanation. Start here.
`agent-ontology` | Domain discovery, entity modelling, source mapping.
`agent-artifact` | Physical schema generation (SQL DDL, JSON Schema, Parquet, Cypher).
`agent-architect` | Data product design, architecture discussion, ODPS manifests.
`agent-governance` | Standards conformance, compliance auditing, governance assurance.

## Validation

Run the mechanical pre-flight checks with `md-ddl lint <domain-folder>`.
Everything beyond syntax is agent-driven review — see
`.md-ddl/guides/validation-tooling.md`.

## Key references

- MD-DDL specification: `.md-ddl/md-ddl-specification/`
- Complete spec (single file): `.md-ddl/md-ddl-specification/MD-DDL-Complete.md`
- Examples: `.md-ddl/examples/`

## Project layout

```
semprini-blog-dataproducts/
  .md-ddl/         MD-DDL standard (installed — do not edit)
  .github/agents/  Copilot custom agent wrappers
  domains/         Domain files (one per business domain)
  entities/        Entity detail files
```

Upgrade the standard with `pip install --upgrade md-ddl && md-ddl init`.
