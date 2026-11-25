---
name: img2threejs-setup
description: "img2threejs'i kur, guncelle ve dogrula — tek checkout, Claude ve Antigravity'ye symlink, test suiti. Triggers: img2threejs kur, img2threejs setup, img2threejs guncelle, img2threejs calismiyor, image to threejs kurulum."
---

# img2threejs — kurulum ve bakim

Referans gorseldeki nesneyi **kod olarak** prosedurel bir Three.js modeline cevirir.
Photogrammetry degil, mesh indirme degil: cikti okunabilir bir TypeScript factory
(`createXModel(): THREE.Group`) ve bir `ObjectSculptSpec` JSON'u.

Apache-2.0 · Python 3.10+ **stdlib**, ucuncu parti bagimlilik yok.

## Tek checkout, iki host

Upstream'in kendi kurali: **bir** checkout tut, her host oraya symlink ile girsin.
Yoksa Claude ve Antigravity iki ayri kopyayi calistirip birbirinden ayrisir.

```
~/Projects/img2threejs                  <- kanonik checkout (git repo)
~/.claude/skills/img2threejs        -> ~/Projects/img2threejs
~/.gemini/config/skills/img2threejs -> ~/Projects/img2threejs
```

`install.sh` yalnizca `claude-config/global/skills/*` altini kopyalar, tanimadigi
dizinlere dokunmaz — symlink kurulumdan sonra ayakta kalir. **Bu skill'in kendisi
claude-config'te durur; img2threejs'in kodu durmaz.** Repoyu vendor etme.

## Kur

```bash
git clone https://github.com/img2threejs/img2threejs.git ~/Projects/img2threejs
ln -sfn ~/Projects/img2threejs ~/.claude/skills/img2threejs
mkdir -p ~/.gemini/config/skills
ln -sfn ~/Projects/img2threejs ~/.gemini/config/skills/img2threejs
```

## Guncelle

```bash
git -C ~/Projects/img2threejs pull --ff-only
```

Symlink'ler oldugu icin iki host da ayni anda guncellenir. Guncelledikten sonra
**dogrulama adimini kos** — surum atlamalari pipeline sozlesmesini degistirebiliyor.

## Dogrula

```bash
cd ~/Projects/img2threejs && python3 -m unittest discover -s forge/tests -q
```

Beklenen: `OK` (bir miktar `skipped` normal). Referans olcum: **1083 test, 42 sn,
OK (skipped=38)**, Python 3.14.5, 2026-08-26.

Test ciktisinin **icinde** `FAILED: 1 node(s) below --min-confidence` gibi satirlar
gorursun — bunlar fixture'larin kendi stdout'u, test basarisizligi degil. Karar
satiri en sondaki `OK` / `FAILED (...)` satiridir; ona bak.

Symlink kontrolu:

```bash
ls -l ~/.claude/skills/img2threejs ~/.gemini/config/skills/img2threejs
```

Ikisi de `-> /Users/<sen>/Projects/img2threejs` gostermeli. Symlink degil de gercek
dizin gorunuyorsa biri repoyu oraya klonlamis demektir: sil, symlink'i yeniden kur.

## Ariza

| Belirti | Sebep | Cozum |
|---|---|---|
| `No module named pytest` | Suit `unittest` ile kosar | `python3 -m unittest discover -s forge/tests` |
| `SyntaxError` / eski Python | 3.10 alti | `python3 --version` — 3.10+ gerekir |
| Claude skill'i gormuyor | symlink yok ya da kirik | Kur bolumundeki `ln -sfn`'i tekrarla |
| Antigravity gormuyor | `~/.gemini/config/skills/` yok | `mkdir -p` sonra symlink |
| Iki host farkli davraniyor | iki ayri checkout var | Fazlasini sil, tek checkout'a symlink |

## Ne zaman kullanilir, ne zaman kullanilmaz

**Kullan:** brief 3B model istiyorsa; kahraman bir prop, silah, arac, makine parcasi,
bitki ya da karakter elde referans gorselden yeniden kurulacaksa; malzeme calismasi
ya da animasyona hazir hiyerarsi (pivot + socket) gerekiyorsa.

**Kullanma:** brief sprite ise. `prototype` ve `threejs-prototype-starter`'daki kural
degismedi — **sprite varsayilandir, 3B kelimelerle istenmelidir.** img2threejs'in var
olmasi bir sprite oyununu 3B'ye cevirmek icin gerekce degildir.

**Sinir:** tek gorsel gizli geometriyi gostermez; sonuc yaklasiktir, ozellikle
karakterlerde. Arac guven seviyesini ve cikarim yapilan bolgeleri kendisi isaretler —
o isaretleri raporda tasi, sessizce yutma.

## Model yonlendirmesi

> `global/model-routing.md`

Sculpt pipeline'i mekanik ve deterministik: **`agy` uzerinden Gemini'ye delege edilir.**
Referans gorseli uretmek de Gemini (`generate_image`). Claude'da kalan tek sey
**kabul karari** — benzedi mi, oyunun stiline oturdu mu, kahraman prop bunu hak
ediyor mu. O bakis Opus'undur.
