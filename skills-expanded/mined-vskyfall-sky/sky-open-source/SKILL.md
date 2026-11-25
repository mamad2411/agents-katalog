---
name: sky-open-source
description: >-
  Açık kaynak projesi yayınlama ve sürdürme: lisans seçimi (MIT/Apache-2.0/AGPL ve etkileri),
  depoyu halka hazırlama (sır temizleme, README, örnekler), katkı altyapısı (CONTRIBUTING, davranış
  kuralları, issue/PR şablonları, iyi ilk issue'lar), sürümleme ve yayın otomasyonu, topluluk
  yönetimi ve tükenmişlikten kaçınma, güvenlik politikası (SECURITY.md), sürdürülebilirlik ve
  sponsorluk, açık çekirdek iş modelleri. Bir projeyi açık kaynak yapmak veya sürdürmek için kullan.
disable-model-invocation: true
---

# Sky · Açık Kaynak

## Yayın öncesi

- **Sır temizliği** (en kritik): git geçmişinde anahtar/parola/iç bilgi var mı? (`gitleaks` tüm geçmişi tara); varsa döndür + geçmişi temizle (bkz. `sky-secrets`). İç referanslar, müşteri verisi, özel yapılandırma çıkar.
- Lisans dosyası (aşağıda), çalışan README, en az bir örnek, net kurulum.

## Lisans

| Lisans | Etkisi |
|---|---|
| **MIT** / BSD / ISC | en izin verici; herkes (ticari dahil) kullanır, tek şart telif bildirimi |
| **Apache-2.0** | MIT gibi + açık patent hibesi (kurumsal benimseme için iyi) |
| **MPL-2.0** | dosya bazında copyleft (ılımlı) |
| **GPL-3.0** | türev işler de GPL olmalı (güçlü copyleft) |
| **AGPL-3.0** | GPL + ağ üzerinden kullanım da kaynak paylaşımı gerektirir (SaaS'ı korur) |
Kütüphanenin yaygın benimsenmesini istiyorsan MIT/Apache-2.0; SaaS olarak ticarileştirip başkasının bedava host etmesini engellemek istiyorsan AGPL veya açık çekirdek. Lisans seçimi hukuki sonuç doğurur — büyük/kurumsal projede hukukçuya danış.

## Katkı altyapısı

`README` (ne, neden, hızlı başlangıç, rozetler), `LICENSE`, `CONTRIBUTING.md` (geliştirme kurulumu, test, PR süreci, commit kuralları), `CODE_OF_CONDUCT.md` (Contributor Covenant), issue/PR şablonları (`.github/`), `good first issue` etiketli erişilebilir görevler, `CODEOWNERS`. Katkı yapanı üç dakikada çalışır hâle getir (bkz. `sky-claude-md`, `sky-docs-site`).

## Sürüm ve yayın

semver + changesets/release-please (bkz. `sky-changelog`), GitHub Actions ile otomatik yayın + provenance (bkz. `sky-npm-library`), CHANGELOG, kullanımdan kaldırma politikası.

## Güvenlik

`SECURITY.md` (desteklenen sürümler, açık bildirim yolu — herkese açık issue değil, özel kanal), GitHub güvenlik danışmanları ve özel düzeltme, bağımlılık güncellemeleri (Dependabot), gerekiyorsa ödül programı. Sorumlu açıklama: bildireni say, düzeltmeden önce detay yayınlama.

## Topluluk ve sürdürülebilirlik

- Hızlı ve nazik ilk yanıt, net kapsam ("bu proje şunu yapar, şunu yapmaz" — hayır demek de bakımdır), şablonlar tekrar eden soruları azaltır.
- **Tükenmişlikten kaçın**: sınırlar koy, yanıt süresi vaadi verme, bakımcı ekle, "bakım modu" dürüstçe ilan et.
- Sürdürülebilirlik: GitHub Sponsors / Open Collective, kurumsal destek, açık çekirdek (açık kaynak + ücretli bulut/kurumsal özellikler), danışmanlık. İzin verici lisansta büyük şirketler bedava kullanır — iş modelini baştan düşün.

## Tanıtım

İyi README + örnekler + doküman sitesi; ilgili topluluklarda paylaşım (abartısız, değer odaklı), konuşma/yazı, "awesome" listelerine ekleme. Yıldız sayısı hedef değil; gerçek kullanım ve katkı önemli.
