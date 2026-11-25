---
name: algo-dfa-matching
description: "Build a DFA transition table via the KMP prefix function, then scan text in O(n) with zero backtracking. Use when repeatedly searching one fixed pattern (motif, restriction site, primer) against many sequences or texts."
tool_type: python
primary_tool: Python
---

# DFA-Based Pattern Matching

## When to Use

- Searching the same fixed pattern (a motif, restriction site, primer, or start codon) against **many** different texts/sequences — build the DFA once, reuse it everywhere.
- You need a hard guarantee of no backtracking on the text pointer (streaming/online matching, where re-reading input isn't possible).
- Teaching/explaining *why* KMP works — the DFA is the "unrolled" state machine that the KMP failure-link trick simulates lazily.
- The alphabet is small and fixed (DNA: `ACGT`, protein: 20 letters) so the `O(m·|Σ|)` build cost is cheap.
- Not the right tool for: searching many different patterns against one text (use `algo-aho-corasick`), or a huge/unbounded alphabet (use KMP instead, see `algo-kmp-algorithm`).

## Version Compatibility

Pure Python standard library only — no third-party dependencies. Works unchanged on Python ≥ 3.8 (uses only `list`/`dict` and `str` slicing; the `list[int]` / `dict[int, dict[str, int]]` type hints require Python ≥ 3.9 or `from __future__ import annotations` on 3.8).

## Prerequisites

- No packages to install.
- Prior concept: the KMP prefix (failure) function — see `algo-kmp-algorithm` — since `build_dfa` reuses it to compute fallback transitions.

## How It Works

Build a DFA with `m+1` states where **state i** = "matched the first i characters of the pattern". State `m` is accepting. The transition function `δ(state, char)` gives the length of the longest prefix of the pattern that is a suffix of `pattern[:state] + char`.

## vs KMP

| | DFA | KMP |
|--|-----|-----|
| Build | O(m·\|Σ\|) | O(m) |
| Search | O(n) | O(n) |
| Space | O(m·\|Σ\|) | O(m) |
| Backtracking | None (table lookup) | Via failure links |
| Multi-text reuse | Ideal (precomputed table) | Rebuild failure links per pattern (cheap, but still work) |

Use DFA when you search one pattern against many texts and want table-lookup speed. Use KMP to save memory or when you only search once.

**Goal:** find every (possibly overlapping) occurrence of `pattern` in `text` with a single linear pass and no re-reading of `text`.
**Approach:** compute the KMP prefix function once, use it to fill in a full `state × alphabet` transition table, then drive the search with pure table lookups.

```python
def compute_prefix_function(pattern: str) -> list[int]:
    """KMP prefix (failure) function: pi[i] = length of the longest proper
    prefix of pattern[:i+1] that is also a suffix of it."""
    m = len(pattern)
    pi = [0] * m
    k = 0
    for i in range(1, m):
        while k > 0 and pattern[i] != pattern[k]:
            k = pi[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        pi[i] = k
    return pi


def build_dfa(pattern: str, alphabet: str) -> dict[int, dict[str, int]]:
    """Build the DFA transition table for exact matching of `pattern`.

    dfa[state][ch] = next state after reading `ch` while in `state`.
    Time/space: O(m * |alphabet|).
    """
    m = len(pattern)
    pi = compute_prefix_function(pattern)
    dfa: dict[int, dict[str, int]] = {}

    for state in range(m + 1):
        dfa[state] = {}
        for ch in alphabet:
            if state < m and ch == pattern[state]:
                dfa[state][ch] = state + 1
            else:
                # fall back using the prefix function, mirroring KMP's
                # failure-link traversal
                k = state
                while k > 0:
                    k = pi[k - 1]
                    if k < m and ch == pattern[k]:
                        k += 1
                        break
                    if k == 0:
                        k = 1 if ch == pattern[0] else 0
                        break
                dfa[state][ch] = k

    return dfa


def dfa_search(text: str, pattern: str, alphabet: str) -> list[int]:
    """Return 0-based start positions of every (possibly overlapping)
    occurrence of `pattern` in `text` using a precomputed DFA."""
    if not pattern:
        return []
    m = len(pattern)
    dfa = build_dfa(pattern, alphabet)
    state = 0
    results = []
    for i, ch in enumerate(text):
        state = dfa[state].get(ch, 0)  # unknown chars: fall back to state 0
        if state == m:
            results.append(i - m + 1)
    return results
```

**Goal:** amortize the DFA build cost by reusing it across many texts (e.g. scanning a restriction-site motif against thousands of reads).
**Approach:** build once, then call a lightweight scan function per text.

```python
def scan_many(texts: list[str], pattern: str, alphabet: str) -> dict[str, list[int]]:
    """Search `pattern` across multiple `texts`, building the DFA only once.

    Returns a dict mapping each text to its list of match start positions.
    """
    dfa = build_dfa(pattern, alphabet)
    m = len(pattern)
    hits: dict[str, list[int]] = {}
    for text in texts:
        state = 0
        positions = []
        for i, ch in enumerate(text):
            state = dfa[state].get(ch, 0)
            if state == m:
                positions.append(i - m + 1)
        hits[text] = positions
    return hits
```

## Example

```text
Pattern: "ABABC"   Text: "ABABABC"

State: 0→1→2→3→4→3→4→5
                  ↑
          δ(4,'A')=3 (fell back; "ABAB"+"A" → suffix "ABA" = pattern[:3])

Match at position 2: text[2:7] = "ABABC"
```

## Pitfalls

- **Alphabet must cover all text characters**: characters not in `alphabet` get no entry in `dfa[state]`; handle via `.get(ch, 0)` or enumerate the actual text to build the alphabet.
- **Build is O(m × |Σ|), not O(m)**: for large alphabets (Unicode), this is expensive — prefer KMP or Aho-Corasick.
- **State m is accepting but search continues**: after reaching state m, the DFA naturally transitions to the correct fallback state to find overlapping matches — do not reset to 0.
- **Empty pattern edge case**: `m=0` means every position matches; handle before building the DFA.
- **Fallback loop in build**: the while loop mirrors KMP's failure-link traversal; an off-by-one in the `pi` index (`pi[k-1]` vs `pi[k]`) silently produces wrong transitions.
- **Rebuilding per text wastes the whole point of DFA**: if you find yourself calling `build_dfa` inside a loop over texts, switch to `scan_many`-style reuse or just use plain KMP.

## See Also

- `algo-kmp-algorithm` — the failure-function algorithm this DFA is built from; use it instead when memory matters or you search only once.
- `algo-aho-corasick` — multi-pattern generalization of this same automaton idea.
- `bio-restriction-analysis-restriction-sites` — applies fixed-motif scanning like this to restriction enzyme recognition sites.
- `bio-sequence-manipulation-motif-search` — higher-level motif search over `Seq` objects, often backed by exactly this kind of automaton.
