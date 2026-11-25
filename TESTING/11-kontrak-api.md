# 11 — Kontrak & API testing (REST, GraphQL, gRPC, WebSocket)

## 1. Kontrak dulu, baru kode
Sumber kebenaran: `openapi.yaml` / `*.proto` / `schema.graphql` / Pact. Test kontrak
memastikan **bentuk** dan **perilaku** tidak berubah tanpa sengaja.

```bash
# 1) spec → validasi request/response nyata
npx --yes @stoplight/spectral-cli lint openapi.yaml          # gaya + kesalahan spec
python3 -m schemathesis run openapi.yaml --base-url http://localhost:8000 \
        --checks all --hypothesis-max-examples 50                 # fuzz + property
# 2) konsumen vs penyedia (Pact)
npx --yes pactum ...
```

Wajib ada di spec: setiap endpoint punya 2xx, 4xx, 5xx, contoh, tipe, batas,
autentikasi, rate limit. Spec yang tidak punya 4xx = belum selesai.

## 2. Matriks test API (salin per endpoint)
| Dimensi | Kasus minimum |
|---|---|
| Metode | method salah → 405 + `Allow` |
| Path | id tidak ada → 404; id salah format → 400; trailing slash konsisten |
| Body | kosong, bukan JSON, field ekstra, field hilang, tipe salah, terlalu besar → 413/422 |
| AuthN | tanpa token → 401; token kedaluwarsa → 401; token dicabut → 401; signature salah |
| AuthZ | user A akses resource B → 403 (bukan 404 bocor); role naik → 403 |
| Idempotensi | POST dengan `Idempotency-Key` 2× → 1 efek samping |
| Pagination | page 0/negatif, limit 0/1000, cursor rusak, total benar |
| Sorting/filter | field tak dikenal → 400; nilai aneh tetap aman |
| Konkurensi | 2 update bersamaan → 409/optimistic lock, bukan lost update |
| Rate limit | 429 + `Retry-After` |
| Error format | schema error konsisten (`type`, `title`, `detail`, `trace_id`) |
| Header | `Content-Type` salah → 415; `Accept` tak didukung → 406 |
| Unicode/encoding | emoji, RTL, NUL, 1 MB teks |
| Keamanan input | SQLi, XSS, template injection, path traversal, SSRF, JSON bomb |
| Observability | response punya `trace_id`; error tercatat di log |
| Performa | p95 sesuai anggaran (lihat `14-performa.md`) |

## 3. Contoh test API (python + httpx, tanpa server nyata dapat dipakai)
```python
import httpx, pytest

@pytest.mark.parametrize("payload,status", [
    ({"name": "ok"}, 201),
    ({}, 422),
    ({"name": ""}, 422),
    ({"name": "x" * 5000}, 422),
])
def test_create_item(client: httpx.Client, payload, status):
    r = client.post("/items", json=payload)
    assert r.status_code == status
    if status == 422:
        assert r.json()["type"].endswith("validation_error")

def test_user_tidak_bisa_baca_item_user_lain(client, token_a, item_b):
    r = client.get(f"/items/{item_b.id}", headers={"Authorization": f"Bearer {token_a}"})
    assert r.status_code in (403, 404)          # jangan bocorkan keberadaan
```

## 4. GraphQL
- Introspection dimatikan di produksi (uji: query `__schema` → ditolak).
- Uji: field tidak ada → error jelas; depth/besar query → ditolak (limit kompleksitas);
  N+1 (hitung resolver call); nullability; fragment; batched query; authz per field.
- DataLoader: uji 1 query untuk 50 item, bukan 51.

## 5. gRPC
- `grpcurl` untuk smoke; `buf lint`/`buf breaking` untuk kompatibilitas.
- Uji: deadline/timeout, metadata auth, status code (`INVALID_ARGUMENT`, `PERMISSION_DENIED`,
  `NOT_FOUND`, `RESOURCE_EXHAUSTED`), streaming setengah putus, pesan maksimum.

## 6. WebSocket / SSE
- Handshake tanpa token → ditolak; token kedaluwarsa saat koneksi.
- Pesan tidak valid tidak mematikan server; reconnect + resume (last event id).
- Ordering, duplikasi, backpressure, slow consumer, limit koneksi per user.

## 7. Fuzz & property (menemukan yang tidak terpikir)
```python
# hypothesis untuk payload acak; schemathesis untuk kontrak
@given(st.dictionaries(st.text(), st.one_of(st.text(), st.integers(), st.none())))
def test_endpoint_tidak_pernah_500(client, payload):
    r = client.post("/items", json=payload)
    assert r.status_code < 500, r.text
```
Aturan: 5xx untuk input pengguna = **bug**, bukan "input aneh".

## 8. Perintah
```bash
uv run pytest -q tests/api
python3 -m schemathesis run openapi.yaml --base-url $URL --checks all
npx --yes @stoplight/spectral-cli lint openapi.json
k6 run load.js                              # beban (lihat 14)
```
