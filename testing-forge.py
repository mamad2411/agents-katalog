#!/usr/bin/env python3
"""testing-forge — peta, rencana, scaffold, dan audit JENIS test (bukan coverage baris).

0 token, tanpa MCP. Semua orang/AI bisa memakai ini untuk tahu test apa yang wajib.

  testing-forge matrix                         # peta lapisan x jenis x teknik (jumlah kombinasi)
  testing-forge layers                         # daftar lapisan + dokumen + alat
  testing-forge show <lapisan>                 # ringkas 1 lapisan + checklist
  testing-forge plan --stack web --risk high
  testing-forge generate tests-web --stack web # playwright + vitest + axe + k6 siap jalan
  testing-forge generate tests-api --stack api # pytest + httpx + schemathesis + k6
  testing-forge audit <dir>                    # jenis test yang belum ada di repo
  testing-forge selftest                       # cek katalog internal (dipakai CI)

Dokumen lengkap: ~/.agents/TESTING.md -> ~/.agents/TESTING/*.md
"""
import json
import os
import re
import sys

AG = os.path.dirname(os.path.realpath(__file__))
TDIR = os.path.join(AG, "TESTING")

# ─── katalog lapisan ─────────────────────────────────────────────────────────
LAYERS = {
    "unit": {
        "title": "Unit & component", "doc": "10-unit-integrasi.md", "speed": "< 100 ms",
        "tools": ["pytest", "vitest", "go test", "cargo test", "dotnet test"],
        "gate": "semua cabang keputusan kode yang berubah",
        "checklist": [
            "satu perilaku per test, nama jelas (perilaku_kondisi_harapan)",
            "batas: 0, -1, maks, string kosong, unicode",
            "error path diuji (raise/throw), bukan hanya happy path",
            "waktu & acak di-freeze",
            "setiap bug lama punya test regresi permanen",
        ],
    },
    "integrasi": {
        "title": "Integrasi (DB, queue, cache, storage)", "doc": "10-unit-integrasi.md",
        "speed": "< 1 s", "tools": ["pytest + postgres container", "testcontainers", "docker compose"],
        "gate": "constraint, transaksi, konkurensi, migrasi up dari DB kosong",
        "checklist": [
            "pakai DB nyata (Postgres/MySQL), bukan sqlite bila produksi bukan sqlite",
            "rollback/truncate per test, data tidak saling ganggu",
            "uji unique/FK/check benar-benar menolak data salah",
            "uji dua update bersamaan (lost update)",
            "hitung query untuk mendeteksi N+1",
        ],
    },
    "kontrak": {
        "title": "Kontrak API (OpenAPI, Pact, proto, GraphQL)", "doc": "11-kontrak-api.md",
        "speed": "< 5 s", "tools": ["schemathesis", "spectral", "pact", "buf", "prism"],
        "gate": "spec punya 2xx/4xx/5xx + contoh; bentuk respons tidak berubah tak sengaja",
        "checklist": [
            "setiap endpoint punya minimal satu kasus 4xx",
            "authz matrix: anon/user/staff/admin per endpoint sensitif",
            "masukan aneh tidak boleh 5xx (harus 4xx)",
            "idempotency key diuji 2x -> 1 efek samping",
            "pagination/sort/filter stabil & punya tiebreaker",
        ],
    },
    "e2e": {
        "title": "E2E browser (Playwright)", "doc": "12-e2e-browser.md", "speed": "< 60 s/skenario",
        "tools": ["playwright", "playwright device profiles", "storageState"],
        "gate": "3-10 alur kritis hijau di Chromium+WebKit+Firefox",
        "checklist": [
            "hanya alur uang/kepercayaan (login, checkout, bayar, unduh, hapus akun)",
            "selector role/label, bukan CSS/XPath/nth",
            "data dibuat lewat API/seed, bukan UI",
            "login sekali -> storageState dipakai ulang",
            "tidak ada waitForTimeout; tunggu kondisi nyata",
        ],
    },
    "visual": {
        "title": "Visual regression & UI", "doc": "12-e2e-browser.md", "speed": "< 30 s",
        "tools": ["dvisual", "playwright --update-snapshots"],
        "gate": "diff piksel <= 0.1% per viewport (360/768/1440) & tema",
        "checklist": [
            "baseline per viewport dan per tema",
            "mask konten dinamis (tanggal, avatar), bukan seluruh halaman",
            "review manual bila diff di atas ambang",
        ],
    },
    "a11y": {
        "title": "Aksesibilitas (WCAG 2.2 AA)", "doc": "15-a11y-i18n.md", "speed": "< 20 s",
        "tools": ["axe", "pa11y", "dcheck", "playwright + axe"],
        "gate": "0 violation serius/kritis; kontras >= 4.5:1; target sentuh >= 24 px",
        "checklist": [
            "seluruh alur kritis bisa diselesaikan dengan keyboard",
            "fokus terlihat, tidak ada focus trap, Esc menutup modal",
            "label form eksplisit + error terhubung aria-describedby",
            "status tidak hanya dibedakan warna",
        ],
    },
    "i18n": {
        "title": "i18n / l10n / format", "doc": "15-a11y-i18n.md", "speed": "< 20 s",
        "tools": ["Intl.NumberFormat/DateTimeFormat", "render per locale"],
        "gate": "locale id + 1 locale panjang + 1 RTL tanpa overflow",
        "checklist": [
            "angka/tanggal/mata uang lewat API locale, bukan string manual",
            "pluralisasi ICU, bukan if-else",
            "tidak ada string UI hardcode",
            "kunci terjemahan hilang tercatat, bukan undefined",
        ],
    },
    "performa": {
        "title": "Performa & beban", "doc": "14-performa.md", "speed": "menit",
        "tools": ["k6", "locust", "ab", "lighthouse", "dref"],
        "gate": "p95 baca <= 200 ms, tulis <= 400 ms, error < 0.1%, LCP <= 2.5 s",
        "checklist": [
            "threshold ditulis di kode (k6 thresholds) supaya CI bisa gagal",
            "pantau CPU/RAM/DB/latensi bersamaan, bukan hanya klien",
            "uji spike dan soak terpisah dari load",
            "setiap query baru punya EXPLAIN tanpa Seq Scan tabel besar",
        ],
    },
    "security": {
        "title": "Keamanan (OWASP/API10)", "doc": "13-security.md", "speed": "menit",
        "tools": ["security-forge", "semgrep", "bandit", "gitleaks", "trivy", "nuclei", "zap"],
        "gate": "0 HIGH/CRITICAL, 0 secret nyata, TLS 1.2+, authz matrix lulus",
        "checklist": [
            "IDOR: ganti id/tenant -> 403/404, bukan bocor",
            "mass assignment: kirim role=admin -> diabaikan",
            "rate limit: 1000 paralel -> 429, bukan 5xx",
            "upload: MIME nyata, ekstensi ganda, zip bomb, path traversal",
            "error tidak membocorkan stack trace/PII",
        ],
    },
    "data": {
        "title": "Data, DB, migrasi", "doc": "16-data-db-ml.md", "speed": "menit",
        "tools": ["pytest + container", "pg_dump/pg_restore", "pandera", "dbt tests"],
        "gate": "migrasi up dari DB kosong + rollback; backup/restore dibuktikan",
        "checklist": [
            "migrasi idempoten (2x tidak gagal)",
            "transaksi gagal di tengah tidak menyisakan data separuh",
            "backup & restore diuji dengan jumlah baris/checksum",
            "encoding unicode/emoji utuh; waktu disimpan UTC",
        ],
    },
    "ml": {
        "title": "ML & model", "doc": "16-data-db-ml.md", "speed": "menit",
        "tools": ["pytest", "eval harness", "great_expectations"],
        "gate": "metrik holdout > baseline; drift & fairness tercatat",
        "checklist": [
            "evaluasi hanya pada data yang tidak dipakai latih",
            "bandingkan dengan baseline naif",
            "metrik per segmen (gender/wilayah/usia)",
            "uji prompt injection & kebocoran PII pada output",
            "seed + versi data/dependency tercatat (reproducible)",
        ],
    },
    "infra": {
        "title": "Infra, deploy, chaos, DR", "doc": "17-infra-deploy-chaos.md", "speed": "menit",
        "tools": ["hadolint", "docker compose config", "kubeconform", "helm lint", "terraform validate", "ansible-lint"],
        "gate": "manifest valid, smoke hijau setelah deploy, rollback pernah diuji",
        "checklist": [
            "container non-root, read-only, cap_drop ALL, HEALTHCHECK nyata",
            "k8s: requests/limits, probe, PDB, NetworkPolicy, runAsNonRoot",
            "env wajib hilang -> gagal cepat dengan pesan jelas",
            "minimal 1 skenario chaos dijalankan & dicatat",
            "restore backup diukur waktu + diverifikasi isi",
        ],
    },
    "manual": {
        "title": "Manual, exploratory, UAT, regresi", "doc": "18-manual-uat-regresi.md", "speed": "30-60 menit",
        "tools": ["charter SFDPOT", "checklist UAT", "bug report format"],
        "gate": "charter tercatat; UAT P1/P2 lulus dengan bukti; bug -> test regresi",
        "checklist": [
            "charter tertulis: tujuan, area, durasi, heuristik",
            "tur: CRUD, state transition, data aneh, jaringan, interupsi, akses",
            "bug report lengkap (langkah, aktual, harapan, bukti, prioritas)",
            "UAT kriteria Given/When/Then disetujui sebelum dikerjakan",
        ],
    },
    "ci": {
        "title": "Gate CI & rilis", "doc": "19-ci-gate-policy.md", "speed": "< 15 menit/PR",
        "tools": ["github actions", "gitlab ci", "pre-commit"],
        "gate": "semua gate wajib hijau di commit yang dirilis; rollback teruji",
        "checklist": [
            "urutan cepat -> lambat, gagal cepat",
            "tidak ada continue-on-error pada gate wajib",
            "flake dikarantina maksimal 7 hari bertiket",
            "coverage 70-85%, modul uang/authz 100% cabang",
            "canary 5% -> 25% -> 50% -> 100% dengan kriteria angka",
        ],
    },
}

KINDS = [
    "functional", "regression", "smoke", "sanity", "exploratory", "usability",
    "accessibility", "i18n", "compatibility", "install-upgrade", "recovery",
    "failover", "disaster-recovery", "concurrency", "idempotency",
    "data-integrity", "migration", "backup-restore", "performance-load",
    "performance-stress", "performance-soak", "performance-spike", "scalability",
    "security-sast", "security-dast", "security-sca", "security-secrets",
    "security-authz", "fuzz", "property-based", "mutation", "differential",
    "contract", "chaos", "observability", "privacy-compliance", "cost",
]

TECHNIQUES = [
    "equivalence-partitioning", "boundary-value", "decision-table",
    "state-transition", "pairwise-combinatorial", "cause-effect",
    "error-guessing", "property-based", "mutation", "differential",
    "fuzz", "model-based", "risk-based",
]

STACKS = {
    "web": ["unit", "integrasi", "kontrak", "e2e", "visual", "a11y", "i18n", "performa", "security", "ci"],
    "api": ["unit", "integrasi", "kontrak", "performa", "security", "data", "ci"],
    "cli": ["unit", "kontrak", "manual", "security", "ci"],
    "lib": ["unit", "kontrak", "ci"],
    "data": ["unit", "integrasi", "data", "performa", "security", "ci"],
    "ml": ["unit", "integrasi", "ml", "data", "performa", "ci"],
    "infra": ["infra", "security", "performa", "ci", "manual"],
    "mobile": ["unit", "integrasi", "e2e", "visual", "a11y", "performa", "security", "ci"],
    "desktop": ["unit", "integrasi", "e2e", "visual", "manual", "security", "ci"],
}


def jml_kombinasi():
    return len(LAYERS) * len(KINDS) * len(TECHNIQUES)


def cmd_matrix():
    print(f"lapisan: {len(LAYERS)} · jenis test: {len(KINDS)} · teknik desain: {len(TECHNIQUES)}")
    print(f"kombinasi yang bisa dibentuk: {jml_kombinasi():,}".replace(",", "."))
    print("\nLapisan                     Kecepatan      Alat utama")
    print("-" * 78)
    for k, v in LAYERS.items():
        print(f"{k:<26} {v['speed']:<14} {', '.join(v['tools'][:3])}")
    print("\nJenis test: " + ", ".join(KINDS))
    print("\nTeknik: " + ", ".join(TECHNIQUES))
    print("\nPilih yang menutup risiko, bukan semua. Lihat ~/.agents/TESTING.md §2-§5.")


def cmd_layers():
    for k, v in LAYERS.items():
        print(f"{k:<12} {v['title']}")
        print(f"  dokumen : TESTING/{v['doc']}")
        print(f"  alat    : {', '.join(v['tools'])}")
        print(f"  gate    : {v['gate']}")


def cmd_show(layer):
    v = LAYERS.get(layer)
    if not v:
        print(f"lapisan tidak ada: {layer}. Pilihan: {', '.join(LAYERS)}")
        return 1
    print(f"# {v['title']}  ({layer})")
    print(f"dokumen : ~/.agents/TESTING/{v['doc']}")
    print(f"kecepatan: {v['speed']}")
    print(f"alat    : {', '.join(v['tools'])}")
    print(f"gate    : {v['gate']}")
    print("\nchecklist:")
    for c in v["checklist"]:
        print(f"  - [ ] {c}")
    return 0


RISK_EXTRA = {
    "low": [],
    "medium": ["security", "kontrak"],
    "high": ["security", "performa", "data", "manual"],
    "critical": ["security", "performa", "data", "manual", "infra"],
}


def cmd_plan(stack, risk):
    if stack not in STACKS:
        print(f"stack tidak ada: {stack}. Pilihan: {', '.join(STACKS)}")
        return 1
    if risk not in RISK_EXTRA:
        print(f"risk tidak ada: {risk}. Pilihan: {', '.join(RISK_EXTRA)}")
        return 1
    lap = []
    for x in STACKS[stack] + RISK_EXTRA[risk]:
        if x not in lap:
            lap.append(x)
    urut = [k for k in LAYERS if k in lap]
    print(f"# Rencana testing · stack={stack} · risiko={risk}")
    print("urutan wajib (murah -> mahal):")
    for i, k in enumerate(urut, 1):
        v = LAYERS[k]
        print(f"{i}. {v['title']}  [{k}]  ({v['speed']})")
        print(f"   alat : {', '.join(v['tools'][:3])}")
        print(f"   gate : {v['gate']}")
        print(f"   baca : TESTING/{v['doc']}")
    print("\nJangan mulai dari e2e. Tulis test yang gagal dulu (red) -> baru implementasi.")
    print("Lampirkan bukti: perintah + exit code + ringkasan hasil.")
    return 0


# ─── templates scaffold ──────────────────────────────────────────────────────
T_WEB = {
    "package.json": """{
  "name": "tests-web",
  "private": true,
  "type": "module",
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "e2e": "playwright test",
    "a11y": "axe http://localhost:3000 --exit",
    "load": "k6 run load.js"
  },
  "devDependencies": {
    "@axe-core/cli": "^4.9.0",
    "@axe-core/playwright": "^4.10.0",
    "@playwright/test": "^1.47.0",
    "@testing-library/dom": "^10.4.0",
    "@testing-library/user-event": "^14.5.2",
    "jsdom": "^25.0.0",
    "msw": "^2.4.0",
    "vitest": "^2.1.0"
  }
}
""",
    "vitest.config.ts": """import { defineConfig } from "vitest/config"
export default defineConfig({
  test: { environment: "jsdom", globals: true, include: ["src/**/*.test.ts"] },
})
""",
    "src/harga.test.ts": """import { describe, expect, it } from "vitest"
import { hitungTotal } from "./harga.js"

// oracle: total = qty * harga; qty negatif harus ditolak
describe("hitungTotal", () => {
  it.each([[1, 10_000, 10_000], [0, 10_000, 0], [3, 10_000, 30_000]])(
    "qty %i harga %i -> %i", (q, h, harap) => expect(hitungTotal(q, h)).toBe(harap))
  it("menolak qty negatif", () => expect(() => hitungTotal(-1, 10_000)).toThrow(/qty/))
})
""",
    "src/harga.ts": """export function hitungTotal(qty: number, harga: number): number {
  if (!Number.isInteger(qty) || qty < 0) throw new Error("qty harus bilangan bulat >= 0")
  if (harga < 0) throw new Error("harga tidak boleh negatif")
  return qty * harga
}
""",
    "playwright.config.ts": """import { defineConfig, devices } from "@playwright/test"
export default defineConfig({
  testDir: "e2e",
  retries: 0,
  reporter: [["list"], ["html", { open: "never" }]],
  use: {
    baseURL: process.env.BASE_URL ?? "http://localhost:3000",
    trace: "on-first-retry", video: "retain-on-failure",
    screenshot: "only-on-failure", locale: "id-ID", timezoneId: "Asia/Jakarta",
  },
  projects: [
    { name: "chromium", use: devices["Desktop Chrome"] },
    { name: "firefox", use: devices["Desktop Firefox"] },
    { name: "webkit", use: devices["Desktop Safari"] },
    { name: "mobile", use: devices["iPhone 15"] },
  ],
})
""",
    "e2e/alur-kritis.spec.ts": """import { expect, test } from "@playwright/test"

test("pengguna bisa menyelesaikan alur kritis", async ({ page }) => {
  await page.goto("/")
  // sesuaikan selector dengan role/label nyata aplikasi
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible()
  await page.getByRole("link", { name: /masuk/i }).click()
  await page.getByLabel(/email/i).fill(process.env.UJI_EMAIL ?? "uji@example.com")
  await page.getByLabel(/kata sandi/i).fill(process.env.UJI_SANDI ?? "Rahasia123!")
  await page.getByRole("button", { name: /masuk/i }).click()
  await expect(page.getByRole("heading", { name: /produk|dashboard/i })).toBeVisible()
})

test("tidak ada error console baru", async ({ page }) => {
  const galat: string[] = []
  page.on("console", (m) => m.type() === "error" && galat.push(m.text()))
  await page.goto("/")
  expect(galat).toEqual([])
})
""",
    "e2e/a11y.spec.ts": """import AxeBuilder from "@axe-core/playwright"
import { expect, test } from "@playwright/test"

test("halaman utama tidak punya pelanggaran serius", async ({ page }) => {
  await page.goto("/")
  const hasil = await new AxeBuilder({ page }).analyze()
  const serius = hasil.violations.filter((v) => ["serious", "critical"].includes(v.impact ?? ""))
  expect(serius, JSON.stringify(serius.map((v) => v.id))).toEqual([])
})
""",
    "load.js": """import http from "k6/http"
import { check, sleep } from "k6"

export const options = {
  stages: [
    { duration: "30s", target: 10 },
    { duration: "2m", target: 20 },
    { duration: "30s", target: 0 },
  ],
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<200", "p(99)<500"],
  },
}

export default function () {
  const r = http.get(`${__ENV.BASE_URL ?? "http://localhost:3000"}/`)
  check(r, { "status 200": (x) => x.status === 200 })
  sleep(1)
}
""",
}

T_API = {
    "requirements.txt": """pytest>=8
pytest-cov>=5
httpx>=0.27
hypothesis>=6
schemathesis>=3.3
locust>=2.29
fastapi>=0.115
""",
    "app.py": """\"\"\"Stub API pengganti: ganti dengan aplikasi Anda, test tetap sama.\"\"\"
from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="contoh")


class Item(BaseModel):
    name: str = Field(min_length=1, max_length=1000)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/items", status_code=status.HTTP_201_CREATED)
def buat_item(item: Item):
    return {"id": 1, "name": item.name}


@app.delete("/users/{uid}", status_code=status.HTTP_200_OK)
def hapus_user(uid: int, authorization: str | None = Header(default=None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="butuh token")
    role = authorization.split("token-", 1)[1].split("-")[0] if "token-" in authorization else "user"
    if role not in ("staff", "admin"):
        raise HTTPException(status_code=403, detail="tidak berwenang")
    return {"dihapus": uid}
""",
    "tests/test_health.py": """import pytest


def test_health_selalu_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


@pytest.mark.parametrize("payload,status", [
    ({"name": "ok"}, 201),
    ({}, 422),
    ({"name": ""}, 422),
    ({"name": "x" * 5_000}, 422),
])
def test_create_item_validasi(client, payload, status):
    r = client.post("/items", json=payload)
    assert r.status_code == status, r.text
""",
    "tests/test_authz.py": """import pytest

# matriks otorisasi: anon=401, user=403, staff/admin=200
KASUS = [("anon", 401), ("user", 403), ("staff", 200), ("admin", 200)]


@pytest.mark.parametrize("role,harap", KASUS)
def test_hapus_user_hanya_staff(client, token, role, harap):
    r = client.delete("/users/2", headers=token(role))
    assert r.status_code == harap, r.text
""",
    "tests/test_fuzz.py": """from hypothesis import given, settings, strategies as st


@settings(max_examples=50, deadline=None)
@given(st.dictionaries(st.text(), st.one_of(st.text(), st.integers(), st.none())))
def test_endpoint_tidak_pernah_500(client, payload):
    # 5xx untuk input pengguna = bug, bukan "input aneh"
    r = client.post("/items", json=payload)
    assert r.status_code < 500, r.text
""",
    "tests/conftest.py": """import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE = "http://localhost:8000"


@pytest.fixture(scope="session")
def client():
    \"\"\"Utamakan app lokal (tanpa server). Set BASE_URL untuk menguji server nyata.\"\"\"
    import os

    import httpx

    url = os.environ.get("BASE_URL")
    if not url:
        try:
            from fastapi.testclient import TestClient

            from app import app as asgi_app

            with TestClient(asgi_app) as c:
                yield c
            return
        except Exception:
            pass
    with httpx.Client(base_url=url or BASE, timeout=10) as c:
        yield c


@pytest.fixture
def token():
    def _buat(role: str):
        if role == "anon":
            return {}
        return {"Authorization": f"Bearer token-{role}-uji"}
    return _buat
""",
    "locustfile.py": """from locust import HttpUser, between, task


class ApiUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def baca_daftar(self):
        self.client.get("/items?limit=20", name="/items")

    @task(1)
    def health(self):
        self.client.get("/health", name="/health")
""",
}

T_CLI = {
    "app.py": """\"\"\"Stub CLI pengganti: sesuaikan dengan perintah nyata aplikasi.\"\"\"
import argparse
import sys

VERSI = "0.1.0"


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="app")
    sub = p.add_subparsers(dest="perintah")
    sub.add_parser("versi", help="tampilkan versi")
    sub.add_parser("count", help="hitung baris dari stdin")
    a = p.parse_args(argv)
    if a.perintah == "versi":
        print(f"app {VERSI}")
        return 0
    if a.perintah == "count":
        print(len([b for b in sys.stdin.read().splitlines() if b.strip()]))
        return 0
    p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
""",
    "tests/test_cli.py": """import subprocess
import sys


def jalankan(*args):
    return subprocess.run([sys.executable, "-m", "app", *args], capture_output=True, text=True)


def test_help_exit_nol():
    r = jalankan("--help")
    assert r.returncode == 0
    assert "usage" in r.stdout.lower()


def test_argumen_tidak_dikenal_exit_nol_bukan():
    r = jalankan("--tidak-ada")
    assert r.returncode != 0
    assert r.stderr.strip()


def test_stdin_pipe():
    r = subprocess.run([sys.executable, "-m", "app", "count"], input="a\\nb\\n",
                       capture_output=True, text=True)
    assert r.returncode == 0
    assert r.stdout.strip() == "2"


def test_output_snapshot():
    r = jalankan("versi")
    assert r.stdout.strip() == open("tests/snapshot_versi.txt").read().strip()
""",
    "tests/snapshot_versi.txt": "app 0.1.0\n",
}

T_LIB = {
    "mylib.py": """\"\"\"Stub pengganti: ganti dengan paket Anda, atau sesuaikan import di test.\"\"\"


def utama(x: int) -> int:
    return x * 2


versi = "0.1.0"
""",
    "tests/conftest.py": """import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
""",
    "tests/test_api_publik.py": """import mylib


def test_api_publik_stabil():
    # nama & signature yang dijanjikan ke pengguna tidak boleh hilang
    for nama in ("utama", "versi"):
        assert hasattr(mylib, nama)


def test_import_sebagai_konsumen():
    import importlib
    m = importlib.import_module("mylib")
    assert m.utama(2) == 4
""",
    "tests/test_tipe.py": """from typing import get_type_hints


def test_anotasi_tipe_lengkap():
    import mylib
    hints = get_type_hints(mylib.utama)
    assert "return" in hints
""",
}

T_INFRA = {
    "smoke.sh": """#!/usr/bin/env bash
# Smoke setelah deploy. exit != 0 -> rollback.
set -euo pipefail
BASE="${BASE_URL:?BASE_URL wajib diisi}"

status=$(curl -fsS -o /dev/null -w '%{http_code}' "$BASE/health")
[[ "$status" == "200" ]] || { echo "health gagal: $status"; exit 1; }

curl -fsS "$BASE/api/items?limit=1" >/dev/null || { echo "endpoint baca gagal"; exit 1; }

security-forge headers "$BASE" | tail -3 || true
echo "SMOKE OK: $BASE"
""",
    "chaos-checklist.md": """# Checklist chaos (jalankan di staging)

| Gangguan | Harapan | Hasil |
|---|---|---|
| Matikan 1 instance | trafik pindah, tanpa downtime | [ ] |
| DB mati 30 s | retry/backoff, pulih otomatis | [ ] |
| Cache mati | fallback DB, tetap jalan | [ ] |
| Latensi +2 s | timeout masuk akal | [ ] |
| Disk penuh | gagal terkontrol | [ ] |
| Dependency 500 | circuit breaker | [ ] |
| Payload 100 MB | 413, memori aman | [ ] |
""",
}

T_DATA = {
    "tests/test_migrasi.py": """import subprocess

import pytest


@pytest.fixture
def db_bersih():
    # jalankan postgres sementara; sesuaikan URL dengan lingkungan
    url = "postgresql://dev:dev@localhost:55432/uji"
    subprocess.run(["createdb", "-h", "localhost", "-p", "55432", "-U", "dev", "uji"],
                   check=False, capture_output=True)
    return url


def test_migrasi_up_dari_kosong(db_bersih):
    r = subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True,
                       env={"DATABASE_URL": db_bersih})
    assert r.returncode == 0, r.stderr


def test_migrasi_idempoten(db_bersih):
    for _ in range(2):
        r = subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True,
                           env={"DATABASE_URL": db_bersih})
        assert r.returncode == 0, r.stderr
""",
    "tests/test_integritas.py": """import pytest


def test_unique_menolak_duplikat(db):
    db.execute("insert into items(nama) values ('a')")
    with pytest.raises(Exception):
        db.execute("insert into items(nama) values ('a')")


def test_transaksi_tidak_menyisakan_data_separuh(db):
    with pytest.raises(Exception):
        with db.transaction():
            db.execute("insert into items(nama) values ('ok')")
            raise RuntimeError("gagal di tengah")
    assert db.scalar("select count(*) from items where nama='ok'") == 0
""",
}

T_ML = {
    "eval/hasil_holdout.json": """{
  "model": { "akurasi": 0.88 },
  "baseline_naif": { "akurasi": 0.71 },
  "per_segmen": { "umum": 0.87, "baru": 0.84, "lama": 0.89 }
}
""",
    "eval/uji_pii.py": """\"\"\"Stub: periksa output model tidak memuat PII (email/NIK/telepon).\"\"\"
import re
import sys

CONTOH_OUTPUT = "Ringkasan: pesanan dikirim besok."

POLA = [r"[\\w.+-]+@[\\w-]+\\.[\\w.]{2,}", r"\\b\\d{16}\\b", r"\\b08\\d{8,11}\\b"]

if any(re.search(p, CONTOH_OUTPUT) for p in POLA):
    print("BOCOR PII", file=sys.stderr)
    sys.exit(1)
print("bersih")
""",
    "tests/test_model.py": """import json

import pytest


@pytest.fixture(scope="module")
def metrik():
    with open("eval/hasil_holdout.json") as f:
        return json.load(f)


def test_holdout_mengalahkan_baseline(metrik):
    assert metrik["model"]["akurasi"] > metrik["baseline_naif"]["akurasi"]


def test_per_segmen_tidak_jauh_berbeda(metrik):
    nilai = list(metrik["per_segmen"].values())
    assert max(nilai) - min(nilai) < 0.15, metrik["per_segmen"]


def test_tidak_ada_kebocoran_pii_di_output():
    import subprocess
    r = subprocess.run(["python3", "eval/uji_pii.py"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
""",
}

GEN = {
    "web": (T_WEB, "tests-web"),
    "api": (T_API, "tests-api"),
    "cli": (T_CLI, "tests-cli"),
    "lib": (T_LIB, "tests-lib"),
    "infra": (T_INFRA, "tests-infra"),
    "data": (T_DATA, "tests-data"),
    "ml": (T_ML, "tests-ml"),
}


def cmd_generate(nama, dest, force=False):
    kunci = nama.replace("tests-", "")
    if kunci not in GEN:
        print(f"template tidak ada: {nama}. Pilihan: {', '.join('tests-' + k for k in GEN)}")
        return 1
    files, _ = GEN[kunci]
    if os.path.exists(dest) and not force and os.listdir(dest):
        print(f"folder sudah ada dan tidak kosong: {dest} (pakai --force untuk menimpa)")
        return 1
    dibuat = 0
    for rel, isi in files.items():
        path = os.path.join(dest, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(isi)
        dibuat += 1
    print(f"dibuat {dibuat} file di {dest}")
    if kunci == "web":
        print("lanjut: npm install && npx playwright install --with-deps && npm test")
    elif kunci == "api":
        print("lanjut: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/pytest -q")
    elif kunci == "infra":
        print("lanjut: chmod +x smoke.sh && BASE_URL=https://staging ./smoke.sh")
    return 0


POLA_AUDIT = [
    ("unit", [r"def test_|it\(|test\(", r"\.test\.[jt]s$"]),
    ("integrasi", [r"conftest", r"testcontainers|postgres|docker compose", r"transaction|rollback"]),
    ("kontrak", [r"\bopenapi\b|swagger", r"schemathesis|\bspectral\b|\bpact\b", r"\bproto\b|graphql"]),
    ("e2e", [r"playwright|cypress|selenium", r"\.spec\.[jt]s$", r"storageState|page\.goto"]),
    ("visual", [r"snapshot|toMatchSnapshot|dvisual"]),
    ("a11y", [r"axe|pa11y|WCAG"]),
    ("i18n", [r"Intl\.(NumberFormat|DateTimeFormat)|\bi18n\b|\bl10n\b|localeCompare"]),
    ("performa", [r"k6|locust|artillery|wrk", r"thresholds?|p\(95\)"]),
    ("security", [r"semgrep|bandit|gitleaks|trivy|security-forge"]),
    ("data", [r"alembic|migrate|migration|pg_dump"]),
    ("ml", [r"holdout|eval|baseline|drift"]),
    ("infra", [r"hadolint|kubeconform|helm lint|terraform validate|ansible-lint"]),
    ("manual", [r"CHARTER|SFDPOT|\bUAT\b|exploratory"]),
    ("ci", [r"\.github/workflows|\.gitlab-ci|pre-commit"]),
]


def cmd_audit(target):
    if not os.path.isdir(target):
        print(f"bukan direktori: {target}")
        return 1
    teks = []
    for akar, dirs, files in os.walk(target):
        dirs[:] = [d for d in dirs if d not in {
            ".git", "node_modules", ".venv", "venv", "dist", "build",
            "__pycache__", ".next", "target", "vendor",
            "skills-expanded", "skills-store", "agent-assets", "refs",
            ".cache", "site-packages", ".bun", ".npm", "playwright"}]
        for f in files:
            if len(teks) >= 4000:
                break
            if f.endswith((".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".rb",
                           ".php", ".cs", ".java", ".kt", ".swift", ".yml", ".yaml",
                           ".sh", ".sql", ".toml", ".json", ".md")):
                try:
                    with open(os.path.join(akar, f), encoding="utf-8", errors="ignore") as fh:
                        isi = fh.read(200_000)
                except OSError:
                    continue
                teks.append((os.path.relpath(os.path.join(akar, f), target), isi))
    ada, kurang = [], []
    for lapisan, polas in POLA_AUDIT:
        ketemu = []
        for rel, isi in teks:
            for p in polas:
                if re.search(p, isi, re.I) or re.search(p, rel, re.I):
                    ketemu.append(rel)
                    break
        if ketemu:
            ada.append((lapisan, sorted(set(ketemu))[:3]))
        else:
            kurang.append(lapisan)
    print(f"# Audit jenis test: {os.path.abspath(target)}")
    print(f"file diperiksa: {len(teks)}\n")
    print("ADA:")
    for lapisan, contoh in ada:
        print(f"  + {lapisan:<12} {', '.join(contoh)}")
    print("\nBELUM ADA:")
    for lapisan in kurang:
        print(f"  - {lapisan:<12} baca TESTING/{LAYERS[lapisan]['doc']}")
    print(f"\nRingkas: ada={len(ada)} belum={len(kurang)} dari {len(POLA_AUDIT)} lapisan")
    print("Catatan: ini mendeteksi JEJAK lapisan, bukan mutu test. Baca dokumen sebelum menyimpulkan.")
    return 0


def cmd_selftest():
    gagal = 0
    for s, lap in STACKS.items():
        tak = [x for x in lap if x not in LAYERS]
        if tak:
            print(f"GAGAL: stack {s} -> lapisan tak dikenal {tak}")
            gagal += 1
    for k, v in LAYERS.items():
        if not os.path.exists(os.path.join(TDIR, v["doc"])):
            print(f"GAGAL: dokumen hilang untuk {k}: {v['doc']}")
            gagal += 1
        if not v["checklist"] or not v["gate"]:
            print(f"GAGAL: lapisan {k} tanpa checklist/gate")
            gagal += 1
    if not os.path.exists(os.path.join(AG, "TESTING.md")):
        print("GAGAL: TESTING.md tidak ada")
        gagal += 1
    for k, (files, _) in GEN.items():
        if not files:
            print(f"GAGAL: template {k} kosong")
            gagal += 1
    print(f"selftest: lapisan={len(LAYERS)} jenis={len(KINDS)} teknik={len(TECHNIQUES)} "
          f"kombinasi={jml_kombinasi()} template={len(GEN)}")
    print("HASIL: " + ("LULUS" if gagal == 0 else f"GAGAL ({gagal})"))
    return 0 if gagal == 0 else 1


def main(argv):
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(__doc__.strip())
        return 0
    cmd, rest = argv[0], argv[1:]
    if cmd == "matrix":
        cmd_matrix()
        return 0
    if cmd == "layers":
        cmd_layers()
        return 0
    if cmd == "show":
        if not rest:
            print("pakai: testing-forge show <lapisan>")
            return 1
        return cmd_show(rest[0])
    if cmd == "plan":
        stack, risk = "web", "medium"
        i = 0
        while i < len(rest):
            if rest[i] in ("--stack", "-s") and i + 1 < len(rest):
                stack = rest[i + 1]; i += 2
            elif rest[i] in ("--risk", "-r") and i + 1 < len(rest):
                risk = rest[i + 1]; i += 2
            else:
                i += 1
        return cmd_plan(stack, risk)
    if cmd == "generate":
        if not rest:
            print("pakai: testing-forge generate tests-web|tests-api|tests-cli|tests-lib|tests-infra|tests-data|tests-ml [dest] [--force]")
            return 1
        nama = rest[0]
        force = "--force" in rest
        sisa = [x for x in rest[1:] if not x.startswith("--")]
        dest = sisa[0] if sisa else nama
        return cmd_generate(nama, dest, force)
    if cmd == "audit":
        return cmd_audit(rest[0] if rest else ".")
    if cmd == "selftest":
        return cmd_selftest()
    print(f"perintah tidak dikenal: {cmd}")
    print(__doc__.strip())
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
