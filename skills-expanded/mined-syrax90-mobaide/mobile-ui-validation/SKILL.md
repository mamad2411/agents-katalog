---
name: mobile-ui-validation
description: Use whenever a UI component or flow of the Android (`android/`) or iOS (`ios/`) app must be checked to really work, or when E2E tests are created or run. Requires deploying the infrastructure locally with `tests/e2e/manual_stack.py` and using the Android emulator / iOS simulator — never a production server.
---

# Mobile UI validation & E2E

To verify that a mobile UI component works, or to create E2E tests, deploy the infrastructure
(central_server + agent) **locally** with `tests/e2e/manual_stack.py` and run the real app on the
**Android emulator** (for `android/` changes) and the **iOS simulator** (for `ios/` changes).
Full reference: `docs/manual-e2e-testing.md`; the automated pytest harness (`tests/e2e/`,
`python -m pytest tests/e2e/ -v`) is described in `docs/e2e-harness.md`.

```bash
# 1. one command, from any directory (main checkout or a worktree -- the stack runs THAT checkout's code).
#    Boots + shows the Android emulator and the iOS simulator, installs, launches and signs in both
#    debug apps, and opens the web client signed in. Run it detached; `status` exit 0 = READY.
~/venvs/main/bin/python tests/e2e/manual_stack.py up --all &

# 2. after app changes: rebuild + reinstall + relaunch (signed in) against the running stack
~/venvs/main/bin/python tests/e2e/manual_stack.py android --install-app
~/venvs/main/bin/python tests/e2e/manual_stack.py ios --install-app

# 3. exercise the UI (adb / `xcrun simctl` / `axe`), then stop -- this restores
#    android/local.properties and ios/Config/Local.xcconfig
~/venvs/main/bin/python tests/e2e/manual_stack.py stop
```

On **Windows** there is no iOS simulator; validate Android + web only. One command boots the
emulator (AVD `Mobaide-E2E`, created on first use), builds + installs + launches the debug app, and
serves the web client; `stop` is the graceful shutdown (Windows has no `kill -TERM`) and also shuts
down the emulator the stack booted:

```powershell
# conda env with the editable installs, e.g. mobaide-e2e-tests; run detached (background task)
python tests/e2e/manual_stack.py up --host 127.0.0.1 --android-url emulator --emulator --install-app --web --no-browser
python tests/e2e/manual_stack.py status          # exit 0 = READY
# exercise the UI: adb -s emulator-5554 shell input ... / exec-out screencap -p; web at http://localhost:5173
python tests/e2e/manual_stack.py android --emulator --install-app   # reinstall after app changes
python tests/e2e/manual_stack.py stop            # restores android/local.properties, stops the emulator
```

In Git Bash, prefix `adb shell` commands with `MSYS_NO_PATHCONV=1` or `/sdcard/...` paths get mangled.

Login shown in the READY banner: `dev@test.local` / `Qwe>1234`.
