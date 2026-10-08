---
name: algo-hash-tables-bloom
description: "Implement Python hash tables (chaining, open addressing, rehashing) and Bloom filters for set membership. Use when building a hash table from scratch, resolving hash collisions, sizing a Bloom filter, or checking k-mer/key set membership under memory limits."
tool_type: python
primary_tool: Python
---

# Hash Tables and Bloom Filters

## When to Use

- Implementing or explaining a hash table (dict/symbol table) from first principles instead of just using `dict`.
- Choosing between chaining and open addressing (linear/quadratic probing, double hashing) for a given workload.
- Diagnosing performance degradation caused by high load factor or a bad hash function.
- Building a memory-bounded set-membership check (Bloom filter) for large key sets — e.g. known-variant positions, seen k-mers, deduplicating reads/URLs — where a small false-positive rate is acceptable and false negatives are not.
- Sizing a Bloom filter (bits `m`, hash count `k`) for a target false-positive rate.

## Version Compatibility

- Python ≥ 3.9 (stdlib `hash()`, dict/set).
- Optional production Bloom filter: `mmh3` ≥ 4.0 (stable, non-randomized hashing) and `bitarray` ≥ 2.9 (packed bit storage).

## Prerequisites

- `pip install mmh3 bitarray` — only needed for the production Bloom filter; the educational version below uses pure Python.
- Big-O notation and amortized analysis — see `algo-complexity-analysis`.
- Basic linked lists (for chaining buckets) — see `algo-linked-lists`.

## Complexity

| Operation | Average | Worst |
|-----------|---------|-------|
| Insert / Search / Delete | O(1) | O(n) |
| Space | O(n) | O(n) |

Worst case occurs when all keys collide (pathological hash function or adversarial input).

## Hash Functions

**Goal:** map arbitrary keys to array indices `[0, table_size)`.
**Approach:** modulo hashing for ints, polynomial rolling hash for strings, multiplicative (Knuth) hashing as an alternative that avoids low-order-bit bias.

```python
def mod_hash(key: int, table_size: int) -> int:
    """Modulo hash. table_size should be prime to reduce clustering."""
    return key % table_size


def string_hash(key: str, table_size: int) -> int:
    """Polynomial rolling hash: h(s) = sum(s[i] * 31**i)."""
    h = 0
    for ch in key:
        h = h * 31 + ord(ch)
    return h % table_size


def mult_hash(key: int, table_size: int) -> int:
    """Knuth multiplicative hash using the golden-ratio conjugate."""
    A = 0.6180339887  # (sqrt(5) - 1) / 2
    return int(table_size * ((key * A) % 1))
```

## Collision Resolution

### Chaining (Separate Chaining)

Each bucket holds a linked list of `(key, value)` pairs. Load factor can exceed 1.0.

```python
class HashTableChaining:
    """Hash table using separate chaining for collision resolution."""

    def __init__(self, size: int = 7):
        self.size = size
        self.buckets: list[list] = [[] for _ in range(size)]
        self.count = 0

    def _hash(self, key) -> int:
        return hash(key) % self.size

    def put(self, key, value) -> None:
        """Insert or update a key-value pair."""
        i = self._hash(key)
        for j, (k, _) in enumerate(self.buckets[i]):
            if k == key:
                self.buckets[i][j] = (key, value)
                return
        self.buckets[i].append((key, value))
        self.count += 1

    def get(self, key):
        """Return value for key, or None if absent."""
        for k, v in self.buckets[self._hash(key)]:
            if k == key:
                return v
        return None

    def delete(self, key) -> bool:
        """Remove key. Returns True if it was present."""
        i = self._hash(key)
        for j, (k, _) in enumerate(self.buckets[i]):
            if k == key:
                self.buckets[i].pop(j)
                self.count -= 1
                return True
        return False

    def load_factor(self) -> float:
        return self.count / self.size
```

### Open Addressing Probe Sequences

```text
Linear probing:   h(key, i) = (h(key) + i) % m
Quadratic probing: h(key, i) = (h(key) + i*i) % m
Double hashing:   h(key, i) = (h1(key) + i * h2(key)) % m
                  # h2 must never return 0: h2(k) = 1 + (k % (m-1))
```

```python
class HashTableLinearProbing:
    """Hash table with linear probing and tombstone deletes."""

    DELETED = object()

    def __init__(self, size: int = 11):
        self.size = size
        self.keys = [None] * size
        self.values = [None] * size
        self.count = 0

    def _hash(self, key) -> int:
        return hash(key) % self.size

    def put(self, key, value) -> bool:
        """Insert/update via linear probing. Returns False if table is full."""
        if self.count >= self.size:
            return False
        index = start = self._hash(key)
        first_deleted = None
        while True:
            if self.keys[index] is None:
                slot = first_deleted if first_deleted is not None else index
                self.keys[slot], self.values[slot] = key, value
                self.count += 1
                return True
            if self.keys[index] is self.DELETED:
                first_deleted = first_deleted if first_deleted is not None else index
            elif self.keys[index] == key:
                self.values[index] = value
                return True
            index = (index + 1) % self.size
            if index == start:
                return False

    def get(self, key):
        """Probe forward from h(key) until key is found or an empty slot is hit."""
        index = start = self._hash(key)
        while self.keys[index] is not None:
            if self.keys[index] is not self.DELETED and self.keys[index] == key:
                return self.values[index]
            index = (index + 1) % self.size
            if index == start:
                break
        return None

    def delete(self, key) -> bool:
        """Mark slot with a tombstone rather than clearing it."""
        index = start = self._hash(key)
        while self.keys[index] is not None:
            if self.keys[index] is not self.DELETED and self.keys[index] == key:
                self.keys[index] = self.DELETED
                self.values[index] = None
                self.count -= 1
                return True
            index = (index + 1) % self.size
            if index == start:
                break
        return False
```

### Chaining vs Open Addressing

| Aspect | Chaining | Open Addressing |
|--------|----------|----------------|
| Load factor | Can exceed 1.0 | Must stay < 1.0 |
| Cache | Poor (pointer chasing) | Better (contiguous) |
| Delete | Simple | Needs tombstones |
| Clustering | None | Primary/secondary |

## Load Factor & Rehashing

- Rehash when load factor > 0.75 (chaining) or > 0.5 (open addressing).
- Double the table size (round up to the next prime) and reinsert every key.
- Amortized cost stays O(1) per operation since the occasional O(n) rehash is spread across many insertions.

```python
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    return all(n % i for i in range(3, int(n**0.5) + 1, 2))


def next_prime(n: int) -> int:
    """Smallest prime >= n; used to pick rehash-target table sizes."""
    while not is_prime(n):
        n += 1
    return n
```

## Bloom Filter

Probabilistic set: **no false negatives, possible false positives**. Optimal params: `m = -n*ln(p) / (ln 2)^2` bits, `k = (m/n)*ln 2` hash functions.

**Goal:** test set membership in O(k) time and O(m) bits, independent of key size.
**Approach:** hash each item with `k` functions (derived from two base hashes via double hashing) and set those bits; membership requires all `k` bits to be set.

```python
import math


class BloomFilter:
    """Space-efficient probabilistic set-membership filter."""

    def __init__(self, size: int = 1000, num_hashes: int = 3):
        self.size = size
        self.num_hashes = num_hashes
        self.bits = [0] * size
        self.count = 0

    def _hashes(self, item) -> list[int]:
        """Generate k indices via double hashing from two base hash values."""
        h1 = hash(item) % self.size
        h2 = (hash(str(item) + "salt") % (self.size - 1)) + 1
        return [(h1 + i * h2) % self.size for i in range(self.num_hashes)]

    def add(self, item) -> None:
        for index in self._hashes(item):
            self.bits[index] = 1
        self.count += 1

    def __contains__(self, item) -> bool:
        """False = definitely not in set. True = probably in set."""
        return all(self.bits[index] == 1 for index in self._hashes(item))

    def false_positive_probability(self) -> float:
        """Estimate current FP rate: (1 - e^(-k*n/m))^k."""
        if self.count == 0:
            return 0.0
        k, m, n = self.num_hashes, self.size, self.count
        return (1 - math.exp(-k * n / m)) ** k


def optimal_bloom_filter_params(n: int, target_fp: float) -> dict:
    """
    Compute optimal Bloom filter size (bits) and hash count for n elements
    and a target false-positive rate.
    """
    m = int(-n * math.log(target_fp) / (math.log(2) ** 2))
    k = max(1, int((m / n) * math.log(2)))
    actual_fp = (1 - math.exp(-k * n / m)) ** k
    return {"num_bits": m, "num_hashes": k, "actual_fp_rate": actual_fp, "memory_bytes": m // 8}
```

For production use (persisted or cross-process filters), replace `hash()` with `mmh3.hash(item, seed)` and pack bits with `bitarray` instead of a Python list — see Pitfalls.

### Genomics example: k-mer counting and known-variant lookup

```python
def count_kmers(sequence: str, k: int) -> dict[str, int]:
    """Count all overlapping k-mers in a DNA sequence using a hash table (dict)."""
    counts: dict[str, int] = {}
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i + k]
        counts[kmer] = counts.get(kmer, 0) + 1
    return counts


def build_variant_filter(known_positions: list[int], target_fp: float = 0.01) -> BloomFilter:
    """Build a Bloom filter of known variant positions for fast 'definitely not a variant' checks."""
    params = optimal_bloom_filter_params(len(known_positions), target_fp)
    bf = BloomFilter(size=params["num_bits"], num_hashes=params["num_hashes"])
    for pos in known_positions:
        bf.add(pos)
    return bf
```

## Pitfalls

- **Table size should be prime**: reduces clustering in modular hash functions.
- **Open addressing requires tombstones on delete**: simply clearing a slot breaks the probe chain for keys inserted after a collision at that slot.
- **Never resize a Bloom filter**: it cannot grow without a full rebuild; pre-size using `optimal_bloom_filter_params` for the expected element count.
- **Python's `hash()` is randomized per-process** (`PYTHONHASHSEED`): never persist it across runs or share it cross-process; use `mmh3` or `hashlib` for on-disk/networked structures.
- **Load factor threshold matters**: at load 0.9 with linear probing, expected probe length exceeds 5; keep load < 0.5–0.7 for open addressing, < 0.75 for chaining.
- **Bloom filters cannot delete** items (a counting Bloom filter is needed for that) and give no false negatives but arbitrarily many false positives if oversubscribed.

## See Also

- `algo-tries` — exact-match/prefix structures as an alternative to hashing strings.
- `algo-linked-lists` — underlying structure for chaining buckets.
- `algo-complexity-analysis` — Big-O background for the tables above.
- `bio-sequence-manipulation-motif-search` — k-mer/motif operations that often feed into hash-based counting.
