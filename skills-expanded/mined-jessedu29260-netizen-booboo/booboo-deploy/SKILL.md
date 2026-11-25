---
name: booboo-deploy
description: Stand up a Booboo brain end to end — scaffold the project, write booboo.config.yaml against a real Postgres/Supabase or JSON source, build the snapshot, then wire the REST API, the MCP server, the 3D viewer and the panel. Use when someone wants a brain built for the first time, wants to point Booboo at their own database, or asks an agent to deploy one for them.
---

# Deploy a brain, end to end

Read `RULES.md` in this pack first. The walls rule and the verify rule both bite
during deployment.

## The path

```bash
npx create-booboo my-brain     # scaffold: config + org + AGENTS.md + ONBOARDING.md
cd my-brain && npm install
npm run build                  # booboo.config.yaml → the snapshot
npm run serve                  # REST on :8787
npm run mcp                    # MCP over stdio
```

The scaffold ships a JSON starter with a commented Postgres upgrade path, so a
brain exists before any database is involved. Prove the loop on the starter, then
repoint it — debugging a config and a connection string at the same time is how
deployments stall.

## Shape the config

```yaml
title: "My System"
root: { id: core, type: root, label: "MY SYSTEM" }

layers:                                   # order is Z-order, first is back
  - { name: agents,    color: "#c9a04a", label: "AGENTS" }
  - { name: memory,    color: "#a78bd0", label: "MEMORY" }
  - { name: knowledge, color: "#4ECDC4", label: "KNOWLEDGE" }

walls: [private, sealed]                  # filtered IN THE BUILDER, before anything exists

sources:
  - adapter: postgres
    url: ${DATABASE_URL}
    nodes:
      - { table: agents,       layer: agents,    id: slug, label: name, parent: core, weight: 0.6, icon: emoji }
      - { table: observations, layer: memory,    id: id,   label: title, cluster: project, where: "kind <> 'noise'" }
      - { table: kg_entities,  layer: knowledge, id: id,   label: name, weight_from: degree }
    links:
      - { table: edges, source: src, target: dst, type: rel }

  - adapter: json
    path: ./data/extra.booboo.json

output:
  snapshot: ./build/booboo.json
```

`${VAR}` reads from the environment or a `.env`. **Nothing secret belongs in this
file** — it is committed, and a connection string with a password in it is a
credential in git history forever.

Layers are yours to choose. The three above are a sensible default, not a schema.
Pick planes that match how the system actually stacks.

## Decide the walls before the first build

Walls are the one decision that is expensive to get wrong, because the fix for a
leaked build is not a rebuild — it is a conversation about what already left.

Ask directly, before building: which namespaces must never leave this machine?
Anything personal, sealed, client-confidential or credential-bearing goes in
`walls:` on the first pass. Widening later is cheap; narrowing after a snapshot
has been served is not.

## Wire it to an agent

```jsonc
// Claude Code: .mcp.json · Claude Desktop: claude_desktop_config.json · Cursor: .cursor/mcp.json
{
  "mcpServers": {
    "booboo": {
      "command": "npx",
      "args": ["-y", "@booboo-brain/cli", "mcp",
               "--snapshot", "my.booboo.json", "--org", "org.booboo.json"]
    }
  }
}
```

Use **absolute paths** for `--snapshot` and `--org` when the client's working
directory differs from the project — which it usually does. A relative path that
works in your shell and fails in the client is the most common wiring failure.

Add `--no-write` for anything public or locked down. It still reads the journal;
it refuses `booboo_remember` and `booboo_report`.

## Verify — all four surfaces, actually

Do not report a deployment done until each of these has been observed:

1. **Build** — read the quality line: `quality · authored:N · orphans:N ·
   dump-suspects:N`. A build that emits a snapshot of zero nodes still exits 0.
   Check the node count is plausible for the source.
2. **REST** — hit `/stats`, then `/search`, then `/nodes/:id` with a real id from
   the search result. `/graph` `/neighbors/:id` `/path/:a/:b` are the rest.
3. **MCP** — call `booboo_boot` with a real agent id and read the slice. A process
   that starts is not a server that answers.
4. **Visual** — open `booboo view` (the 3D brain) and `booboo panel` (the
   organigram). Look at them. A brain whose spines all converge on nothing is a
   parent-mapping bug that no status code reveals.

Then confirm the walls held: search the served graph for a term you know exists
only inside a walled namespace. It must return nothing.

## Hand over

The project's `AGENTS.md` (imported by `CLAUDE.md`) is the contract the next agent
reads automatically — boot from the org, one atomic fact per note, author the
links, corrections replace, respect the walls, watch the quality gate, close
honestly. Point the owner at it and tell them it is theirs to edit as their
conventions evolve. It is the system's constitution, versioned next to the org.

If `org.booboo.json` still says `"seed": true`, the brain is not deployed — it is
scaffolded. Run `ONBOARDING.md` (see `booboo-org`) before calling it done.
