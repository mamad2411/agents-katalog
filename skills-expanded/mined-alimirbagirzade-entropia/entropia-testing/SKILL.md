---
name: entropia-testing
description: >
  Entropia'nın test ve doğrulama kapıları: backend pytest + %90 coverage kapısı,
  frontend vitest eşikleri, alt-küme koşarken --no-cov, TEST_DATABASE_URL ile
  worktree izolasyonu, L1 FK insert-order proof, alembic up/down/up, xfail
  politikası ve exit-code okuma tuzakları. Test yazarken, "testler geçiyor mu"
  sorusunda, coverage düştüğünde, commit/PR öncesi ve migration eklerken oku.
license: MIT
---

# Entropia testing — kapılar, rapor değil

**Coverage bir kapıdır.** Düşen sayıyı indirmek yasak; eksik testi yaz. Bu kural
ponytail merdiveninin üstündedir.

## Backend

Tam kapı (CI'ın gördüğünün yerel karşılığı):

```bash
cd backend && uv run ruff check . && uv run ruff format --check . && uv run mypy src && uv run pytest -q
```

`addopts` zaten `--cov-fail-under=90` taşır → **tam suite koşusu coverage
kapısını da doğrular.** Ayrıca CI'da bloklayıcı: `openapi_export --check`,
`generate_repository_facts.py --check`, `acceptance_semantic_scan.py`,
`alembic upgrade head`, `pip-audit`.

### Exit code'u ayrı oku — `| tail` KULLANMA

`pytest ... | tail` çalıştırdığında exit code `tail`'in olur; bu hata gerçekten
yaşandı (ADIM 17'de özet satırı ve exit code yakalanmadı).

```bash
cd backend && uv run pytest -q > /tmp/pytest.out 2>&1; echo "exit=$?"; tail -25 /tmp/pytest.out
```

### Alt küme koşarken `--no-cov`

```bash
cd backend && uv run pytest -q --no-cov tests/path/test_x.py
```

Tek dosyalık koşu paketin tamamını ~%4 ölçer → kapı **sahte kırmızı** verir.

### Worktree izolasyonu

Paralel worktree oturumları aynı DB'de çakışır. Worktree'ye özel izole DB kullan:

```bash
export TEST_DATABASE_URL='postgresql+asyncpg://entropia:entropia@localhost:5432/entropia_wt_<slug>'
```

**Sürücü `postgresql+asyncpg://` olmalı.** Yerel Postgres `:5432`
(`entropia`/`entropia`).

### Suite koşarken yapma

- Tam suite'i **tek pytest çağrısında** koş, **ortada öldürme**.
- Suite koşarken `uv sync` / paralel `uv run` çalıştırma.

### xfail politikası

**Bilinçli `xfail(strict)` sayısı 1'dir** (eskiden "4" yazan belgeler BAYAT):
`test_research_point_in_time_parity.py:583`, izleme issue **#558** — available-time
policy pin'i bir **ürün kararı**, bug değil. Oracle paketinde xfail **sıfır**.
Yeni bir xfail ekleyeceksen issue numarası ve gerekçe zorunlu; "şimdilik" xfail yok.

## Yeni migration eklediyse — üç kanıt birden

1. **L1 FK insert-order proof** — her yeni `create_*` için.
2. **alembic `<n>` up → down → up**
   `LC_ALL=en_US.UTF-8`, proof öncesi:
   ```sql
   DROP SCHEMA public CASCADE; CREATE SCHEMA public;
   ```
3. **migration ↔ model kolon paritesi.**

Migration dosyasını elle "düzeltip" geçme; üçü de koşmadan slice kapanmaz.

## Frontend

```bash
cd frontend && npm run lint && npm run typecheck && npm run coverage && npm run build
```

- **vitest için `--no-file-parallelism` ZORUNLU.**
- Eşikler `frontend/vite.config.ts` içinde — **kapıdır**, indirilmez.
- Worktree'de `frontend/node_modules` yoksa önce `npm ci`; ilk koşudaki
  `ERR_MODULE_NOT_FOUND` bir test hatası **değildir**.

## Test kalitesi

- Davranışı test et, implementasyonu değil — testler refactor'dan sağ çıkmalı.
- İsimler davranışı anlatır: `should_reject_expired_token`.
- Testler bağımsızdır: paylaşılan mutable state yok, sıra bağımlılığı yok.
- Mock'lar **sınırda**: HTTP, DB, filesystem, saat, rastgelelik. Test edilen
  birimi mock'lama.
- Kod silinince geçen test yazma.

## Sayı raporlama disiplini

Test sayılarını **çıktıdan** al, hatırladığından ya da belgeden değil.
Sayısal otorite: CI job log'u ve `docs/generated/repository_facts.md`
(**collection** sayıları). `CLAUDE.md` §Current position elle yazılır ve
bayatlayabilir.

Doğrula: `gh run list --branch main --limit 1` → job log. **`gh` yoksa** (remote
container: yok): `mcp__github__actions_list` → `mcp__github__get_job_logs`.
