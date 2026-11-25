---
name: line-locator
description: >
  Định vị dòng trước khi đọc file hoặc tìm file trong cây thư mục — tránh đọc mù, tiết kiệm token. Dùng khi cần tìm hàm, class, symbol, hoặc bất kỳ pattern nào trong source code trước khi gọi view_range. Hai công cụ: findtree.py (tìm file nào có chứa pattern) và findtool.py (tìm dòng nào trong một file).
author: Kluco
github: unkluco
email: huylet334@gmail.com
version: 1.1.1
---

# Line-Locator

Hai script phối hợp để định vị chính xác trước khi đọc:

| Script | Phạm vi | Câu hỏi trả lời |
|---|---|---|
| `findtree.py` | Cả cây thư mục | *File nào* chứa pattern này? |
| `findtool.py` | Một file duy nhất | *Dòng nào* trong file này? |

**Workflow:**
```
findtree.py (shortlist files) → findtool.py (locate lines) → view_range (read)
```

Script nằm tại: `skills/line-locator/scripts/`

---

## Output contract

**Tất cả pattern dùng Python regex.**

**findtool — success (stdout):**
```json
{"matches": {"processOrder": [247, 312]}}
{"line": 248}
{"matched": true}
```

**findtree — success (stdout):**
```json
{"matched_files": ["src/order.js", "tests/order.test.js"]}
```

**Failure — cả hai tool (stderr, exit 1):**
```json
{"ok": false, "error": "No line matching pattern 'foo' was found after line 0."}
```

**Parse nhanh:**
```python
import json, subprocess
out = subprocess.check_output([...])
data = json.loads(out)

# findtool
lines   = data["matches"]["pat"]   # -mr  → list[int]
line    = data["line"]             # -n / -b / -c / -o → int
matched = data["matched"]          # -e   → bool

# findtree
files   = data["matched_files"]    # list[str] relative paths
```

---

## findtree — tìm file

```bash
python findtree.py --root ROOT --pattern PAT [options]
```

| Option | Mặc định | Mô tả |
|---|---|---|
| `--root` | *(required)* | Thư mục gốc |
| `--pattern` | *(required)* | Regex pattern |
| `--include GLOB...` | *(tất cả)* | Chỉ tìm file khớp glob |
| `--exclude GLOB...` | *(không)* | Bỏ qua file/thư mục khớp glob |
| `--ignore-case` | off | Case-insensitive |
| `--max-results N` | *(không giới hạn)* | Dừng sau N file |
| `--show` | `matched` | `matched` / `errors` / `both` / `summary` / `all` |
| `--max-file-size` | *(không)* | Bỏ qua file lớn hơn (VD: `64K`, `10M`) |
| `--no-default-dir-excludes` | off | Tắt auto-skip `.git`, `node_modules`, v.v. |
| `--text` | off | Output text thay vì JSON |

**Auto-excluded dirs:** `.git`, `.hg`, `node_modules`, `venv`, `.venv`, `__pycache__`, `dist`, `build`, `target`, `.mypy_cache`, `.pytest_cache`, `.tox`, `coverage`

```bash
python findtree.py --root ./src --pattern "processOrder"
python findtree.py --root ./src --pattern "class\s+\w+Service"
python findtree.py --root . --pattern "TODO" --include "*.ts" "*.js" --exclude "dist/**"
python findtree.py --root . --pattern "deprecated_api" --max-results 1
```

---

## findtool — tìm dòng

```bash
python findtool.py --file FILE [--ignore-case] [-s] FLAG... [--text]
```

| Flag | Args | Mô tả | `result` key |
|---|---|---|---|
| `-mr` | `PAT [PAT ...]` | Tất cả dòng khớp một hoặc nhiều pattern | `{"matches": {"pat": [1,5]}}` |
| `-n` | `PAT LINE` | Dòng đầu tiên khớp **sau** LINE (0 = từ đầu file) | `{"line": 45}` |
| `-b` | `PAT LINE` | Dòng cuối cùng khớp **trước** LINE (999999 = cuối file) | `{"line": 12}` |
| `-e` | `PAT` | File có chứa pattern không? | `{"matched": true}` |
| `-c` | `OPEN CLOSE LINE N` | Dòng đóng khớp với OPEN thứ N trên LINE (scan xuôi) | `{"line": 89}` |
| `-o` | `OPEN CLOSE LINE N` | Dòng mở khớp với CLOSE thứ N trên LINE (scan ngược) | `{"line": 34}` |

Flag `-s` (chỉ dùng với `-c`/`-o`): bỏ qua nội dung string và comment khi đếm depth.

```bash
python findtool.py --file app.js -mr "processOrder"
python findtool.py --file app.js -mr "processOrder" "cancelOrder" "getUser"
python findtool.py --file app.js -n "function\s+\w+" 0
python findtool.py --file app.js -b "^import\s" 999999
python findtool.py --file app.js -e "TODO"
python findtool.py --file app.js -c "\{" "\}" 248 1
python findtool.py --file app.js -c "\{" "\}" 248 1 -s
python findtool.py --file app.js -o "\{" "\}" 298 1
```

---

## Pair matching (-c / -o)

Cả hai flag đều nhận `OPEN CLOSE LINE N` theo cùng thứ tự:

```
-c  OPEN  CLOSE  LINE  N  →  anchor tại OPEN thứ N trên LINE, scan xuôi  → trả về dòng CLOSE
-o  OPEN  CLOSE  LINE  N  →  anchor tại CLOSE thứ N trên LINE, scan ngược → trả về dòng OPEN
```

**Algorithm:** depth-tracking. Mỗi dòng tiếp theo: `depth += count(OPEN) - count(CLOSE)`. Khi `depth == 0` → trả về dòng đó.

**Flag `-s`:** trước khi đếm, mask toàn bộ string literals và comments (`//`, `#`, `/* */`, `'...'`, `"..."`, backtick, triple-quote). Dùng khi file có nhiều delimiter trong string/comment.

### Pairs phổ biến theo ngôn ngữ

| Ngôn ngữ | Block mở | Block đóng | Ghi chú |
|---|---|---|---|
| JS/TS/Java/Go/Rust/C/C++/C# | `\{` | `\}` | Dùng `-s` nếu file có `{` trong string |
| Bất kỳ — argument list | `\(` | `\)` | Áp dụng mọi ngôn ngữ |
| Bất kỳ — array/list | `\[` | `\]` | Áp dụng mọi ngôn ngữ |
| HTML/XML | `<div\b[^>]*>` | `</div>` | Thay `div` bằng tên tag |
| Ruby | `\bdo\b` | `\bend\b` | Hoặc `\bdef\b` / `\bend\b` |
| Lua / Pascal-like | `\bdo\b` | `\bend\b` | |
| Shell (bash) | `\bthen\b\|\bdo\b` | `\bfi\b\|\bdone\b` | Phức tạp hơn |
| Python | *(không có bracket)* | *(xem note bên dưới)* | Dùng `-n` tìm def tiếp theo |

> **Python note:** Python dùng indentation thay vì `{}`. Để tìm cuối hàm, dùng `-n "^(def\|class)\s" FUNC_LINE` tìm `def`/`class` tiếp theo cùng cấp, hoặc đọc từ `FUNC_LINE` đến dòng trước đó. Với argument list nhiều dòng: `-c "\(" "\)" FUNC_LINE 1` vẫn hoạt động.

```bash
# JS/TS function
python findtool.py --file service.ts -c "\{" "\}" 248 1 -s
# → {"line": 298}

# HTML div
python findtool.py --file index.html -c "<div\b[^>]*>" "</div>" 10 1
# → {"line": 25}

# Ruby method
python findtool.py --file user.rb -c "\bdef\b" "\bend\b" 42 1
# → {"line": 67}

# Argument list dài nhiều dòng (mọi ngôn ngữ)
python findtool.py --file builder.java -c "\(" "\)" 120 1
# → {"line": 128}

# -o: đang ở dòng }, tìm dòng {
python findtool.py --file app.go -o "\{" "\}" 298 1
# → {"line": 248}
```

---

## Workflows

### 1. Đọc một hàm đã biết tên

```bash
# Bước 1: Tìm dòng định nghĩa
python findtool.py --file app.js -mr "processOrder"
# → {"matches": {"processOrder": [247, 312]}}  → 247 là định nghĩa

# Bước 2: Tìm dòng OPEN thực sự (KHÔNG đoán cùng dòng hay dòng dưới)
python findtool.py --file app.js -n "\{" 247
# → {"line": 248}

# Bước 3: Tìm dòng đóng
python findtool.py --file app.js -c "\{" "\}" 248 1
# → {"line": 298}

# Bước 4: Đọc
view_range [247, 298]
```

### 2. Từ repository lạ → đọc hàm

```bash
python findtree.py --root ./src --pattern "processOrder"
# → {"matched_files": ["services/order.js"]}

python findtool.py --file services/order.js -mr "processOrder"
# → tiếp tục Workflow 1
```

### 3. Scan cấu trúc tổng thể file

```bash
# JS/TS/Java/Go/C#
python findtool.py --file service.ts -mr "class\s+\w+" "function\s+\w+" "\bexport\b"

# Python
python findtool.py --file service.py -mr "^class\s+\w+" "^def\s+\w+" "^    def\s+\w+"

# Ruby
python findtool.py --file user.rb -mr "^\s*def\s+\w+" "^\s*class\s+\w+"

# Java/C#
python findtool.py --file Service.java -mr "public\s+\w" "private\s+\w" "protected\s+\w"
```

### 4. Tìm nhiều symbol cùng lúc

```bash
python findtool.py --file app.js -mr "processOrder" "cancelOrder" "getUser"
# → {"matches": {"processOrder": [247], "cancelOrder": [312], "getUser": [89]}}
# Lên kế hoạch đọc toàn bộ từ một lần call
```

### 5. Đọc tất cả imports

```bash
# JS/TS
python findtool.py --file app.ts -mr "^import\s"
# → {"matches": {"^import\\s": [1,2,3,14,15]}} → view_range [1, 15]

# Python
python findtool.py --file app.py -mr "^import\s" "^from\s"

# Java/C#
python findtool.py --file App.java -mr "^import\s" "^using\s"

# Go
python findtool.py --file main.go -mr "^\s*\"" 
# (lines inside import block — hoặc tìm block import trước)
```

### 6. Xác định dòng đang thuộc scope nào (ngôn ngữ có `{}`)

```bash
python findtool.py --file dao.js -b "\{" X    # → OPEN_LINE
python findtool.py --file dao.js -c "\{" "\}" OPEN_LINE 1  # verify X trong scope này
view_range [OPEN_LINE - 1, OPEN_LINE]         # đọc tên scope
```

### 7. Leo scope chain

```bash
python findtool.py --file app.js -b "\{" 245  →  198
python findtool.py --file app.js -b "\{" 198  →  134
python findtool.py --file app.js -b "\{" 134  →  12
python findtool.py --file app.js -b "\{" 12   →  error → top-level
```

### 8. Tìm decorator / annotation

```bash
# Python decorator
python findtool.py --file routes.py -b "@\w+" FUNC_LINE
# → nếu kết quả >= FUNC_LINE - 3 → có decorator trực tiếp

# Java/C# annotation
python findtool.py --file Controller.java -b "@\w+" FUNC_LINE

# JS/TS decorator
python findtool.py --file service.ts -b "@\w+" FUNC_LINE
```

### 9. Tìm else / catch / finally

```bash
python findtool.py --file handler.js -c "\{" "\}" IF_LINE 1  # → close of if-block
python findtool.py --file handler.js -n "else|catch|finally" CLOSE_LINE
# → nếu ngay sau CLOSE_LINE → đây là else/catch của block đó
```

---

## ⚠️ Sai lầm phổ biến

### 1. Gọi `-c` trên dòng function name thay vì dòng `{`

```bash
# ❌ SAI — dòng 247 có tên hàm nhưng chưa chắc có {
python findtool.py --file app.js -c "\{" "\}" 247 1
# → error: "Line 247 contains only 0 occurrence(s) of open pattern '\{'"

# ✅ ĐÚNG — tìm dòng { trước, rồi mới -c
python findtool.py --file app.js -n "\{" 247   # → {"line": 248}
python findtool.py --file app.js -c "\{" "\}" 248 1
```

Lý do: Trong nhiều ngôn ngữ, `{` có thể ở dòng tiếp theo sau tên hàm (Allman style). **Không bao giờ đoán.**

---

### 2. Nhầm lẫn kết quả đầu tiên của `-mr` là định nghĩa

```bash
python findtool.py --file app.js -mr "processOrder"
# → {"matches": {"processOrder": [89, 247, 312]}}
#   89  = call site hoặc comment
#   247 = định nghĩa hàm (def/function)
#   312 = call site khác
```

Số nhỏ nhất chưa chắc là định nghĩa. Đọc thêm vài dòng context để xác nhận, hoặc dùng pattern cụ thể hơn:

```bash
python findtool.py --file app.js -mr "function processOrder" "processOrder\s*\("
# → pattern cụ thể hơn → ít kết quả giả hơn
```

---

### 3. Pattern có ký tự đặc biệt không escape

```bash
# ❌ SAI — regex error vì ( không được escape
python findtool.py --file app.py -mr "foo(bar)"
# → {"ok": false, "error": "Invalid regex pattern 'foo(bar)': missing ), ..."}

# ✅ ĐÚNG
python findtool.py --file app.py -mr "foo\(bar\)"
# hoặc dùng word boundary thay vì match toàn bộ call:
python findtool.py --file app.py -mr "foo"
```

Ký tự cần escape trong regex: `. ^ $ * + ? { } [ ] \ | ( )`

---

### 4. Dùng Python `{}` để match scope hàm

Python không dùng `{}` cho function/class body. Dùng `-c "\{" "\}"` sẽ chỉ match dict/set literals.

```bash
# ❌ Không có tác dụng cho Python function body
python findtool.py --file service.py -c "\{" "\}" 42 1

# ✅ Python: tìm def/class tiếp theo cùng level
python findtool.py --file service.py -n "^def \|^class " 42
# → dòng tiếp theo ở cùng indent level = kết thúc hàm hiện tại

# ✅ Python method trong class:
python findtool.py --file service.py -n "^    def " 42
```

---

### 5. Quên rằng `-n` là **sau** LINE, không phải **tại** LINE

```bash
python findtool.py --file app.js -n "def " 247
# → Tìm match STRICTLY AFTER dòng 247, không phải tại 247
# Nếu def ở dòng 247 → sẽ không được trả về

# Để bao gồm chính dòng đó:
python findtool.py --file app.js -n "def " 246  # tìm sau dòng 246
```

---

### 6. Bỏ qua `-s` khi file có nhiều `{` trong string/comment

```bash
# File có: const tmpl = `SELECT * FROM t WHERE col = '{value}'`
# ❌ Không -s: depth tracking đếm sai vì { trong template string
python findtool.py --file query.ts -c "\{" "\}" 50 1
# → kết quả sai

# ✅ Dùng -s để bỏ qua string/comment
python findtool.py --file query.ts -c "\{" "\}" 50 1 -s
```

Nên dùng `-s` khi: file là template (`.html`, `.ejs`, `.hbs`), SQL inline, hoặc bất kỳ file nào có nhiều `{` không phải code.

---

### 7. Dùng findtool trực tiếp mà không biết file ở đâu

```bash
# ❌ Tốn thời gian — không biết file nào
python findtool.py --file src/auth/service.js -mr "validateToken"
# → File not found

# ✅ findtree trước
python findtree.py --root ./src --pattern "validateToken"
# → {"matched_files": ["src/auth/service.js"]}
```

---

### 8. Không biết ngôn ngữ dùng `{` hay không → kiểm tra trước

Trước khi dùng `-c "\{" "\}"`, xác nhận file có `{` không:
```bash
python findtool.py --file service.py -e "\{"
# → {"matched": false} → Python file, không có {-based scope
# → {"matched": true}  → file có {, tiến hành bình thường
```

### 9. Dùng `\|` thay vì `|` cho alternation trong Python regex

```bash
# ❌ SAI — \| trong Python regex là ký tự pipe literal, không phải alternation
python findtool.py --file app.java -mr "focusLost\|hidePopup\|showPopup"
# → {"matches": {"focusLost\\|hidePopup\\|showPopup": []}}  ← tìm chuỗi literal   "focusLost|hidePopup|showPopup"

# ✅ ĐÚNG — | không cần escape trong Python regex
python findtool.py --file app.java -mr "focusLost|hidePopup|showPopup"
# → {"matches": {"focusLost|hidePopup|showPopup": [192, 723, 701]}}

Lý do nhầm: grep basic mode (BRE) dùng \| cho alternation. Python dùng ERE-style — | đã là   alternation, \| là literal pipe.

Khi nào \| hợp lệ: không bao giờ trong Python regex nếu mục đích là alternation.
```

---

## Bảng quyết định nhanh

| Tình huống | Dùng gì |
|---|---|
| Chưa biết file nào | `findtree --root ... --pattern ...` |
| Biết tên hàm, muốn đọc body (ngôn ngữ có `{}`) | `-mr "name"` → `-n "\{" LINE` → `-c "\{" "\}" OPEN 1` |
| Ngôn ngữ không có `{}` (Python...) | `-mr "name"` → `-n "^def\|^class" LINE` |
| Nhiều hàm cùng lúc | `-mr "fn1" "fn2" "fn3"` |
| Pattern có ký tự đặc biệt | escape: `\(`, `\)`, `\{`, `\.`, v.v. |
| File có nhiều `{` trong string | thêm `-s` vào `-c`/`-o` |
| Duyệt từng hàm không biết tên | `-mr "\{"` → `-c "\{" "\}"` → `-n "\{"` → lặp |
| Ở dòng X, muốn biết thuộc hàm nào | `-b "\{" X` → `-c "\{" "\}" OPEN 1` verify |
| Đọc hết imports | `-mr "^import\s"` → min/max → `view_range` |
| Argument list nhiều dòng | `-c "\(" "\)" LINE 1` |
| Tìm else/catch/finally | `-c "\{" "\}" IF_LINE 1` → `-n "else\|catch\|finally"` |
| Có decorator/annotation không? | `-b "@\w+" FUNC_LINE` → check khoảng cách |
| HTML tag pair | `-c "<tag\b[^>]*>" "</tag>" LINE 1` |
| Ruby/Lua method body | `-c "\bdef\b" "\bend\b" LINE 1` |
| Scope ngoài cùng | `-b "\{"` lặp đến error |
| File có chứa pattern không? | `-e "pattern"` |
| Chỉ tìm trong file .ts .js | findtree `--include "*.ts" "*.js"` |
| Dừng sớm khi tìm đủ | findtree `--max-results 1` |

---

## Xử lý lỗi

| Lỗi | Nguyên nhân | Cách xử lý |
|---|---|---|
| `"For -n, LINE must be >= 0"` | Truyền số âm vào `-n` | Dùng 0 để tìm từ đầu file |
| `"For -b, LINE must be >= 1"` | Truyền 0 vào `-b` | Dùng 999999 để tìm từ cuối file |
| `"Line X contains only 0 occurrence(s) of open pattern"` | `{` không ở dòng đó | Dùng `-n "\{" FUNC_LINE` để tìm dòng `{` thực tế |
| `"No closing match for open pattern"` | Không tìm thấy CLOSE trong file | File chưa đóng bracket, hoặc dùng thêm `-s` |
| `"No line matching pattern ... was found"` | Pattern không khớp trong phạm vi | Kiểm tra lại regex; với `-b` có thể tăng LINE |
| `"Invalid regex pattern"` | Regex sai cú pháp | Escape: `\(`, `\)`, `\{`, `\.` |
| `"Root directory not found"` | `--root` không tồn tại | Kiểm tra lại đường dẫn |
| `"N must be >= 1"` | N = 0 trong `-c`/`-o` | N bắt đầu từ 1 |

---

## Ví dụ end-to-end

**Bài toán:** Đọc hàm `validateToken` trong codebase 50 file, không biết nó nằm ở đâu.

```bash
# 1. Tìm file
python findtree.py --root ./src --pattern "validateToken"
# → {"matched_files": ["auth/service.ts"]}

# 2. Tìm dòng định nghĩa
python findtool.py --file auth/service.ts -mr "validateToken"
# → {"matches": {"validateToken": [312, 467]}}  → 312 là định nghĩa

# 3. Kiểm tra decorator
python findtool.py --file auth/service.ts -b "@\w+" 312
# → {"line": 310}  → có decorator ở dòng 310

# 4. Tìm dòng {
python findtool.py --file auth/service.ts -n "\{" 312
# → {"line": 313}

# 5. Tìm dòng đóng (dùng -s vì file TS hay có template string)
python findtool.py --file auth/service.ts -c "\{" "\}" 313 1 -s
# → {"line": 389}

# 6. Đọc
view_range [310, 389]
```

**Token tiêu thụ:** ~80 dòng thay vì hàng nghìn. Tiết kiệm >90%.
