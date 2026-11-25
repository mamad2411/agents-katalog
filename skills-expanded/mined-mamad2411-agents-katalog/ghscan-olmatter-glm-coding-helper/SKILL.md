---
name: glm-coding-helper-install
description: Install, configure, verify, explain, and repair the 智谱 GLM Coding Plan 抢购助手 / GLM Coding Rush helper project for non-technical Windows users. Use when a user wants an AI agent to set up the local CPU/GPU OCR backend, Tampermonkey/油猴 userscript, GLM Coding Plan 抢购 flow, one-click purchase helper, Chinese captcha OCR auto-click service, GreasyFork/GitHub release copy, or troubleshoot backend/browser/OCR/payment-popup issues in this repository.
---

# GLM Coding Plan Rush Helper Install And Repair Skill

This skill helps an AI agent install and repair the 智谱 GLM Coding Plan 抢购助手 / GLM Coding Rush project end to end.
The target user may not know Python, PowerShell, Git, virtual environments, browser extension
permissions, or OCR backends. Act as the user's local setup engineer.

The project is a Tampermonkey userscript plus a local OCR backend:

- Frontend userscript: `glm-coding-helper.user.js` at the repository root.
- Compatibility userscript copy: `scripts/userscripts/glm-coding-helper.user.js`.
- Backend startup wrapper: `scripts/start_backend.ps1`.
- First-time Windows bootstrap: `scripts/bootstrap_windows.ps1`.
- Backend setup wrapper: `scripts/setup_backend.ps1`.
- Backend config reference: `docs/backend_config.md`.
- Detector weights: `models/weights/yolo-captcha-detector.pt`.
- Default backend URL: `http://127.0.0.1:8888`.

Never expose or print the full built-in invite code. If checking for sensitive data, say that the
full code was or was not found, but do not repeat it.

## Operating Principles

1. Prefer the repository scripts over manual package installation.
2. Keep the user on Windows PowerShell unless they clearly use another OS.
3. Verify every major step with a command or browser check.
4. If a command fails, read the error and repair the specific cause instead of restarting blindly.
5. Do not upload captcha screenshots to third-party OCR services. This project is designed for local OCR.
6. Keep root `glm-coding-helper.user.js` and `scripts/userscripts/glm-coding-helper.user.js` synchronized if either one is edited.
7. Default to safe payment behavior: invalid payment/rate-limit popups must not auto-close unless the user manually enables that setting.

## Quick Install Workflow

Use this workflow for a normal new Windows user.

### 1. Locate The Repository

Ask the user where the repository was downloaded or cloned. If you are already inside the repo,
verify these files exist:

```powershell
Test-Path .\glm-coding-helper.user.js
Test-Path .\scripts\bootstrap_windows.ps1
Test-Path .\scripts\start_backend.ps1
Test-Path .\models\weights\yolo-captcha-detector.pt
```

If any required file is missing, tell the user to download the full repository, not just the
userscript file.

### 2. Install The Backend

If the user may not have Python installed, run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\bootstrap_windows.ps1 -Target auto
```

If Python is already installed, run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup_backend.ps1 -Target auto
```

Useful explicit modes:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup_backend.ps1 -Target cpu
powershell -ExecutionPolicy Bypass -File scripts\setup_backend.ps1 -Target gpu
powershell -ExecutionPolicy Bypass -File scripts\setup_backend.ps1 -Target both
```

Expected environments:

- `.venv_paddle` for CPU inference.
- `.venv_paddle_gpu` for GPU inference.

### 3. Start The Backend

Start with auto mode:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\start_backend.ps1 -Mode auto
```

Force GPU:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\start_backend.ps1 -Mode gpu
```

Force CPU:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\start_backend.ps1 -Mode cpu
```

Force CPU with a worker count:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\start_backend.ps1 -Mode cpu -CpuWorkers 3
```

If the user wants a visible backend window, use the normal wrapper above. If they want terminal-only
operation, use the Python headless entry described in `docs/backend_config.md`.

### 4. Verify The Backend

Run:

```powershell
Invoke-RestMethod http://127.0.0.1:8888/health
```

The response should include fields like:

- `backend.ocr_mode`
- `backend.cpu_workers`
- `backend.gpu_available`
- selected YOLO/OCR settings

If `/health` fails, the userscript cannot solve captchas. Fix the backend first.

### 5. Install The Userscript

Tell the user to install Tampermonkey, then:

1. Open root `glm-coding-helper.user.js`.
2. Copy all content.
3. Create a new Tampermonkey script.
4. Paste and save.
5. Open the GLM Coding Plan page.

For Chrome extension permissions, guide the user to:

1. Open `chrome://extensions/`.
2. Enable Developer mode in the top right.
3. Open Tampermonkey details.
4. Enable "Allow user scripts".
5. Enable "Allow in Incognito" if they use incognito windows.
6. Enable "Allow access to file URLs" if they install from a local file.

### 6. Confirm Browser To Backend Connectivity

The userscript sends captcha requests to:

```text
http://127.0.0.1:8888
```

If the browser shows network errors, confirm:

- backend is running,
- `/health` works,
- local firewall did not block Python,
- the userscript is enabled on the GLM page,
- the page URL matches the script includes for `bigmodel.cn`.

## Recommended User Operation During GLM Rush

Use the user's own procedure when explaining the workflow:

1. Install Tampermonkey, configure the userscript, and enable required Chrome extension permissions.
2. Install the backend from GitHub manually or ask an AI assistant to follow this skill.
3. Open the rush page and test that everything works before the real rush window.
4. Enter the rush page before 9:30 every day. It may be hard to open later.
5. Prepare mobile Alipay payment in advance. A payment page with an amount can still fail if payment is too late.
6. Open several windows. Near 10:00, solve/click captchas but do not confirm too early; start confirming at 10:00.
7. If the first wave fails, keep one window and let local OCR identify and click.
8. The script defaults to not closing payment pages automatically.
9. If a payment page has no amount, it usually means that attempt did not get stock; close it and continue.

Shortcut keys:

- `Esc`: close a busy/payment popup.
- `Enter` or `Space`: click the captcha confirm button.

## How It Works

The userscript modifies and automates the GLM Coding Plan page:

1. It makes package buttons clickable earlier when the page marks them disabled.
2. It scans package/month choices in the configured priority order.
3. It opens or watches purchase/captcha dialogs.
4. When a Chinese click captcha appears, it sends the prompt text to the local backend.
5. The backend captures/crops the captcha from the local browser window.
6. YOLO detects the candidate character boxes.
7. OCR recognizes the detected boxes using CPU or GPU PaddleOCR workers.
8. Prompt-constrained matching maps the requested characters to detected boxes.
9. The backend returns click positions.
10. The userscript clicks the requested boxes and can press confirm with a shortcut.

GPU mode is usually faster. CPU mode uses a parallel worker pool and should still be usable on
ordinary machines. The backend auto mode tries GPU first when available, then falls back to CPU.

Payment safety:

- Real payment pages should stay open.
- Invalid payment or rate-limit popups are not auto-closed by default.
- Auto-close behavior exists only after the user manually enables it in the config panel.

## Backend Configuration

Prefer command-line flags first:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\start_backend.ps1 -Mode auto
powershell -ExecutionPolicy Bypass -File scripts\start_backend.ps1 -Mode gpu
powershell -ExecutionPolicy Bypass -File scripts\start_backend.ps1 -Mode cpu -CpuWorkers 3
```

Use environment variables only for advanced repair:

```powershell
$env:CNCAPTCHA_PORT='8888'
$env:CNCAPTCHA_OCR_MODE='cpu'
$env:CNCAPTCHA_CPU_OCR_WORKERS='3'
$env:CNCAPTCHA_YOLO_DEVICE='cpu'
$env:CNCAPTCHA_SKIP_GPU_DETECT='1'
```

Common detector override:

```powershell
$env:CNCAPTCHA_DETECTOR_PATH='D:\path\to\yolo-captcha-detector.pt'
```

## QA And Troubleshooting

### Q: The user has no Python.

Run the bootstrap script:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\bootstrap_windows.ps1 -Target auto
```

It should find Python 3.12, install through `winget` if possible, or download the official Python
installer. If corporate policy blocks installers, ask the user to install Python 3.12 manually,
then run `scripts\setup_backend.ps1`.

### Q: PowerShell says script execution is disabled.

Use the per-command bypass form:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup_backend.ps1 -Target auto
```

Do not ask the user to permanently weaken system policy unless necessary.

### Q: `winget` is missing.

The bootstrap script should fall back to official Python download. If that fails, send the user to
install Python 3.12 from python.org, then run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup_backend.ps1 -Target auto
```

### Q: GPU mode fails.

Check:

```powershell
nvidia-smi
powershell -ExecutionPolicy Bypass -File scripts\start_backend.ps1 -Mode auto
```

If `nvidia-smi` is missing or Paddle cannot see CUDA, use CPU:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\start_backend.ps1 -Mode cpu
```

Explain that users do not need GPU for correctness; GPU mainly reduces latency.

### Q: CPU is slow.

Try worker tuning:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\start_backend.ps1 -Mode cpu -CpuWorkers 2
powershell -ExecutionPolicy Bypass -File scripts\start_backend.ps1 -Mode cpu -CpuWorkers 3
```

More workers are not always faster. On low-core machines, too many workers can slow down OCR.

### Q: `/health` does not respond.

Check whether the server process is running and whether port 8888 is occupied:

```powershell
netstat -ano | findstr :8888
```

If occupied by an old process, close the old backend window or kill the specific PID only after
confirming it belongs to the old backend. Alternatively use another port:

```powershell
$env:CNCAPTCHA_PORT='8890'
powershell -ExecutionPolicy Bypass -File scripts\start_backend.ps1 -Mode auto
```

If changing the port, the userscript must also be updated to call that port.

### Q: Tampermonkey script does not run.

Check:

- script is enabled,
- the page is under `bigmodel.cn`,
- Chrome Developer mode is enabled,
- Tampermonkey permissions are enabled,
- the script was saved after paste,
- browser console has no syntax error.

If the user installed from GitHub, tell them to use root `glm-coding-helper.user.js`, not only a
partial snippet.

### Q: Captcha appears but no automatic click happens.

Check in order:

1. Backend `/health` works.
2. Backend window logs receive a `/captcha` request.
3. Browser console does not show connection refused.
4. The GLM page is visible and not minimized.
5. Windows scaling or multi-monitor layout did not move the screenshot area unexpectedly.
6. The captcha prompt text contains Chinese characters.
7. Detector weight exists at `models/weights/yolo-captcha-detector.pt`.

If logs say the popup was not found or was closed, ask the user to keep the captcha popup visible
and retry.

### Q: OCR returns wrong positions.

Collect one failing screenshot if the user agrees. Do not send it to third-party OCR. Inspect:

- detected boxes count,
- OCR text for each box,
- whether prompt characters are visually similar,
- whether the browser zoom/scaling is unusual,
- whether the captcha is partially covered.

Then retry CPU/GPU mode. If one mode is consistently better, force that mode.

### Q: Error says OCR result cannot map prompt to boxes.

This means detection or recognition produced boxes/text that cannot match the prompt. Fix by:

1. ensuring the popup is fully visible,
2. retrying once,
3. switching OCR mode,
4. reducing visual obstruction,
5. checking whether the prompt text was read correctly.

### Q: Payment page still auto-closes.

Verify the userscript version is current and contains the safe default migration:

- root `glm-coding-helper.user.js` should be installed,
- `AUTO_CLOSE_INVALID` should default to `false`,
- config panel should not have auto-close enabled,
- Tampermonkey may still run an older saved script, so reinstall from root file if needed.

The intended default is: payment/rate-limit popups stay open unless the user manually enables
auto-close.

### Q: User sees a payment page with no amount.

Explain that a no-amount payment page usually means the attempt did not really get stock. The user
can close it and continue. If they want speed, `Esc` closes the popup.

### Q: User sees a payment page with an amount.

Tell the user not to close it automatically. They should confirm the amount and pay manually.

### Q: GitHub users cannot find the script.

Point them to the repository root:

```text
glm-coding-helper.user.js
```

The nested `scripts/userscripts/` copy is for development and old-path compatibility.

### Q: Root and nested userscripts differ.

Synchronize them before release. On Windows:

```powershell
Copy-Item -LiteralPath .\glm-coding-helper.user.js -Destination .\scripts\userscripts\glm-coding-helper.user.js -Force
Get-FileHash .\glm-coding-helper.user.js
Get-FileHash .\scripts\userscripts\glm-coding-helper.user.js
```

The hashes should match.

## Release Checks For Agents

Before publishing changes:

```powershell
node --check .\glm-coding-helper.user.js
node --check .\scripts\userscripts\glm-coding-helper.user.js
Get-FileHash .\glm-coding-helper.user.js
Get-FileHash .\scripts\userscripts\glm-coding-helper.user.js
git diff --check
git status --short
```

Search for sensitive data without printing secrets:

```powershell
rg -n "api[_-]?key|password|secret" .
```

Also search for any known private invite code if the maintainer provides it out of band, but do not
print that code in logs, public docs, or final answers.

## Escalation Guidance

Ask the user before:

- installing Python or dependencies,
- changing firewall/security settings,
- killing a process,
- changing browser extension permissions on their behalf,
- pushing to GitHub or publishing to GreasyFork.

Proceed without asking when:

- reading repository files,
- checking file existence,
- running `/health`,
- running syntax checks,
- updating documentation in the local working tree after the user asked for it.

## Final Report Template

When finished, tell the user:

- what was installed or changed,
- which commands verified it,
- the backend URL,
- whether CPU or GPU is active,
- how to install/update the userscript,
- any remaining manual step, especially browser permissions or payment confirmation.
