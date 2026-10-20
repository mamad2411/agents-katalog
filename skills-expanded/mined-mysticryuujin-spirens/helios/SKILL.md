---
name: helios
description: Helios — a16z's trustless Ethereum light client. When to run one, where it fits between dweb-proxy and an upstream RPC, the eth_getProof requirement, checkpoint-URL trust, failure modes. Use when a user asks about light clients, trustless RPC, Merkle-proof verification of contract reads, or Helios-specific deployment.
---

# Helios

## What You Probably Got Wrong

**You think Helios removes the need for an upstream RPC.** It doesn't.
Helios is a verifier, not a source of truth. Every `eth_*` call goes to
an **untrusted execution RPC** under the hood — Helios just proves the
response via Merkle proof against the beacon-chain state root. No
upstream = no answers.

**You think any Ethereum RPC works as Helios' upstream.** Most public
RPCs (chainlist.org endpoints, `cloudflare-eth.com`, eRPC's
`repository` default provider, even some free vendor tiers) don't
reliably serve `eth_getProof`. Helios needs proofs for every state
read. If the upstream can't produce them, Helios returns errors.
Paid Alchemy / QuickNode / Infura tiers all support `eth_getProof`;
your own node supports it; free public endpoints usually don't.

**You think the `checkpoint` URL is just a hint.** It is the one trust
root Helios has. Everything after the weak-subjectivity checkpoint is
cryptographically verified against the sync committee; the checkpoint
itself is trusted by declaration. A malicious checkpoint provider can
poison the chain Helios believes in. Pick a reputable provider; for
paranoia, cross-check the finalized slot across two providers.

**You think Helios is a drop-in replacement for a full node.** It's
not. Helios proves state at head (and a few finalized blocks back).
It can't answer archive queries, can't trace transactions, can't
serve big `eth_getLogs` ranges, and isn't built for validator duties.
Use it where "did this contract read return the correct value?" is the
whole question.

**You think you can front Helios with an aggressive cache and be
fine.** Proofs are block-specific. If a cache serves a proof for block
N when Helios asked for block M, verification fails and Helios re-
fetches. That's safe. But a cache that rewrites block numbers or
drops proof fields will silently break verification.

**You forget Helios is read-only.** `eth_sendRawTransaction` goes
straight to the upstream unverified. Helios can't prove a transaction
landed until it finalizes. For apps that submit transactions, Helios
is a read shield, not a write shield.

## When to run one

- **You want trustless ENS resolution** without running a full node.
  The SPIRENS default placement: dweb-proxy → Helios → eRPC →
  upstreams. ENS contenthash reads are cryptographically proven; the
  public `rpc.*` endpoint stays vanilla eRPC.
- **You want to detect a compromised vendor.** If Alchemy returns a
  bogus contract read, Helios catches it at the proof step. Without
  Helios, dweb-proxy would trust whatever it got and serve wrong CIDs.
- **You're building an app where state correctness matters more than
  latency.** Helios adds ~100ms+ per call. Fine for occasional ENS
  lookups; not fine for a busy indexer.

## When NOT to run one

- You already trust your upstream (your own node, a vendor you pay
  for SLA-ed responses). The marginal trust gain is near-zero.
- Your use case needs archive data, traces, big `eth_getLogs`. Helios
  can't serve those.
- You're on a free-tier vendor. You'll burn your quota on
  `eth_getProof` calls; pay up or skip Helios.
- You're serving high-volume traffic. Helios is not built for
  thousands of RPS. Run a full node instead.

## Architecture: where Helios goes

```text
                                    ┌─ public rpc.*       ──▶ eRPC ──▶ vendors   (fast, not verified)
          public clients ──▶ Traefik┤
                                    └─ ENS browse *.eth.* ──▶ dweb-proxy
                                                              │ DWEB_ETH_RPC=http://helios:8545
                                                              ▼
                                                           helios :8545
                                                              │ verifies via beacon chain
                                                              ▼
                                                           eRPC or vendor (needs eth_getProof)
```

Key decisions:

- **Helios is internal.** Backend network only; never Traefik-routed.
- **One upstream, not many.** Helios has a single `--execution-rpc`
  flag. If you want failover, point it at eRPC (which itself fans out
  to vendors). If you want simplicity, point it at one vendor.
- **Checkpoint URL is separate from execution RPC.** Beacon state, not
  execution state. One-time bootstrap + periodic sync-committee
  updates.

## Config: the three flags that matter

```yaml
command:
  - ethereum
  - --network=mainnet
  - --execution-rpc=${HELIOS_EXECUTION_RPC} # your proof source
  - --checkpoint=${HELIOS_CHECKPOINT} # weak-subjectivity anchor
  - --rpc-bind-ip=0.0.0.0
  - --rpc-port=8545
```

Everything else is optional. Don't over-tune a light client — it's
already as small as it gets.

## Debugging

```bash
# Did Helios bootstrap from checkpoint?
docker logs spirens-helios | grep -i 'checkpoint\|consensus'

# Is it keeping up with the head?
docker logs spirens-helios --tail=20 | grep -i 'head\|synced'

# Does a direct RPC call work?
docker exec spirens-dweb-proxy \
  wget -qO- --post-data='{"jsonrpc":"2.0","id":1,"method":"eth_chainId","params":[]}' \
  --header='Content-Type: application/json' http://helios:8545
# expect: {"jsonrpc":"2.0","id":1,"result":"0x1"}

# Does it pass through a typical ENS call?
docker exec spirens-dweb-proxy \
  wget -qO- --post-data='{"jsonrpc":"2.0","id":1,"method":"eth_call","params":[{"to":"0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e","data":"0x0178b8bf93cdeb708b7545dc668eb9280176169d1c33cfd8ed6f04690a0bcc88a93fc4ae"},"latest"]}' \
  --header='Content-Type: application/json' http://helios:8545
```

If Helios returns but dweb-proxy still fails, check that `DWEB_ETH_RPC`
is actually set in `.env` and the container picked it up:

```bash
docker inspect spirens-dweb-proxy | grep ETH_RPC_ENDPOINT
```

## Worked example: SPIRENS

SPIRENS ships Helios as opt-in under `compose/single-host/optional/`
and `compose/swarm/optional/`. See:

- [`docs/helios.md`](../docs/helios.md) — full architecture, activation
  walkthrough, failure modes.
- `compose/single-host/optional/compose.helios.yml.example` — working
  single-host compose; copy to `compose.helios.yml` and include.
- `compose/swarm/optional/stack.helios.yml.example` — swarm variant
  with placement constraint.

The `.env.example` `HELIOS_*` section lists the two URLs you need
(`HELIOS_EXECUTION_RPC`, `HELIOS_CHECKPOINT`) plus the `DWEB_ETH_RPC`
flip.

## Upstream references

- [a16z/helios](https://github.com/a16z/helios) — source, releases,
  roadmap.
- [Helios announcement post (a16z crypto)](https://a16zcrypto.com/posts/article/building-helios-ethereum-light-client/)
  — the "why" and the design principles.
- [Ethereum light-client specs](https://github.com/ethereum/consensus-specs/tree/dev/specs/altair/light-client)
  — the Altair light-client protocol Helios implements.
- [eth-clients checkpoint sync endpoints](https://eth-clients.github.io/checkpoint-sync-endpoints/)
  — active mainnet checkpoint providers.
