# 20 — Matriks alat (yang ada di mesin ini + cara pakai)

Cek dulu: kalau `⏭️` berarti belum terpasang → pakai alternatif, jangan install tanpa izin.

## 1. Sudah terpasang (jalankan sekarang)
| Alat | Perintah | Membuktikan |
|---|---|---|
| pytest (venv) | `~/.agents/test-venv/bin/pytest -q` | unit/integrasi python |
| hypothesis | `~/.agents/test-venv/bin/pytest` + `@given` | property, kasus tepi |
| schemathesis | `~/.agents/test-venv/bin/schemathesis run openapi.yaml --base-url $URL --checks all` | kontrak + fuzz API |
| locust | `~/.agents/test-venv/bin/locust -f locustfile.py --headless -u 50 -r 5 -t 2m` | beban python |
| k6 | `k6 run load.js -e BASE_URL=$URL` | beban + threshold |
| ab | `ab -n 1000 -c 50 $URL/health` | baseline HTTP cepat |
| playwright | `npx playwright test` / `playwright codegen $URL` | e2e browser nyata |
| vitest | `npx vitest run --coverage` | unit/component TS |
| axe (npx) | `npx --yes @axe-core/cli $URL` | a11y otomatis |
| pa11y (npx) | `npx --yes pa11y $URL --standard WCAG2AA` | a11y (runner lain) |
| lighthouse (npx) | `npx --yes lighthouse $URL --preset=desktop` | performa web |
| semgrep | `semgrep --config semgrep.yml --error --metrics=off .` | SAST |
| bandit | `bandit -q -r . --exclude ./.venv` | SAST python |
| gitleaks | `gitleaks detect --no-git --redact -f json -r out.json .` | secret |
| trivy | `trivy fs --scanners vuln,misconfig --severity HIGH,CRITICAL .` | dependency + misconfig |
| hadolint | `hadolint --failure-threshold warning Dockerfile` | praktik Dockerfile |
| shellcheck | `shellcheck -S error script.sh` | bug shell |
| nuclei | `nuclei -u $URL -config nuclei.yaml` | DAST (butuh izin) |
| security-forge | `security-forge audit .` `headers <url>` `tls <host>` | agregat keamanan |
| dcheck | `dcheck $URL` | kontras, target sentuh, overflow, a11y |
| dvisual | `dvisual $URL [--update]` | visual regression |
| dref | `dref $URL` | referensi + axe + LCP/CLS nyata |
| testing-forge | `testing-forge matrix|plan|show|generate|audit` | perencanaan & scaffold test |
| project-forge | `project-forge verify .` | gate proyek (7 gate) |
| curl + jq | `curl -fsS $URL/api/x | jq .` | smoke/assert cepat |
| docker | `docker compose config -q`, container DB sementara | integrasi infra |
| kubeconform/helm | `kubeconform -strict k8s/`, `helm lint chart` | manifest valid |
| terraform | `terraform validate` | IaC valid |
| ansible-lint | `ansible-lint playbook.yml` | playbook aman |

## 2. Belum terpasang (pakai bila perlu izin)
`cypress`, `jest`, `mocha`, `newman` (Postman), `artillery`, `wrk`, `hey`, `siege`,
`jmeter`, `pact`, `dredd`, `spectral` (via npx), `prism` (via npx), `stryker`, `mutmut`,
`owasp-zap` (docker), `syft`/`grype`/`cosign`, `checkov`, `tflint`, `vegeta`.

## 3. Pemetaan "butuh apa" → "pakai apa"
| Butuh | Alat |
|---|---|
| logika murni | pytest / vitest |
| komponen UI | vitest + Testing Library |
| endpoint API | pytest + httpx / vitest + supertest |
| bentuk API berubah | schemathesis / spectral |
| alur pengguna | playwright |
| tampilan berubah | dvisual |
| aksesibilitas | axe / pa11y / dcheck |
| kecepatan halaman | lighthouse / dref |
| tahan beban | k6 / locust / ab |
| DB | container + pytest fixture |
| secure coding | semgrep / bandit |
| secret bocor | gitleaks / security-forge |
| dependency rapuh | trivy / `npm audit` |
| kontainer | hadolint + trivy image |
| k8s | kubeconform + helm lint + dry-run |
| infra as code | terraform validate + ansible-lint |

## 4. Aturan pemakaian alat oleh AI
- Jalankan yang **sudah ada** dulu; jangan install tool baru tanpa izin user.
- Selalu lampirkan perintah + exit code + 5–20 baris output.
- Output panjang → ringkas dengan `jq`/`grep`/`tail`, jangan dump.
- Jangan arahkan DAST/beban besar ke domain yang bukan milik user.
- Alat yang butuh akun/berbayar → tawarkan alternatif lokal.
