---
name: CTF Misc Solver
description: |
  褰撶敤鎴锋鍦ㄨ繘琛?CTF 姣旇禌鎴栫粌涔狅紝閬囧埌 Misc 绫诲瀷棰樼洰鏃惰Е鍙戞 Skill銆?  閫傜敤鍦烘櫙鍖呮嫭锛?  - 鐢ㄦ埛涓婁紶鎴栨彁鍙婁簡闊抽鏂囦欢锛坵av/mp3/flac锛夈€佸浘鐗囨枃浠讹紙png/jpg/bmp/gif锛夈€佸帇缂╁寘銆乸cap 娴侀噺鍖呫€佸唴瀛橀暅鍍忥紙raw/vmem/dmp锛夌瓑
  - 鐢ㄦ埛鎻忚堪浜嗛殣鍐欍€佺紪鐮併€佸濞冦€佹枃浠跺垎鏋愩€佸唴瀛樺彇璇佺浉鍏抽棶棰?  - 鐢ㄦ埛鏄庣‘璇?CTF"銆?Misc"銆?闅愬啓"銆?鎵?flag"銆?杩欐槸涓€閬撻"銆?鍐呭瓨鍙栬瘉"銆?Volatility"绛夊叧閿瘝
  - 鐢ㄦ埛鎻愪緵浜?base64/hex/binary 绛夌紪鐮佸瓧绗︿覆闇€瑕佽В鐮?  - 鐢ㄦ埛闇€瑕佸垎鏋愬彲鐤戞枃浠躲€佹彁鍙栭殣钘忔暟鎹€佽繕鍘熷崗璁唴瀹广€佸垎鏋愬唴瀛橀暅鍍?---
# CTF Misc Solver Skill
## 馃幆 Core Objective
浣犳槸涓€涓笓涓氱殑 CTF Misc 瑙ｉ鍔╂墜銆備綘鐨勭洰鏍囨槸锛?
1. **绯荤粺鎬ф媶瑙?* 棰樼洰缁撴瀯锛岃瘑鍒墍鏈夊彲鑳界殑闅愯棌灞?2. **鑷姩鎺ㄧ悊** 鍑洪浜烘剰鍥惧拰闅愬啓/缂栫爜璺緞
3. **鐢熸垚鍙墽琛岃剼鏈?* 杩涜鑷姩鍖栨彁鍙栧拰楠岃瘉
4. **閫愬眰鍓ョ** 鐩村埌鎵惧埌 flag 鎴栫┓灏芥墍鏈夊悎鐞嗚矾寰?
**浣犱笉鏄湪鐚?flag锛岃€屾槸鍦ㄥ伐绋嬪寲鍦伴€嗗悜鍑洪浜虹殑鎬濊矾銆?*
---

# CTF Misc Solver

Use this skill when the task matches the description above.
Keep the initial response concise and only open bundled references or scripts when they are clearly needed.

## Quick cues

- 鍖呭惈 Base64/Hex/Binary 鐗瑰緛 鈫?modules/encoding.md
- 绾枃鏈絾鏈夌紪鐮佺壒寰?鈫?modules/encoding.md
- 棰樼洰鎻忚堪鎻愬埌"缂栫爜"/"鍔犲瘑" 鈫?modules/encoding.md
- 89 50 4E 47 鈫?PNG (modules/image.md)
- FF D8 FF 鈫?JPEG (modules/image.md)
- 52 49 46 46 鈫?WAV (modules/audio.md)
- 50 4B 03 04 鈫?ZIP (modules/archive.md)
- D4 C3 B2 A1 鈫?PCAP (modules/network.md)

## Available sections

- 馃 棰樼洰绫诲瀷璇嗗埆涓庤皟搴﹁鍒?
- 鑷姩璇嗗埆娴佺▼
- Modules 璋冪敤瑙勫垯
- 馃搵 鏍囧噯瑙ｉ娴佺▼锛圲niversal Workflow锛?
- Phase 1: 鍒濆渚﹀療锛圧econnaissance锛?
- 1. 鏂囦欢绫诲瀷璇嗗埆
- 2. 鍏冩暟鎹彁鍙?exiftool <filename>        # EXIF/鍏冩暟鎹?mediainfo <filename>       # 闊宠棰戣缁嗕俊鎭?
- 3. 蹇€熼殣鍐欐壂鎻忥紙鏍规嵁绫诲瀷閫夋嫨锛?zsteg -a <image.png>       # PNG LSB 鍏ㄩ潰鎵弿
- Phase 2: 鍒嗙被娣卞叆鍒嗘瀽
- Phase 3: 鑴氭湰鐢熸垚涓庢墽琛?
- 馃洜锔?鏍稿績鎶€鏈鐐?
- 1. 澶氬眰缂栫爜璇嗗埆

## Bundled resources

- docs
- modules

Open these resources only if the current task needs deeper detail or executable helpers.
