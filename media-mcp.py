#!/usr/bin/env python3
"""media-mcp — 1 tool MCP untuk media-forge (video, audio, gambar, vektor, animasi).

Kenapa 1 tool: setiap tool MCP menambah schema ke SETIAP request. Satu tool = biaya
tetap paling kecil (~250 token) dan tetap membuka 20 aksi.

Jalankan: python3 ~/.agents/media-mcp.py   (stdio JSON-RPC, tanpa dependency)
Nyalakan : pow mcp on media   → lalu restart opencode
"""
import json
import os
import subprocess
import sys
import tempfile

HOME = os.path.expanduser("~")
AG = os.path.join(HOME, ".agents")
FORGE = os.path.join(AG, "media-forge.py")
PY = sys.executable

ACTIONS = ["scan", "probe", "video", "gif", "thumb", "concat", "enhance", "upscale",
           "bgremove", "vectorize", "svg2png", "anim", "lottie", "manim", "audio",
           "tts", "music", "waveform", "3d"]

TOOL = {
    "name": "media",
    "description": (
        "Editing media lokal kelas profesional (ffmpeg/ImageMagick/Potrace/Manim/Lottie). "
        "action: " + ", ".join(ACTIONS) + ". "
        "input/output = path file. options = objek opsi, contoh "
        '{"w":1920,"fps":30,"crf":18} atau {"style":"cinematic","sec":30} '
        "atau untuk anim: {\"spec\":{...}} (inline) / {\"spec\":\"spec.json\"}."),
    "inputSchema": {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ACTIONS},
            "input": {"type": "string", "description": "file/teks/spec sumber"},
            "output": {"type": "string", "description": "file hasil"},
            "options": {"type": "object", "description": "opsi tambahan (--key value)"},
        },
        "required": ["action"],
    },
}

MAX_CHARS = 6000


def _argv(action, inp, out, opts):
    cmd = [PY, FORGE, action]
    if action == "tts":
        cmd += [inp or "", out or "out.wav"]
    elif action == "music":
        cmd += [out or "music.wav"]
    elif action in ("scan",):
        pass
    elif action == "concat":
        cmd += [out or "out.mp4"] + list(opts.pop("files", []) or [])
        if inp:
            cmd.insert(3, inp)
    elif action == "manim":
        cmd += [inp or "", opts.pop("scene", "Scene"), opts.pop("quality", "m"),
                out or ""]
    else:
        cmd += [inp or "", out or "out"]
    for k, v in (opts or {}).items():
        key = "--" + k.replace("_", "-")
        if isinstance(v, bool):
            if v:
                cmd.append(key)
        elif isinstance(v, (list, tuple)):
            cmd += [key, ",".join(str(x) for x in v)]
        elif isinstance(v, str) and v.startswith("{"):
            cmd += [key, v]
        else:
            cmd += [key, str(v)]
    return [c for c in cmd if c is not None]


def handle_call(args):
    action = args.get("action")
    if action not in ACTIONS:
        return f"action tidak dikenal: {action}"
    opts = dict(args.get("options") or {})
    inp = args.get("input") or ""
    out = args.get("output") or ""
    # spec animasi inline
    if action == "anim" and isinstance(opts.get("spec"), dict):
        tmp = tempfile.mkdtemp(prefix="spec-")
        sp = os.path.join(tmp, "spec.json")
        json.dump(opts["spec"], open(sp, "w"))
        inp, opts["spec"] = sp, None
        opts = {k: v for k, v in opts.items() if v is not None}
    cmd = _argv(action, inp, out, opts)
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=5400)
    except subprocess.TimeoutExpired:
        return "timeout: proses > 90 menit"
    log = ((p.stdout or "") + "\n" + (p.stderr or "")).strip()
    lines = log.splitlines()
    if len(log) > MAX_CHARS:
        log = "\n".join(lines[:20] + ["…"] + lines[-60:])
    outfile = out or None
    extra = ""
    if outfile and os.path.exists(outfile):
        extra = f"\nOK file={outfile} size={os.path.getsize(outfile)}B"
    elif action not in ("scan", "probe"):
        extra = "\n(tidak ada file hasil — cek log)"
    return f"$ {' '.join(cmd[2:])}\n{log[-MAX_CHARS:]}{extra}"


def reply(obj):
    sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()


def handle(msg):
    mid = msg.get("id")
    m = msg.get("method", "")
    if m == "initialize":
        want = (msg.get("params") or {}).get("protocolVersion") or ""
        reply({"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": want if isinstance(want, str) and want else "2024-11-05",
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "media-forge", "version": "1.0.0"}}})
    elif m.startswith("notifications/"):
        return
    elif m == "ping":
        reply({"jsonrpc": "2.0", "id": mid, "result": {}})
    elif m == "tools/list":
        reply({"jsonrpc": "2.0", "id": mid, "result": {"tools": [TOOL]}})
    elif m == "tools/call":
        params = msg.get("params") or {}
        if params.get("name") not in ("media",):
            reply({"jsonrpc": "2.0", "id": mid,
                   "error": {"code": -32601, "message": "tool tidak ada"}})
            return
        try:
            text = handle_call(params.get("arguments") or {})
            reply({"jsonrpc": "2.0", "id": mid,
                   "result": {"content": [{"type": "text", "text": text}]}})
        except Exception as e:
            reply({"jsonrpc": "2.0", "id": mid,
                   "result": {"content": [{"type": "text", "text": f"error: {e}"}],
                              "isError": True}})
    elif mid is not None:
        reply({"jsonrpc": "2.0", "id": mid,
               "error": {"code": -32601, "message": f"method tidak dikenal: {m}"}})


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            handle(json.loads(line))
        except Exception:
            continue


if __name__ == "__main__":
    main()
