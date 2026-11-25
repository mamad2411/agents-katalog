---
name: ponytail-entropia
description: >
  Entropia'ya uyarlanmış "tembel kıdemli geliştirici" merdiveni. Kod yazmadan
  önce YAGNI → codebase'de var mı → stdlib → native → kurulu bağımlılık → tek
  satır sırasını uygular; ama Entropia'nın PAZARLIKSIZ invariant'larını
  (coverage kapısı, katman deseni, adjudicated spec alanları, kapanış ritüeli)
  kısaltmaz. Yeni slice yazarken, refactor ederken, "bunu nasıl en az kodla
  yaparız" diye sorarken, gereğinden fazla mühendislik şüphesi varken kullan.
  Spec metni yazarken / dokümantasyon üretirken KULLANMA.
license: MIT
---

# Ponytail — Entropia uyarlaması

Kaynak: [dietrichgebert/ponytail](https://github.com/dietrichgebert/ponytail) v4.8.4 (MIT).
Merdiven upstream'den; **override bölümü Entropia'ya özgüdür ve merdivene üstün gelir.**

> Tembel = verimli, dikkatsiz değil. En iyi kod hiç yazılmayan koddur.

## Merdiven — ilk tutan basamakta dur

1. **Bu var olmak zorunda mı?** Spekülatif ihtiyaç → yazma, tek satırla söyle. (YAGNI)
2. **Bu codebase'de zaten var mı?** Entropia'da bu basamak en pahalı olanı:
   önce ilgili `docs/CODEMAPS/*` haritasını oku, sonra `codebase-memory-mcp`
   (`search_graph` / `trace_path` / `get_code_snippet`) ile sembolü ara. Kickoff
   dokümanının **REUSE list**'i zaten yeniden kullanılacakları isimleriyle verir.
   Var olanı yeniden yazmak buradaki en yaygın israftır.
3. **Stdlib yapıyor mu?** Yap.
4. **Native platform özelliği kapsıyor mu?** DB constraint > app kodu, CSS > JS,
   `<input type="date">` > picker lib.
5. **Kurulu bağımlılık çözüyor mu?** Kullan. Birkaç satırlık iş için yeni
   bağımlılık ekleme.
6. **Tek satır olabilir mi?** Tek satır.
7. **Ancak o zaman:** çalışan minimum kod.

Merdiven problemi **anladıktan sonra** koşar, anlamanın yerine değil. Yanlış
yerdeki en küçük diff tembellik değil, ikinci bir bug'dır.

**Bug fix = kök neden.** Dokunacağın fonksiyonun tüm çağıranlarını ara; paylaşılan
fonksiyona konan tek guard, her çağırana konan guard'dan küçük diff'tir — ve
ticket'ın adını verdiği yolu yamamak kardeş çağıranı bozuk bırakır.

## Entropia override — burada TEMBEL OLMA (merdiven bunları kesemez)

Bunlar "gereğinden fazla mühendislik" gibi görünür ama **adjudicated karardır**;
silmek sözleşmeyi bozar. Ultra seviye bu listeye hiç uygulanmaz.

| Alan | Neden kısaltılamaz |
|---|---|
| **Test kapısı** | `--cov-fail-under=90` **kapıdır, rapor değil**. Upstream'in "tek runnable check, framework yok" kuralı burada GEÇERSİZ — düşen sayıyı indirme, eksik testi yaz. Her yeni `create_*` için **L1 FK insert-order proof** + alembic `<n>` up/down/up + migration↔model kolon paritesi zorunlu. |
| **Katman deseni** | `commands/` · `queries/` · `domain/` · `routes/` ayrımı ve modül-seviyesi async command + tek-tx no-commit + `run_idempotent` + `session.refresh(with_for_update=True)` + `_audit_and_outbox` deseni **kopyalanır**, "daha az dosya" için birleştirilmez. |
| **Hata zarfı** | `shared/responses.py::ErrorBody` alan adları **asla değişmez**. `suggested_action` (makine token'ı) ile `remediation` (insan metni) ayrı alanlardır — birleştirmek birini kaybettirir. |
| **OCC dual-token** | `shared/concurrency.py::reconcile_occ_tokens` tek kuraldır; route'a kopyalama, oradan geçir. Çelişki → 409 `OCC_TOKEN_CONFLICT`. |
| **Idempotency** | Kalıcı satır yazan her mutating op `Idempotency-Key` okur ve `application/idempotency.py::run_idempotent` ile sarılır. Fingerprint'e komutun kendi değiştirdiği durumu koyma. |
| **O-30 purge gövdesi** | `deletion_state` **ve** `root_lifecycle_state` aynı değerle birlikte döner. Tekrar gibi görünür; adjudicated'dır, biri silinmez. |
| **Upload kapısı** | `domain/importing/source_file.py::assert_supported_source_file` fail-closed; filename yoksa **RED**, "atla" yok. |
| **Trash kataloğu** | `domain/trash/page.py::TRASH_OBJECT_LOCATIONS` içindeki her tip `trash_repo.add_trash_entry` **yazmak zorundadır**; yeni tip eklerken `commands/deletion.py` + `jobs/purge.py` + `queries/trash.py` dallarını birlikte ekle. |
| **Typed response** | Mutating route gövdesi typed model olarak bildirilir; `dict[str, Any]` dönüşü sözleşmeyi şemadan gizler. |
| **UI** | v18 mockup (`docs/spec/index_guncellenmis_duzeltilmis_v18.html`) görsel otoritedir; route path / react-query key / OCC token / Idempotency-Key / SSE taksonomisi presentation işinde **hiç** ellenmez. |
| **Kapanış ritüeli** | Handoff + kickoff + `PROJECT_HISTORY.md` + memory checkpoint + codemap tazeleme **açıkça istenmiş çıktıdır** → "gereksiz prose" sayılmaz, kısaltılmaz. |

Ayrıca hiçbir zaman kısaltılmaz: trust boundary'de input validation, veri kaybını
önleyen error handling, güvenlik, erişilebilirlik, açıkça istenmiş her şey.

## Bilinçli sadeleştirmeyi işaretle

Gerçek bir tavanı olan kestirme (global lock, O(n²) tarama, naive heuristic) →
kod içinde `# ponytail:` yorumu ile tavanı ve yükseltme yolunu yaz, **ve**
kapanışta `docs/PROJECT_HISTORY.md`'deki slice kaydına *honest boundary* olarak
geçir. İşaretlenmemiş kestirme = gizli borç.

## Çıktı

Önce kod. Sonra en fazla üç kısa satır: ne atlandı, ne zaman eklenir.
Kalıp: `[kod] → atlandı: [X], şu olunca ekle: [Y].`
Kullanıcının açıkça istediği anlatım (rapor, handoff, faz notları) bu kuralın dışında.

## Şiddet seviyesi

- **lite** — İstenen yapılır, daha tembel alternatif tek satırla söylenir. Karar kullanıcıda.
- **full** *(Entropia varsayılanı)* — Merdiven uygulanır; stdlib ve native önce, en kısa diff.
- **ultra** — Sadece spec dışı yardımcı kod / script / tooling için. Spec'in şeklini
  dikte ettiği yüzeylerde (route, command, migration, hata zarfı) **kullanma**.
