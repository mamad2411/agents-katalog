---

name: gossip-round-rng-seeded-reproducible-sim
description: Seed a PRNG per gossip round so randomized peer selection is reproducible across replays and snapshots.
category: algorithms
triggers:
  - gossip round rng seeded reproducible sim
tags: [algorithms, gossip, round, rng, seeded, reproducible]
version: 1.0.0
---

# gossip-round-rng-seeded-reproducible-sim

Gossip / anti-entropy simulations pick random peers each round, which makes bugs ("why did replica 3 never converge?") un-reproducible and snapshot/step-back features impossible. The pattern: derive a per-round seed deterministically from `(sessionSeed, roundNumber)` using a cheap mixer (splitmix64 or `hash(seed ^ round)`), instantiate a fresh PRNG from that seed, and use **only** that PRNG for peer selection, fanout sampling, and message-drop coin flips within the round. Any round can then be replayed in isolation, and scrubbing a timeline slider re-derives the exact same peer choices.

```js
function roundRng(sessionSeed, round) {
  let s = (sessionSeed ^ Math.imul(round, 0x9E3779B9)) >>> 0;
  return () => { s = Math.imul(s ^ (s >>> 16), 0x85EBCA6B) >>> 0;
                 s = Math.imul(s ^ (s >>> 13), 0xC2B2AE35) >>> 0;
                 return ((s ^= s >>> 16) >>> 0) / 2**32; };
}
```

This generalizes far past gossip: any stepwise simulation with randomness (chaos injection, load balancers, scheduler jitter, Monte Carlo demos) benefits from per-step seeding over a single global PRNG, because a global PRNG's state depends on *how many* random calls happened before, which breaks when you add a feature that consumes one extra random number.
