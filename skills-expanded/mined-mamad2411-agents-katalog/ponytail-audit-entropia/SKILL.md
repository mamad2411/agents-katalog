---
name: ponytail-audit-entropia
description: >
  Entropia'da repo geneli over-engineering denetimi. Upstream ponytail-audit'in
  yöntemini kullanır ama ponytail-entropia'daki PAZARLIKSIZ override listesini
  önce okur ve o alanlardaki bulguları bastırır. "codebase'i denetle", "neyi
  silebiliriz", "bloat bul", "fazla mühendislik var mı", "/ponytail-audit"
  dendiğinde bu skill kullanılır — Entropia deposunda çıplak ponytail-audit
  KOŞTURULMAZ. Tek seferlik rapor, hiçbir şey değiştirmez.
argument-hint: "[backend|frontend|scripts|<yol>]"
license: MIT
---

# ponytail-audit — Entropia sarmalayıcısı

Yöntem: `ponytail-audit` (upstream v4.9.0, vendored). Etiketler (`delete:`,
`stdlib:`, `native:`, `yagni:`, `shrink:`) ve çıktı biçimi aynen geçerli.
**Bu dosya üstüne gelen kısıttır.**

## 1. Önce override'ı oku — ZORUNLU

`.claude/skills/ponytail-entropia/SKILL.md` §"Entropia override" tablosunu oku.
O tablo **tek otoritedir ve buraya kopyalanmaz** (kopya ayrışır). Tablodaki her
alan denetim dışıdır: bulgu üretme, "ranked list"e koyma, `net: -N lines`
sayısına katma.

## 2. Upstream sezgisi → Entropia'da neye çarpar

Upstream §Hunt'ın altı ifadesi bu repoda **doğrudan adjudicated karara** çarpar.
Bir bulgu bunlardan birine denk geliyorsa **bastır**:

| Upstream ne arıyor | Entropia'da denk geldiği şey | Karar |
|---|---|---|
| *single-implementation interfaces* | `commands/` · `queries/` · `domain/` · `routes/` katman ayrımı | mandated desen — bastır |
| *wrappers that only delegate* | `reconcile_occ_tokens`, `run_idempotent`, `assert_supported_source_file` | tek-kural noktaları; route'a kopyalanmasın diye varlar — bastır |
| *files exporting one thing* | modül-seviyesi tek async command deseni | mandated desen — bastır |
| *dead flags and config* | `SHARED_ALLOCATION_STATUS = future_dev` (containment KAPALI) | bilerek duruyor — bastır |
| *`delete:` tekrar* | O-30 purge gövdesi: `deletion_state` **+** `root_lifecycle_state` | adjudicated, ikisi birlikte döner — bastır |
| *`shrink:` birleştir* | `ErrorBody`: `suggested_action` (makine) + `remediation` (insan) | ayrı alanlar; birleştirmek birini kaybettirir — bastır |

Ayrıca hiç bulgu üretme: coverage kapısı ve test altyapısı (`--cov-fail-under=90`,
L1 FK insert-order proof, alembic up/down/up, `scripts/schema_parity_gate.py`),
typed response zorunluluğu, trust boundary validation, güvenlik, erişilebilirlik,
kapanış ritüeli çıktıları (handoff / kickoff / `PROJECT_HISTORY.md` / codemap).

## 3. Kapsamı daralt — maliyet kapısı

Depo 488 dosya / ~114k satır; CLAUDE.md cost-conscious. **Tüm ağacı tarama.**
Argüman verilmişse yalnız o alanı tara. Verilmemişse şu sırayla sor/seç ve
taradığın alanı çıktının başında yaz:

1. `scripts/` ve spec dışı tooling — **en verimli alan**, ultra seviye serbest
2. `frontend/src/` presentation katmanı — route path / react-query key / OCC token /
   Idempotency-Key / SSE taksonomisi **hariç** (bunlar presentation işinde ellenmez)
3. `backend/src/` — en düşük getiri: yüzeyin çoğu spec'in dikte ettiği şekil

Dosya okumadan önce `docs/CODEMAPS/` + `codebase-memory-mcp` kullan (kör grep yok).

## 4. Zaten ölçülmüş kalemleri yeniden "keşfetme"

K-2..K-6 ve P4-3 (60 `modify_default`, `alembic check` exit 255) **ölçüldü,
düzeltilmedi** — bunlar bilinen açık kalemdir, bulgu değil. Tekrar raporlama;
gerekiyorsa tek satırla "bilinen: P4-3" diye geç.

## 5. Çıktı

Upstream biçimi + **bastırılanı söyle**:

```
kapsam: <taranan yol>
<ranked bulgular>
net: -<N> satır, -<M> bağımlılık mümkün.
bastırıldı: <K> aday — adjudicated (override tablosu), <hangileri tek kelimeyle>.
```

Bastırılanı gizleme: sessiz kırpma "her şeyi taradım" gibi okunur. Kesecek bir
şey yoksa `Lean already. Ship.`

## Sınır

Salt-okunur, tek seferlik. Düzeltme uygulamaz. Correctness / güvenlik /
performans kapsam dışı — onlar `ecc:code-review` ve `sast-*` skill'lerinin işi.
Bir bulgunun adjudicated olup olmadığından emin değilsen **bastır ve sor** —
yanlış pozitif burada sözleşme bozar.
