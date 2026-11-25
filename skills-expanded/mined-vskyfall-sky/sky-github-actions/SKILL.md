---
name: sky-github-actions
description: >-
  GitHub Actions ileri seviye: iş akışı yapısı ve tetikleyiciler, önbellek (setup-* cache,
  actions/cache), matris build'ler, paralel işler ve bağımlılıklar, yeniden kullanılabilir iş
  akışları ve composite action'lar, ortamlar ve onay kapıları, OIDC ile bulut kimliği (anahtarsız),
  sırlar ve izinler (en az yetki, SHA ile sabitleme), concurrency, path filtreleri, artifact ve
  sürüm yayınlama, Dependabot, hızlandırma ve sık hatalar. CI/CD iş akışı yazarken kullan.
disable-model-invocation: true
---

# Sky · GitHub Actions

Temel CI iskeleti `sky-deploy`'da; burada ileri teknikler.

## Güvenlik temeli

```yaml
permissions:
  contents: read             # varsayılanı daralt; iş bazında ihtiyacı artır
jobs:
  release:
    permissions: { contents: write, id-token: write }
```
- Üçüncü parti action'ları **commit SHA** ile sabitle (`uses: some/action@a1b2c3…  # v4.2.0`) — etiketler değiştirilebilir. Dependabot `github-actions` ekosistemi SHA'ları da günceller.
- `pull_request_target` + PR kodunu checkout etmek = sır sızıntısı riski; çatallardan gelen PR'larda sırlar yok.
- Kullanıcı girdisini (`github.event.pull_request.title`) doğrudan `run:` içine gömme (script injection) → önce env değişkenine al.

## OIDC ile anahtarsız bulut erişimi

```yaml
- uses: aws-actions/configure-aws-credentials@<sha>
  with:
    role-to-assume: arn:aws:iam::123456789012:role/gha-deploy
    aws-region: eu-central-1
```
Bulutta GitHub OIDC sağlayıcısına güven + repo/branch koşullu rol. Statik erişim anahtarı sırlarda tutulmaz. GCP/Azure/Vercel benzer.

## Hız

```yaml
- uses: actions/setup-node@<sha>
  with: { node-version-file: .nvmrc, cache: pnpm }
- uses: actions/cache@<sha>
  with:
    path: |
      .next/cache
      ~/.cache/ms-playwright
    key: ${{ runner.os }}-build-${{ hashFiles('pnpm-lock.yaml') }}-${{ hashFiles('src/**') }}
    restore-keys: ${{ runner.os }}-build-${{ hashFiles('pnpm-lock.yaml') }}-
```
- Bağımsız işleri paralel (`lint`, `typecheck`, `test` ayrı job), birbirine bağlı olanları `needs:`.
- Path filtresi: `on: push: paths: ["apps/web/**", "packages/**"]` veya `dorny/paths-filter` ile monorepoda yalnızca etkilenenler.
- E2E'yi `--shard=${{ matrix.shard }}/4` ile böl.
- `concurrency: { group: ${{ github.workflow }}-${{ github.ref }}, cancel-in-progress: true }` — eski çalıştırmaları iptal et.

## Matris

```yaml
strategy:
  fail-fast: false
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
    node: [20, 22]
    exclude: [{ os: windows-latest, node: 20 }]
runs-on: ${{ matrix.os }}
```

## Yeniden kullanım

- **Reusable workflow** (`on: workflow_call` + `inputs`/`secrets`) — birçok repoda aynı CI/deploy.
- **Composite action** (`.github/actions/setup/action.yml`) — tekrar eden adımlar (checkout + pnpm + cache + install).

## Ortamlar ve onay

`environment: production` → korumalı ortam: gerekli onaylayıcılar, yalnızca `main`'den deploy, ortama özel sırlar. Deploy URL'si
PR/commit'te görünür.

## Sürüm yayınlama

- `release-please` / `changesets` ile otomatik sürüm PR'ı + changelog + etiket (bkz. `sky-changelog`).
- Etiket push'unda build → `softprops/action-gh-release` ile artifact yükleme; npm yayını `--provenance` ile (OIDC, `id-token: write`).
- Docker: `docker/build-push-action` + `cache-from/to: type=gha` + GHCR (`ghcr.io/${{ github.repository }}`).

## Diğer

- `workflow_dispatch` (elle çalıştırma, girdilerle), `schedule` (cron, UTC; sessiz repolarda 60 gün sonra devre dışı kalır).
- `actions/upload-artifact` ile test raporu/trace (başarısızlıkta).
- İş özeti: `echo "### Sonuç" >> $GITHUB_STEP_SUMMARY` — PR'da güzel rapor.
- Yerel deneme: `act` (sınırlı).
- Kendi runner'ın (self-hosted) yalnızca özel repolarda; açık repoda çatal PR'ları kodunu çalıştırır.

## Sık hatalar

| Sorun | Çözüm |
|---|---|
| Her çalıştırmada bağımlılık sıfırdan | setup-* `cache` veya actions/cache |
| Sırlar çatal PR'da boş | beklenen davranış; sır gerektiren işleri `push`/korumalı ortama al |
| `GITHUB_TOKEN` ile tetiklenen push yeni iş akışı başlatmıyor | beklenen; PAT/GitHub App token gerekir |
| Cron çalışmıyor | varsayılan dalda olmalı, UTC, repo aktif olmalı |
| Uzun süren E2E | shard + yalnızca etkilenen projeler |
