# semprini-blog-dataproducts

A companion repo for a blog series on model-driven data product generation (see
[README.md](./README.md) for the full narrative). It demonstrates the whole path from a
running platform to a declared model to a generated, deployed data product:

1. **Platform** — [compose.yml](./compose.yml) runs a standalone "Digital" domain: PostgreSQL
   (operational store) reflected into GraphQL by pg_graphql + PostgREST, Kafka + Apicurio
   Registry for events, Flink for stream processing, and Trino + DuckLake + MinIO for
   analytics via pg_duckpipe CDC replication. `docker compose up -d --build` starts it.
2. **Model** — [data_model/](./data_model/) holds the MD-DDL domain **Digital Core**: the
   shared spine of a digital business — parties, the roles they play, the accounts and
   agreements they hold, and the transactions between them. It is deliberately generic and
   carries no industry-specific or regulatory content. Edited with the MD-DDL agents below.
3. **Template** — [template/](./template/README.md) is the contract for what one deployable
   data product directory looks like on this platform: ODS SQL, a GraphQL surface, per-entity
   event JSON Schemas, a Flink job, lake registration, a Trino smoke test, an ODPS manifest,
   and the `product.yaml` manifest the CLI reads. [template/example/](./template/example/) is
   a filled-in instance for one entity (Address) — both the reference for what a finished
   product looks like and its own working test of the template and CLI.
4. **Generated products** — `products/<slug>/`, each a copy of `template/` with every
   `{{placeholder}}` and `>>> repeat` block resolved for one MD-DDL data product declaration
   in [data_model/data_products/](./data_model/data_products/). None exist yet; the pending
   [handoff-to-artifact.md](./handoff-to-artifact.md) hands the settled decisions to
   `/agent-product` to generate `products/canonical-party/` from
   [data_model/data_products/canonical.md](./data_model/data_products/canonical.md).
5. **Deploy / test / undeploy** — the platform CLI in
   [src/semprini_blog_dataproducts/](./src/semprini_blog_dataproducts/):
   ```bash
   uv run semprini-blog-dataproducts deploy   products/<slug>
   uv run semprini-blog-dataproducts test     products/<slug>
   uv run semprini-blog-dataproducts undeploy products/<slug>
   ```
   It applies a product directory's SQL, topics, registry artifacts and Flink job to the
   running Compose stack, then smoke-tests every interface.

## MD-DDL: modelling the domain

This project uses the [MD-DDL standard](https://github.com/Semprini/md-ddl) for step 2
above. MD-DDL is installed from PyPI (`pip install md-ddl`) and unpacked into `.md-ddl/` by
`md-ddl init`. It provides AI agents for every stage of the modelling lifecycle, invoked with
slash commands in Claude Code and scoped to [data_model/](./data_model/):

Command | Agent | Purpose
--- | --- | ---
`/agent-guide` | Agent Guide | Learning, navigation, concept explanation. Start here.
`/agent-ontology` | Agent Ontology | Domain discovery, entity modelling, source mapping.
`/agent-artifact` | Agent Artifact | Physical schema generation (SQL DDL, JSON Schema, Parquet, Cypher) — used here to instantiate `template/` into a product directory.
`/agent-architect` | Agent Architect | Data product design, architecture discussion, ODPS manifests.
`/agent-governance` | Agent Governance | Standards conformance, compliance auditing, governance assurance.

### Project agent

`/agent-product` ([.claude/agents/agent-product.md](./.claude/agents/agent-product.md)) is this
project's specialisation of Agent Artifact for step 4. It instantiates `template/` into
`products/<slug>/` for one declaration, deploys and tests it with the CLI, and reports. It
skips Agent Artifact's assessment dialogue and generic 3NF skills because `template/README.md`
has already made those decisions, and it adds the rules the template leaves implicit (scope
boundary, subtype keys, relationship attribute types, pg_graphql field-name directives).
`/agent-artifact` stays available for physical artifacts that are not products of this
template.

Run the mechanical pre-flight checks with `md-ddl lint data_model`. Everything beyond syntax
is agent-driven review — see `.md-ddl/guides/validation-tooling.md`. The linter only
understands MD-DDL domain files; it does not check `template/` or `products/`, whose
`{{placeholders}}` are not valid MD-DDL.

### Key references

- MD-DDL specification: `.md-ddl/md-ddl-specification/`
- Complete spec (single file): `.md-ddl/md-ddl-specification/MD-DDL-Complete.md`
- Examples: `.md-ddl/examples/`

## Project layout

```
semprini-blog-dataproducts/
  .md-ddl/                 MD-DDL standard (installed — do not edit)
  .claude/agents/          Project agents (agent-product)
  .claude/commands/        Claude slash commands
  compose.yml               The Digital domain platform
  data_model/               The Digital Core domain (MD-DDL)
    domain.md                 Domain summary: entities, relationships, enums, data products
    entities/                 Entity detail files
    enums.md                  Enumerations
    data_products/             MD-DDL data product declarations
  template/                 Data product template: what a deployable product looks like here
    README.md                  The contract: naming, type mapping, generation input rules
    example/                   Worked, deployable instance of the template (entity: Address)
  products/                 Generated data products, one directory per product, from template/
  src/                      Platform CLI (deploy | test | undeploy, see above)
  handoff-to-artifact.md   Pending MD-DDL handoff: settled decisions for the next /agent-artifact run
```

Upgrade the MD-DDL standard with `pip install --upgrade md-ddl && md-ddl init`.
