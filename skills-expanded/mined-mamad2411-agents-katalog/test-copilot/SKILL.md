---
name: test-copilot
description: Pure routing skill for test authoring in the TDD/ATDD pipeline — Claude (the orchestrating/main agent) must NEVER write or edit test files itself in this workflow. Runs BEFORE code-copilot (test-first — red step): no implementation exists yet, this skill dispatches a Haiku sub-agent to write failing tests against atdd.md's Acceptance Criteria. It converts atdd.md into a self-contained task prompt for the Agent tool (model: haiku), then reads and verifies the result landed on disk. The orchestrating Claude only builds the prompt, dispatches the sub-agent, reads the result, and writes a report; it never authors a single line of test code itself.
---

# test-copilot — test routing only, no authoring, no verification (red step)

> **Adı tarihsel.** Yazma işi artık Codex CLI'da veya Aider'da değil, bir
> Haiku alt-ajanında (`Agent` tool, `model: "haiku"`) yapılıyor 
>

> **GİT YASAĞI .** Aynı gün
> `code-copilot`'un dispatch ettiği bir Haiku alt-ajanı kendiliğinden
> `git add`/`git commit` çalıştırdı — onaysız bir commit oluşturdu VE bu
> sırada bu skill'in yazdığı red-step test dosyalarını sildi/geri aldı
> (hiç commit'e alınmamış oldukları için kurtarılamaz veri kaybı). Bu
> yüzden her dispatch prompt'unun SONUNA şu satır MUTLAKA eklenir:
> "GİT KOMUTU ÇALIŞTIRMA — add/commit/checkout/reset/restore/stash dahil
> hiçbir git komutu kullanma. Sadece dosya içeriğini Write/Edit ile
> değiştir. Commit tamamen ayrı, kullanıcı onaylı bir adımda yapılır."

## Kullanılacak destek skiller
- `caveman`, `ponytail` (full) — her zaman aktif.
- `superpowers:subagent-driven-development` — test dosyaları birden çok modülü kapsıyorsa, birden fazla Haiku alt-ajan çağrısına bölmek için.

## Why this exists
Same rule as `code-copilot`: the orchestrating Claude routes, a dispatched
`Agent` call (pinned to `model: "haiku"`) authors. This skill is the
bridge for the **test-authoring** side of an ATDD task.

- **Test-first order .** copilot-instructions.md mandates
  "Process — Test-first (red → green → refactor)". This skill runs BEFORE
  `code-copilot`: tests are written against atdd.md's Acceptance Criteria
  with no implementation on disk yet, expected to fail (red). `code-copilot`
  then dispatches a separate Haiku sub-agent to write the implementation
  that makes them pass (green).
- **Single responsibility, on purpose.** This skill only gets tests written
  and confirms they landed on disk. Running them belongs to `verify` (after
  `code-copilot`, once there's an implementation to run tests against).
- **Kept separate from code-copilot on purpose.** One dispatch per concern —
  a bad test run doesn't force redoing the implementation call, and vice versa.
- **The model is always pinned explicitly — and this is load-bearing.**
  Pass `model: "haiku"` on every `Agent` call in this skill — never omit it.
- **The sub-agent has no memory of this conversation.** It starts cold —
  the task prompt built in step 3 must be fully self-contained (absolute
  project root, exact file paths, full Acceptance Criteria and Davranış
  Sözleşmesi text). Don't write "as discussed above" — the sub-agent never
  saw it.

## Precondition
`obss_project/artifacts/<task-slug>/atdd.md` must already exist (and
`plan.md` if the `plan` skill ran). If atdd.md is missing, say so and point
at the `atdd` skill — don't guess at scope.

## Steps

### 1. Read atdd.md (and plan.md if present)
Pull out: Acceptance Criteria (happy path + edge cases), the **Davranış
Sözleşmesi** table, and the Benchmark section. From plan.md (if it exists):
which files the implementation is expected to land in — tests target those
same paths even though the files don't exist yet.

**Every row of the behaviour-contract table gets its own test.** That table
is the error taxonomy the user actually agreed to; a row without a test is an
error path nobody verified. Pay particular attention to the two rows that are
easiest to skip and most expensive to miss:
- **partial success** — assert the exact documented state, not just "no crash";
- **nothing done, no error** — assert the call reports failure. A function
  that returns success while changing nothing must fail its test.

Also assert that "empty result" and "error" are distinguishable where the
contract says they must be — identical return values for "no data" and "not
allowed" is a contract violation, not a detail.

If atdd.md has no behaviour-contract table (written before this section
existed), say so and test the error cases from the Acceptance Criteria — but
tell the user the taxonomy was never pinned down.

### 2. Decide test file paths
Follow whatever convention the project already uses (e.g. `test_<module>.py`
next to the planned `<module>.py`) — check plan.md or the surrounding
directory. Don't invent a new test directory layout without checking.

### 3. Build the sub-agent task prompt
Assemble one self-contained prompt — AC/sözleşme/benchmark metnini İNLİNE
KOPYALAMA (orkestratörün 1. adımda zaten okuduğu metni ikinci kez üretmek
gereksiz token maliyeti), sadece dosya yolunu ver, sub-agent kendi Read'ini
yapsın:

```
Proje kökü (MUTLAK yol): <ABSOLUTE PROJECT ROOT — from atdd.md/plan.md>
Yazılacak/genişletilecek test dosyaları: <absolute paths, from step 2>
Not: <bu dosyalar zaten varsa "mevcut dosyaya EKLE, üzerine yazma"; yoksa
"yeni dosya oluştur", proje test konvansiyonuna uy>

## Görev
Önce şu dosyayı Read et: <atdd.md mutlak yolu>. "Acceptance Criteria",
"Davranış Sözleşmesi" ve "Benchmark" bölümlerine göre testleri yaz. Henüz
implementasyon YOK — code-copilot yazana kadar BAŞARISIZ (red) olmaları
BEKLENİR. Davranış Sözleşmesi tablosunun HER satırı kendi testini almalı
(özellikle "kısmi başarı" ve "hiçbir şey yapılamadı ama hata yok" satırları).

## Test deseni
<projenin zaten kullandığı test framework/fixture deseni — mevcut bir test
dosyasından örnek gösterilerek anlatılır, ör. "FastAPI TestClient + gerçek
in-memory DB deseni, mevcut test_x.py'deki AYNI yapı">

## Rapor formatı (yanıtının sonunda)
1. Oluşturulan/genişletilen dosyalar.
2. Her Acceptance Criteria'yı hangi test fonksiyonunun hedeflediği.
3. Varsayımlar (varsa).

## GİT KOMUTU ÇALIŞTIRMA
add/commit/checkout/reset/restore/stash dahil hiçbir git komutu kullanma.
Sadece dosya içeriğini Write/Edit ile değiştir. Commit tamamen ayrı,
kullanıcı onaylı bir adımda yapılır — bu senin işin değil.

## ARAMA KAPSAMI
Grep/Glob/Bash ile arama yaparken HER ZAMAN yukarıdaki proje kökü ile
sınırlı kal. Bu ortamda git reposunun kökü proje klasöründen daha geniş
(örn. ev dizini) olabilir ve devasa bir geçmiş taşıyabilir — kök dizinden
veya parametresiz geniş kapsamda arama RAM'i tüketip yanıt vermeyebilir.
```

Use atdd.md's own wording — don't invent scope not present there.

### 4. Dispatch the Haiku sub-agent
```
Agent({
  description: "Write failing tests for <task-slug> (red step)",
  subagent_type: "general-purpose",
  model: "haiku",
  run_in_background: false,
  prompt: "<the full self-contained prompt from step 3>",
})
```
Run in the foreground — the next step (confirming files landed) depends on
it. Tell the user this is the real authoring step — **make it once**, not
speculatively; get the file list and project root right first.

### 5. Confirm the files landed — nothing more
- Run `git status --short <test dir>` (or list it) on the REAL project
  location. Empty/unexpected result means the sub-agent's prompt had a
  wrong/relative project root — fix it and re-dispatch before treating
  anything written elsewhere as usable.
- `Read` the test files the sub-agent wrote, just enough to confirm they
  cover each Acceptance Criteria atdd.md lists (happy path + every edge
  case) — a presence check, not a quality review or a test run.
- Write `obss_project/artifacts/<task-slug>/test_diff.md`, listing the test
  files created and which Acceptance Criteria each targets.

### 6. If the sub-agent's output looks wrong
Don't fix it yourself with `Edit`. Dispatch another `Agent` call with a
sharper prompt describing what's missing or wrong.

### 7. Hand off to code-copilot
Tell the user the failing tests are in place (red) and the next step is
`code-copilot`, which will dispatch its own Haiku sub-agent to write the
implementation that makes them pass (green). Don't run the tests here — no
implementation exists yet, a run would just fail on missing files/imports,
not report anything useful.

Eğer atdd.md'de bir Görsel/UI kriteri işaretliyse, bunu code-copilot'a da
hatırlat — o kriter `verify` adımında `vision-test` ile kontrol edilecek,
zincirin ortasında unutulmasın.

## The one rule that can't bend
Every line of test code comes from the dispatched Haiku sub-agent, never
from the orchestrating Claude directly. Reading files to confirm they exist
and roughly match scope is fine; editing a test file directly is not, and
running/verifying anything belongs to `verify`, not here.
