#!/usr/bin/env python3
"""fix-15-descriptions.py — perbaiki 8 deskripsi SKILL.md yang placeholder/thin.

Alasan: `skill-curate.py --report` menandai 15 skill; triase manual menunjukkan
7 sudah baik (desc + "Use when"), 8 placeholder/tidak informatif sehingga
routing skill_for_task/skill-rank tidak bisa memilihnya dengan tepat.

Idempotent: hanya menulis kalau deskripsi lama masih bernilai placeholder.
Backup: satu file .bak-YYYYMMDD per skill.
"""
import os
import re
import shutil
import sys
from datetime import datetime, timezone

STORE = os.path.expanduser("~/.agents/skills-store")
STAMP = datetime.now(timezone.utc).strftime("%Y%m%d")

# skill -> (deskripsi_lama_pendek, deskripsi_baru)
FIX = {
    "gws-gmail-send": (
        "Gmail: Send an email.",
        "Kirim email lewat Gmail via CLI gws. Use when the user wants to send, "
        "compose, reply, or forward an email. Butuh binary gws + auth (gws-shared).",
    ),
    "mcp-create-adaptive-cards": (
        "Skill converted from mcp-create-adaptive-cards.prompt.md",
        "Buat Adaptive Card response templates untuk MCP API plugin agar data "
        "tampil visual di Microsoft 365 Copilot. Use when an MCP server response "
        "should render as rich cards, not plain text.",
    ),
    "mcp-create-declarative-agent": (
        "Skill converted from mcp-create-declarative-agent.prompt.md",
        "Buat declarative agent Microsoft 365 Copilot yang mengintegrasikan MCP "
        "server (auth, tool selection, config). Use when building a Copilot agent "
        "that must call an external MCP API.",
    ),
    "mcp-deploy-manage-agents": (
        "Skill converted from mcp-deploy-manage-agents.prompt.md",
        "Deploy & kelola MCP declarative agent di Microsoft 365 admin center "
        "(assignment, distribusi, governance). Use setelah agent jadi dan perlu "
        "dipublikasikan ke organisasi.",
    ),
    "rivet-workflows": (
        "Workflows: Durable, replayable multi-step operations.",
        "Rivet Workflows: operasi multi-step yang durable & replayable (queue, "
        "timer, concurrency, failure recovery, versioning). Use when building "
        "long-running jobs yang harus selamat dari restart.",
    ),
    "structured-autonomy-plan": (
        "Structured Autonomy Planning Prompt",
        "Riset & susun development plan (plans/<feature>/plan.md) tanpa menulis "
        "kode. Use when user minta rencana implementasi fitur/PR.",
    ),
    "structured-autonomy-generate": (
        "Structured Autonomy Implementation Generator Prompt",
        "Hasilkan implementation.md berisi langkah + kode lengkap dari plan.md "
        "yang sudah ada. Use when plan selesai dan butuh dokumentasi implementasi "
        "siap copy-paste.",
    ),
    "structured-autonomy-implement": (
        "Structured Autonomy Implementation Prompt",
        "Implementasi plan secaraStrict tanpa deviasi (hanya perubahan yang ada "
        "di plan). Use when sudah ada implementation plan dan eksekusi diminta.",
    ),
}


def replace_desc(path, new_desc):
    with open(path, encoding="utf-8", errors="ignore") as f:
        txt = f.read()
    # ganti description: ... (sampai baris key berikutnya atau penutup ---)
    pat = re.compile(r"^description:\s*(.*?)(?=\n[a-zA-Z_-]+:\s|\n---\s*$)", re.S | re.M)
    if not pat.search(txt):
        return False, "pola description tidak ketemu"
    new = pat.sub("description: " + new_desc.replace("\\", "\\\\") + "\n", txt, count=1)
    if new == txt:
        return False, "tidak berubah"
    shutil.copy2(path, f"{path}.bak-{STAMP}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(new)
    return True, "ok"


def main():
    changed = skipped = 0
    for skill, (old, new) in sorted(FIX.items()):
        p = os.path.join(STORE, skill, "SKILL.md")
        if not os.path.isfile(p):
            print(f"  (skip) {skill}: SKILL.md tidak ada")
            continue
        with open(p, encoding="utf-8", errors="ignore") as f:
            head = f.read(1500)
        if new.split(".")[0][:20] in head:
            print(f"  (sudah) {skill}")
            skipped += 1
            continue
        if old.lower() not in head.lower():
            # mungkin sudah diubah manual — jangan ditimpa
            print(f"  (wajar) {skill}: deskripsi sudah berbeda, tidak ditimpa")
            skipped += 1
            continue
        ok, why = replace_desc(p, new)
        print(f"  {'OK   ' if ok else 'GAGAL'} {skill}: {why}")
        if ok:
            changed += 1
    print(f"\n{changed} diperbaiki, {skipped} dilewati (idempotent).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())