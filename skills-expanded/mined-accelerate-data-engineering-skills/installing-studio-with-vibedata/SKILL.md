---
name: installing-studio-with-vibedata
description: Use when a customer, operator, or support engineer wants to install, deploy, set up, run, update, restart, or tear down Studio with the vibedata CLI — local Docker on one machine or Kubernetes (Azure/AKS) for a team — including prerequisite checks, Azure secret and infra gap handling, sign-in (vibedata login vs az login vs gh auth login), and day-2 lifecycle.
---

# Installing Studio with vibedata

Drive the whole `vibedata` CLI by chatting the customer through it: ask what they want, check their machine, run the right command, read the output, and hand back the exact thing to fix. **Run the checks and drive the CLI — never just print doc steps.**

Audience: customers self-serving their own install, and our eng/support running it against a customer's environment. Both get the same conversational flow.

## First question (always)

Ask, in plain words: **"Are you just trying Studio on one machine, or running it for your team on a cluster?"**

| Answer | Path | Detail |
| --- | --- | --- |
| one machine / laptop / just trying it | **Local Docker** | [`references/local-docker.md`](references/local-docker.md) |
| a cluster / for the team / production | **Kubernetes (Azure today)** | [`references/kubernetes.md`](references/kubernetes.md) → cloud file [`references/azure.md`](references/azure.md) |

If they already said which, skip the question and go. Don't guess when it's genuinely unclear — ask.

## Both paths, same shape

1. **Gate the prerequisites.** Run the checks. On any miss, stop and hand back the exact fix command — do not proceed past a failed gate.
2. **Drive the install.** Run the real `vibedata install …` command, stream its output, and report the outcome (state + URLs).
3. **Hand off what the CLI can't do.** For anything the installer doesn't create (Azure infra, in-container Fabric sign-in), give the exact command and say plainly it's theirs to run.

## Day-2 routing (route to what exists, per mode)

| Goal | Local Docker | Kubernetes |
| --- | --- | --- |
| Sign the CLI in to Studio | `vibedata login [--studio-url URL]` | same |
| Sign the CLI out | `vibedata logout` | same |
| Check the OS keyring | `vibedata auth keyring-check` | same |
| Update to a new version | update the binary, then `vibedata update compose` | **no CLI, and not automatic** — Studio never upgrades itself. Argo reports the release `OutOfSync` and waits for a requested sync, so a backup can exist first (k8s file) |
| Start / stop / restart | `vibedata compose up \| down \| restart` | **no CLI** — `kubectl` / Argo; pause the cluster with `az aks stop` / `az aks start` |
| Back up | `vibedata backup compose` → `DATA_DIR/backups` (no flags) | `vibedata backup kubernetes --to <share-url>` → an existing second share |
| Restore | `vibedata restore compose` (in place, no flags) | `vibedata restore kubernetes --from <share>/<package>` — recovery restores into a **new** cluster, not over the broken one (k8s file) |
| Tear down | `vibedata cleanup` (Compose project only) | **no CLI** — ordered `az` resource deletes, order and gotchas in the cloud file (`az aks delete`, `az afd profile delete`, `az network private-link-service delete`, `az storage account delete`, `az keyvault delete`) |
| Fabric cloud/GitHub creds | in-container `az login` / `gh` (walk them through it) | the cluster identity + vault secrets set up during prereqs |

## Hard gates (never violate)

- **Block on a failed prereq.** Missing Docker, missing sign-in, unreachable cluster → stop with the exact fix command. Never install past a red check.
- **Cloud scope.** Offer **Azure**. For `aws`/`gcp`, say "not supported yet — Azure only today" in plain words. Never surface a raw `UnsupportedCloud`
  traceback.
- **Infra honesty.** `vibedata install kubernetes` creates **nothing** in Azure — it only reads coordinates. Never claim you created a cluster, share,
  Key Vault, or Front Door. Hand back the exact `az` command and say it's the customer's to run.
- **Placeholder honesty.** Every placeholder secret you create to unblock install ships with the exact command to set the real value **and** verify it.
  Never leave a placeholder silent.
- **No invented commands.** Only run commands in the surface below. Kubernetes has no `vibedata update`, `compose`, or `cleanup` — do not invent one; route k8s day-2 to Argo/`kubectl`/`az`.
- **No auth conflation.** The three sign-ins are different things (below).

## Three sign-ins — never conflate

| Command | Signs in to | When |
| --- | --- | --- |
| `vibedata login` | **Studio** (browser/loopback OAuth against a Studio URL) | to use the CLI against a running Studio; `--studio-url` to target one |
| `az login` | **Azure** | k8s prereqs (reading coordinates); Docker Fabric (inside the API container) |
| `gh auth login` | **GitHub** | Local Docker prereq on the laptop (required to create a domain) |

## Command surface (all that exists — never go beyond it)

```
vibedata version
vibedata install compose [--with-observability | --full-observability | --no-observability] [--studio-url http://host[:port]]
vibedata install kubernetes --cloud azure --domain … --storage-url … --vault-url … --vault-identity-client-id …
                            [--with-observability | --full-observability | --no-observability]
                            [--version] [--kube-context] [--storage-resource-group] [--timeout] [--kubeconfig]
vibedata update compose
vibedata compose up [--with-observability | --full-observability | --no-observability] | down | restart
vibedata backup  compose                      # → DATA_DIR/backups
vibedata backup  kubernetes --to <share-url> [--name] [--cloud] [--kube-context] [--kubeconfig] [--storage-resource-group]
vibedata restore compose
vibedata restore kubernetes --from <share-url>[/<package>] [--list] [--force] [--yes] [--with-langfuse] [--cloud] [--kube-context] [--kubeconfig] [--storage-resource-group]
vibedata login | logout   [--studio-url URL]
vibedata auth keyring-check
vibedata cleanup [--force | -y] [--keep-images]      # Compose project only
```

An observability profile is **never** inferred from silence: omitting the flag on either `install` blocks and prints both the keep and the remove command, and
`compose up` starts the installed profile unchanged. Only `--no-observability`
removes it. `install kubernetes --version` pins one release instead of tracking the auto-upgrade channel — the recovery install, not the normal one.

Global `--json` (machine-readable, event streams) and `--verbose` work on every command. `install kubernetes` with no flags opens an interactive form
(kubeconfig, domain, storage URL, vault URL).

## Anchored to the reference docs (maintenance)

The command sequences and secret list in the references are the operative subset of Studio's canonical docs — a customer running this skill has the
`vibedata` binary, not the repo, so the steps must be self-contained here:

- Local Docker → `docs/user-guide/reference/local-docker-deployment.md`
- Kubernetes/Azure → `docs/user-guide/reference/k8s-deployment-azure.md`

When those docs change (secret names, flags, prereqs, day-2 surface), update these references to match. If a command's behaviour is uncertain, trust the
CLI (`vibedata … --help`) and the doc over memory.
