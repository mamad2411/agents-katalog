#!/usr/bin/env python3
"""mamat-auto — aktifkan/matikan default model "auto" (routing otomatis).

pakai:
  mamat auto            aktifkan auto (default: smart/auto/best)
  mamat auto coding     auto untuk coding (smart/auto/coding)
  mamat auto status     lihat status + model sebelumnya
  mamat auto off        kembalikan model sebelumnya

Mengubah `model` + `small_model` di ~/.config/opencode/opencode.json (backup .bak-YYYYMMDD-HHMM).
"""
import json
import os
import shutil
import sys
import time

HOME = os.path.expanduser("~")
CFG = f"{HOME}/.config/opencode/opencode.json"
STATE = f"{HOME}/.local/state/mamat/auto.json"
PROVIDER = "smart"
VARIANTS = ("best", "coding", "cheap", "quick", "reasoning")

# nama tugas sehari-hari -> varian auto
ALIAS = {
    "ui": "coding", "frontend": "coding", "backend": "coding", "kode": "coding",
    "refactor": "coding", "fix": "coding", "bug": "coding", "test": "coding",
    "debug": "reasoning", "arsitektur": "reasoning", "architecture": "reasoning",
    "review": "reasoning", "audit": "reasoning", "riset": "reasoning",
    "research": "reasoning", "desain": "reasoning", "design": "reasoning",
    "docs": "quick", "dokumentasi": "quick", "rename": "quick", "format": "quick",
    "chat": "quick", "tanya": "quick",
    "bulk": "cheap", "massal": "cheap", "sed": "cheap", "cari": "cheap",
    "grep": "cheap", "scan": "cheap",
    "kualitas": "best", "penting": "best", "produksi": "best",
}


def load():
    with open(CFG) as f:
        return json.load(f)


def models_in(cfg):
    out = {}
    for pid, p in (cfg.get("provider") or {}).items():
        for mid in (p.get("models") or {}):
            out[f"{pid}/{mid}"] = mid
    return out


def status() -> int:
    cfg = load()
    cur = cfg.get("model", "-")
    small = cfg.get("small_model", "-")
    prev = "-"
    if os.path.exists(STATE):
        try:
            prev = json.load(open(STATE)).get("previous", {}).get("model", "-")
        except Exception:
            pass
    on = "/auto/" in cur
    print(f"auto      : {'ON' if on else 'OFF'}")
    print(f"model     : {cur}")
    print(f"small     : {small}")
    print(f"sebelumnya: {prev}")
    avail = [k for k in models_in(cfg) if "/auto/" in k]
    print(f"pilihan   : {', '.join(avail) or '(tidak ada provider auto)'}")
    return 0


def set_auto(variant: str) -> int:
    cfg = load()
    target = f"{PROVIDER}/auto/{variant}"
    if target not in models_in(cfg):
        print(f"GAGAL: model {target} tidak terdaftar di config. "
              f"Ada: {[k for k in models_in(cfg) if '/auto/' in k]}", file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    prev = {"model": cfg.get("model"), "small_model": cfg.get("small_model")}
    if "/auto/" not in (cfg.get("model") or ""):
        with open(STATE, "w") as f:
            json.dump({"previous": prev, "at": time.strftime("%FT%T")}, f, indent=1)
    bak = f"{CFG}.bak-{time.strftime('%Y%m%d-%H%M')}"
    if not os.path.exists(bak):
        shutil.copy2(CFG, bak)
    cfg["model"] = target
    cfg["small_model"] = target
    with open(CFG, "w") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
    print(f"auto ON  -> {target}")
    print(f"backup   -> {bak}")
    print("buka ulang `mamat` (atau /models) supaya berlaku.")
    return 0


def unset_auto() -> int:
    if not os.path.exists(STATE):
        print("tidak ada state auto sebelumnya — tidak ada yang dikembalikan", file=sys.stderr)
        return 1
    prev = json.load(open(STATE)).get("previous", {})
    cfg = load()
    bak = f"{CFG}.bak-{time.strftime('%Y%m%d-%H%M')}"
    if not os.path.exists(bak):
        shutil.copy2(CFG, bak)
    cfg["model"] = prev.get("model") or cfg.get("model")
    cfg["small_model"] = prev.get("small_model") or cfg.get("small_model")
    with open(CFG, "w") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
    os.remove(STATE)
    print(f"auto OFF -> {cfg['model']} (small: {cfg['small_model']})")
    print("buka ulang `mamat` supaya berlaku.")
    return 0


def main() -> int:
    a = sys.argv[1:]
    if not a:
        return set_auto("best")
    cmd = a[0]
    if cmd == "status":
        return status()
    if cmd in ("off", "disable"):
        return unset_auto()
    if cmd in ("on", "enable"):
        return set_auto("best")
    if cmd in VARIANTS:
        return set_auto(cmd)
    if cmd in ALIAS:
        print(f"tugas '{cmd}' -> auto/{ALIAS[cmd]}")
        return set_auto(ALIAS[cmd])
    if cmd in ("help", "-h", "--help"):
        print(__doc__)
        print("alias tugas: " + ", ".join(sorted(ALIAS)))
        return 0
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
