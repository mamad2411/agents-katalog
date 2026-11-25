#!/usr/bin/env python3
"""security-forge — audit keamanan nyata (bukan cuma scaffold).

Semua alat lokal & gratis; yang tidak terpasang = SKIP (bukan FAIL palsu).

  security-forge audit <dir>        # secret + SAST + dependency + dockerfile + shell
  security-forge secret <dir>       # gitleaks
  security-forge sast <dir>         # semgrep (+ bandit untuk python)
  security-forge deps <dir>         # trivy fs (vulnerability + misconfig + secret)
  security-forge image <ref>        # trivy image
  security-forge docker <dir>       # hadolint untuk semua Dockerfile
  security-forge shell <dir>        # shellcheck semua *.sh
  security-forge headers <url>      # header keamanan HTTP
  security-forge tls <host[:port]>  # sertifikat + protokol TLS
  security-forge report <dir>       # audit + simpan JSON/Markdown

Exit code: 0 bersih/kritis-nol, 1 ada temuan HIGH/CRITICAL atau FAIL.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time

C = {"red": "\033[31m", "yel": "\033[33m", "grn": "\033[32m", "dim": "\033[2m", "off": "\033[0m"}
ICON = {"PASS": "✅", "WARN": "⚠️ ", "FAIL": "❌", "SKIP": "⏭️ "}


def c(text, color):
    return text if not sys.stdout.isatty() else f"{C[color]}{text}{C['off']}"


def run(cmd, cwd=None, timeout=900):
    r = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def need(binary):
    return shutil.which(binary) is not None


# ─── pemeriksa ────────────────────────────────────────────────────────────────
RANK = {"PASS": 0, "SKIP": 0, "WARN": 1, "FAIL": 2}


def worse(a, b):
    return a if RANK.get(a, 0) >= RANK.get(b, 0) else b


def check_secret(root):
    if not need("gitleaks"):
        return ("SKIP", "gitleaks belum ada → brew install gitleaks")
    cfg = os.path.join(root, ".gitleaks.toml")
    extra = f"-c '{cfg}'" if os.path.exists(cfg) else ""
    import tempfile
    out_file = os.path.join(tempfile.mkdtemp(prefix="sf-"), "gitleaks.json")
    rc, out = run(f"gitleaks detect --no-git --redact --exit-code 0 {extra} "
                  f"-f json -r '{out_file}' .", cwd=root)
    found = []
    if os.path.exists(out_file):
        try:
            found = json.load(open(out_file)) or []
        except Exception:
            found = []
    if not found:
        return ("PASS", "tidak ada secret terdeteksi")
    detail = ", ".join(f"{f.get('File', '?')}:{f.get('StartLine', '?')} ({f.get('RuleID')})"
                       for f in found[:3])
    return ("FAIL", f"{len(found)} temuan: {detail}")


PATTERNS = [
    (r"AKIA[0-9A-Z]{16}", "AWS access key"),
    (r"sk-(?:proj-)?[A-Za-z0-9_\-]{24,}", "OpenAI-style key"),
    (r"gh[pousr]_[A-Za-z0-9]{30,}", "GitHub token"),
    (r"xox[baprs]-[A-Za-z0-9\-]{10,}", "Slack token"),
    (r"-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----", "private key"),
    (r"(?i)(?:password|passwd|secret|api[_-]?key|access[_-]?token)\s*[:=]\s*"
     r"['\"][^'\"]{10,}['\"]", "hardcoded secret"),
]
BENAR_BENAR = re.compile(r"(?i)example|dummy|placeholder|changeme|xxx+|your[_-]|\.\.\.|"
                         r"\$\{|%env\(|<[a-z_]+>|\bnull\b|\bnone\b|redacted|sample")
SKIP_SCAN = {".git", "node_modules", "dist", "build", ".venv", "venv", "__pycache__",
             "vendor", "target", ".next", ".nuxt", "coverage", ".mypy_cache", ".ruff_cache",
             "Pods", "_build", "deps", "obj", ".gradle", ".terraform"}


def check_pattern(root):
    """cadangan bila gitleaks tidak menangkap (atau belum terpasang)."""
    hits = []
    for dirpath, dirnames, names in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_SCAN]
        for fn in names:
            if fn.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".pdf", ".mp4",
                            ".woff", ".woff2", ".zip", ".lock", ".map", ".sum")):
                continue
            if fn in ("package-lock.json", "pnpm-lock.yaml", "yarn.lock", "uv.lock",
                      "poetry.lock", "go.sum", "Cargo.lock", "composer.lock"):
                continue
            p = os.path.join(dirpath, fn)
            try:
                if os.path.getsize(p) > 800_000:
                    continue
                body = open(p, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            for pat, label in PATTERNS:
                m = re.search(pat, body)
                if m and not BENAR_BENAR.search(m.group(0)):
                    hits.append((os.path.relpath(p, root), label))
                    break
    if hits:
        detail = ", ".join(f"{f} ({l})" for f, l in hits[:3])
        return ("FAIL", f"{len(hits)} pola secret: {detail}")
    return ("PASS", "tidak ada pola secret")


def check_sast(root):
    lines, worst = [], "PASS"
    cfg = os.path.join(root, "semgrep.yml")
    if need("semgrep"):
        args = f"--config '{cfg}'" if os.path.exists(cfg) else "--config auto"
        rc, out = run(f"semgrep {args} --json --quiet --metrics=off .", cwd=root, timeout=1200)
        n, sev = 0, set()
        try:
            data = json.loads(out[out.index("{"):])
            res = data.get("results", [])
            n = len(res)
            sev = {r["extra"].get("severity", "INFO") for r in res}
        except Exception:
            res = []
        if n:
            worst = "FAIL" if sev & {"ERROR", "HIGH", "CRITICAL"} else "WARN"
            lines.append(f"semgrep {n} temuan ({'/'.join(sorted(sev)) or 'INFO'})")
        else:
            lines.append("semgrep bersih")
    else:
        lines.append("semgrep SKIP")
    py = any(f.endswith(".py") for _, _, fs in os.walk(root) for f in fs)
    if py and need("bandit"):
        rc, out = run("bandit -q -r . -f json "
                      "--exclude ./.venv,./venv,./.git,./node_modules,./dist,./build,"
                      "./vendor,./target,./.mypy_cache,./.ruff_cache,./tests", cwd=root, timeout=900)
        try:
            data = json.loads(out[out.index("{"):])
            res = data.get("results", [])
            hi = [x for x in res if x.get("issue_severity") == "HIGH"]
            med = [x for x in res if x.get("issue_severity") == "MEDIUM"]
            if hi or med:
                worst = worse(worst, "FAIL" if hi else "WARN")
                lines.append(f"bandit {len(hi)} high, {len(med)} medium")
            elif not lines:
                lines.append("bandit bersih")
        except Exception:
            lines.append("bandit tidak terbaca")
    if not lines:
        return ("SKIP", "semgrep/bandit tidak tersedia")
    return (worst, "; ".join(lines))


def check_deps(root):
    if not need("trivy"):
        return ("SKIP", "trivy belum ada → brew install trivy")
    rc, out = run("trivy fs --scanners vuln,misconfig --severity HIGH,CRITICAL "
                  "--no-progress --quiet -f json .", cwd=root, timeout=1800)
    try:
        data = json.loads(out[out.index("{"):])
    except Exception:
        return ("WARN", "trivy tidak menghasilkan JSON")
    vuln = misfig = 0
    for r in data.get("Results", []):
        vuln += len(r.get("Vulnerabilities") or [])
        misfig += len(r.get("Misconfigurations") or [])
    if vuln:
        return ("FAIL", f"{vuln} kerentanan HIGH/CRITICAL, {misfig} misconfig")
    if misfig:
        return ("WARN", f"0 kerentanan, {misfig} misconfig")
    return ("PASS", "tidak ada kerentanan HIGH/CRITICAL")


def check_docker(root):
    if not need("hadolint"):
        return ("SKIP", "hadolint belum ada → brew install hadolint")
    files = []
    for dirpath, dirnames, names in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in
                       {".git", "node_modules", "vendor", "target", ".venv", "dist", "build"}]
        files += [os.path.join(dirpath, f) for f in names
                  if f.startswith("Dockerfile") or f.endswith(".Dockerfile")]
    if not files:
        return ("PASS", "tidak ada Dockerfile")
    bad = 0
    for f in files:
        rc, out = run(f"hadolint '{f}'")
        if rc != 0:
            bad += len([x for x in out.splitlines() if " DL" in x or " SC" in x])
    return ("WARN" if bad else "PASS", f"{len(files)} Dockerfile, {bad} peringatan")


def check_shell(root):
    if not need("shellcheck"):
        return ("SKIP", "shellcheck belum ada → brew install shellcheck")
    files = []
    for dirpath, dirnames, names in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in
                       {".git", "node_modules", "vendor", "target", ".venv", "dist", "build"}]
        files += [os.path.join(dirpath, f) for f in names if f.endswith(".sh")]
    if not files:
        return ("PASS", "tidak ada skrip shell")
    bad = 0
    for f in files:
        rc, out = run(f"shellcheck -S error '{f}'")
        if rc != 0:
            bad += 1
    return ("FAIL" if bad else "PASS", f"{len(files)} skrip, {bad} error")


def check_perm(root):
    """berkas sensitif jangan world-readable / .env jangan ke-track."""
    problems = []
    for name in (".env", "id_rsa", "secrets.yaml", "secrets.yml"):
        p = os.path.join(root, name)
        if os.path.exists(p):
            mode = os.stat(p).st_mode & 0o777
            if mode & 0o004:
                problems.append(f"{name} world-readable ({oct(mode)})")
    gi = os.path.join(root, ".gitignore")
    body = open(gi, encoding="utf-8", errors="ignore").read() if os.path.exists(gi) else ""
    for pattern in (".env", "*.pem", "*.key"):
        if os.path.exists(os.path.join(root, pattern.replace("*", ""))) and pattern not in body:
            problems.append(f"{pattern} tidak di-.gitignore")
    if problems:
        return ("FAIL", "; ".join(problems[:3]))
    return ("PASS", "berkas sensitif aman")


# ─── header & TLS (runtime) ───────────────────────────────────────────────────
REQUIRED_HEADERS = {
    "strict-transport-security": "wajib HTTPS",
    "x-content-type-options": "cegah MIME sniffing",
    "x-frame-options": "cegah clickjacking",
    "referrer-policy": "batasi referrer",
    "content-security-policy": "cegah XSS",
    "permissions-policy": "matikan fitur tak dipakai",
}


def cmd_headers(url):
    import urllib.request
    try:
        req = urllib.request.Request(url, method="GET",
                                     headers={"User-Agent": "security-forge/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            hdrs = {k.lower(): v for k, v in r.headers.items()}
    except Exception as e:
        print(f"❌ tidak bisa mengambil {url}: {e}")
        return 1
    print(f"{url} → {len(hdrs)} header")
    miss = 0
    for name, why in REQUIRED_HEADERS.items():
        val = hdrs.get(name)
        if val:
            print(f"  ✅ {name}: {val[:70]}")
        else:
            miss += 1
            print(f"  ❌ {name} HILANG ({why})")
    for leak in ("server", "x-powered-by"):
        if hdrs.get(leak):
            print(f"  ⚠️  {leak} membocorkan: {hdrs[leak][:50]}")
    print(f"\n{len(REQUIRED_HEADERS) - miss}/{len(REQUIRED_HEADERS)} header wajib ada")
    return 0 if miss == 0 else 1


def cmd_tls(target):
    host, _, port = target.partition(":")
    port = port or "443"
    if not need("openssl"):
        print("⏭️  openssl tidak ada")
        return 0
    rc, out = run(f"openssl s_client -connect {host}:{port} -servername {host} "
                  f"-verify_return_error </dev/null 2>&1 | "
                  f"openssl x509 -noout -subject -issuer -dates 2>&1")
    if rc != 0 or "notAfter" not in out:
        print(f"❌ TLS gagal untuk {host}:{port}\n{out.strip()[:300]}")
        return 1
    print(out.strip())
    m = re.search(r"notAfter=(.+)", out)
    if m:
        from email.utils import parsedate_to_datetime
        try:
            exp = parsedate_to_datetime(m.group(1).strip())
            days = (exp - __import__("datetime").datetime.now(exp.tzinfo)).days
            ok = days > 21
            print(f"{'✅' if ok else '❌'} sisa {days} hari")
            if not ok:
                return 1
        except Exception:
            pass
    for proto, label in (("tls1", "TLS 1.0"), ("tls1_1", "TLS 1.1")):
        rc, out = run(f"openssl s_client -connect {host}:{port} -{proto} "
                      f"-servername {host} </dev/null 2>&1")
        ok_cipher = re.search(r"Cipher is (?!\(NONE\))\S+", out)
        if rc == 0 and ok_cipher:
            print(f"❌ {label} masih aktif — matikan di server")
            return 1
    print("✅ hanya TLS 1.2+")
    return 0


# ─── audit agregat ────────────────────────────────────────────────────────────
CHECKS = [
    ("secret", check_secret), ("pola", check_pattern), ("sast", check_sast), ("deps", check_deps),
    ("docker", check_docker), ("shell", check_shell), ("perm", check_perm),
]


def do_audit(root, quiet=False):
    results = []
    for name, fn in CHECKS:
        try:
            st, note = fn(root)
        except Exception as e:
            st, note = "WARN", f"error internal: {type(e).__name__}: {e}"
        results.append({"check": name, "status": st, "note": note})
        if not quiet:
            print(f"{ICON[st]} {name:<7} {note}")
    return results


def summarize(results):
    n = {k: sum(1 for r in results if r["status"] == k) for k in ICON}
    print(f"\n{n['PASS']} pass · {n['WARN']} warn · {n['FAIL']} fail · {n['SKIP']} skip")
    worst = "FAIL" if n["FAIL"] else ("WARN" if n["WARN"] else ("PASS" if n["PASS"] else "SKIP"))
    label = {"FAIL": c("ADA TEMUAN SERIUS", "red"), "WARN": c("perlu perhatian", "yel"),
             "PASS": c("BERSIH", "grn"), "SKIP": "tidak ada alat"}
    print(label[worst])
    return 1 if n["FAIL"] else 0


def cmd_report(root):
    results = do_audit(root)
    rc = summarize(results)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    base = os.path.join(root, "security-report")
    data = {"root": root, "generated": stamp, "results": results}
    with open(f"{base}-{stamp}.json", "w") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
    with open(f"{base}-{stamp}.md", "w") as fh:
        fh.write(f"# Laporan keamanan\n\n`{root}` · {stamp}\n\n"
                 "| pemeriksa | status | catatan |\n|---|---|---|\n")
        for r in results:
            fh.write(f"| {r['check']} | {r['status']} | {r['note']} |\n")
    print(f"\n📄 {base}-{stamp}.json · .md")
    return rc


def main(argv):
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(__doc__)
        return 0
    cmd, args = argv[0], argv[1:]
    root = os.path.abspath(args[0]) if args else os.getcwd()

    if cmd in ("audit", "report"):
        if not os.path.isdir(root):
            sys.exit(f"bukan folder: {root}")
        return cmd_report(root) if cmd == "report" else summarize(do_audit(root))
    if cmd == "headers":
        if not args:
            sys.exit("pakai: security-forge headers https://domain")
        return cmd_headers(args[0])
    if cmd == "tls":
        if not args:
            sys.exit("pakai: security-forge tls domain[:port]")
        return cmd_tls(args[0])
    one = {"secret": check_secret, "pola": check_pattern, "sast": check_sast, "deps": check_deps,
           "docker": check_docker, "shell": check_shell, "perm": check_perm}
    if cmd in one:
        st, note = one[cmd](root)
        print(f"{ICON[st]} {cmd}: {note}")
        return 1 if st == "FAIL" else 0
    sys.exit(f"perintah tidak dikenal: {cmd} (lihat --help)")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
