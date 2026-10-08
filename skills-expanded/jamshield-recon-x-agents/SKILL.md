# AGENTS.md

## Repository Working Rule

Bu repoda çalışan ajan, kullanıcıdan gelen **her yeni görev/prompt** için herhangi bir analiz, öneri, plan veya kod değişikliği yapmadan önce repo içindeki Markdown dokümantasyonunu okuyarak bağlam toplamak zorundadır.

## Mandatory Pre-Action Read Pass

Her yeni görevde, **action almadan önce** şu okuma sırası uygulanır:

1. Repo kökündeki `plan.md`
2. `docs/README.md`
3. `docs/roadmap/master-plan.md`
4. `docs/roadmap/progress-tracker.md`
5. `docs/architecture/**/*.md`
6. `docs/interfaces/**/*.md`
7. `docs/scenario-design/**/*.md`
8. `docs/evaluation/**/*.md`
9. `docs/runbooks/**/*.md`
10. `docs/decisions/**/*.md`

## Reading Policy

- Bu okuma turu, her yeni kullanıcı prompt’unda tekrar yapılır.
- Okuma tamamlanmadan ajan çözüm önermemeli, plan çıkarmamalı, dosya editlememeli, test çalıştırmamalı.
- Markdown dosyaları UTF-8 olarak okunmalı.
- Okuma sonrasında ajan, görev için gerekli dokümantasyon bağlamını kısa bir iç özet halinde toplamalı ve sonra işe başlamalı.

## Artifact Markdown Policy

`artifacts/**` altındaki `.md` dosyaları varsayılan olarak **kaynak dokümantasyon** sayılmaz. Bunlar generated output olarak kabul edilir.

- Eğer görev regression, replay, summary artifact, geçmiş run çıktısı veya kanıt incelemesi ile ilgiliyse, ilgili `artifacts/**/*.md` dosyaları da ayrıca okunur.
- Eğer görev kaynak kodu, mimari, planlama veya implementation ise `artifacts/**/*.md` dosyaları zorunlu ilk okuma turuna dahil edilmez.

## Priority Rule

Doküman ile kod çelişirse ajan bunu açıkça belirtmeli:

- Mimari niyet için dokümantasyonu
- Gerçek mevcut davranış için kodu

beraber değerlendirmelidir.

## Goal

Amaç, sistemi bağlamsız parça parça değiştirmek yerine:

- roadmap ile uyumlu,
- mevcut faz ile uyumlu,
- mimari kararlarla uyumlu,
- progress tracker ile çelişmeyen

bir çalışma disiplini zorlamaktır.
