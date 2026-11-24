#!/usr/bin/env python3
"""media-forge — tool editing kelas profesional untuk AI (0 API, jalan lokal).

Filosofi: yang dipakai profesional = ffmpeg + ImageMagick + G'MIC + Potrace + Inkscape
+ Cairo/rsvg + Manim + Lottie. Semua di-wrap jadi satu CLI, lalu dibuka lewat MCP
(`media-mcp.py`, 1 tool, DISABLED default).

  media-forge.py scan                       cek kapabilitas terpasang
  media-forge.py probe  in.mp4
  media-forge.py video  in.mp4 out.mp4 [--w 1920 --h 1080 --fps 30 --crf 18
                        --codec h264|h265|vp9|av1 --trim 0:5 --speed 1.5 --mute
                        --fade 0.5:0.5 --sub a.srt --rotate 0]
  media-forge.py gif    in.mp4 out.gif   [--fps 15 --w 720 --start 0 --dur 3]
  media-forge.py thumb  in.mp4 out.jpg   [--at 1.5 --w 1280]
  media-forge.py concat out.mp4 a.mp4 b.mp4 ...
  media-forge.py enhance in.jpg out.jpg  [--strength 1.0]        (ala Magnific, G'MIC)
  media-forge.py upscale in.jpg out.jpg  [--scale 2] [--strength 1.0]
  media-forge.py bgremove in.jpg out.png                          (rembg u2net)
  media-forge.py vectorize in.png out.svg [--colors 8] [--turdsize 2]  (posterize+potrace)
  media-forge.py svg2png in.svg out.png  [--w 2000 --bg '#0b1020']
  media-forge.py anim   spec.json out.mp4 [--preview]             (engine animasi vektor)
  media-forge.py lottie in.json out.mp4  [--w 1080 --fps 30]
  media-forge.py manim  scene.py Scene   [--quality l|m|h]
  media-forge.py audio  in.wav out.mp3   [--normalize -14 --fade 0.5:1 --trim 0:10
                        --speed 1 --pitch 0 --mono --bitrate 192k]
  media-forge.py tts    "teks" out.wav   [--voice Samantha --rate 175 --file teks.txt]
  media-forge.py music  out.wav          [--prompt "epic cinematic" --sec 30 --bpm 90]
  media-forge.py waveform in.wav out.png [--w 1200 --h 200 --color '#4ade80']
  media-forge.py stem   in.wav outdir/   [--model htdemucs]       (butuh demucs)
  media-forge.py 3d     scene.py out.mp4 [--res 1080 --engine eevee|cycles --samples 64]
                        (Blender headless; script baca env MF_FRAMES/MF_RES/MF_ENGINE)
  media-forge.py gen    "prompt" out.png [--size 1024x1024] [--model gpt-image-1]
                        [--provider openai|xkiro]   (text-to-image via API key)
  media-forge.py see    in.jpg ["pertanyaan"] [--provider openai|xkiro|openrouter]
                        [--model ...]               (vision: tanya/deskripsikan gambar)
  media-forge.py find   "kata kunci" [--limit 20] [--in ~/dir]
                        (cari file/aset via Spotlight + walk)
  media-forge.py screen out.png [--area x,y,w,h]     (screenshot macOS)
  media-forge.py transcribe in.mp3|mp4 [--lang id]   (Whisper API → teks)
  media-forge.py tile   in1.jpg in2.jpg ... out.jpg [--cols 4 --w 400]
                        (contact sheet / kolase)
  media-forge.py format in.jpg out.webp [--w 800]    (konversi png/jpg/webp + resize)
"""
import json
import math
import os
import random
import shutil
import subprocess
import sys
import tempfile
import wave

HOME = os.path.expanduser("~")
AG = os.path.join(HOME, ".agents")
VENV = os.path.join(AG, "media-venv")
VPY = os.path.join(VENV, "bin", "python")


# ── util ────────────────────────────────────────────────────────────────────
def opt(a, name, default=None):
    if name in a:
        i = a.index(name)
        if i + 1 < len(a):
            return a[i + 1]
    return default


def flag(a, name):
    return name in a


def pos(a):
    """argumen posisional (buang --opsi nilai)."""
    out, skip = [], False
    for i, x in enumerate(a):
        if skip:
            skip = False
            continue
        if x.startswith("--"):
            if i + 1 < len(a) and not a[i + 1].startswith("--"):
                skip = True
            continue
        out.append(x)
    return out


def sh(cmd, timeout=3600, quiet=False):
    if not quiet:
        print("»", " ".join(str(c) for c in cmd)[:400], file=sys.stderr, flush=True)
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if p.returncode != 0:
        sys.stderr.write((p.stderr or p.stdout or "")[-1500:] + "\n")
        raise SystemExit(f"gagal ({p.returncode}): {os.path.basename(str(cmd[0]))}")
    return p.stdout


def has(bin_name):
    return shutil.which(bin_name) is not None


def py_mod(mod):
    try:
        r = subprocess.run([VPY, "-c", f"import {mod}"], capture_output=True, timeout=60)
        return r.returncode == 0
    except Exception:
        return False


def num(a, name, default, cast=float):
    v = opt(a, name)
    try:
        return cast(v) if v is not None else default
    except Exception:
        return default


def pair(v, default):
    """'a:b' -> (a,b)"""
    if not v:
        return default
    p = str(v).split(":")
    try:
        return (float(p[0]), float(p[1]) if len(p) > 1 else 0.0)
    except Exception:
        return default


def out_path(p):
    d = os.path.dirname(os.path.abspath(p))
    os.makedirs(d, exist_ok=True)
    return p


def vpy(code, timeout=1800):
    """jalankan snippet di venv (numpy/PIL/rembg/...)."""
    r = subprocess.run([VPY, "-c", code], capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise SystemExit((r.stderr or r.stdout)[-1200:])
    return r.stdout


# ── inti: video ─────────────────────────────────────────────────────────────
CODECS = {
    "h264": ["-c:v", "libx264", "-preset", "slow", "-pix_fmt", "yuv420p"],
    "h265": ["-c:v", "libx265", "-preset", "slow", "-tag:v", "hvc1", "-pix_fmt", "yuv420p"],
    "vp9": ["-c:v", "libvpx-vp9", "-b:v", "0", "-row-mt", "1"],
    "av1": ["-c:v", "libsvtav1", "-preset", "6", "-pix_fmt", "yuv420p"],
    "prores": ["-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le"],
}


def cmd_probe(a):
    p = pos(a)
    src = p[0]
    raw = sh(["ffprobe", "-v", "error", "-print_format", "json",
              "-show_format", "-show_streams", src], quiet=True)
    d = json.loads(raw)
    fmt = d.get("format", {})
    info = {"file": src, "dur": float(fmt.get("duration") or 0),
            "size": int(fmt.get("size") or 0), "bitrate": int(fmt.get("bit_rate") or 0),
            "streams": []}
    for s in d.get("streams", []):
        item = {"type": s.get("codec_type"), "codec": s.get("codec_name")}
        if s.get("codec_type") == "video":
            item.update(w=int(s.get("width") or 0), h=int(s.get("height") or 0),
                        fps=eval_fps(s.get("avg_frame_rate") or s.get("r_frame_rate")),
                        pix=s.get("pix_fmt"), frames=s.get("nb_frames"))
        elif s.get("codec_type") == "audio":
            item.update(rate=int(s.get("sample_rate") or 0), ch=int(s.get("channels") or 0),
                        layout=s.get("channel_layout"))
        info["streams"].append(item)
    print(json.dumps(info, indent=2, ensure_ascii=False))


def eval_fps(expr):
    try:
        if "/" in str(expr):
            a, b = str(expr).split("/")
            return round(float(a) / float(b), 3) if float(b) else 0
        return round(float(expr), 3)
    except Exception:
        return 0


def _srt_cues(path):
    txt = open(path, encoding="utf-8", errors="ignore").read().replace("\r", "")
    cues = []
    for block in txt.split("\n\n"):
        lines = [l for l in block.strip().split("\n") if l.strip()]
        if not lines:
            continue
        idx = 0
        if "-->" not in lines[0]:
            idx = 1
        if idx >= len(lines) or "-->" not in lines[idx]:
            continue
        a, b = lines[idx].split("-->")
        def sec(x):
            x = x.strip().replace(",", ".")
            hh, mm, ss = x.split(":")
            return int(hh) * 3600 + int(mm) * 60 + float(ss)
        body = "\n".join(lines[idx + 1:])
        if body:
            cues.append((sec(a), sec(b), body))
    return cues


def burn_sub(src, srt, size=28, color="#ffffff", margin=60):
    """Bakar subtitle TANPA libass: render PNG transparan (PIL) + overlay ffmpeg."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        return None
    cues = _srt_cues(srt)
    if not cues:
        return None
    info = json.loads(sh(["ffprobe", "-v", "error", "-print_format", "json",
                          "-select_streams", "v:0", "-show_entries",
                          "stream=width,height", src], quiet=True))
    st = (info.get("streams") or [{}])[0]
    W = int(st.get("width") or 1280)
    H = int(st.get("height") or 720)
    px = max(14, int(float(size) * H / 720))
    tmp = tempfile.mkdtemp(prefix="sub-")
    inputs, graph_nodes = [], []
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", px)
    except Exception:
        font = ImageFont.load_default()
    for i, (a, b, text) in enumerate(cues):
        lines = text.split("\n")
        # bungkus baris panjang
        out_lines = []
        for ln in lines:
            words, cur = ln.split(), ""
            for w in words:
                test = (cur + " " + w).strip()
                if font.getlength(test) > W * 0.86 and cur:
                    out_lines.append(cur)
                    cur = w
                else:
                    cur = test
            out_lines.append(cur)
        lh = px + int(px * 0.35)
        img = Image.new("RGBA", (W, lh * len(out_lines) + px), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        y = px // 2
        for ln in out_lines:
            wpx = font.getlength(ln)
            x = (W - wpx) / 2
            for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2)):
                d.text((x + dx, y + dy), ln, font=font, fill=(0, 0, 0, 230))
            d.text((x, y), ln, font=font, fill=hexrgb(color) + (255,))
            y += lh
        fp = os.path.join(tmp, f"s{i:03d}.png")
        img.save(fp)
        inputs += ["-i", fp]
        graph_nodes.append((fp, a, b, img.height))
    if not graph_nodes:
        return None
    parts, last = [], "[v0]"
    for i, (_, a, b, h) in enumerate(graph_nodes):
        lab = f"[v{i + 1}]"
        parts.append(f"{last}[{i + 1}:v]overlay=0:{H - h - int(float(margin))}"
                     f":enable='between(t,{a:.3f},{b:.3f})'{lab}")
        last = lab
    return inputs, ";".join(parts), last.strip("[]")


def cmd_video(a):
    p = pos(a)
    src, dst = p[0], p[1]
    vf, af = [], []
    trim = opt(a, "--trim")
    if trim:
        s, e = pair(trim, (0, 0))
        vf.append(f"trim=start={s}:end={e},setpts=PTS-STARTPTS")
        af.append(f"atrim=start={s}:end={e},asetpts=PTS-STARTPTS")
    sp = num(a, "--speed", 1.0)
    if sp != 1.0:
        vf.append(f"setpts=PTS/{sp}")
        af.append(f"atempo={min(2.0, max(0.5, sp))}")
    w, h = num(a, "--w", 0, int), num(a, "--h", 0, int)
    if w or h:
        if w and h:
            vf.append(f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
                      f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black")
        else:
            vf.append(f"scale={w or -2}:{h or -2}")
    fps = num(a, "--fps", 0, int)
    if fps:
        vf.append(f"fps={fps}")
    rot = num(a, "--rotate", 0, int)
    if rot:
        vf.append({90: "transpose=1", 180: "transpose=2,transpose=2",
                   270: "transpose=2"}.get(rot, f"rotate={math.radians(rot)}"))
    if flag(a, "--hdr2sdr"):
        vf.append("zscale=t=linear:npl=100,tonemap=hable,zscale=p=bt709:t=bt709:m=bt709")
    fade = pair(opt(a, "--fade"), (0, 0))
    dur = 0.0
    if any(fade):
        try:
            dur = float(json.loads(sh(["ffprobe", "-v", "error", "-print_format", "json",
                                       "-show_format", src], quiet=True))["format"].get("duration") or 0)
        except SystemExit:
            dur = 0
        dur = dur / max(sp, 0.001)
    if fade[0] > 0:
        vf.append(f"fade=t=in:st=0:d={fade[0]}")
        af.append(f"afade=t=in:st=0:d={fade[0]}")
    if fade[1] > 0 and dur:
        vf.append(f"fade=t=out:st={max(0, dur - fade[1])}:d={fade[1]}")
        af.append(f"afade=t=out:st={max(0, dur - fade[1])}:d={fade[1]}")

    cmd = ["ffmpeg", "-y", "-i", src]
    if opt(a, "--audio"):
        cmd += ["-i", opt(a, "--audio")]
    sub = opt(a, "--sub")
    burnt = burn_sub(src, sub, opt(a, "--sub-size", "28"), opt(a, "--sub-color", "#ffffff"),
                     opt(a, "--sub-margin", "60")) if sub else None
    if burnt:
        extra, graph, label = burnt
        cmd += extra
        pre = "[0:v]" + (",".join(vf) if vf else "null") + "[v0];"
        cmd += ["-filter_complex", pre + graph, "-map", f"[{label}]"]
    elif vf:
        cmd += ["-vf", ",".join(vf)]
    if af:
        cmd += ["-af", ",".join(af)]
    codec = opt(a, "--codec", "h264")
    cmd += CODECS.get(codec, CODECS["h264"])
    crf = num(a, "--crf", 18, int)
    if codec in ("h264", "h265", "vp9", "av1"):
        cmd += ["-crf", str(crf)]
    if flag(a, "--mute"):
        cmd += ["-an"]
    else:
        cmd += ["-c:a", "aac", "-b:a", opt(a, "--abitrate", "192k")]
    cmd += ["-movflags", "+faststart", out_path(dst)]
    sh(cmd)


def cmd_gif(a):
    p = pos(a)
    src, dst = p[0], p[1]
    fps = num(a, "--fps", 15, int)
    width = num(a, "--w", 720, int)
    start, dur = num(a, "--start", 0), num(a, "--dur", 0)
    tmp = tempfile.mkdtemp(prefix="gif-")
    pal = os.path.join(tmp, "pal.png")
    ss = ["-ss", str(start)] if start else []
    dd = ["-t", str(dur)] if dur else []
    vf = f"fps={fps}" + (f",scale={width}:-1:flags=lanczos" if width else "")
    # pass 1: palet optimal (kualitas GIF jauh lebih baik dari default 256 warna)
    sh(["ffmpeg", "-y", *ss, *dd, "-i", src, "-vf", f"{vf},palettegen=stats_mode=diff",
        pal], quiet=True)
    # pass 2: pakai palet + dither
    sh(["ffmpeg", "-y", *ss, *dd, "-i", src, "-i", pal, "-lavfi",
        f"{vf}[x];[x][1:v]paletteuse=dither=sierra2_4a:diff_mode=rectangle",
        "-loop", "0", out_path(dst)], quiet=True)
    print("gif:", dst, os.path.getsize(dst), "bytes")


def cmd_thumb(a):
    p = pos(a)
    at = num(a, "--at", 0)
    w = num(a, "--w", 1280, int)
    sh(["ffmpeg", "-y", "-ss", str(at), "-i", p[0], "-frames:v", "1",
        "-vf", f"scale={w}:-2:flags=lanczos", "-q:v", "2", out_path(p[1])])


def cmd_concat(a):
    p = pos(a)
    dst, files = p[0], p[1:]
    tmp = tempfile.mkdtemp(prefix="cat-")
    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as f:
        for x in files:
            f.write(f"file '{os.path.abspath(x)}'\n")
    if flag(a, "--reencode"):
        sh(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst,
            "-c:v", "libx264", "-crf", "18", "-c:a", "aac", "-b:a", "192k", out_path(dst)])
    else:
        sh(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out_path(dst)])


# ── inti: gambar / vektor ───────────────────────────────────────────────────
def cmd_enhance(a):
    p = pos(a)
    s = num(a, "--strength", 1.0)
    # CLAHE (local contrast) + unsharp adaptif + saturasi ringan = rasa "enhance upres"
    sh(["magick", p[0], "-colorspace", "sRGB",
        "-clahe", f"{15}x{15}+128+{2.5*s}",
        "-unsharp", f"0x{1.0*s}+{0.8*s}+0.02",
        "-modulate", "100,106",
        "-quality", "95", out_path(p[1])], quiet=True)
    if has("gmic"):
        try:  # sentuhan detail G'MIC bila tersedia (opsional, tidak fatal)
            sh(["gmic", "-i", p[1], "-to_rgb", "-unsharp", f"{1.5*s},{1.0*s},0",
                "-o", p[1]], quiet=True)
        except SystemExit:
            pass


def cmd_upscale(a):
    p = pos(a)
    scale = num(a, "--scale", 2)
    pct = int(round(scale * 100))
    tmp = tempfile.mkdtemp(prefix="up-")
    t1 = os.path.join(tmp, "up.png")
    # Lanczos + CLAHE + unsharp halus: tidak "plastik" seperti sharpen keras
    sh(["magick", p[0], "-filter", "Lanczos", "-resize", f"{pct}%",
        "-clahe", "10x10+128+1.5", "-unsharp", "0x0.8+0.6+0.02", t1], quiet=True)
    shutil.copy(t1, out_path(p[1]))


def cmd_bgremove(a):
    p = pos(a)
    if not py_mod("rembg"):
        raise SystemExit("rembg belum ada → ~/.agents/media-venv/bin/python -m pip install rembg")
    src, dst = os.path.abspath(p[0]), os.path.abspath(p[1])
    out_path(dst)
    vpy(f"""
from rembg import remove, new_session
from PIL import Image
s = new_session("u2net")
im = Image.open({src!r}).convert("RGBA")
Image.alpha_composite(Image.new("RGBA", im.size, (0,0,0,0)), remove(im, session=s)).save({dst!r})
""", timeout=900)


def cmd_vectorize(a):
    p = pos(a)
    colors = num(a, "--colors", 8, int)
    turd = num(a, "--turdsize", 4, int)
    if not has("potrace"):
        raise SystemExit("potrace belum ada → brew install potrace")
    tmp = tempfile.mkdtemp(prefix="vec-")
    pgm = os.path.join(tmp, "in.pgm")
    sh(["magick", p[0], "-colorspace", "gray", "-resize", "1600x1600>",
        "-median", "1", "-threshold", "55%", pgm], quiet=True)
    sh(["potrace", "-s", "-o", out_path(p[1]), "--turdsize", str(turd),
        "--alphamax", "1.0", "--opttolerance", "0.2", pgm], quiet=True)
    # versi berwarna: posterize lalu trace tiap layer
    if colors > 1:
        base = os.path.splitext(os.path.abspath(p[1]))[0]
        sh(["magick", p[0], "-resize", "1600x1600>", "-colors", str(colors),
            f"{base}-poster.png"], quiet=True)


def cmd_svg2png(a):
    p = pos(a)
    w = num(a, "--w", 2000, int)
    bg = opt(a, "--bg")
    tmp = tempfile.mkdtemp(prefix="svg-")
    base = os.path.join(tmp, "svg.png")
    if has("rsvg-convert"):
        sh(["rsvg-convert", "-w", str(w), "-o", base, p[0]], quiet=True)
    elif py_mod("cairosvg"):
        vpy(f"import cairosvg; cairosvg.svg2png(url={os.path.abspath(p[0])!r}, "
            f"write_to={base!r}, output_width={w})")
    else:
        raise SystemExit("butuh rsvg-convert (brew install librsvg) atau cairosvg")
    if bg:
        sh(["magick", base, "-background", bg, "-alpha", "remove", "-alpha", "off",
            out_path(p[1])], quiet=True)
    else:
        shutil.copy(base, out_path(p[1]))


# ── engine animasi vektor (tanpa dependensi cloud) ─────────────────────────
EASES = {
    "linear": lambda t: t,
    "in": lambda t: t * t * t,
    "out": lambda t: 1 - (1 - t) ** 3,
    "inout": lambda t: 4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2,
    "inQuad": lambda t: t * t,
    "outQuad": lambda t: 1 - (1 - t) ** 2,
    "outBack": lambda t: 1 + 2.7 * (t - 1) ** 3 + 1.7 * (t - 1) ** 2,
    "outElastic": lambda t: 1 if t in (0, 1) else 2 ** (-10 * t) * math.sin((t * 10 - 0.75) * 2.094) + 1,
}


def lerp(a, b, t):
    return a + (b - a) * t


def hexrgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def frame_value(el, key, t, default):
    """nilai sebuah properti pada detik t (keyframes multi-titik, dengan delay+dur)."""
    kf = (el.get("keyframes") or {}).get(key)
    if not kf:
        return el.get(key, default)
    if not isinstance(kf, list):
        return kf
    delay = float(el.get("delay") or 0)
    dur = float(el.get("dur") or 0)
    if dur <= 0:
        dur = max(0.001, float(el.get("total") or 1))
    u = (t - delay) / dur
    if u <= 0:
        return kf[0]
    if u >= 1:
        return kf[-1]
    seg = u * (len(kf) - 1)
    i = int(seg)
    return lerp(kf[i], kf[min(i + 1, len(kf) - 1)], EASES.get(el.get("ease", "out"), EASES["out"])(seg - i))


def render_anim(spec, dst, preview=False):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception:
        raise SystemExit("PIL belum ada di media-venv")
    W, H = int(spec.get("w", 1920)), int(spec.get("h", 1080))
    fps = int(spec.get("fps", 30))
    dur = float(spec.get("dur", 6))
    bg = hexrgb(spec.get("bg", "#0b1020"))
    els = spec.get("els", [])
    tmp = tempfile.mkdtemp(prefix="anim-")
    n = max(1, int(round(dur * fps)))
    for i in range(n):
        t = i / fps
        im = Image.new("RGB", (W, H), bg)
        d = ImageDraw.Draw(im, "RGBA")
        for el in els:
            total = dur
            el = dict(el, total=total)
            a = frame_value(el, "opacity", t, 1.0)
            if a <= 0.001:
                continue
            alpha = max(0, min(255, int(255 * a)))
            fill = el.get("fill", "#ffffff")
            col = hexrgb(fill) + (alpha,)
            typ = el.get("type", "rect")
            if typ == "text":
                txt = el.get("text", "")
                size = int(frame_value(el, "size", t, 64))
                try:
                    font = ImageFont.truetype(el.get("font", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
                                              if el.get("weight") == "bold"
                                              else "/System/Library/Fonts/Supplemental/Arial.ttf"), size)
                except Exception:
                    font = ImageFont.load_default()
                x = frame_value(el, "x", t, W / 2)
                y = frame_value(el, "y", t, H / 2)
                anchor = {"mm": "mm", "lt": "la", "ct": "ma", "rb": "rd"}.get(el.get("anchor", "mm"), "mm")
                d.text((x, y), txt, font=font, fill=col, anchor=anchor)
            elif typ == "rect":
                w = frame_value(el, "w", t, 100)
                h = frame_value(el, "h", t, 100)
                x = frame_value(el, "x", t, 0)
                y = frame_value(el, "y", t, 0)
                r = int(frame_value(el, "radius", t, 0))
                if el.get("stroke"):
                    d.rounded_rectangle([x, y, x + w, y + h], radius=r,
                                        outline=hexrgb(el["stroke"]) + (alpha,),
                                        width=int(el.get("strokeWidth", 2)))
                d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=col)
            elif typ == "circle":
                r = frame_value(el, "r", t, 50)
                x = frame_value(el, "cx", t, W / 2)
                y = frame_value(el, "cy", t, H / 2)
                d.ellipse([x - r, y - r, x + r, y + r], fill=col,
                          outline=hexrgb(el["stroke"]) + (alpha,) if el.get("stroke") else None,
                          width=int(el.get("strokeWidth", 2)))
            elif typ == "polygon":
                pts = el.get("points", [[0, 0], [100, 0], [50, 80]])
                ox = frame_value(el, "x", t, 0)
                oy = frame_value(el, "y", t, 0)
                sc = frame_value(el, "scale", t, 1)
                rot = math.radians(frame_value(el, "rotate", t, 0))
                P = []
                for px, py in pts:
                    X, Y = px * sc, py * sc
                    P.append((ox + X * math.cos(rot) - Y * math.sin(rot),
                              oy + X * math.sin(rot) + Y * math.cos(rot)))
                d.polygon(P, fill=col)
            elif typ == "line":
                d.line([frame_value(el, "x1", t, 0), frame_value(el, "y1", t, 0),
                        frame_value(el, "x2", t, W), frame_value(el, "y2", t, H)],
                       fill=col, width=int(frame_value(el, "width", t, 3)))
            elif typ == "image":
                try:
                    src = Image.open(os.path.expanduser(el["path"])).convert("RGBA")
                    w = int(frame_value(el, "w", t, src.width))
                    h = int(el.get("h", int(src.height * w / max(1, src.width))))
                    src = src.resize((w, h), Image.LANCZOS)
                    if alpha < 255:
                        src.putalpha(src.getchannel("A").point(lambda v: v * alpha // 255))
                    im.paste(src, (int(frame_value(el, "x", t, 0)), int(frame_value(el, "y", t, 0))), src)
                except Exception:
                    pass
            if el.get("progress") is not None and typ == "rect":  # bar progres
                p_ = max(0.0, min(1.0, t / max(0.001, dur)))
                d.rectangle([el.get("x", 0), el.get("y", 0),
                             el.get("x", 0) + el.get("w", 100) * p_,
                             el.get("y", 0) + el.get("h", 10)], fill=col)
        im.save(os.path.join(tmp, f"f{i:05d}.png"))
        if preview and i == int(n / 2):
            shutil.copy(os.path.join(tmp, f"f{i:05d}.png"), os.path.expanduser("~/Desktop/anim-preview.png"))
    sh(["ffmpeg", "-y", "-framerate", str(fps), "-i", os.path.join(tmp, "f%05d.png"),
        "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", out_path(dst)], quiet=True)


def cmd_anim(a):
    p = pos(a)
    spec = json.load(open(p[0]))
    render_anim(spec, p[1], preview=flag(a, "--preview"))


def cmd_lottie(a):
    """render Lottie (json/tgs) ATAU SVG (vektor statis) jadi video."""
    p = pos(a)
    src = os.path.abspath(p[0])
    w = num(a, "--w", 0, int)
    fps = num(a, "--fps", 0, int)
    tmp = tempfile.mkdtemp(prefix="lottie-")
    py = f'''
import json, os
from lottie.objects import Animation
from lottie.exporters.cairo import export_png
src = {src!r}; tmp = {tmp!r}; want_w = {w}; want_fps = {fps}
if src.lower().endswith(".svg"):
    from lottie.importers.svg import parse_svg_file
    anim = parse_svg_file(src)
else:
    raw = open(src, "rb").read()
    if raw[:2] == b"\\x1f\\x8b":
        import gzip; raw = gzip.decompress(raw)
    d = json.loads(raw.decode("utf-8"))
    if isinstance(d, list): d = d[0]
    anim = Animation.load(d)
fr = want_fps or int(anim.frame_rate or 30)
n = max(1, int(round(anim.out_point - anim.in_point)))
dpi = 96.0 * (want_w / anim.width) if want_w else 96.0
for i in range(n):
    with open(os.path.join(tmp, "f%05d.png" % i), "wb") as fh:
        export_png(anim, fh, frame=anim.in_point + i, dpi=dpi)
print(f"{{n}} frame @ {{fr}}fps ({{anim.width}}x{{anim.height}})")
'''
    vpy(py, timeout=3600)
    frames = sorted(f for f in os.listdir(tmp) if f.endswith(".png"))
    if not frames:
        raise SystemExit("tidak ada frame ter-render")
    fr = fps or 30
    vf = ["-vf", f"scale={w}:-2:flags=lanczos"] if w else []
    sh(["ffmpeg", "-y", "-framerate", str(fr), "-i", os.path.join(tmp, "f%05d.png"),
        *vf, "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", out_path(p[1])], quiet=True)


def cmd_manim(a):
    p = pos(a)
    srcfile = p[0]
    scene = p[1] if len(p) > 1 else "Scene"
    quality = p[2] if len(p) > 2 and p[2] in ("l", "m", "h", "k") else "m"
    out = p[3] if len(p) > 3 else None
    q = {"l": "-ql", "m": "-qm", "h": "-qh", "k": "-qk"}[quality]
    media_dir = os.path.join(AG, "media", "manim")
    sh([os.path.join(VENV, "bin", "manim"), q, "--media_dir", media_dir, "-v", "WARNING",
        srcfile, scene], timeout=7200, quiet=True)
    d = os.path.join(media_dir, "videos")
    hits = []
    for root, _, files in os.walk(d):
        for f in files:
            if f == f"{scene}.mp4":
                hits.append(os.path.join(root, f))
    if not hits:
        raise SystemExit("render manim tidak menghasilkan mp4")
    src = max(hits, key=os.path.getmtime)
    if out:
        shutil.copy(src, out_path(out))
        print("manim:", out)
    else:
        print("manim:", src)


# ── audio ───────────────────────────────────────────────────────────────────
def cmd_audio(a):
    p = pos(a)
    src, dst = p[0], p[1]
    flt = []
    trim = opt(a, "--trim")
    if trim:
        s, e = pair(trim, (0, 0))
        flt.append(f"atrim=start={s}:end={e},asetpts=PTS-STARTPTS")
    sp = num(a, "--speed", 1.0)
    if sp != 1:
        flt.append(f"atempo={min(2.0, max(0.5, sp))}")
    pitch = num(a, "--pitch", 0)
    if pitch:
        r = 2 ** (pitch / 12)
        flt += [f"asetrate=48000*{r}", "aresample=48000"]
    mode = opt(a, "--mono")
    if mode:
        flt.append("pan=mono|c0=0.5*c0+0.5*c1")
    fade = pair(opt(a, "--fade"), (0, 0))
    if fade[0]:
        flt.append(f"afade=t=in:st=0:d={fade[0]}")
    if fade[1]:
        dur = float(json.loads(sh(["ffprobe", "-v", "error", "-print_format", "json", "-show_format",
                                   src], quiet=True))["format"].get("duration") or 0)
        flt.append(f"afade=t=out:st={max(0, dur - fade[1])}:d={fade[1]}")
    lufs = opt(a, "--normalize")
    if lufs is not None:
        flt.append(f"loudnorm=I={float(lufs)}:TP=-1.5:LRA=11")
    cmd = ["ffmpeg", "-y", "-i", src]
    if flt:
        cmd += ["-af", ",".join(flt)]
    cmd += ["-ar", "48000"]
    if dst.endswith(".mp3"):
        cmd += ["-c:a", "libmp3lame", "-b:a", opt(a, "--bitrate", "192k")]
    elif dst.endswith((".m4a", ".aac")):
        cmd += ["-c:a", "aac", "-b:a", opt(a, "--bitrate", "192k")]
    elif dst.endswith(".flac"):
        cmd += ["-c:a", "flac"]
    else:
        cmd += ["-c:a", "pcm_s24le"]
    cmd += [out_path(dst)]
    sh(cmd)


def cmd_tts(a):
    p = pos(a)
    text = opt(a, "--file")
    if text:
        text = open(os.path.expanduser(text)).read()
    else:
        text = p[0]
    dst = p[-1]
    voice = opt(a, "--voice", "Samantha")
    rate = opt(a, "--rate", "175")
    out_path(dst)
    tmp = tempfile.mkdtemp(prefix="tts-")
    aiff = os.path.join(tmp, "v.aiff")
    if shutil.which("say"):
        sh(["say", "-v", voice, "-r", str(rate), "-o", aiff, text])
    elif shutil.which("piper"):
        raise SystemExit("pakai: piper --model x.onnx --output_file out.wav")
    else:
        raise SystemExit("butuh macOS `say` atau piper")
    if dst.endswith(".wav"):
        sh(["ffmpeg", "-y", "-i", aiff, "-c:a", "pcm_s24le", "-ar", "48000", dst], quiet=True)
    else:
        sh(["ffmpeg", "-y", "-i", aiff, "-c:a", "libmp3lame", "-b:a", "192k", dst], quiet=True)


# ── musik prosedural (numpy) ────────────────────────────────────────────────
STYLES = {
    "cinematic": dict(bpm=80, scale=[0, 2, 3, 5, 7, 8, 10], prog=[0, 5, 3, 4], drums=0.35, pad=0.9, arp=0.35),
    "epic": dict(bpm=100, scale=[0, 2, 3, 5, 7, 8, 11], prog=[0, 5, 2, 6], drums=0.6, pad=0.8, arp=0.5),
    "lofi": dict(bpm=78, scale=[0, 2, 3, 5, 7, 9, 10], prog=[0, 3, 5, 4], drums=0.45, pad=0.6, arp=0.55),
    "edm": dict(bpm=126, scale=[0, 2, 3, 5, 7, 9, 10], prog=[0, 4, 5, 3], drums=0.9, pad=0.4, arp=0.8),
    "ambient": dict(bpm=60, scale=[0, 2, 4, 7, 9], prog=[0, 3, 1, 4], drums=0.0, pad=1.0, arp=0.2),
}


def cmd_music(a):
    p = pos(a)
    dst = p[0]
    sec = num(a, "--sec", 30)
    prompt = (opt(a, "--prompt") or "").lower()
    style = opt(a, "--style") or next((k for k in STYLES if k in prompt), "cinematic")
    st = STYLES[style]
    bpm = num(a, "--bpm", st["bpm"])
    key = num(a, "--key", 0, int)
    seed = num(a, "--seed", random.randint(1, 99999), int)
    out_path(dst)
    code = f"""
import math, random, wave, struct
import numpy as np
random.seed({seed}); np.random.seed({seed})
SR=48000; SEC={sec}; BPM={bpm}; STYLE={st!r}; KEY={key}; PROMPT={prompt!r}
style_name={style!r}
N=int(SR*SEC); t=np.arange(N)/SR
L=np.zeros(N); R=np.zeros(N)
def env(n, a=0.01, d=0.2, s=0.7, r=0.3):
    e=np.ones(n); A=int(a*SR); D=int(d*SR); RR=int(r*SR)
    A=min(A,n); e[:A]=np.linspace(0,1,A)
    if D+A<n: e[A:A+D]=np.linspace(1,s,min(D,n-A))
    if RR: e[-RR:]*=np.linspace(1,0,min(RR,n))
    return e
def note(freq, dur, kind='saw', amp=0.2, detune=0.0):
    n=int(dur*SR); tt=np.arange(n)/SR
    f=freq*(2**(detune/1200))
    if kind=='saw':
        # band-limited-ish saw via additive
        sig=np.zeros(n)
        for h in range(1,9):
            if f*h>SR/2.2: break
            sig+=np.sin(2*np.pi*f*h*tt)/h
    elif kind=='sine': sig=np.sin(2*np.pi*f*tt)
    elif kind=='square':
        sig=np.sign(np.sin(2*np.pi*f*tt))*0.6
    else: sig=np.sin(2*np.pi*f*tt)
    return sig*amp*env(n, 0.005, 0.25, 0.65, min(0.5,dur*0.4))
def midi(m): return 440.0*(2**((m-69)/12))
scale=STYLE['scale']; prog=STYLE['prog']
root=48+KEY
beat=60.0/BPM; bar=beat*4
bars=int(SEC/bar)+1
for b in range(bars):
    t0=b*bar
    if t0>SEC-0.2: break
    deg=prog[b%len(prog)]
    base=root+scale[deg%len(scale)]+12*(deg//len(scale))
    chord=[base, base+scale[2], base+scale[4], base+12]
    idx0=int(t0*SR); 
    # pad
    for m in chord:
        sig=note(midi(m), bar*1.02, 'saw', 0.055*STYLE['pad'], detune=random.uniform(-8,8))
        sig2=note(midi(m), bar*1.02, 'saw', 0.055*STYLE['pad'], detune=random.uniform(-8,8))
        n=min(len(sig), N-idx0)
        if n>0:
            L[idx0:idx0+n]+=sig[:n]*0.6
            R[idx0:idx0+n]+=sig2[:n]*0.6
    # bass
    if t0+bar<=SEC:
        sig=note(midi(base-12), beat*0.95, 'sine', 0.35)
        n=min(len(sig), N-idx0); L[idx0:idx0+n]+=sig[:n]; R[idx0:idx0+n]+=sig[:n]
    # arp
    if STYLE['arp']>0:
        steps=8
        for s_ in range(steps):
            ts=t0+s_*(bar/steps)
            if ts>=SEC: break
            m=chord[s_%len(chord)]+12
            sig=note(midi(m), bar/steps*0.9, 'square', 0.05*STYLE['arp'])
            i0=int(ts*SR); n=min(len(sig), N-i0)
            if n>0:
                pan=0.5+0.4*math.sin(s_)
                L[i0:i0+n]+=sig[:n]*(1-pan); R[i0:i0+n]+=sig[:n]*pan
    # drums
    if STYLE['drums']>0:
        for beat_i in range(4):
            ts=t0+beat_i*beat
            if ts>=SEC: break
            i0=int(ts*SR)
            if beat_i in (0,2):
                n=int(0.18*SR); tt=np.arange(n)/SR
                kick=np.sin(2*np.pi*(55*np.exp(-tt*18)+45)*tt)*np.exp(-tt*9)*0.9
                m=min(n,N-i0); L[i0:i0+m]+=kick[:m]*STYLE['drums']; R[i0:i0+m]+=kick[:m]*STYLE['drums']
            if beat_i in (1,3):
                n=int(0.15*SR)
                sn=np.random.randn(n)*np.exp(-np.arange(n)/SR*30)*0.35*STYLE['drums']
                m=min(n,N-i0); L[i0:i0+m]+=sn[:m]; R[i0:i0+m]+=sn[:m]
        hat_n=int(0.05*SR)
        for k in range(int(bar/(beat/2))):
            ts=t0+k*beat/2
            if ts>=SEC: break
            i0=int(ts*SR); n=hat_n
            h=np.random.randn(n)*np.exp(-np.arange(n)/SR*90)*0.09*STYLE['drums']
            m=min(n,N-i0); L[i0:i0+m]+=h[:m]*0.7; R[i0:i0+m]+=h[:m]*1.0
# reverb (delay jaringan sederhana)
for dly,gain in ((0.031,0.32),(0.047,0.26),(0.071,0.2),(0.113,0.14)):
    d=int(dly*SR)
    L[d:]+=L[:-d]*gain; R[d:]+=R[:-d]*gain
# lowpass halus + limiter
k=np.ones(24)/24
L=np.convolve(L,k,'same'); R=np.convolve(R,k,'same')
mix=np.maximum(np.abs(L),np.abs(R)); peak=mix.max() if mix.max()>0 else 1
g=min(1.0, 0.89/peak); L*=g; R*=g
L=np.tanh(L*1.25)/1.25; R=np.tanh(R*1.25)/1.25
# fade in/out
f=int(0.8*SR); L[:f]*=np.linspace(0,1,f); R[:f]*=np.linspace(0,1,f)
L[-f:]*=np.linspace(1,0,f); R[-f:]*=np.linspace(1,0,f)
st=np.stack([L,R],axis=1); st=np.clip(st,-1,1)
pcm=(st*32767).astype('<i2')
with wave.open({dst!r},'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('dur', SEC, 'peak', float(np.abs(st).max()))
"""
    vpy(code, timeout=1800)
    # perdengarkan bila diminta
    if flag(a, "--play"):
        subprocess.run(["afplay", dst])


def cmd_waveform(a):
    p = pos(a)
    if has("audiowaveform"):
        sh(["audiowaveform", "-i", p[0], "-o", out_path(p[1]), "--width",
            str(num(a, "--w", 1200, int)), "--height", str(num(a, "--h", 200, int)),
            "--waveform-color", opt(a, "--color", "#4ade80").lstrip("#"),
            "--background-color", "00000000", "--border-color", "00000000",
            "--waveform-style", "bars", "--amplitude-scale", "auto"])
    else:
        sh(["ffmpeg", "-y", "-i", p[0], "-filter_complex",
            "showwavespic=s=1200x200:colors=#4ade80", "-frames:v", "1", out_path(p[1])], quiet=True)


def cmd_stem(a):
    p = pos(a)
    if not py_mod("demucs"):
        raise SystemExit("demucs belum ada → ~/.agents/media-venv/bin/python -m pip install demucs")
    sh([VPY, "-m", "demucs", "-n", opt(a, "--model", "htdemucs"),
        "-o", out_path(p[1]), p[0]], timeout=7200)


BLENDER_APP = "/Applications/Blender.app/Contents/MacOS/Blender"


def blender_bin():
    return shutil.which("blender") or (BLENDER_APP if os.path.exists(BLENDER_APP) else None)


def cmd_blender(a):
    """render animasi 3D dari script bpy secara headless."""
    p = pos(a)
    bl = blender_bin()
    if not bl:
        raise SystemExit("blender belum ada → brew install --cask blender")
    script = os.path.abspath(p[0])
    out = p[1] if len(p) > 1 else None
    res = num(a, "--res", 1080, int)
    engine = opt(a, "--engine", "eevee")
    samples = str(num(a, "--samples", 64, int))
    fps = str(num(a, "--fps", 24, int))
    tmp = tempfile.mkdtemp(prefix="blender-")
    env = dict(os.environ, MF_FRAMES=tmp, MF_RES=str(res), MF_ENGINE=engine,
               MF_SAMPLES=samples, MF_END=str(num(a, "--frames", 90, int)))
    run = subprocess.run([bl, "-b", "-P", script], env=env,
                         capture_output=True, text=True, timeout=7200)
    if run.returncode != 0:
        raise SystemExit((run.stderr or run.stdout)[-1200:])
    frames = sorted(f for f in os.listdir(tmp) if f.lower().endswith((".png", ".jpg")))
    if not frames:
        raise SystemExit("blender tidak menghasilkan frame (cek MF_FRAMES di script)")
    if out:
        import re as _re
        m = _re.match(r"^(.*?)(\d+)\.(png|jpg|jpeg)$", frames[0])
        if m:
            pat = f"%0{len(m.group(2))}d.png"
            first = m.group(2)
        else:
            pat, first = "%04d.png", "1"
        sh(["ffmpeg", "-y", "-framerate", fps, "-start_number", str(int(first)),
            "-i", os.path.join(tmp, pat),
            "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
            "-c:v", "libx264", "-crf", "17",
            "-pix_fmt", "yuv420p", out_path(out)], quiet=True)
        print("3d:", out)
    else:
        print("frame 3d:", tmp, len(frames))


# ── API helpers (stdlib only) ───────────────────────────────────────────────
def _api_post(url, key, payload, timeout=180, extra_headers=None):
    import urllib.request
    data = json.dumps(payload).encode()
    hdr = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
    if extra_headers:
        hdr.update(extra_headers)
    req = urllib.request.Request(url, data=data, headers=hdr)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def _api_providers(kind="chat"):
    """provider chain yang punya key: (name, base_url, key, default_model)."""
    out = []
    env = os.environ
    if env.get("OPENAI_API_KEY"):
        out.append(("openai", "https://api.openai.com/v1", env["OPENAI_API_KEY"],
                    "gpt-4o-mini" if kind == "chat" else "gpt-image-1"))
    if env.get("XKIRO_API_KEY"):
        out.append(("xkiro", "https://api.xkiro.com/v1", env["XKIRO_API_KEY"],
                    "cohere/command-a-vision" if kind == "chat" else "google/gemini-2.5-flash"))
    if env.get("OPENROUTER_API_KEY"):
        out.append(("openrouter", "https://openrouter.ai/api/v1", env["OPENROUTER_API_KEY"],
                    "nvidia/nemotron-3.5-super-vl:free" if kind == "chat" else "google/gemini-2.5-flash-image"))
    return out


def _b64_image(path, max_px=1280):
    import base64, io
    from PIL import Image
    im = Image.open(path).convert("RGB")
    im.thumbnail((max_px, max_px))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()


# ── gen: text-to-image ──────────────────────────────────────────────────────
def cmd_gen(a):
    p = pos(a)
    if len(p) < 2:
        raise SystemExit('pakai: media-forge.py gen "prompt" out.png [--size 1024x1024] [--provider openai|xkiro]')
    prompt, out = p[0], out_path(p[1])
    size = opt(a, "--size", "1024x1024")
    want = opt(a, "--provider")
    model = opt(a, "--model")
    errs = []
    for name, base, key, dmodel in _api_providers("image"):
        if want and name != want:
            continue
        try:
            if name == "openrouter":
                # OpenRouter tidak punya /images/generations → chat + modalities image
                r = _api_post(f"{base}/chat/completions", key, {
                    "model": model or dmodel,
                    "messages": [{"role": "user", "content": prompt}],
                    "modalities": ["image", "text"],
                })
                msg = (r.get("choices") or [{}])[0].get("message") or {}
                imgs = msg.get("images") or []
                url = ((imgs[0].get("image_url") or {}).get("url") if imgs else "") or ""
                if url.startswith("data:") and ";base64," in url:
                    import base64
                    with open(out, "wb") as f:
                        f.write(base64.b64decode(url.split(";base64,", 1)[1]))
                elif url.startswith("http"):
                    import urllib.request
                    with urllib.request.urlopen(url, timeout=120) as resp, open(out, "wb") as f:
                        f.write(resp.read())
                else:
                    errs.append(f"{name}: tidak ada gambar di respons")
                    continue
            else:
                r = _api_post(f"{base}/images/generations", key,
                              {"model": model or dmodel, "prompt": prompt, "size": size, "n": 1})
                item = (r.get("data") or [{}])[0]
                if item.get("b64_json"):
                    import base64
                    with open(out, "wb") as f:
                        f.write(base64.b64decode(item["b64_json"]))
                elif item.get("url"):
                    import urllib.request
                    with urllib.request.urlopen(item["url"], timeout=120) as resp, open(out, "wb") as f:
                        f.write(resp.read())
                else:
                    errs.append(f"{name}: response tanpa data")
                    continue
            print(f"gen: {out} ({name}, {model or dmodel})")
            return
        except Exception as e:
            errs.append(f"{name}: {str(e)[:200]}")
    raise SystemExit("gen gagal semua provider:\n  " + "\n  ".join(errs) +
                     "\n  alternatif: sk -l image-generation (runcomfy) / sk -l imagegen")


# ── see: vision ─────────────────────────────────────────────────────────────
def cmd_see(a):
    p = pos(a)
    if not p:
        raise SystemExit('pakai: media-forge.py see in.jpg ["pertanyaan"] [--provider ...] [--model ...]')
    img, question = p[0], " ".join(p[1:]) or "Deskripsikan gambar ini secara detail."
    if not os.path.exists(img):
        raise SystemExit(f"file tidak ada: {img}")
    ext = img.lower().rsplit(".", 1)[-1]
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
            "webp": "image/webp", "gif": "image/gif"}.get(ext, "image/jpeg")
    import base64
    with open(img, "rb") as f:
        raw = base64.b64encode(f.read()).decode()
    url = f"data:{mime};base64,{raw}"
    want = opt(a, "--provider")
    model = opt(a, "--model")
    errs = []
    for name, base, key, dmodel in _api_providers("chat"):
        if want and name != want:
            continue
        try:
            r = _api_post(f"{base}/chat/completions", key, {
                "model": model or dmodel,
                "messages": [{"role": "user", "content": [
                    {"type": "text", "text": question},
                    {"type": "image_url", "image_url": {"url": url}}]}],
                "max_tokens": int(opt(a, "--max", "1200")),
            })
            txt = ((r.get("choices") or [{}])[0].get("message") or {}).get("content", "")
            if not txt:
                errs.append(f"{name}: respons kosong")
                continue
            print(txt)
            return
        except Exception as e:
            errs.append(f"{name}: {str(e)[:200]}")
    raise SystemExit("see gagal semua provider:\n  " + "\n  ".join(errs))


# ── find: cari aset ─────────────────────────────────────────────────────────
def cmd_find(a):
    q = opt(a, "--q") or " ".join(x for x in pos(a))
    if not q:
        raise SystemExit('pakai: media-forge.py find "kata kunci" [--limit 20] [--in ~/dir]')
    limit = int(opt(a, "--limit", "20"))
    base = os.path.expanduser(opt(a, "--in", ""))
    hits = []
    if has("mdfind") and not base:
        try:
            out = subprocess.run(["mdfind", f'kMDItemDisplayName == "*{q}*"ccd || kMDItemFSName == "*{q}*"c'],
                                 capture_output=True, text=True, timeout=30).stdout
            hits = [l for l in out.splitlines() if l.strip()]
        except Exception:
            hits = []
    if not hits:
        roots = [base] if base else [os.path.expanduser(d) for d in
                ("~/assets", "~/Pictures", "~/Downloads", "~/Desktop", "~/Documents", "~/Movies")]
        exts = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".mp4", ".mov",
                ".mp3", ".wav", ".pdf", ".psd", ".ai", ".fig", ".sketch")
        ql = q.lower()
        for root in roots:
            if not os.path.isdir(root):
                continue
            for dp, dn, fn in os.walk(root):
                dn[:] = [d for d in dn if not d.startswith(".")]
                for f in fn:
                    if ql in f.lower() and f.lower().endswith(exts):
                        hits.append(os.path.join(dp, f))
                    if len(hits) >= limit * 3:
                        break
                if len(hits) >= limit * 3:
                    break
            if len(hits) >= limit * 3:
                break
    if base:
        hits = [h for h in hits if h.startswith(os.path.abspath(base))]
    for h in hits[:limit]:
        print(h)
    print(f"— {min(len(hits), limit)}/{len(hits)} hasil", file=sys.stderr)


# ── screen: screenshot ──────────────────────────────────────────────────────
def cmd_screen(a):
    p = pos(a)
    out = out_path(p[0] if p else os.path.join(tempfile.gettempdir(), "screen.png"))
    cmd = ["screencapture", "-x"]
    area = opt(a, "--area")
    if area:
        cmd += ["-R", area]
    cmd.append(out)
    sh(cmd, timeout=30)
    print(out)


# ── transcribe: Whisper API ─────────────────────────────────────────────────
def cmd_transcribe(a):
    p = pos(a)
    if not p:
        raise SystemExit("pakai: media-forge.py transcribe in.mp3|mp4 [--lang id]")
    src = p[0]
    if not os.path.exists(src):
        raise SystemExit(f"file tidak ada: {src}")
    lang = opt(a, "--lang")
    errs = []
    for name, base, key, _ in _api_providers("chat"):
        try:
            boundary = "----mf" + os.urandom(8).hex()
            ext = src.rsplit(".", 1)[-1].lower()
            mime = {"mp3": "audio/mpeg", "wav": "audio/wav", "m4a": "audio/mp4",
                    "mp4": "video/mp4", "webm": "audio/webm", "ogg": "audio/ogg"}.get(ext, "application/octet-stream")
            fields = {"model": "whisper-1", "response_format": "json"}
            if lang:
                fields["language"] = lang
            body = b""
            for k, v in fields.items():
                body += f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
            with open(src, "rb") as f:
                data = f.read()
            body += (f'--{boundary}\r\nContent-Disposition: form-data; name="file"; '
                     f'filename="audio.{ext}"\r\nContent-Type: {mime}\r\n\r\n').encode() + data + b"\r\n"
            body += f"--{boundary}--\r\n".encode()
            import urllib.request
            req = urllib.request.Request(f"{base}/audio/transcriptions", data=body,
                headers={"Content-Type": f"multipart/form-data; boundary={boundary}",
                         "Authorization": f"Bearer {key}"})
            with urllib.request.urlopen(req, timeout=600) as r:
                res = json.loads(r.read().decode())
            txt = res.get("text", "")
            out = out_path(src.rsplit(".", 1)[0] + ".txt")
            with open(out, "w") as f:
                f.write(txt)
            print(txt[:2000])
            print(f"— disimpan: {out}", file=sys.stderr)
            return
        except Exception as e:
            errs.append(f"{name}: {str(e)[:200]}")
    raise SystemExit("transcribe gagal semua provider:\n  " + "\n  ".join(errs))


# ── tile: contact sheet ─────────────────────────────────────────────────────
def cmd_tile(a):
    p = pos(a)
    if len(p) < 3:
        raise SystemExit("pakai: media-forge.py tile in1.jpg in2.jpg ... out.jpg [--cols 4 --w 400]")
    out = out_path(p[-1])
    files = [f for f in p[:-1] if os.path.exists(f)]
    cols = int(opt(a, "--cols", "4"))
    w = int(opt(a, "--w", "400"))
    from PIL import Image, ImageOps
    thumbs = []
    for f in files:
        try:
            im = ImageOps.exif_transpose(Image.open(f)).convert("RGB")
            im.thumbnail((w, w * 2))
            thumbs.append((f, im.copy()))
        except Exception:
            pass
    if not thumbs:
        raise SystemExit("tidak ada gambar valid")
    rows = (len(thumbs) + cols - 1) // cols
    cellw, cellh = w, int(w * 1.5)
    sheet = Image.new("RGB", (cols * cellw, rows * cellh), (20, 20, 24))
    from PIL import ImageDraw
    dr = ImageDraw.Draw(sheet)
    for i, (f, im) in enumerate(thumbs):
        x, y = (i % cols) * cellw, (i // cols) * cellh
        sheet.paste(im, (x + (cellw - im.width) // 2, y + (cellh - im.height) // 2))
        dr.text((x + 6, y + 6), os.path.basename(f)[:40], fill=(255, 255, 255))
    sheet.save(out, quality=90)
    print(out)


# ── format: konversi ────────────────────────────────────────────────────────
def cmd_format(a):
    p = pos(a)
    if len(p) < 2:
        raise SystemExit("pakai: media-forge.py format in.jpg out.webp [--w 800]")
    src, out = out_path(p[0]), out_path(p[1])
    w = int(opt(a, "--w", "0"))
    from PIL import Image, ImageOps
    im = ImageOps.exif_transpose(Image.open(src))
    if w and im.width > w:
        im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    ext = out.rsplit(".", 1)[-1].lower()
    if ext in ("jpg", "jpeg"):
        im.convert("RGB").save(out, quality=int(opt(a, "--q", "90")))
    elif ext == "webp":
        im.save(out, "WEBP", quality=int(opt(a, "--q", "88")))
    elif ext == "png":
        im.save(out, "PNG")
    else:
        im.save(out)
    print(out)


# ── scan kapabilitas ────────────────────────────────────────────────────────
BINS = ["ffmpeg", "ffprobe", "magick", "gmic", "potrace", "rsvg-convert", "inkscape",
        "gs", "sox", "lame", "audiowaveform", "say", "screencapture", "mdfind"]
MODS = ["numpy", "PIL", "cairosvg", "moviepy", "cv2", "rembg", "lottie", "manim", "demucs"]


def cmd_scan(a):
    print("binary:")
    for b in BINS:
        print(f"  {'ok ' if has(b) else '-- '} {b}")
    print(f"  {'ok ' if blender_bin() else '-- '} blender")
    print("python (media-venv):")
    for m in MODS:
        print(f"  {'ok ' if py_mod(m) else '-- '} {m}")
    print("\ncontoh cepat:")
    print("  media-forge.py music out.wav --style cinematic --sec 20")
    print("  media-forge.py anim spec.json out.mp4")
    print("  media-forge.py upscale foto.jpg besar.jpg --scale 2")


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return
    cmd, rest = a[0], a[1:]
    table = {
        "probe": cmd_probe, "video": cmd_video, "gif": cmd_gif, "thumb": cmd_thumb,
        "concat": cmd_concat, "enhance": cmd_enhance, "upscale": cmd_upscale,
        "bgremove": cmd_bgremove, "vectorize": cmd_vectorize, "svg2png": cmd_svg2png,
        "anim": cmd_anim, "lottie": cmd_lottie, "manim": cmd_manim, "audio": cmd_audio,
        "tts": cmd_tts, "music": cmd_music, "waveform": cmd_waveform, "stem": cmd_stem,
        "3d": cmd_blender, "blender": cmd_blender, "scan": cmd_scan,
        "gen": cmd_gen, "see": cmd_see, "find": cmd_find, "screen": cmd_screen,
        "transcribe": cmd_transcribe, "tile": cmd_tile, "format": cmd_format,
    }
    fn = table.get(cmd)
    if not fn:
        sys.exit(f"perintah tidak dikenal: {cmd}\n\n{__doc__}")
    fn(rest)


if __name__ == "__main__":
    main()
