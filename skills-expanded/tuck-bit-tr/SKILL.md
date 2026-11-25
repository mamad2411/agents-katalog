---
name: tuck-bit-tr
description: "TuckBit, kodlama ajanları için taşınabilir bir beceridir. Doğruluktan ödün vermeden ilgili bağlamı, araçları ve kontrolleri seçmeye yardımcı olur."
license: MIT
compatibility: Portable Agent Skills; project-scoped install only.
metadata:
  author: TuckBit contributors
  version: "0.4.0"
  locale: tr
---

# TuckBit — Türkçe

> Temel beceri çevrilmiştir; teknik başvurular şimdilik İngilizcedir ve topluluk incelemesi gerekir.

Yalnızca token sayısını değil, kullanılan kaynak başına doğru ve doğrulanmış sonucu iyileştir.

Dört varsayılan yetenek: kayıt, bağlam, doğrulama ve bütçe. Orkestrasyon ve ölçümler isteğe bağlıdır.

## Çalışma yöntemi

Tam kullanıcı isteği, gerçekten mevcut talimatlar ve yetkili araçlarla başla. Tüm kısıtları, onayları ve zorunlu kontrolleri koru.

1. Hedefi, sınırları, riskleri ve durma koşulunu tanımla; basit işler için gereksiz plan yapma.
2. En dar ilgili kodu, belgeyi veya aracı bul; yalnızca gerektiğinde kapsamı genişlet.
3. Yerleşik araç keşfini tercih et; üstveriler ipucudur, çalıştırma izni değildir.
4. Küçük işler için tek ajan kullan; bağımsız işleri ancak açık sorumluluk ve teslim ölçütleriyle böl.
5. Hedefli testleri, ardından son sürüm üzerinde tüm zorunlu entegrasyon ve güvenlik kontrollerini çalıştır.
6. Değişiklikleri, testleri, riskleri ve engelleri doğrulanabilir biçimde bildir. Sonsuz kontrol yerine kontrol noktaları kullan.

## Yalnızca ilgili kaynağı yükle

- `references/task-contract.md` — task contracts / host instructions.
- `references/workflows.md` — Fast / Standard / Deep workflows.
- `references/registry.md` — discovery and permission limits.
- `references/context.md` — source-linked evidence and checkpoints.
- `references/verification.md` — tests and integration checks.
- `references/budget.md` — bounded iterations.
- `references/orchestration.md` — optional independent agents.
- `references/metrics.md` — optional evaluation.

## Zorunlu sınırlar

Güvenlik kontrollerini atlama, doğruluğu azaltma, sonuç uydurma, kimlik bilgilerini okuma veya onayları aşma. İzinler ana sistem tarafından yönetilir.

**Geliştirici önizlemesi. Kurulum, gerçek etkinleştirmeyi veya token tasarrufunu kanıtlamaz.**
