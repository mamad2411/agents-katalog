---
name: sky-cli-tools
description: >-
  Komut satırı aracı geliştirme (Node/TS ağırlıklı, Python/Go notlarıyla): argüman ayrıştırma
  (commander, citty, yargs), etkileşimli istemler (@clack/prompts), renkli ve okunur çıktı,
  spinner ve ilerleme çubukları, yapılandırma dosyası ve env, hata mesajları ve çıkış kodları,
  --json çıktı ve betiklenebilirlik, Ink ile TUI, npx ile çalıştırma, tek binary dağıtım,
  otomatik tamamlama ve güncelleme bildirimi. "CLI aracı yap", "komut satırı uygulaması",
  "terminal aracı" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · CLI Araçları

## İskelet (Node + TS)

```ts
#!/usr/bin/env node
import { Command } from "commander";
import * as p from "@clack/prompts";
import pc from "picocolors";

const program = new Command().name("sky-init").description("Yeni Sky projesi oluşturur").version(pkg.version);

program
  .argument("[dir]", "hedef klasör")
  .option("-t, --template <name>", "şablon (next|vite)")
  .option("--json", "makine okunur çıktı")
  .option("-y, --yes", "soruları varsayılanla geç")
  .action(async (dir, opts) => {
    p.intro(pc.bgBlue(pc.white(" sky-init ")));
    const name = dir ?? (opts.yes ? "my-app" : await p.text({ message: "Proje adı?", placeholder: "my-app", validate: (v) => (v ? undefined : "Ad gerekli") }));
    if (p.isCancel(name)) { p.cancel("İptal edildi."); process.exit(130); }
    const template = opts.template ?? (await p.select({ message: "Şablon", options: [{ value: "next", label: "Next.js" }, { value: "vite", label: "Vite + React" }] }));
    const s = p.spinner(); s.start("Dosyalar oluşturuluyor");
    await scaffold(String(name), String(template));
    s.stop("Hazır");
    p.outro(`Sonraki adım: ${pc.cyan(`cd ${name} && pnpm dev`)}`);
  });

program.parseAsync().catch((e) => { console.error(pc.red(`✖ ${e.message}`)); process.exit(1); });
```
`package.json`: `"bin": { "sky-init": "./dist/cli.js" }`, `"type": "module"`; tsup ile tek dosya bundle.

## İnsanların sevdiği CLI özellikleri

- **Etkileşimli ama atlanabilir**: her soru bir bayrakla da verilebilir (`--template next`), `-y` ile varsayılanlar — CI'da çalışır.
- **İyi hata mesajı**: ne oldu + nasıl düzelir + (varsa) dokümana bağlantı: `✖ "sky.config.json" bulunamadı. Oluşturmak için: sky init`
- Renk, ama `NO_COLOR` ve TTY değilse renksiz (picocolors bunu yapar); `--json` ile makine çıktısı (stdout'a yalnızca veri, loglar stderr'e).
- Spinner/ilerleme yalnızca TTY'de; uzun işlerde ne yapıldığını söyle.
- `--help` örneklerle (`program.addHelpText("after", "\nÖrnekler:\n  $ sky-init my-app -t next")`), `--version`.
- "Bunu mu demek istedin?" (yanlış komut adında öneri — commander yapar).
- Yıkıcı işlemde onay (`--force` ile atlanır), `--dry-run` ile önizleme.
- Güncelleme bildirimi (`update-notifier` benzeri, günde bir kez kontrol).
- Kabuk otomatik tamamlama (`tabtab`/`omelette`, Go'da cobra yerleşik).

## Çıkış kodları

`0` başarı, `1` genel hata, `2` yanlış kullanım (argüman), `130` Ctrl+C. Betiklerde zincirlenebilsin.

## Yapılandırma

Öncelik: bayrak > env (`SKY_TOKEN`) > proje dosyası (`sky.config.ts/json`, `cosmiconfig`/`c12` ile) > kullanıcı dosyası (`~/.config/sky/config.json`, XDG) > varsayılan.
Sırları kullanıcı yapılandırmasında `0600` izinle veya işletim sistemi anahtarlığında (keytar) sakla.

## TUI (tam ekran)

**Ink** (React ile terminal arayüzü) — paneller, listeler, canlı güncellenen tablolar. Go'da Bubble Tea, Python'da Textual.

## Dağıtım

- `npx sky-init` / `pnpm dlx` — kurulumsuz çalıştırma (en kolay).
- Tek binary: Bun `bun build --compile`, Node SEA, ya da Go/Rust ile yaz (hızlı açılış, bağımlılıksız). Homebrew tap, Scoop, GitHub Releases.
- Python: Typer + `uv tool install` / pipx. Go: cobra + goreleaser.

## Test

Komutları fonksiyon olarak çağırıp test et (I/O'yu enjekte et); uçtan uca: `execa` ile süreci çalıştır, stdout/çıkış kodunu doğrula; geçici klasörlerde dosya üretimi.
