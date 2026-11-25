---
name: uretim-hatti-sec
description: "Hangi uretim hattini kullanacagini sec: video mu, sprite animasyonu mu, tek gorsel mi, 3D model mi. Dort ayri hat var ve tetikleyicileri cakisiyor. Triggers: hangi skill, hangi hat, video mu sprite mi, animasyon uret, karakter uret, 3d model uret, asset uret, ne kullanmaliyim."
user-invocable: true
---

# Üretim hattı seç — video / sprite / görsel / 3D

Dört ayrı hat var. **Tetikleyicileri çakışıyor** ("animasyon üret" hem videoyu
hem sprite'ı çağırabilir), o yüzden sınır burada yazılı. Yanlış hatta girmek
saatler kaybettirir: hatların modelleri, çıktıları ve kapıları farklı.

## Karar tablosu

| İstenen | Hat | Neyle üretir | Çıktı |
|---|---|---|---|
| Oyun içi **sprite animasyonu** (yürüyüş, saldırı, idle) | **[/spritesheet-character-generator](../spritesheet-character-generator/SKILL.md)** | imagegen + HF FLUX LoRA | sprite sheet PNG (grid) |
| **Video / sinematik** (kesme sahne, tanıtım, hareketli plan) | **[/animate](../animate/SKILL.md)** | Wan 2.2 I2V | mp4 klip |
| **Tek duran görsel** (ikon, portre, sahne, kart resmi) | **[/gorsel-uret](../gorsel-uret/SKILL.md)** | ortak GPU kuyruğu (SDXL / Qwen) | PNG |
| **3D model** (mesh, rig, GLB) | **[/threejs-3d-character-pipeline](../threejs-3d-character-pipeline/SKILL.md)** | TRELLIS.2 + Blender + Mixamo | GLB / FBX |
| **3D model, kod olarak** (prosedurel, animasyona hazir, bagimliliksiz) | **[/img2threejs](../img2threejs-setup/SKILL.md)** | referans görsel + prosedurel sculpt | TS factory + spec JSON |

## Sınır nerede — sprite mi video mu

Bu ikisi en sık karıştırılan çift ve ikisi de "animasyon" üretir.

**Sprite animasyonu** oyunun içinde çalışır: sabit kamera, yerinde döngü,
şeffaf zemin, kare ızgarası. Motor karakteri hareket ettirir, animasyon
yerinde döner. Buraya `/spritesheet-character-generator` gider.

**Video** izlenir: kamera hareket edebilir, arka plan vardır, döngü şart
değil. Buraya `/animate` gider.

Sorunun cevabı belirsizse şunu sor: **çıktı oyun motoruna sprite olarak mı
girecek, yoksa ekranda video olarak mı oynayacak?**

> `/animate` bir zamanlar sprite sheet de üretiyordu ve hâlâ o kodu taşıyor.
> Yeni sprite işleri için **kullanılmıyor** — sprite tarafı
> `/spritesheet-character-generator`'a taşındı. `/animate` video hattıdır.

## Sınır nerede — görsel mi sprite mi

**Tek bir duran görsel** istiyorsan (bir ikon, bir portre, bir kart resmi)
`/gorsel-uret` yeterli: ortak kuyruğa istek bırakır, GPU makinesi üretir.

**Hareket eden bir karakterin kare dizisi** istiyorsan sprite hattına git.
Tek tek görsel üretip elle birleştirmek, tutarlılığı kaybettirir —
kareler arasında karakter değişir.

## Sınır nerede — mesh mi kod mu

İkisi de 3B, çıktıları farklı türden.

- **[/threejs-3d-character-pipeline](../threejs-3d-character-pipeline/SKILL.md)** →
  **mesh**. Foto-gerçekçi yüzey, doku haritaları, Mixamo rig'i. Bedeli: TRELLIS.2 +
  Blender bağımlılığı, ikili dosyalar, repoda diff'lenemeyen varlıklar.
- **[/img2threejs](../img2threejs-setup/SKILL.md)** → **kod**. Primitive ve prosedurel
  shader'lardan kurulu bir TS factory; okunur, diff'lenir, pivot/socket hiyerarşisiyle
  animasyona hazır gelir. Bedeli: yaklaşıklık — tek görsel gizli geometriyi göstermez,
  foto-gerçekçilik hedefliyorsan yanlış hat.

Karar: **stilize / düşük poli / versiyonlanabilir kaynak** → img2threejs.
**Gerçekçi doku + standart rig** → mesh hattı.

## Hepsinin ortak kuralı: referans

Elde referans varken stil **tarif edilmez, gösterilir**. Bu dört hatta da
geçerli: **[/reference-style](../reference-style/SKILL.md)**.

Aynı karakterin farklı çıktıları için **aynı kaynak görsel** kullanılır.
Ölçüldü: yürüyüşte kapüşonlu, saldırıda kel bir karakter tutarsızlığı tam
olarak buradan çıkıyor.

## Altyapı hangi hatta ait

| | video | sprite | görsel | 3D |
|---|---|---|---|---|
| Ortak GPU kuyruğu | ✅ `anim_jobs` | — | ✅ `anim_image_jobs` | — |
| Web arayüzü | ✅ VİDEO sekmesi | — | ✅ RESİM sekmesi | — |
| Yerel/proje içi | — | ✅ | — | ✅ |

Video ve görsel hatları **ortak GPU makinesini** paylaşıyor ve tek kuyruktan
sırayla üretiliyor (öbek politikası: bkz. `/gorsel-uret`). Sprite ve 3D
hatları proje içinde, kendi araçlarıyla çalışıyor — GPU kuyruğuna girmiyorlar.

## Ne zaman hiçbiri

Prompt yazımı ayrı bir iş: **[/image-prompt](../image-prompt/SKILL.md)**.
Fikir/tasarım aşamasındaysan üretime hiç başlama — önce
**[/greenlight](../greenlight/SKILL.md)**.
