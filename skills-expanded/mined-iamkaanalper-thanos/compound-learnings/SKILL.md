---
name: compound-learnings
description: Grok-native self-improvement flywheel. Analyzes past /implement and /execute-plan runs via the existing memory system, extracts patterns with real consolidation, and proposes high-quality, ready-to-apply improvements (rules, persona updates, small skills).
keywords: [self-improvement, learning, compound, patterns, memory, rules, evolution]
---

# compound-learnings (Grok Edition) — v2

This skill turns the passive memory from `/implement` and `/execute-plan` into an **active compounding engine**.

It is the Grok-native implementation of the powerful self-improvement loop from the Claude side (`compound-learnings`, `continuous-learning-v2`, `skill-evolution`).

## Current State (Advanced + Generation)

- **Semantic clustering support** (when available)
- **Multi-signal Impact + Priority Scoring** using recent run data (friction, security involvement, etc.)
- **Strong Meta-Pattern Detection** with concrete recommendations
- **Artifact Generation & Application**:
  - `--draft`: Generates real, reviewable draft files for High-impact proposals (safe location).
  - `--apply`: Carefully applies previously generated High-impact drafts.
  - Shows unified diff for persona changes before asking for confirmation.
  - Clear "New file" preview for rule creation.
  - Always creates timestamped backups before touching real files.
  - Philosophy: **Review the diff → Confirm per change → Safe apply with backup**.

This makes the self-improvement loop significantly more practical and trustworthy.

This moves the skill from "analysis + suggestions" toward a true **self-improvement flywheel** that can propose and materialize improvements.

## Core Idea

Grok has one of the best passive memory systems among AI coding setups (`memory.py` + workspace-scoped, locked, compacted pattern files).

This skill makes that memory **active and compounding**:
- Read the real data from past runs
- Consolidate noisy variations into general principles
- Detect when a pattern is important enough to become permanent capability
- Generate ready-to-review proposals with actual content you can use

## How It Works Now

### 1. Data Source (Unchanged — Excellent Foundation)
```bash
python3 ~/.grok/bundled/skills/implement/scripts/memory.py snapshot
```

### 2. Consolidation (New in v2)
The analyzer now performs:
- Aggressive but safe text normalization
- Synonym handling (`null check` ≈ `undefined guard` ≈ `missing None check`)
- Keyword-overlap + substring clustering
- Proper count merging

Result: "Missing null check on userId" and "No undefined guard on input parameter" become one clean pattern.

### 3. Proposal Generation (Significantly Improved)
Every proposal now includes:
- Clean pattern name
- Real occurrence count + confidence
- Contextual rationale (why this matters *in Grok's current system*)
- Concrete draft content (copy-paste ready)
- Precise list of files that should be modified

### 4. Meta-Pattern Detection (New Powerful Feature)
When 3+ patterns fall into the same category with high total volume, the analyzer surfaces a **meta opportunity**:

> "Instead of fixing these 6 separate patterns one by one, create **one strong artifact** that raises the bar for the entire category."

This is one of the highest-leverage behaviors in self-improving AI coding systems.

## Usage

```bash
# Basic analysis (recommended starting point)
python3 ~/.grok/skills/compound-learnings/scripts/analyze.py --min 3

# JSON output (for further processing or agents)
python3 ~/.grok/skills/compound-learnings/scripts/analyze.py --min 3 --json
```

## Current Capabilities (v2)

| Capability                    | Status     | Notes |
|-------------------------------|------------|-------|
| Read from existing memory     | Excellent  | Uses the production `memory.py` |
| Pattern normalization         | Strong     | Handles most common review phrasing variations |
| Clustering & count merging    | Good       | Keyword overlap + normalization |
| Artifact type classification  | Good       | Context-aware (persona vs rule vs security) |
| Draft content generation      | Strong     | Actually useful copy-paste content |
| Rationale quality             | Strong     | References current Grok artifacts (personas, handoff, etc.) |

## Design Principles

- Prefer **one high-leverage change** (strong rule or persona constraint) over ten small rules.
- High signal threshold — we deliberately produce fewer, better proposals.
- Everything must be generalizable across projects.
- Human stays in the loop (we propose, you decide and apply).

## Relationship to Other Work

This skill directly feeds and improves:
- `personas/implementer.md`, `reviewer.md`, `security-auditor.md`
- `~/.grok/rules/` directory
- `role-assignment.md`
- `handoff` skill templates
- Future small skills

It is currently the most direct way to make Grok **permanently better** at software engineering work over time.

## Automatic Integration (New)

The output of this analyzer (when run with `--draft`) is now **automatically embedded** into the Final Report of both primary orchestrators:

- `/implement` → Final Report always contains a "Compound Learnings & Self-Improvement Proposals" section with the full captured analysis + draft paths.
- `/execute-plan` → Same treatment for large plan executions.

This means every serious coding run now ends with a permanent, reviewable record of "what the system learned about itself this time" — exactly the compound flywheel the user requested. No manual invocation needed for the analysis step; the orchestrators drive it.

---

## Faz 2 İyileştirmeleri (Aktif Geliştirme)

Faz 2 kapsamında yapılan ilk teknik iyileştirmeler:

- High friction pattern extraction güçlendirildi:
  - 3+ round review'lar artık daha ağır friction sinyali olarak değerlendiriliyor.
  - Security'li run'larda 2+ round bile friction olarak kabul ediliyor (güvenlikte friction daha kritik).
  - Friction bonusu scoring'de 25 → 30 olarak yükseltildi.

- compound-learnings artık review sonuçlarından gelen friction sinyallerini daha iyi değerlendirecek şekilde evriliyor.

- Basit friction ledger (`~/.grok/compound-friction.jsonl`) oluşturulmaya başlandı. Analyzer her çalışmasında yüksek friction pattern'leri buraya append ediyor.

- Review skill'i artık bittikten sonra otomatik olarak compound analyzer'ı hafif modda çağırıyor (`--source review`).

- 3 ana persona'ya (implementer, reviewer, security-auditor) "Önceki Friction Pattern'leri Kontrol Et" maddesi eklendi.

Bu iyileştirmeler, Claude tarafındaki "monster cross-training" mantığına doğru atılan ilk somut adımlardır.

---

## Daha Proaktif Kullanım Önerileri (Faz 2)

compound-learnings sistemini sadece implement/execute-plan sonuyla sınırlı tutmayın. Aşağıdaki noktalarda da manuel veya otomatik tetiklenmesi önerilir:

- **Review bittikten sonra** (zaten otomatik olarak yapılıyor)
- **Design / plan oluşturma** bittikten sonra (özellikle büyük mimari kararlar)
- **Yüksek riskli değişiklik** öncesi (auth, payment, core data model değişiklikleri)
- **Birden fazla round review** yaşayan bir iş sonrası (friction yüksekse)
- **Güvenlik audit** sonrası (security-auditor bulguları sonrası)

Öneri komutları:
```bash
# Genel
python3 ~/.grok/skills/compound-learnings/scripts/analyze.py --min 3 --draft

# Review sonrası (düşük eşik)
python3 ~/.grok/skills/compound-learnings/scripts/analyze.py --min 2 --source review
```

Gelecekte bu tetiklemelerin bir kısmı hook veya orchestrator seviyesinde otomatikleştirilebilir.

## Limitations (Still Honest)

- Only looks at `implement` / `execute-plan` memory for now (the richest data source)
- No semantic embeddings yet (purely rule + keyword based)
- Does not auto-apply changes (by design)

---

## Faz 2: Self-Improvement Loop'un Olgunlaştırılması (Başlangıç)

Bu bölüm, Faz 1'in (Orchestration Disiplini + Assignment Matrix + Bounded QA-Loop) tamamlanmasının ardından gelen **Faz 2** çalışmasının başlangıcını işaret eder.

**Faz 2 Hedefleri (Öncelik Sırasıyla):**

1. **Veri Kaynağını Genişletmek**
   - Review sonuçlarını (özellikle friction yaratan bulguları) daha iyi değerlendirmek.
   - Security audit bulgularını, uzun fix cycle'larını ve tekrar eden pattern'leri daha güçlü sinyal olarak kullanmak.

2. **Friction & Cross-Training Sinyallerini Güçlendirmek**
   - Claude tarafındaki "monster" mantığına doğru ilk adımlar:
     - Yüksek friction yaratan pattern'leri (3+ round review, güvenlik bulgusu, aynı kategoride tekrar eden sorun) sistematik olarak izlemek.
     - Bu pattern'leri sadece öneri olarak değil, persona'lara ve kurallara daha proaktif şekilde yansıtmak.

3. **Daha Otomatik & Proaktif Compound Öğrenme**
   - Sadece implement/execute-plan sonunda değil, review ve yüksek riskli işler sonrası da otomatik/lightweight tetikleme.
   - Draft önerisi üretimini daha sık ve düşük eforlu hale getirmek.
   - "High friction" pattern'ler için otomatik meta-pattern önerisi.

4. **Basit Skill Evolution Başlangıcı**
   - Pattern'lere basit scoring (güven + etki + friction) ekleyerek, hangi önerilerin daha hızlı kristalleşeceğini belirlemek.

**Bu Fazda Yapılmayacaklar (Kasıtlı):**
- Tam hook ekosistemi kurmak (Grok'un mevcut yapısına uymuyor, daha sonra değerlendirilecek).
- 130+ agent kopyalamak.
- Memory Palace gibi ağır mimari değişiklikler (mevcut memory.py + compound pipeline üzerine inşa edeceğiz).

**İlk Somut Adımlar (Bu Tur ve Sonraki):**
- Review friction sinyallerini analyzer'a daha iyi entegre etmek.
- compound-learnings'in tetiklenme kapsamını genişletmek (review sonrası otomatik hafif analiz önerisi).
- Friction ledger benzeri basit bir izleme mekanizması tasarlamak (dosya veya basit yapı).

---

This is how Grok develops its own version of the "monster cross-training + continuous learning" loop that made the Claude side so effective.

**Faz 2 şu anda aktif olarak geliştirilmektedir.**