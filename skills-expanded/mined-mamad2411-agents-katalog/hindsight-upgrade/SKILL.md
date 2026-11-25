---
name: hindsight-upgrade
description: Check for and install hindsight-skills updates. Detects new versions, offers upgrade options, and shows what changed.
---

# Hindsight Skills Upgrade

You manage upgrades for hindsight-skills. This skill is invoked in two ways:

1. **Automatically by the preamble** when `UPGRADE_AVAILABLE` or `JUST_UPGRADED` is detected
2. **Directly by the user** via `/hindsight-upgrade`

---

## Inline Upgrade Flow (called by preamble)

When the preamble detects `UPGRADE_AVAILABLE <old> <new>`, follow these steps:

### Step 1: Check auto_upgrade preference

```bash
# Check if auto-upgrade is enabled
_HS_BIN_DIR=""
for _d in ~/.claude/skills ~/.codex/skills ~/.kiro/skills ~/.factory/skills; do
  [ -x "$_d/hindsight-upgrade/bin/hindsight-config" ] && _HS_BIN_DIR="$_d/hindsight-upgrade/bin" && break
done
[ -n "$_HS_BIN_DIR" ] && _AUTO_UPGRADE=$("$_HS_BIN_DIR/hindsight-config" get auto_upgrade 2>/dev/null || echo "false")
echo "AUTO_UPGRADE: ${_AUTO_UPGRADE:-false}"
```

If `AUTO_UPGRADE` is `true`, skip to Step 2 and proceed with the upgrade silently.

If `AUTO_UPGRADE` is `false`, use `AskUserQuestion` to ask:

> hindsight-skills **{new}** is available (you have **{old}**). How would you like to proceed?

Options:
- **Upgrade now** — Install the update and continue
- **Always auto-upgrade** — Install now and auto-upgrade in the future
- **Snooze 24h** — Remind me tomorrow
- **Never ask** — Disable update checks permanently

Handle each response:
- **Upgrade now**: proceed to Step 2
- **Always auto-upgrade**: run `hindsight-config set auto_upgrade true`, then proceed to Step 2
- **Snooze 24h**: write snooze file and stop

```bash
# Snooze for 24 hours
_HS_STATE_DIR="${HINDSIGHT_SKILLS_STATE_DIR:-$HOME/.hindsight-skills}"
echo "{new_version} $(date +%s)" > "$_HS_STATE_DIR/update-snoozed"
```

- **Never ask**: run `hindsight-config set update_check false` and stop

### Step 2: Detect install type

```bash
# Read the install source breadcrumb
_HS_STATE_DIR="${HINDSIGHT_SKILLS_STATE_DIR:-$HOME/.hindsight-skills}"
_INSTALL_SOURCE=""
[ -f "$_HS_STATE_DIR/install-source" ] && _INSTALL_SOURCE=$(cat "$_HS_STATE_DIR/install-source")
echo "INSTALL_SOURCE: ${_INSTALL_SOURCE:-not found}"
```

If `INSTALL_SOURCE` is empty or the path doesn't exist, tell the user:

> I can't find the hindsight-skills installation. Please re-run setup from your clone:
> ```
> cd /path/to/hindsight-skills && ./setup
> ```

And stop.

### Step 3: Save old version

```bash
_HS_STATE_DIR="${HINDSIGHT_SKILLS_STATE_DIR:-$HOME/.hindsight-skills}"
_INSTALL_SOURCE=$(cat "$_HS_STATE_DIR/install-source")
_OLD_VERSION=$(cat "$_INSTALL_SOURCE/VERSION" 2>/dev/null | tr -d '[:space:]')
echo "OLD_VERSION: $_OLD_VERSION"
```

### Step 4: Upgrade

Check if the install source is a git repo:

```bash
_INSTALL_SOURCE=$(cat "${HINDSIGHT_SKILLS_STATE_DIR:-$HOME/.hindsight-skills}/install-source")
cd "$_INSTALL_SOURCE"
if [ -d .git ]; then
  echo "INSTALL_TYPE: git"
else
  echo "INSTALL_TYPE: vendored"
fi
```

**Git install:**
```bash
_INSTALL_SOURCE=$(cat "${HINDSIGHT_SKILLS_STATE_DIR:-$HOME/.hindsight-skills}/install-source")
cd "$_INSTALL_SOURCE" && git pull origin main && ./setup
```

**Vendored install** (no .git directory — downloaded/copied, not cloned):
```bash
_INSTALL_SOURCE=$(cat "${HINDSIGHT_SKILLS_STATE_DIR:-$HOME/.hindsight-skills}/install-source")
_PARENT=$(dirname "$_INSTALL_SOURCE")
_NAME=$(basename "$_INSTALL_SOURCE")
cd "$_PARENT"
# Clone fresh, run setup, move into place
git clone https://github.com/vectorize-io/hindsight-skills.git "${_NAME}-upgrade-tmp"
cd "${_NAME}-upgrade-tmp" && ./setup
cd "$_PARENT"
rm -rf "$_NAME"
mv "${_NAME}-upgrade-tmp" "$_NAME"
```

### Step 5: Write marker and clear state

```bash
_HS_STATE_DIR="${HINDSIGHT_SKILLS_STATE_DIR:-$HOME/.hindsight-skills}"
echo "$_OLD_VERSION" > "$_HS_STATE_DIR/just-upgraded-from"
rm -f "$_HS_STATE_DIR/last-update-check"
rm -f "$_HS_STATE_DIR/update-snoozed"
```

### Step 6: Show What's New

Read the CHANGELOG.md from the installed skill and show the user what changed between their old version and the new version:

```bash
# Find the changelog
for _d in ~/.claude/skills ~/.codex/skills ~/.kiro/skills ~/.factory/skills; do
  [ -f "$_d/hindsight-upgrade/CHANGELOG.md" ] && cat "$_d/hindsight-upgrade/CHANGELOG.md" && break
done
```

Parse the changelog and display only the sections between the old and new versions. Format as:

> **hindsight-skills upgraded: {old} → {new}**
>
> {relevant changelog entries}

Then continue with the user's original task.

---

## Handling JUST_UPGRADED

When the preamble detects `JUST_UPGRADED <old> <new>`, the upgrade already happened in a previous session. Show What's New (Step 6 above) and continue.

---

## Standalone Usage

When invoked directly as `/hindsight-upgrade`:

### Force check (bypass cache)

```bash
# Clear cache and run check
_HS_STATE_DIR="${HINDSIGHT_SKILLS_STATE_DIR:-$HOME/.hindsight-skills}"
rm -f "$_HS_STATE_DIR/last-update-check"
rm -f "$_HS_STATE_DIR/update-snoozed"

# Find and run the update check
for _d in ~/.claude/skills ~/.codex/skills ~/.kiro/skills ~/.factory/skills; do
  [ -x "$_d/hindsight-upgrade/bin/hindsight-update-check" ] && "$_d/hindsight-upgrade/bin/hindsight-update-check" && break
done
```

If the output is `UPGRADE_AVAILABLE`, follow the Inline Upgrade Flow from Step 1.

If the output is empty, tell the user: "hindsight-skills is up to date (version {version})."

If the output is `JUST_UPGRADED`, show What's New.

### Config management

Users can also use `/hindsight-upgrade` to manage settings:

- "enable auto-upgrade" → `hindsight-config set auto_upgrade true`
- "disable update checks" → `hindsight-config set update_check false`
- "re-enable update checks" → `hindsight-config set update_check true`
- "show config" → `hindsight-config list`
