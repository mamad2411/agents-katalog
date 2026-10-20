# Compress — image/video biar hemat

```bash
# image → max 1600px, q80
ffmpeg -y -i in.png -vf "scale='min(1600,iw)':-2" -q:v 3 out.jpg
# atau PIL: python3 -c "from PIL import Image; im=Image.open('in.png'); im.thumbnail((1600,1600)); im.save('out.jpg',quality=80)"
# video → h264 crf23 + audio aac
ffmpeg -y -i in.mp4 -vcodec libx264 -crf 23 -preset fast -acodec aac out.mp4
# thumbnail saja
ffmpeg -y -ss 1 -i in.mp4 -vframes 1 -q:v 3 thumb.jpg
```

Aturan: tawarkan dulu sebelum kompres (file asli tetap disimpan). Web output: jpg q80 / webp.
