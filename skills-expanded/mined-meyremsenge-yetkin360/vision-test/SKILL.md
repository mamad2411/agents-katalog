---
name: vision-test
description: Screenshot/visual analysis step that saves Claude's own vision tokens — Playwright takes the screenshot, Codex CLI (codex exec -i, read-only, pinned vision model) looks at the image and returns a small structured JSON, and Claude only ever reads that JSON, never the raw image. Use whenever a task needs to check what a rendered UI actually looks like (layout broken, error message visible, visual regression vs a baseline) rather than just what the DOM/accessibility tree says.
---

# Vision Test — Playwright screenshot → Codex vision → JSON, Claude reads only the JSON

## Kullanılacak destek skiller
- `caveman`, `ponytail` (full) — her zaman aktif.
- `superpowers:systematic-debugging` — bir görsel bulgu (ör. "layout bozuk") kök nedene inmeyi gerektiriyorsa, kör deneme yerine bunu izle.

## Why this exists
Claude okuyarak (Read/screenshot tool) bir ekran görüntüsünü doğrudan
incelediğinde görsel token maliyeti öder — her karşılaştırma, her sayfa için
tekrar. Bu skill bu maliyeti tek bir ucuz vision-model çağrısına indirger:
Codex CLI'nin `-i/--image` bayrağı resmi gerçekten "gören" bir modele iletir,
model de sorulan soruya sabit şekilli bir JSON ile cevap verir. Claude o
JSON'u okur, resmin kendisini asla görmez — tasarruf burada.

- **Model pinli, ve bu kritik.** `ask_codex.py`'daki `MODEL_VISION`
  . Pinlemeyi kaldırma: pinsiz
  koşumda Codex'in model yöneticisi hesabın yetkili olmadığı bir modele
  düşebiliyor ve hata temiz gelmiyor — çağrı sessizce boş dönüyor.
  Model kimliği değişirse, değiştirmeden önce şununla doğrula:
  `codex exec -m <id> --sandbox read-only --skip-git-repo-check "say ok"`
- **Vision çağrısı read-only koşar.** `--sandbox read-only` ile çalışır;
  ekran görüntüsünü inceleyen adım hiçbir dosyayı değiştiremez.
- **JSON şeması her çağrıda zorunlu.** `analyze_screenshot()`
  bir `json_schema_hint` parametresi ister — modelin kendi taktirine
  bırakılmaz, çağıran taraf her zaman beklediği alanları sabitler.
- **Sadece analiz, asla düzeltme.** Bu skill hiçbir zaman kod/CSS/UI
  değiştirmez — sadece "şu an ekranda ne var" sorusuna JSON cevap üretir.
  Bulgu bir hataysa, düzeltme ayrı bir adımdır (`code-copilot` veya elle).

## Bu skill hangi skillerden çağrılmalı
- **`verify`** — gate 11 "Görsel regresyon (visual regression)". Görev bir
  web UI/sayfa render ediyorsa ve önceki bir baseline screenshot varsa, bu
  gate artık N/A değil: `vision-test` ile mevcut ekranı analiz edip
  baseline ile karşılaştır, PASS/FAIL evidence'ı buradan gelsin.
- **`pipeline`** — Review fazının (`verify`, `red-team`) destek skilleri
  tablosuna opsiyonel bir satır: görev UI/render içeriyorsa `verify`
  içinden çağrılır, zinciri (atdd→...→commit) değiştirmez.

- Bunların dışında herhangi bir görevde kullanıcı doğrudan "ekran görüntüsü
  al ve kontrol et" derse de doğrudan çağrılabilir — pipeline'a bağlı değil.

## Precondition
Kontrol edilecek sayfa çalışır durumda olmalı (dev server ayakta / gerçek
URL erişilebilir). Playwright MCP sunucusu (`mcp__playwright__*`) bağlı
olmalı — deferred listede görünüyorsa önce `ToolSearch` ile yükle.

## Adımlar

### 1. Playwright ile ekran görüntüsü al
```
mcp__playwright__browser_navigate({ url: "<test edilecek sayfa>" })
mcp__playwright__browser_take_screenshot({ type: "png", scale: "css", fullPage: true })
```
Tool sonucundaki gerçek dosya yolunu kullan (varsayılan
`page-{timestamp}.png` olarak kaydedilir) — kendi yolunu uydurma, dönen
sonuçtan al.

### 2. Sorulacak soruyu ve JSON şemasını netleştir
Görevden ne beklendiğine göre değişir, örnekler:
- Hata/layout kontrolü: `{"has_error": bool, "error_text": str|null, "layout_ok": bool, "notes": str}`
- Baseline karşılaştırması: `{"matches_baseline": bool, "differences": [str], "severity": "none"|"minor"|"major"}`
- Belirli bir öğenin varlığı: `{"element_visible": bool, "element_description": str}`

Şemayı görevin ihtiyacına göre sen belirle — ama her zaman sabit ve önceden
tanımlı olsun, modelin serbestçe formatlamasına bırakma.

### 3. Codex vision çağrısını yap
`Bash` ile (inline `-c` değil, aynı `test-copilot`/`code-copilot` desenindeki
gibi bir script dosyasıyla çalıştır):

```python
import sys
sys.path.insert(0, r"/path/to/your/bridge")
import ask_codex

result = ask_codex.analyze_screenshot(
    image_path=r"<adım 1'den dönen MUTLAK yol>",
    question="<adım 2'deki soru, düz dille>",
    json_schema_hint="<adım 2'deki JSON şeması, literal string>",
)
print(result)
```

`result["success"]` False ise `result["error"]`'ı oku, ham görüntüyü Claude
kendisi incelemeye ÇALIŞMASIN (bu skill'in tüm amacı bu) — bunun yerine
soruyu/şemayı sadeleştirip tek bir kez daha dene.

### 4. Sadece JSON'u oku ve raporla
Claude, `result["result"]` sözlüğünü okur ve bulguyu düz dille özetler.
Ham `result["raw_text"]` sadece hata ayıklama için var — normal akışta
kullanıcıya gösterilmez.

### 5. Geçici dosyaları temizle
Playwright'ın kaydettiği screenshot dosyasını, kalıcı bir kanıt olarak
saklanması gerekmiyorsa (`verify_report.md`'ye referans verilmiyorsa) sil.

## Örnek uçtan uca kullanım
```
1) browser_navigate("http://localhost:3000/login")
2) browser_take_screenshot(type="png", scale="css", fullPage=true)
   -> "C:\...\page-2026-08-02T22-10-00.png"
3) analyze_screenshot?",
     json_schema_hint='{"has_error": bool, "error_text": str|null, "layout_ok": bool, "notes": str}',
   )
   -> {"success": true, "result": {"has_error": false, "error_text": null, "layout_ok": true, "notes": "Form renders cleanly, no error banner."}, ...}
4) Claude: "Login formu düzgün render oluyor, hata mesajı yok, layout sağlam."
```

## Değiştiremeyeceği tek kural
Bu skill hiçbir zaman implementasyon/CSS/UI dosyası yazmaz veya değiştirmez
— sadece screenshot alır, Codex gönderir, JSON okur ve raporlar. Bir
görsel sorun bulunursa düzeltme `code-copilot`'a veya kullanıcının kendisine
bırakılır.
