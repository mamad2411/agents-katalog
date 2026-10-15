---
name: local-code-interpreter
description: Execute Python code and shell commands locally on macOS/Linux. No API key, no cloud service — runs directly on your machine.
metadata: {"openclaw": {"os": ["darwin", "linux"], "emoji": "🐍", "user-invocable": true, "homepage": "https://github.com/Allen091080/local-code-interpreter"}}
---

# Local Code Interpreter

Run Python code and shell commands directly on your local machine. No cloud, no API keys, no cold starts — uses the Python already installed on your system.

## When to Use

Use this skill whenever you need to **actually execute code** to get a result:

| Task | Use This? |
|------|-----------|
| Data analysis with pandas/numpy | ✅ Yes |
| Generate charts and visualizations | ✅ Yes |
| Process files (CSV, Excel, JSON, PDF) | ✅ Yes |
| Machine learning with scikit-learn | ✅ Yes |
| Math / statistics calculations | ✅ Yes |
| Explaining code or algorithms | ❌ No — respond with text |
| Formatting code examples | ❌ No — use markdown code blocks |
| Simple mental math | ❌ No — just answer directly |

## How to Execute Code

### Single-line code

```bash
python3 {baseDir}/scripts/run.py --code "print('hello')"
```

### Multi-line code (recommended)

Write code to a temp file, then execute:

```bash
cat > /tmp/ci_script.py << 'PYEOF'
import pandas as pd
import numpy as np

data = {'month': ['Jan','Feb','Mar'], 'revenue': [12, 19, 15]}
df = pd.DataFrame(data)
print(df.describe())
PYEOF
python3 /tmp/ci_script.py
```

### Execute a file directly

```bash
python3 {baseDir}/scripts/run.py --file /path/to/script.py
```

### Shell commands

Use the built-in `execute_command` tool directly — no wrapper needed:

```bash
pip3 install pandas matplotlib
ls -la
```

## Rules

1. **Non-interactive matplotlib backend** — always add before pyplot import:
   ```python
   import matplotlib
   matplotlib.use('Agg')
   import matplotlib.pyplot as plt
   ```

2. **Chinese text in charts** — set font to avoid missing glyphs:
   ```python
   plt.rcParams['font.family'] = 'PingFang HK'   # macOS
   # plt.rcParams['font.family'] = 'WenQuanYi Zen Hei'  # Linux
   ```

3. **Use `print()` for output** — stdout is the only output channel.

4. **Save charts with `savefig()`**, never `plt.show()`:
   ```python
   plt.savefig('/tmp/output.png', dpi=150, bbox_inches='tight')
   ```

5. **Default output directory is `/tmp/`** — specify a different path explicitly if needed.

6. **Install missing packages first**:
   ```bash
   pip3 install <package>
   ```

## Pre-installed Libraries (common)

Install any missing ones with `pip3 install <name>`.

| Category | Libraries |
|----------|-----------|
| Data Analysis | `pandas`, `numpy` |
| Visualization | `matplotlib`, `plotly`, `seaborn` |
| Machine Learning | `scikit-learn`, `xgboost` |
| Excel / Office | `openpyxl`, `python-docx`, `python-pptx` |
| PDF | `PyPDF2`, `reportlab`, `pdfplumber` |
| Image | `Pillow`, `opencv-python` |
| HTTP / Scraping | `requests`, `httpx`, `beautifulsoup4` |
| Math | `scipy`, `sympy` |
| Utilities | `rich`, `pydantic`, `tqdm` |

## Example Workflows

### Data Analysis

```python
import pandas as pd
import numpy as np

df = pd.read_csv('/path/to/data.csv')
print("Shape:", df.shape)
print("\nMissing values:")
print(df.isnull().sum())
print("\nStatistics:")
print(df.describe())
```

### Visualization (Chinese labels)

```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'PingFang HK'

months = ['1月', '2月', '3月', '4月', '5月', '6月']
values = [12, 19, 15, 25, 22, 30]

plt.figure(figsize=(8, 4))
plt.plot(months, values, 'o-', color='#2196F3', linewidth=2)
plt.title('上半年营收趋势（万元）')
plt.xlabel('月份')
plt.ylabel('营收（万元）')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/tmp/chart.png', dpi=150, bbox_inches='tight')
print('Chart saved to /tmp/chart.png')
```

### Install and Use New Package

```bash
pip3 install yfinance
```

```python
import yfinance as yf
ticker = yf.Ticker("AAPL")
info = ticker.info
print(f"Apple stock price: ${info.get('currentPrice', 'N/A')}")
```

## Environment

- **Python**: 3.13 (macOS) or system Python 3.x (Linux)
- **Shell**: zsh (macOS) / bash (Linux)
- **Execution**: local process, full filesystem access
- **Networking**: full internet access via `requests`, `curl`, etc.
- **Session state**: variables do NOT persist between separate calls — use files to pass data across steps
