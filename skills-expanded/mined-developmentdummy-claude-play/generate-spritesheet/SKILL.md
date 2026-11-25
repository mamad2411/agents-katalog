---
name: generate-spritesheet
description: Gemini 이미지 생성으로 게임용 아이콘 스프라이트시트를 만들고 자동 슬라이스한다. 아이콘, UI 리소스, 뱃지, 마커 등 여러 개의 동일 카테고리 에셋이 필요할 때 사용한다.
allowed-tools: Bash, Read, Write, Edit
---

# 스프라이트시트 생성 (Gemini + PIL 슬라이스)

Gemini 이미지 생성 1회로 N×M 그리드 스프라이트시트를 만들고, Python PIL로 개별 아이콘을 자동 추출한다.

## 파이프라인

```
1. 프롬프트 설계 (N×M 그리드, 아이콘 목록)
2. Gemini API 호출 (1장 생성)
3. 생성 대기 (15-20초)
4. 생성된 이미지를 직접 확인하여 실제 그리드 크기 파악 (중요!)
5. Python PIL 슬라이스 (그리드 분할 → 배경 자동 감지 → 크롭 → 정규화 → 배경 제거)
6. 결과 검증
```

## 1단계: 프롬프트 설계

### 프롬프트 템플릿

```
A {cols}x{rows} grid of {카테고리} on a pure black background.
{총 수} icons arranged in a strictly aligned {cols} columns by {rows} rows grid.
Each icon must be inside its own clearly separated rectangular cell.
{스타일 지시}

Row 1 (left to right): {아이템1}, {아이템2}, ...
Row 2: ...
...

Each icon should be {품질/스타일 요구사항}.
```

### 프롬프트 강화 규칙

Gemini는 그리드를 자의적으로 해석하는 경향이 있다. 다음 문구를 반드시 포함하여 정규 그리드를 강제한다:

- **그리드 강제**: `"strictly aligned {cols} columns by {rows} rows grid"` — "perfect" 대신 "strictly aligned" 사용
- **셀 분리 강제**: `"Each icon must be inside its own clearly separated rectangular cell"` — 아이콘 간 겹침 방지
- **배경색 명시**: `"on a pure black background"` — 슬라이서가 배경색을 기준으로 동작
- **정확한 수량 반복**: 프롬프트 첫 줄과 구조 설명 줄에 모두 그리드 크기를 명시

### 주의: Gemini의 그리드 불일치 문제

**Gemini는 요청한 그리드 크기와 다른 결과를 생성할 수 있다.** 예를 들어:
- 4×4(16개) 요청 → 6×4(24개) 생성
- 4×3(12개) 요청 → 6×3(18개) 생성
- 배경색을 검정 대신 흰색으로 생성

**따라서 3단계에서 반드시 이미지를 직접 열어 확인하고, 실제 그리드 크기를 파악한 후 슬라이스해야 한다.**

### 프롬프트 작성 규칙

- 반드시 **영어**로 작성
- `pure black background` 명시 (배경 제거 기준)
- 각 Row의 아이콘을 **왼쪽에서 오른쪽 순서로** 구체적으로 나열
- 스타일 통일 문구 포함: `flat design`, `golden outlines`, `game UI style` 등
- 최대 권장 요청: **4×4 (16개)** — 실제로 더 많이 생성될 수 있지만 품질 유지됨
- 텍스트 라벨 방지: `"no text labels"` 추가 권장 (Gemini가 아이콘에 이름을 적는 경향 있음)

### 프롬프트 예시

무기 아이콘:
```
A 4x4 grid of medieval fantasy RPG weapon icons on a pure black background.
16 weapon icons arranged in a strictly aligned 4 columns by 4 rows grid.
Each icon must be inside its own clearly separated rectangular cell.
Flat design, golden metallic outlines, dark background per icon, game UI style, no text labels.

Row 1 (left to right): iron sword, ornate steel sword, glowing enchanted blade, great sword
Row 2: dagger, curved assassin blade, hunting bow, longbow
Row 3: wooden staff, crystal magic staff with purple glow, battle axe, war hammer
Row 4: spear, halberd, throwing knives, magic wand

Each icon centered in its cell, recognizable silhouette, suitable for inventory UI.
```

클래스 엠블럼:
```
A 4x4 grid of medieval fantasy RPG class emblem icons on a pure black background.
16 class emblems arranged in a strictly aligned 4 columns by 4 rows grid.
Each emblem must be inside its own clearly separated rectangular cell.
Rich colors, metallic gold borders, heraldic style, game UI quality, no text labels.

Row 1 (left to right): crossed swords on red shield (Fighter), silver sword and cross on blue (Knight), flaming axe on black (Berserker), bow and arrow on green crest (Ranger)
Row 2: healing staff on green (Healer), crescent moon and stars on purple (Enchantress), musical note on pink ribbon (Dancer/Bard), spear and shield on gray (Soldier)
Row 3: lance on crimson dragon crest (Dragoon), twin daggers on dark shadow (Thief), holy sun rays on gold (Sage), dark skull on purple flames (Dark Knight)
Row 4: crown on royal blue (General), treasure chest on amber (Treasure Hunter), shuriken on midnight blue (Ninja), crystal ball on purple (Arcane Mage)

Each emblem should look like a heraldic badge, ornate and detailed.
```

상태효과:
```
A 4x3 grid of RPG status effect icons on a pure black background.
12 status effect icons in a strictly aligned 4 columns by 3 rows grid.
Each icon must be inside its own clearly separated rectangular cell.
Clean bold design, glowing effects, game battle UI style, no text labels.

Row 1 (left to right): red upward arrow (ATK buff), blue upward arrow (DEF buff), green healing sparkles (regeneration), golden aura rays (all stats boost)
Row 2: red downward arrow (ATK debuff), blue downward arrow (DEF debuff), purple skull with drip (poison), orange flame (burn)
Row 3: ice crystal snowflake (frozen), yellow lightning (stun), pink swirl hearts (charm), green shield bubble (barrier)

Each icon vibrant, immediately recognizable at small sizes.
```

## 2단계: Gemini 호출

```bash
cat > /tmp/gemini-sprite.json << 'REQEOF'
{
  "prompt": "<설계한 프롬프트>",
  "filename": "<카테고리>-sprite.png",
  "persona": "<페르소나 이름>"
}
REQEOF
curl -s -X POST "http://localhost:{{PORT}}/api/tools/gemini/generate" \
  -H "Content-Type: application/json" \
  -d @/tmp/gemini-sprite.json
```

또는 MCP 도구:
```
mcp__claude_play__gemini_generate({
  prompt: "...",
  filename: "weapons-sprite.png",
  persona: "페르소나이름"
})
```

## 3단계: 생성 확인 + 실제 그리드 파악 (중요!)

```bash
sleep 15 && ls -la "<페르소나경로>/images/<파일명>"
```

**반드시 이미지를 직접 열어서 실제 그리드 크기를 확인한다:**

```
Read 도구로 이미지를 열어 확인
```

확인할 사항:
1. **실제 행×열 수**: 요청한 것과 다를 수 있다 (예: 4×4 요청 → 6×4 생성)
2. **배경색**: 검정인지 흰색인지 확인 — 슬라이서 모드 결정에 필요
3. **텍스트 라벨 유무**: 라벨이 포함됐으면 슬라이싱에 영향 줄 수 있음
4. **아이콘 배치 균일성**: 그리드가 대체로 균일한지

**이 확인 없이 슬라이스하면 아이콘이 잘리거나 병합된다.**

## 4단계: Python PIL 슬라이스 + 배경 제거 (통합)

슬라이스와 배경 제거를 한 번에 처리하는 통합 스크립트. **3단계에서 확인한 실제 그리드 크기와 배경색을 반영하여 설정값을 조정한다.**

```python
python -c "
from PIL import Image
import os, shutil

# ── 설정 (3단계 확인 결과에 맞게 수정) ───────────
INPUT = '<페르소나경로>/images/<카테고리>-sprite.png'
OUTPUT = '<페르소나경로>/images/icons/<카테고리>'
COLS = 4        # 실제 열 수 (이미지 확인 후 조정!)
ROWS = 4        # 실제 행 수 (이미지 확인 후 조정!)
ICON_SIZE = 64  # 출력 아이콘 크기 (px)
BG = 'black'    # 배경색: 'black' 또는 'white' (이미지 확인 후 조정!)
NAMES = [
    'name-1', 'name-2', 'name-3', 'name-4',
    # ... 좌→우, 위→아래 순서로 아이콘 이름 나열
]
# ── 설정 끝 ──────────────────────────────────────

if os.path.exists(OUTPUT):
    shutil.rmtree(OUTPUT)
os.makedirs(OUTPUT, exist_ok=True)

img = Image.open(INPUT)
w, h = img.size
cell_w = w // COLS
cell_h = h // ROWS

BG_THRESHOLD = 20 if BG == 'black' else 230
count = 0

for row in range(ROWS):
    for col in range(COLS):
        idx = row * COLS + col
        if idx >= len(NAMES):
            break

        x1 = col * cell_w
        y1 = row * cell_h
        cell = img.crop((x1, y1, x1 + cell_w, y1 + cell_h))
        if cell.mode != 'RGBA':
            cell = cell.convert('RGBA')

        # 컨텐츠 영역 감지 (배경이 아닌 픽셀의 바운딩박스)
        pixels = cell.load()
        min_x, min_y = cell.size[0], cell.size[1]
        max_x, max_y = 0, 0
        for py in range(cell.size[1]):
            for px in range(cell.size[0]):
                r, g, b, a = pixels[px, py]
                if BG == 'black':
                    is_bg = r < BG_THRESHOLD and g < BG_THRESHOLD and b < BG_THRESHOLD
                else:
                    is_bg = r > BG_THRESHOLD and g > BG_THRESHOLD and b > BG_THRESHOLD
                if not is_bg:
                    min_x = min(min_x, px)
                    min_y = min(min_y, py)
                    max_x = max(max_x, px)
                    max_y = max(max_y, py)

        if max_x <= min_x or max_y <= min_y:
            continue

        # 패딩 + 크롭
        pad = 4
        min_x = max(0, min_x - pad)
        min_y = max(0, min_y - pad)
        max_x = min(cell.size[0], max_x + pad)
        max_y = min(cell.size[1], max_y + pad)
        cropped = cell.crop((min_x, min_y, max_x, max_y))

        # 정규화: ICON_SIZE x ICON_SIZE 투명 캔버스
        inner = ICON_SIZE - 4
        cw, ch = cropped.size
        scale = min(inner / cw, inner / ch)
        new_w = int(cw * scale)
        new_h = int(ch * scale)
        cropped = cropped.resize((new_w, new_h), Image.LANCZOS)

        icon = Image.new('RGBA', (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))
        icon.paste(cropped, ((ICON_SIZE - new_w) // 2, (ICON_SIZE - new_h) // 2))

        # 배경 제거 (슬라이스와 동시 처리)
        px2 = icon.load()
        for py in range(ICON_SIZE):
            for ppx in range(ICON_SIZE):
                r, g, b, a = px2[ppx, py]
                if BG == 'black' and r < BG_THRESHOLD and g < BG_THRESHOLD and b < BG_THRESHOLD:
                    px2[ppx, py] = (0, 0, 0, 0)
                elif BG == 'white' and r > BG_THRESHOLD and g > BG_THRESHOLD and b > BG_THRESHOLD:
                    px2[ppx, py] = (0, 0, 0, 0)

        icon.save(os.path.join(OUTPUT, NAMES[idx] + '.png'))
        count += 1

print('Sliced', count, 'icons to', OUTPUT)
"
```

### 설정값 가이드

| 항목 | 설명 | 기본값 |
|------|------|--------|
| `COLS` | 열 수. **이미지를 직접 보고 세라** | 4 |
| `ROWS` | 행 수. **이미지를 직접 보고 세라** | 4 |
| `BG` | 배경색. `'black'` 또는 `'white'`. **이미지를 직접 보고 판단** | `'black'` |
| `ICON_SIZE` | 출력 아이콘 크기 (px). 게임 UI용 64, 작은 뱃지용 48, 큰 일러스트용 128 | 64 |
| `NAMES` | 아이콘 파일명 리스트. 좌→우, 위→아래 순서. 영문 kebab-case | - |

### 텍스처 슬라이스 (배경 제거 없이 큰 타일로)

배경 텍스처 등 아이콘이 아닌 타일 리소스는 배경 제거 없이 크게 잘라야 한다:

```python
python -c "
from PIL import Image
import os

INPUT = '<경로>/texture-sprite.png'
OUTPUT = '<경로>/icons/textures'
COLS = 2
ROWS = 2
NAMES = ['parchment', 'leather', 'stone', 'wood']

os.makedirs(OUTPUT, exist_ok=True)
img = Image.open(INPUT)
w, h = img.size
cell_w = w // COLS
cell_h = h // ROWS

for row in range(ROWS):
    for col in range(COLS):
        idx = row * COLS + col
        if idx >= len(NAMES):
            break
        cell = img.crop((col * cell_w, row * cell_h, (col+1) * cell_w, (row+1) * cell_h))
        cell.save(os.path.join(OUTPUT, NAMES[idx] + '.png'))

print('Sliced', min(len(NAMES), COLS * ROWS), 'textures')
"
```

## 5단계: 결과 검증

생성된 아이콘을 직접 확인한다:

```bash
ls -la <OUTPUT 경로>/
```

빌더 채팅에서 인라인 확인:
```
$IMAGE:images/icons/<카테고리>/<이름>.png$
```

**잘린 아이콘이 있으면 3단계로 돌아가 그리드 크기를 재확인한다.**

## 주의사항

- **Gemini는 유료 API** — 1장 = 1회 호출. 불필요한 재생성을 피하라
- **그리드 크기를 추측하지 마라** — 반드시 이미지를 직접 열어 행×열을 세라. Gemini는 요청과 다른 그리드를 생성하는 경우가 많다
- **배경색을 추측하지 마라** — 검정을 요청해도 흰색으로 나올 수 있다. 이미지를 보고 `BG` 값을 설정하라
- **최대 요청 그리드** — 4×4 (16개) 권장. Gemini가 더 많이 생성할 수 있지만 그건 보너스
- **파일명** — 영문 kebab-case (예: `iron-sword.png`, `leather-armor.png`)
- **console 출력 주의** — Python에서 한글 이모지를 print하면 Windows cp949 인코딩 에러 발생. print에 ASCII만 사용

## 패널에서 아이콘 사용

```html
<img src="{{sessionImageBase}}/icons/weapons/iron-sword.png" width="32" height="32">
```

```html
<div style="background-image: url('{{sessionImageBase}}/icons/weapons/iron-sword.png');
            background-size: contain; width: 32px; height: 32px;"></div>
```
