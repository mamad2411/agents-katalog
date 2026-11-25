---
name: n8n-node-dev
description: >-
  Get a custom n8n node into a customer's running instance and keep it there:
  choosing between a private npm registry, a mounted extensions directory, and a
  baked Docker image; the queue-mode requirement that every worker carries the
  install; air-gapped installation; the verified-community-node requirements; and
  what n8n Cloud will and will not accept. Use when an engagement needs a
  connector that does not exist, when a customer asks how to distribute an
  internal node, when a custom node works on one process but not another, or when
  planning the packaging and release path for a node. Authoring depth (declarative
  vs programmatic node design, credential types, UI descriptions) is deliberately
  thin here and routes to the node engineering collaboration.
---

# Custom node distribution

Custom node work shows up in FDE engagements as "we need a connector for X".
This skill owns the part the field engineer owns solo: **getting the node
installed, everywhere it has to run, in a way the customer can maintain.**

Deep node design is a collaboration with n8n's node engineering, not a solo
build. Scope your solo work to distribution, and route real authoring through
that channel. That routing is a feature, not a limitation: it is how field
requirements become product.

---

## Decide the distribution path first

Pick before writing any code. The choice constrains the build.

| Path | When | Cost |
|---|---|---|
| **Private npm registry** | Customer already runs one (Artifactory, Nexus, GitHub Packages). Multiple instances or environments consume the node. | Registry auth on every host; version pinning discipline |
| **Mounted extensions directory** (`N8N_CUSTOM_EXTENSIONS`) | Single instance, or a node too specific to publish. Fastest to iterate. | Filesystem access to every process; easy to forget a worker |
| **Baked Docker image** | Immutable-infrastructure customers, k8s deployments, air-gapped. | You own an image build and its rebase cadence |
| **Public npm + GUI installer** | Genuinely reusable, no proprietary logic. | Public release, and the GUI installer needs registry reachability |

Default recommendation for an enterprise customer running queue mode on
Kubernetes: **baked image**. It is the only path where "is the node on every
worker" is answered by construction rather than by procedure.

---

## The rule that breaks installs: every process needs the node

In queue mode the node must be present on **main, every worker, and every webhook
process**. A node installed only on main produces the worst failure shape: the
workflow saves and validates, the editor renders the node, and executions fail on
a worker with a node-not-found error that points at the workflow rather than the
deployment.

Checklist for any queue-mode install:

- [ ] Node present on main
- [ ] Node present on **every** worker replica (including ones that scale up later)
- [ ] Node present on webhook processes
- [ ] Same version everywhere (a version skew is a silent behavior difference)
- [ ] Install survives a pod restart / rescheduling (baked or mounted from
      persistent storage, not `npm install`-on-boot in a shell)
- [ ] Autoscaling brings up nodes that already have it

If the customer scales workers automatically, the mounted-directory path needs a
shared volume or an init container. Say that up front; it is the most common way
this goes wrong three weeks after handoff.

---

## Air-gapped installation

No registry reachability means no GUI installer and no `npm install` at runtime.
The pattern:

1. Download the package and its dependency tree on a connected host
   (`npm pack`, or a full offline mirror for a tree with dependencies).
2. Transfer through the customer's approved path.
3. Install into the extensions directory or bake into the image on the inside.
4. Version-pin explicitly; there is no "latest" in an air-gapped estate.

A node with **zero runtime dependencies** makes this trivial and a node with a
deep dependency tree makes it a project. Design for the former when the customer
is air-gapped.

---

## Verified community nodes

If the node is going into the verified program, the requirements shape the build
from the start:

- **No runtime dependencies.**
- **One service per package.** Do not bundle several integrations.
- Published from CI with **npm provenance** (GitHub Actions publishing with
  provenance attestation).
- Follows the naming and metadata conventions for community nodes.
- Documentation and a maintained repository.

Check the current requirements before committing to the program; they tighten
over time.

---

## n8n Cloud

**Cloud does not accept private custom nodes.** A customer on Cloud who needs a
connector has three options, in order of practicality:

1. HTTP Request node against the target API, with a proper credential type
   (usually the right answer, and shippable today)
2. A published, verified community node
3. Move that workload to self-hosted

Do not design a private node for a Cloud customer and discover this at
deployment.

---

## Authoring: the thin layer

Enough to scope and to have the conversation. Depth routes to node engineering.

- **Start from the node starter template.** It carries the build config,
  linting, and structure that the verification process expects.
- **Declarative vs programmatic:** declarative style describes requests
  declaratively and covers most REST APIs with less code and fewer bugs. Reach
  for programmatic only when the integration needs real logic: pagination that
  is not expressible declaratively, binary handling, multi-step auth, or
  stateful operations.
- **Credentials are a separate type** from the node and are what the customer's
  security review will actually read. Get the auth model right first.
- **Versioning:** nodes carry a `typeVersion`. Changing parameter shape without
  bumping it breaks existing workflows silently. This is the most expensive
  mistake in custom node maintenance, so raise it early.

**When to escalate to node engineering:** anything that will be reused across
customers, anything targeting the verified program, anything where the API's
auth or pagination is unusual, and anything where the right answer might be a
change to a first-party node instead of a new custom one. Bring the field
context: which customer, what the workflow needs, why the HTTP Request node is
not sufficient.

---

## The pre-build question

Before agreeing to a custom node, confirm it is actually needed. The HTTP
Request node with a proper credential type covers a large share of "we need a
connector for X", ships immediately, needs no distribution story, and works on
Cloud. A custom node earns its keep when the integration is used in many
workflows, needs a real UI for non-engineers, or has logic that does not belong
pasted into every workflow.

Ask: how many workflows will use it, who configures it, and does the customer
have anyone to maintain it after handoff.

---

## Handoff requirements for a shipped node

- Source repository the customer can access, with the build documented
- The distribution path written down, including the every-worker rule
- Version pin and the upgrade procedure
- Which n8n versions it is tested against
- Who owns it after handoff, named
