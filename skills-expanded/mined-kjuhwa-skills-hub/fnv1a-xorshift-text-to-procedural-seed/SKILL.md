---

name: fnv1a-xorshift-text-to-procedural-seed
description: Deterministically turn any user text into repeatable procedural layouts using FNV-1a + xorshift32.
category: algorithms
triggers:
  - fnv1a xorshift text to procedural seed
tags: [algorithms, fnv1a, xorshift, text, procedural, seed]
version: 1.0.0
---

# fnv1a-xorshift-text-to-procedural-seed

Small front-end generators (constellation makers, avatar forges, dungeon layouts) often need "same string ⇒ same picture" without pulling in a crypto/seedrandom lib. The pipeline is two 10-line helpers: FNV-1a to collapse the string into a 32-bit seed, then xorshift32 as the PRNG that consumes it. Both are branch-free, allocation-free, and ~one screen of code, so they drop into any zero-dep HTML app.

```js
function hashSeed(s) {
  let h = 2166136261 >>> 0;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619) >>> 0;
  }
  return h;
}
function rngFrom(seed) {
  let s = seed | 0 || 1;
  return () => { s ^= s << 13; s ^= s >>> 17; s ^= s << 5;
                 return ((s >>> 0) % 100000) / 100000; };
}
const rng = rngFrom(hashSeed(userText));
// use rng() wherever you'd use Math.random() — picks stay stable across reloads
```

Wire it so *every* stochastic choice reads from this one `rng()` — positions, names, arm count, jitter — and the whole output becomes a pure function of the input text. Derive secondary things (name = `ROOTS[⌊rng()·N⌋] + EPITHETS[…]`, arm count = `seed % 3 + 2`) from the same seed so recalling a past entry only needs to store the string or the 32-bit seed. Guard `s |= 0 || 1` because xorshift32 locks at zero. Avoid `Math.random()` *anywhere* in the generation path or replays silently diverge.
