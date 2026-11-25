# 17 — Infra, deploy, dan ketahanan (chaos, DR)

## 1. Container & Compose
```bash
hadolint --failure-threshold warning Dockerfile      # praktik image
docker compose config -q                            # validasi + env wajib
docker build --check .                              # BuildKit lint
docker run --rm --read-only --cap-drop ALL -p 8080:3000 img   # jalankan seperti produksi
curl -fsS localhost:8080/health
```
Checklist image:
- [ ] Multi-stage, `USER` non-root, `read_only`, `cap_drop: ALL`, `no-new-privileges`.
- [ ] `HEALTHCHECK` nyata (bukan `curl localhost` tanpa path).
- [ ] Tidak ada secret di layer (`docker history`), `.dockerignore` benar.
- [ ] Ukuran wajar; tag immutable (digest), bukan `latest` di produksi.
- [ ] Scan: `security-forge image <ref>` (trivy) → 0 HIGH/CRITICAL.

## 2. Kubernetes
```bash
kubeconform -strict -summary -ignore-missing-schemas k8s/
helm lint chart && helm template rel chart | kubeconform -strict -summary -
kubectl apply --dry-run=server -f k8s/
kubectl rollout status deploy/app --timeout=120s
```
Checklist manifest:
- [ ] `runAsNonRoot`, `readOnlyRootFilesystem`, `allowPrivilegeEscalation: false`, seccomp.
- [ ] `requests`/`limits` CPU+memori; probe readiness & liveness (path nyata).
- [ ] PDB, HPA, NetworkPolicy default-deny, Ingress TLS.
- [ ] Secret lewat Secret/External-Secrets, bukan env plaintext di manifest.
- [ ] `terminationGracePeriodSeconds` ≥ waktu drain.

## 3. Smoke & rollback (wajib setiap deploy)
```bash
BASE=https://staging.example.com
curl -fsS $BASE/health | jq -e '.status=="ok"'
curl -fsS $BASE/api/items?limit=1 -o /dev/null -w '%{http_code}\n'
security-forge headers $BASE | tail -3
# rollback kalau smoke gagal
kubectl rollout undo deploy/app           # atau: docker compose up -d --force-recreate <tag sebelumnya>
```
Gate: health 200, 1 endpoint baca 200, 1 endpoint tulis (sandbox) 201, tidak ada 5xx baru
di log 5 menit pertama, error rate < 0.1%, p95 sesuai anggaran.

## 4. Konfigurasi & drift
- Semua konfigurasi dari env/secret, tidak ada nilai berbeda antara staging & prod tanpa alas an.
- Uji: hapus satu env wajib → aplikasi **gagal cepat** dengan pesan jelas (bukan jalan setengah).
- Uji: secret salah → error jelas, tidak mencetak nilai secret ke log.
- Uji: `.env.example` lengkap (bandingkan dengan yang dibaca kode).

## 5. Chaos & ketahanan (di staging, terjadwal)
| Gangguan | Harapan |
|---|---|
| Matikan 1 instance | trafik pindah, tidak ada downtime (readiness benar) |
| DB mati 30 detik | retry/backoff, pesan ramah, pulih otomatis tanpa restart manual |
| Redis/cache mati | fallback ke DB, tetap jalan (lebih lambat) |
| Latensi jaringan +2 s | timeout masuk akal, tidak menggantung selamanya |
| Disk penuh | gagal terkontrol, tidak korup |
| Clock skew | token/JWT tidak salah tolak |
| Dependency pihak ketiga 500 | circuit breaker, degradasi bertahap |
| Payload 100 MB | ditolak 413, memori tidak meledak |

## 6. Backup & DR (uji, jangan asumsikan)
- RPO/RTO ditulis; uji restore ke lingkungan bersih dan ukur waktunya.
- Uji: restore 1 tabel, restore penuh, point-in-time (PITR).
- Verifikasi isi (jumlah baris + checksum), bukan cuma "restore selesai".
- Runbook: siapa melakukan apa, perintah persisnya, kontak.

## 7. Observability sebagai test
- Log terstruktur (JSON) dengan `trace_id`, tanpa PII.
- Metrik: request rate, error rate, latency, saturasi; alert punya ambang & pemilik.
- Trace: satu request menghasilkan satu trace lengkap (frontend → API → DB).
- Uji: buat error sengaja → alert muncul < 5 menit; log bisa dicari lewat `trace_id`.
- Health/ready: `/health` (liveness, tanpa dependency) vs `/ready` (dependency dicek).

## 8. Definition of Done infra
- [ ] `security-forge audit` + `image` bersih (0 HIGH/CRITICAL).
- [ ] Manifest/compose lolos validator; dry-run server sukses.
- [ ] Smoke otomatis setelah deploy + rollback teruji (pernah dijalankan).
- [ ] Restore backup dibuktikan dengan angka waktu & checksum.
- [ ] Minimal 1 skenario chaos dijalankan dan hasilnya dicatat.
