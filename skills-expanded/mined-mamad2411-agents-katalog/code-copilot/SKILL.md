---
name: code-copilot
description: Pure routing skill for implementation code in the TDD/ATDD pipeline — Claude (the orchestrating/main agent) must NEVER write or edit code files itself in this workflow. Runs AFTER test-copilot (test-first — green step): the failing tests already exist, this skill dispatches a Haiku sub-agent to write the implementation that makes them pass. It converts atdd.md/test_diff.md into a self-contained task prompt for the Agent tool (model: haiku), then reads and verifies the result. Test files are NEVER written or edited here — that's test-copilot's job, already done. The orchestrating Claude only builds the prompt, dispatches the sub-agent, reads the result, and writes a report; it never authors a single line of the feature code itself.
---

# code-copilot — implementation routing only, no authoring

> **Adı tarihsel.** Yazma işi artık Codex CLI'da veya Aider'da değil, bir
> Haiku alt-ajanında (`Agent` tool, `model: "haiku"`) yapılıyor 
> kararıyla Codex bridge (`/path/to/your/codex_bridge.py`) ve `aider-bridge`
> bu skill'den kaldırıldı. Skill adı, boru hattının her yerinden referans
> verildiği için değiştirilmedi.

> **GİT YASAĞI .** Aynı gün bir Haiku
> alt-ajanı görevi bittikten sonra kendiliğinden `git add`/`git commit`
> çalıştırdı — hem onaysız bir commit oluşturdu (kullanıcının açık onayı
> olmadan, `commit` skill'inin kuralını ihlal ederek) HEM DE bu sırada
> `test-copilot`'un yazdığı red-step test dosyalarını (hiç commit'e
> alınmamış, sadece dosyada duran değişiklikler) sildi/geri aldı —
> kurtarılamaz veri kaybı. Bu yüzden her dispatch prompt'unun (adım 2)
> SONUNA şu satır MUTLAKA eklenir:
> "GİT KOMUTU ÇALIŞTIRMA — add/commit/checkout/reset/restore/stash dahil
> hiçbir git komutu kullanma. Sadece dosya içeriğini Write/Edit ile
> değiştir. Commit tamamen ayrı, kullanıcı onaylı bir adımda yapılır."

## Kullanılacak destek skiller
- `caveman`, `ponytail` (full) — her zaman aktif.
- `superpowers:subagent-driven-development` — implementasyon çok dosyalıysa, birden fazla Haiku alt-ajan çağrısına bölmek için.
- `handoff` (opsiyonel) — session iş bitmeden kapanırsa HANDOFF.md yaz.

## Why this exists
On this pipeline, the orchestrating Claude is only allowed to route — never
to author code files with `Write`/`Edit` itself. The actual authoring
happens in a dispatched `Agent` tool call pinned to `model: "haiku"`. This
skill is the bridge for the **implementation** side of an ATDD task; it
replaces both the old Codex-bridge flow and the `aider-bridge` skill .

Two decisions worth knowing before using this:
- **Code and tests are deliberately SEPARATE calls, in separate skills, test-first.**
  `test-copilot` dispatches its own Haiku sub-agent to write failing test
  files first (red), targeting atdd.md directly since no implementation
  exists yet; `code-copilot` (this skill) dispatches a fresh Haiku sub-agent
  for the implementation afterward, targeting those tests (green). Each
  call stays focused on one concern — easier to review, and if only one side
  needs a retry, you re-run only that call instead of redoing both.
- **The model is always pinned explicitly — and this is load-bearing.**
  Pass `model: "haiku"` on every `Agent` call in this skill — never omit it
  (an omitted `model` inherits the orchestrator's own model, which defeats
  the point: cost drift and the orchestrator quietly authoring code through
  a "sub-agent" wrapper).
- **The sub-agent has no memory of this conversation.** It starts cold —
  the task prompt built in step 2 must be fully self-contained (absolute
  project root, exact file paths, full Acceptance Criteria text, CAVEMAN
  rules). Don't write "as discussed" or "per the plan above" — the
  sub-agent never saw the plan.
- **No Gemma/NVIDIA review gate.** That gate depended on a third-party API
  that turned out unreliable in practice. Review is the orchestrating
  Claude reading the sub-agent's result directly — not authoring, so it
  doesn't conflict with the "orchestrator can't write code" rule.

## Precondition
Both must exist under the same `<task-slug>`:
- `obss_project/artifacts/<task-slug>/atdd.md`
- `obss_project/artifacts/<task-slug>/test_diff.md` (written by `test-copilot`)

If either is missing, say so and point at the missing skill — don't write
implementation code against tests that don't exist yet.

## Steps

### 1. Confirm atdd.md ve test_diff.md var, mutlak yolları çıkar
Sadece dosyaların varlığını ve mutlak proje kökünü doğrulamak için `Read`
et — **içeriği prompt'a kopyalamak için DEĞİL**. Token tasarrufu: alt-ajan
zaten `Read` yetkisine sahip, tam AC/sözleşme metnini burada (orkestratörün
kendi bağlamında) tekrar üretmek gereksiz — dosya yolunu ver, alt-ajan
kendi (ayrı, ucuz) bağlamında okusun.

### 2. Build the sub-agent task prompt
Assemble one self-contained prompt — ama AC/sözleşme metnini İNLİNE KOPYALAMA,
sadece dosya yollarını ve neyi okuyup neye odaklanacağını söyle (sub-agent
kendi Read'ini yapacak):

```
Proje kökü (MUTLAK yol): <ABSOLUTE PROJECT ROOT>
Değiştirilecek/oluşturulacak dosyalar: <implementation file paths, absolute>
Dokunma: <test dosyaları — bunlar zaten yazıldı, ASLA değiştirme>

## Görev
Önce şu dosyaları Read et: <atdd.md mutlak yolu>, <test_diff.md mutlak yolu>.
atdd.md'deki "User Story", "Acceptance Criteria" ve "Davranış Sözleşmesi"
bölümlerine göre implementasyonu yaz. test_diff.md'deki test dosyalarını
YEŞİLE çevirmen gerekiyor — bu testleri OKU ama DEĞİŞTİRME.

## CAVEMAN İlkeleri (zorunlu)
Implement only what the Acceptance Criteria require.
Prefer: the smallest implementation, the fewest files, the fewest
abstractions, the fewest helper functions, explicit code, existing
project patterns.
Never: introduce speculative architecture, optimize for future
requirements, create extension points, add unnecessary configuration,
create utilities "just in case", split files without a real reason.
If two implementations satisfy the Acceptance Criteria, always choose
the simpler one.

## Definition of Done
- Every Acceptance Criterion implemented, none partially.
- No out-of-scope functionality.
- No TODO/FIXME/placeholder/dead code/unused helpers.
- Existing project conventions and structure respected.
- No unnecessary files, abstractions, or public APIs.
- Existing behavior outside these Acceptance Criteria unchanged.

## Rapor formatı (yanıtının sonunda)
1. Oluşturulan dosyalar.
2. Değiştirilen dosyalar.
3. Her Acceptance Criteria için nasıl karşılandığı.
4. Kalan sınırlamalar (varsa).
5. Varsayımlar (varsa).
6. CAVEMAN self-review: yeni dosya/soyutlama/yardımcı fonksiyon var mı, her
   biri için kısa gerekçe.

## GİT KOMUTU ÇALIŞTIRMA
add/commit/checkout/reset/restore/stash dahil hiçbir git komutu kullanma.
Sadece dosya içeriğini Write/Edit ile değiştir. Test dosyalarına ASLA
dokunma (silme/geri alma dahil). Commit tamamen ayrı, kullanıcı onaylı bir
adımda yapılır — bu senin işin değil.

## ARAMA KAPSAMI
Grep/Glob/Bash ile arama yaparken HER ZAMAN yukarıdaki proje kökü ile
sınırlı kal. Bu ortamda git reposunun kökü proje klasöründen daha geniş
(örn. ev dizini) olabilir ve devasa bir geçmiş taşıyabilir — kök dizinden
veya parametresiz geniş kapsamda arama RAM'i tüketip yanıt vermeyebilir.
```

Use atdd.md's own wording for Acceptance Criteria — anything you add here
that isn't in atdd.md is scope you invented, not scope the user approved.

### 3. Dispatch the Haiku sub-agent
```
Agent({
  description: "Implement <task-slug> (green step)",
  subagent_type: "general-purpose",
  model: "haiku",
  run_in_background: false,
  prompt: "<the full self-contained prompt from step 2>",
})
```
Run in the foreground (`run_in_background: false`) — the very next step
(step 4's review) depends on its result and nothing else useful happens
meanwhile. Tell the user before this call that it's the real authoring
step — **make it once**, not speculatively; get the file list and project
root right first.

If the implementation spans clearly independent files/modules, `superpowers:subagent-driven-development`
may split this into multiple parallel Haiku dispatches instead of one —
only do this when the split is genuinely independent, not by default.

### 4. Clean up and verify — never trust the sub-agent's own summary
- Run `git status --short <dir>` (or list the target dir) on the REAL
  project files first — confirm something actually changed on disk before
  reading further. An empty/unexpected result means the sub-agent's prompt
  had a wrong/relative project root; fix the prompt and re-dispatch — don't
  assume files landed somewhere else and reuse them, they were written
  against the wrong file context.
- `Read` the files the sub-agent touched. Check each Acceptance Criteria
  from atdd.md against what's actually there — this is read-only review,
  not authoring. The sub-agent's own summary ("I've successfully
  implemented...") is a claim, not evidence — the `Read` is the evidence.
- Check the result against **Definition of Done** (step 2): any TODO/FIXME/
  placeholder/dead code/unused helper, any file or abstraction without a
  stated justification, or any out-of-scope addition is a finding — don't
  silently accept it, dispatch another Haiku sub-agent with a sharper
  prompt naming exactly what to remove/simplify.
- Confirm no test file was touched — `test-copilot`'s tests are the fixed
  target, not something this step may adjust to make green.
- Write `obss_project/artifacts/<task-slug>/code_diff.md`, built from the
  sub-agent's own summary plus what `Read` actually confirmed. This is a
  report, not code, so `Write` is fine here.

### 5. Hand off to verify
Tell the user the implementation is done (green — tests from `test-copilot`
should now pass) and the next step is the `verify` skill, which actually
runs the tests and the rest of the quality gates (refactor step relies on
that run being green first).

Eğer değişiklik bir rendered web UI dosyasına (`.html`, `.tsx`, `.jsx`,
sayfa bileşeni, CSS) dokunduysa bunu açıkça söyle — `verify`'ın gate 11'i
(`vision-test`) bu durumda N/A değil aktif çalışmalı, atlanmamalı.

## The one rule that can't bend
Every line of implementation code comes from the dispatched Haiku
sub-agent, never from the orchestrating Claude directly. If something looks
wrong after step 4's review, the fix is dispatching another `Agent` call
with a sharper prompt — not `Edit`-ing the file directly, even for "just a
typo" or "just one line."
