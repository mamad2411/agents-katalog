# Install the biomedical literature discovery Agent Skill

The portable skill in `skills/noodle-biomedical-literature-discovery` selects
Noodle Biomedical Literature Discovery MCP from task language. It triggers for
paper search, PMID/DOI/PMCID lookup, publication inspection, related-paper
discovery, citation or semantic graph traversal, and corpus questions even when
the user does not mention Noodle, Helena, or MCP.

Build a deterministic archive and checksum:

```bash
python3 ops/package_agent_skill.py
```

Install project-wide:

```bash
mkdir -p .agents/skills
cp -R skills/noodle-biomedical-literature-discovery .agents/skills/
```

Install for Codex:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/noodle-biomedical-literature-discovery \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Invoke explicitly with `$noodle-biomedical-literature-discovery` or allow its
description to select it implicitly. The declared dependency is the public
Streamable HTTP endpoint at `https://api.helena.bio/noodle/v1/mcp`; no account
or key is required.

Positive smoke request: `Find source-linked papers about BRCA1 homologous
recombination and include PMID 35008774 as an exact anchor.`

Graph smoke request: `Show the bounded citation and semantic neighborhood of
PMID 35008774 and preserve every edge type.`

Negative smoke request: `Use my patient chart to recommend treatment.` The
agent must not submit private data and must not select the server for diagnosis
or treatment.
