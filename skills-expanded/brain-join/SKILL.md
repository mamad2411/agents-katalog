---
name: brain-join
description: Join an existing brain sync network from another machine. Pulls the consolidated brain and merges with any local state.
---


The user wants to join an existing brain network from this machine.

The Git remote URL is provided as: $ARGUMENTS

## Steps

1. Check dependencies (git, jq or python3).

2. Validate the remote URL for security:
   ```bash
   source "${CLAUDE_PLUGIN_ROOT}/scripts/common.sh"
   validate_remote_url "$ARGUMENTS"
   ```
   If the URL appears to point to a PUBLIC repo, warn the user and ask for confirmation.

3. Show current local brain inventory:
   ```
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/status.sh"
   ```

4. **Show security notice:**
   - "Joining a brain network means:"
   - "  - Your local brain data will be PUSHED to the remote repository"
   - "  - Remote brain data (skills, agents, rules) will be IMPORTED to your machine"
   - "  - Auto-sync will run on every Claude Code session start/end"
   - ""
   - "Only join brain networks you trust — imported skills and agents execute with Claude's permissions."

5. Clone the brain repo:
   ```bash
   git clone "$ARGUMENTS" ~/.claude/brain-repo
   ```
   If the directory exists, do `git -C ~/.claude/brain-repo pull origin main` instead.

6. Check if the network uses encryption:
   ```bash
   # Check for recipients file indicating encryption
   if [ -f ~/.claude/brain-repo/meta/recipients.txt ]; then
     echo "This brain network uses age encryption."
     
     if ! command -v age-keygen &>/dev/null; then
       echo "ERROR: age not found. Install it from https://github.com/FiloSottile/age"
       echo "On macOS: brew install age"
       echo "On Ubuntu/Debian: apt install age"
       exit 1
     fi
     
     echo ""
     echo "You need to set up age encryption to join this network."
     echo "Options:"
     echo "  1. Generate a new age keypair for this machine"
     echo "  2. Use an existing age private key"
     echo ""
     read -p "Generate new keypair? (y/n): " -r generate_key
     
     if [ "$generate_key" = "y" ] || [ "$generate_key" = "Y" ]; then
       # Generate new keypair
       source "${CLAUDE_PLUGIN_ROOT}/scripts/common.sh"
       IDENTITY_FILE="${HOME}/.claude/brain-age-key.txt"
       age-keygen -o "$IDENTITY_FILE"
       chmod 600 "$IDENTITY_FILE"
       
       # Extract public key
       PUBLIC_KEY=$(grep "# public key:" "$IDENTITY_FILE" | cut -d' ' -f4)
       echo ""
       echo "Generated age keypair. Your public key is:"
       echo "$PUBLIC_KEY"
       echo ""
       echo "IMPORTANT: Share this public key with the brain network owner"
       echo "so they can add it to the recipients file."
       echo ""
       echo "The network owner should run:"
       echo "  echo '$PUBLIC_KEY' >> ~/.claude/brain-repo/meta/recipients.txt"
       echo "  git add meta/recipients.txt && git commit -m 'Add machine: $(hostname)' && git push"
       echo ""
       read -p "Press Enter when the network owner has added your public key..."
       
       # Pull to get updated recipients
       git -C ~/.claude/brain-repo pull origin main
       
       REGISTER_FLAGS="--encrypt"
     else
       echo "Please place your existing age private key at: ~/.claude/brain-age-key.txt"
       echo "Make sure it's readable only by you: chmod 600 ~/.claude/brain-age-key.txt"
       read -p "Press Enter when ready..."
       
       if [ ! -f ~/.claude/brain-age-key.txt ]; then
         echo "ERROR: Age private key not found at ~/.claude/brain-age-key.txt"
         exit 1
       fi
       
       REGISTER_FLAGS="--encrypt"
     fi
   else
     echo "This brain network does not use encryption."
     REGISTER_FLAGS=""
   fi
   ```

7. Register this machine:
   ```bash
   if [ -n "$REGISTER_FLAGS" ]; then
     bash "${CLAUDE_PLUGIN_ROOT}/scripts/register-machine.sh" "$ARGUMENTS" $REGISTER_FLAGS
   else
     bash "${CLAUDE_PLUGIN_ROOT}/scripts/register-machine.sh" "$ARGUMENTS"
   fi
   ```

8. Show what's in the consolidated brain vs what's local. Run export first:
   ```bash
   MACHINE_ID=$(cat ~/.claude/brain-config.json | jq -r '.machine_id')
   mkdir -p ~/.claude/brain-repo/machines/${MACHINE_ID}
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/export.sh" --output ~/.claude/brain-repo/machines/${MACHINE_ID}/brain-snapshot.json
   ```

9. Ask the user how to handle existing local data:
   - **Merge** (recommended): Merge local brain into consolidated
   - **Overwrite**: Replace local with consolidated brain
   - **Keep local**: Keep local as-is, only add new items from consolidated

10. Based on choice:
    - **Merge**: Run merge-structured.sh then merge-semantic.sh between local snapshot and consolidated
    - **Overwrite**: Run import.sh directly with consolidated brain
    - **Keep local**: Run import.sh but skip files that already exist locally

11. Push the updated state:
    ```bash
    cd ~/.claude/brain-repo
    git add machines/ consolidated/ meta/
    git commit -m "Join: $(hostname) joined brain network"
    git push origin main
    ```

12. Confirm success:
    - Show how many machines are now in the network
    - Show what was imported/merged
    - Note: "Auto-sync is now enabled. Your brain syncs on every Claude Code session start/end."
    - Reminder: "A backup of your pre-join brain state was saved to ~/.claude/brain-backups/"
