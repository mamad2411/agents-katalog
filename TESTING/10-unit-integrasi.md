# 10 — Unit, component, dan integrasi

## 1. Unit test (paling murah, paling banyak)
Aturan: satu perilaku, tanpa I/O, tanpa jaringan, tanpa DB, tanpa waktu nyata.

```python
# python — pytest
@pytest.mark.parametrize("qty,harga,harap", [
    (1, 10_000, 10_000),
    (0, 10_000, 0),
    (3, 10_000, 30_000),
])
def test_total_sebelum_pajak(qty, harga, harap):
    assert hitung_total(qty, harga) == harap

def test_total_menolak_qty_negatif():
    with pytest.raises(ValueError, match="qty"):
        hitung_total(-1, 10_000)
```

```ts
// ts — vitest
import { describe, expect, it } from "vitest"
describe("hitungTotal", () => {
  it.each([[1, 10000, 10000], [0, 10000, 0], [3, 10000, 30000]])(
    "qty %i harga %i → %i", (q, h, harap) => expect(hitungTotal(q, h)).toBe(harap))
  it("menolak qty negatif", () => expect(() => hitungTotal(-1, 10000)).toThrow(/qty/))
})
```

Cakupan yang wajib: cabang keputusan, batas, error path, dan **setiap bug yang pernah
terjadi** (regression test permanen).

Property-based (menemukan kasus yang tidak terpikir):
```python
from hypothesis import given, strategies as st
@given(st.text(), st.integers(min_value=0, max_value=10_000))
def test_encode_decode_identik(teks, qty):
    assert decode(encode({"t": teks, "q": qty})) == {"t": teks, "q": qty}
```

## 2. Component / frontend unit (Testing Library, bukan snapshot buta)
```tsx
render(<Form onSubmit={spy} />)
await user.type(screen.getByLabelText(/email/i), "a@b.co")
await user.click(screen.getByRole("button", { name: /simpan/i }))
expect(spy).toHaveBeenCalledWith({ email: "a@b.co" })
```
- Query urutan prioritas: `getByRole` → `getByLabelText` → `getByText` → `getByTestId`
  (testid hanya bila tak ada aksesibel name).
- Uji: loading, error, empty, disabled, validasi, keyboard, fokus.
- Jangan uji implementasi (state internal, class CSS) — uji yang dilihat pengguna.
- Mock jaringan dengan **MSW** (bukan mock modul fetch), supaya jalur nyata tetap dipakai.

## 3. Integrasi: kode + dependency nyata
| Integrasi | Cara benar | Jangan |
|---|---|---|
| DB | Postgres/MySQL via container, migrasi dijalankan, rollback per test | sqlite kalau produksi Postgres (beda semantik) |
| Cache/queue | Redis/RabbitMQ container, verifikasi publish→consume | mock total |
| HTTP keluar | WireMock/prism/MSW dengan kontrak nyata | mock tanpa skema |
| File/object storage | MinIO lokal | path hardcode |
| Waktu | fake clock | `sleep(2)` |
| Email/SMS | penyedia sandbox atau outbox yang di-assert | kirim nyata |

```python
# fixture DB: transaksi dibungkus, di-rollback
@pytest.fixture
def db(engine):
    conn = engine.connect(); tx = conn.begin()
    yield Session(bind=conn)
    tx.rollback(); conn.close()
```

Checklist integrasi:
- [ ] Migrasi up dari nol berhasil (bukan hanya dari DB yang sudah ada).
- [ ] Constraint benar-benar menolak data salah (unique, FK, check).
- [ ] Transaksi: gagal di tengah → tidak ada data separuh.
- [ ] Konkurensi: dua update bersamaan → tidak ada lost update (uji `SELECT ... FOR UPDATE`).
- [ ] N+1 tidak muncul (hitung query: `assert len(queries) < 5`).
- [ ] Pagination/sort/filter konsisten dan stabil (ada tiebreaker).

## 4. Mock: aturan
Boleh dimock: jaringan luar, jam, acak, sistem file (bila tak relevan), layanan berbayar.
Jangan dimock: logika milik sendiri, validasi, lapisan yang sedang diuji.
Mock harus **gagal** bila kontrak berubah (pakai schema/type, bukan `MagicMock` bebas).

## 5. Coverage: arti yang benar
- Baris 70–85% cukup; 100% bukan tujuan.
- Wajib 100% untuk: kode uang/pajak/authz/migrasi.
- Coverage tanpa assertion = angka kosong. Cek mutasi sekali per modul kritis
  (`mutmut`, `stryker`) — kalau test tidak membunuh mutan, test-nya lemah.

## 6. Perintah
```bash
uv run pytest -q                       # python
uv run pytest --cov=src --cov-report=term-missing
npx vitest run --coverage              # ts/js
go test ./... -race -cover             # go
cargo test --all-targets               # rust
dotnet test --nologo                   # c#
php artisan test                       # php
```
