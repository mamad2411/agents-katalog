---
name: install-claudesidian-command
description: Install claudesidian shell command to launch Claude Code from anywhere. Use when the user wants to install a shell alias/launcher for their vault, or asks to set up the claudesidian command.
---

# Install Claudesidian Command

Creates a shell alias/function that allows you to run `claudesidian` from
anywhere to open your vault in Claude Code.

## Task

Install a shell command that:

1. Changes to your claudesidian vault directory
2. Launches Claude Code
3. Works from any directory in your terminal

Similar to having a quick launcher for your vault.

## Process

### 1. **Detect Current Setup**

- Check which shell the user is using (bash/zsh/fish)
- Find the current working directory (vault path)
- Determine the appropriate config file

### 2. **Create the Command**

The command will be an alias that:

- Changes to the vault directory: `cd /path/to/your/vault`
- Tries to resume existing session: `claude --resume 2>/dev/null`
- Falls back to new session if no existing one: `|| claude`
- All in one command with properly escaped path:
  `(cd "/path/to/vault" && (claude --resume 2>/dev/null || claude))`

**Important:** The path must be properly escaped to handle spaces and special
characters.

This automatically enters resume mode if there's an existing session, or starts
a new one if not.

### 3. **Install to Shell Config**

Add the alias to the appropriate config file:

- **Bash**: `~/.bashrc` or `~/.bash_profile`
- **Zsh**: `~/.zshrc`
- **Fish**: `~/.config/fish/config.fish`

### 4. **Verify Installation**

- Show the added line
- Remind user to reload their shell or source the config
- Provide test command

## Shell Detection

Detects the user's default shell, with support for command-line override:

```bash
# Check if shell specified as argument (/install-claudesidian-command zsh)
if [ -n "$1" ]; then
  # User provided shell type as argument
  SHELL_TYPE="$1"
else
  # Auto-detect from $SHELL (user's default shell, not current shell)
  SHELL_TYPE=$(basename "$SHELL")
fi

# Validate shell type and set appropriate config file
case "$SHELL_TYPE" in
  zsh)
    CONFIG_FILE="$HOME/.zshrc"
    ;;
  bash)
    # Prefer .bashrc on Linux, .bash_profile on macOS
    if [ -f "$HOME/.bashrc" ]; then
      CONFIG_FILE="$HOME/.bashrc"
    else
      CONFIG_FILE="$HOME/.bash_profile"
    fi
    ;;
  fish)
    CONFIG_FILE="$HOME/.config/fish/config.fish"
    ;;
  *)
    echo "❌ Unsupported shell: $SHELL_TYPE"
    echo "   Supported shells: bash, zsh, fish"
    echo "   Usage: /install-claudesidian-command [bash|zsh|fish]"
    exit 1
    ;;
esac

echo "🐚 Installing for: $SHELL_TYPE"
echo "📝 Config file: $CONFIG_FILE"
```

**Key improvements:**

- Uses `$SHELL` to detect default shell (not `$ZSH_VERSION`/`$BASH_VERSION`
  which detect current session)
- Supports command-line argument to override auto-detection
- Shows detected shell and config file for transparency
- Validates shell type and provides clear error message for unsupported shells

## Installation Steps

1. **Detect shell**: Use argument if provided, otherwise auto-detect from
   `$SHELL`
2. **Get vault path**: Use `pwd` to get current directory
3. **Escape the path**: Properly escape quotes and special characters for shell
   safety
   ```bash
   # Escape backslashes FIRST (so we don't double-escape ones we add later)
   ESCAPED_PATH="${VAULT_PATH//\\/\\\\}"
   # Then escape double quotes
   ESCAPED_PATH="${ESCAPED_PATH//\"/\\\"}"
   ```
4. **Check if already installed**: Search config file for existing
   `claudesidian` alias/function
   ```bash
   # Check for existing alias/function
   if grep -q "alias claudesidian\|function claudesidian" "$CONFIG_FILE"; then
     echo "⚠️  Found existing claudesidian command:"
     grep -A 3 "claudesidian" "$CONFIG_FILE"
     echo ""
     read -p "Replace it? (yes/no): " replace_answer
     if [[ ! "$replace_answer" =~ ^[Yy] ]]; then
       echo "Installation cancelled. Existing command preserved."
       exit 0
     fi
     # Mark for replacement (will remove before adding new one)
     REPLACING=true
   fi
   ```
5. **Get user confirmation**: Show what will be added and get final confirmation
6. **Create backup**: Only if proceeding with modification
   ```bash
   # Create backup with timestamp
   BACKUP_FILE="$CONFIG_FILE.backup-$(date +%Y%m%d-%H%M%S)"
   cp "$CONFIG_FILE" "$BACKUP_FILE"
   echo "💾 Backup created: $BACKUP_FILE"
   ```
7. **Build the safe alias/function command**: Use the escaped path from step 3
   ```bash
   # CRITICAL: Use $ESCAPED_PATH in the command (not raw $VAULT_PATH)
   if [ "$SHELL_TYPE" = "fish" ]; then
     # Fish uses function syntax, not alias
     COMMAND_TEXT="function claudesidian
    cd \"$ESCAPED_PATH\" && (claude --resume 2>/dev/null; or claude)
    cd -
   end"
   else
     # Bash/Zsh use alias syntax
     # IMPORTANT: Use double quotes around $ESCAPED_PATH to preserve escaping
     COMMAND_TEXT="alias claudesidian='(cd \"$ESCAPED_PATH\" && (claude --resume 2>/dev/null || claude))'"
   fi
   ```
8. **Remove old command if replacing**:
   ```bash
   if [ "$REPLACING" = true ]; then
     # Bash/Zsh: alias is a single line — delete just that line
     sed -i.tmp '/^alias claudesidian/d' "$CONFIG_FILE"
     # Fish: function spans multiple lines — delete from `function claudesidian`
     # to the matching `end`
     sed -i.tmp '/^function claudesidian/,/^end$/d' "$CONFIG_FILE"
     rm -f "$CONFIG_FILE.tmp"
   fi
   ```

   **Why two separate sed calls:** A combined range like
   `/alias claudesidian\|function claudesidian/,/^end$/d` would, for the alias
   case, keep eating lines until it found the next `^end$` somewhere else in
   the file (or EOF). That could nuke unrelated config below. Single-line
   delete for the alias, range delete for the function — never combine them.
9. **Add command to config file**: Append using the escaped command text
   ```bash
   echo "$COMMAND_TEXT" >> "$CONFIG_FILE"
   ```
10. **Show success message**: With instructions to reload shell

## Example Output

**Bash/Zsh Example (with spaces in path to demonstrate escaping):**

```
🔧 Installing claudesidian command...

📁 Vault path: /home/user/My Obsidian Vault
🐚 Shell detected: zsh
📝 Config file: /home/user/.zshrc

💾 Backup created: /home/user/.zshrc.backup-20250107-143025

✅ Installed! Added to /home/user/.zshrc:
   alias claudesidian='(cd "/home/user/My Obsidian Vault" && (claude --resume 2>/dev/null || claude))'

🔄 To activate, run:
   source ~/.zshrc

   Or start a new terminal session.

✨ Test it: Type 'claudesidian' from any directory!
```

**Fish Shell Example:**

```
🔧 Installing claudesidian command...

📁 Vault path: /home/user/My Obsidian Vault
🐚 Shell detected: fish
📝 Config file: /home/user/.config/fish/config.fish

💾 Backup created: /home/user/.config/fish/config.fish.backup-20250107-143025

✅ Installed! Added to /home/user/.config/fish/config.fish:
   function claudesidian
    cd "/home/user/My Obsidian Vault" && (claude --resume 2>/dev/null; or claude)
    cd -
end

🔄 To activate, run:
   source ~/.config/fish/config.fish

   Or start a new terminal session.

✨ Test it: Type 'claudesidian' from any directory!
```

## Handling Special Characters

The implementation properly handles paths with:

- Spaces: `/Users/noah/My Vault`
- Quotes: `/Users/noah/vault's backup`
- Special characters that need escaping

Paths are double-quoted and any embedded quotes/backslashes are escaped.

## Fish Shell Support

Fish shell uses different syntax than Bash/Zsh:

**Bash/Zsh (alias):**

```bash
alias claudesidian='(cd "/path" && command)'
```

**Fish (function):**

```fish
function claudesidian
    cd "/path" && (command; or fallback)
    cd -
end
```

Key differences:

- Fish uses `function` keyword instead of `alias` for complex commands
- Fish uses `; or` instead of `||` for fallback logic
- Fish uses `cd -` to return to previous directory (instead of subshell)
- Multi-line function definition instead of single-line alias

The installation automatically detects Fish and uses the correct syntax.

## Security Considerations

This command modifies your shell configuration file (a sensitive operation).
Safety measures:

- **You'll see exactly what will be added** before any changes
- **Timestamped backup is automatically created** before modification
- **Vault path is properly escaped** to prevent injection attacks
- **Only the claudesidian command is modified** - nothing else in your config
- **Asks permission** before replacing existing commands

If anything goes wrong, restore from: `$CONFIG_FILE.backup-YYYYMMDD-HHMMSS`

## Important Notes

- The command uses a subshell `()` (or `cd -` in Fish) so it returns to your
  original directory after
- Automatically tries to resume existing sessions, falls back to new session
- If alias/function already exists, asks user if they want to replace it
- Always shows what will be added before modifying config files
- **Always creates timestamped backup** of config file before modifying (format:
  `YYYYMMDD-HHMMSS`)
- Backups are kept indefinitely - users can manually clean up old backups if
  needed
- Shows backup location so users know where to restore from if needed

## Usage Examples

Install for your default shell (auto-detected):

```
/install-claudesidian-command
```

Install for specific shell (override auto-detection):

```
/install-claudesidian-command zsh
/install-claudesidian-command bash
/install-claudesidian-command fish
```

**When to specify shell:**

- You use multiple shells and want to install for a specific one
- Auto-detection picked the wrong shell
- You're setting up for someone else

## How It Works

**Bash/Zsh (alias with subshell):**

```bash
alias claudesidian='(cd "/path/to/vault" && (claude --resume 2>/dev/null || claude))'
```

1. `(cd "/path/to/vault" && ...)` - Subshell that changes directory temporarily
   (path is double-quoted for safety)
2. `claude --resume 2>/dev/null` - Tries to resume existing session, suppresses
   error
3. `|| claude` - If resume fails (no session), starts new session
4. After Claude exits, subshell closes and returns to original directory
   automatically

**Fish (function with cd -):**

```fish
function claudesidian
    cd "/path/to/vault" && (claude --resume 2>/dev/null; or claude)
    cd -
end
```

1. `cd "/path/to/vault"` - Changes to vault directory (path is double-quoted for
   safety)
2. `claude --resume 2>/dev/null` - Tries to resume existing session, suppresses
   error
3. `; or claude` - If resume fails (no session), starts new session (Fish
   syntax)
4. `cd -` - Returns to previous directory after Claude exits
