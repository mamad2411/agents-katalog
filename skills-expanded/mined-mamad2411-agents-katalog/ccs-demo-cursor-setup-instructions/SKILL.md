# GitHub Setup Automation Instructions for Cursor IDE

## Task: Automate GitHub Repository Setup

When a user asks to set up their GitHub repository, follow these steps:

1. **Check for PowerShell/PowerShell Core:**
   - Windows: Check if `powershell` is available (usually pre-installed)
     - Run: `powershell -Command "Write-Host 'PowerShell available'"` to verify
   - Mac/Linux: Check if `pwsh` (PowerShell Core) is available
     - Run: `pwsh --version` to check
     - If not found, install it:
       - Mac: `brew install --cask powershell` or `brew install pwsh`
       - Linux: Follow instructions at https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-linux
       - Windows: PowerShell should already be available

2. **Check for GitHub CLI:**
   - Windows: Run `gh --version` or `powershell -Command "gh --version"`
   - Mac/Linux: Run `gh --version` or `pwsh -Command "gh --version"`
   - If not found, install it:
     - Mac: `brew install gh`
     - Linux: Follow instructions at https://github.com/cli/cli/blob/trunk/docs/install_linux.md
     - Windows: `winget install --id GitHub.cli --silent --accept-package-agreements --accept-source-agreements`

3. **Authenticate with GitHub (if needed):**
   - Check authentication: `gh auth status`
   - If not authenticated, use browser-based login (platform-specific):
     - **Windows PowerShell:** Run: `"y" | gh auth login --web --git-protocol https --hostname github.com`
     - **Mac/Linux:** Run: `echo y | gh auth login --web --git-protocol https --hostname github.com`
     - This opens a browser automatically (non-interactive friendly)
     - User completes authentication in browser
     - Wait for confirmation before proceeding

4. **Run the setup script:**
   - Windows: `powershell -ExecutionPolicy Bypass -File .\setup-github-template.ps1`
   - Mac/Linux: `pwsh -File ./setup-github-template.ps1`
   - Handle any authentication prompts or errors gracefully
   - If script requires interactive input, pause and guide user through manual steps

5. **Verify the setup:**
   - Confirm repository was created
   - Confirm issue was created
   - Provide the repository URL to the user

## Notes:
- Always check for prerequisites before running scripts
- Handle errors gracefully and provide clear feedback
- On Mac/Linux, PowerShell Core (pwsh) may need to be installed first
- The script will handle GitHub authentication interactively if needed
- Provide clear status updates at each step

## Additional: GitHub API Token Creation for n8n

When a user asks to create a GitHub API token for n8n, follow these steps:

1. **Check GitHub CLI authentication:**
   - Run: `gh auth status`
   - If not authenticated, use browser-based login (non-interactive friendly):
     - Run: `gh auth login --web`
     - This will open a browser automatically
     - User completes authentication in browser
     - Wait for confirmation that authentication succeeded

2. **Check if current token has required scopes:**
   - Run: `gh auth status` to see current scopes
   - If scopes are missing, refresh with browser-based method:
     - Run: `gh auth refresh --web -s repo,workflow,admin:org,admin:repo_hook,admin:org_hook`
     - This will open a browser for user to authorize the new scopes
     - Wait for user to complete authorization in browser

3. **Get the token:**
   - Run: `gh auth token`
   - Display the token to the user
   - Warn them to save it securely (they'll need it for n8n)

**Note:** If browser-based authentication fails or user prefers manual creation, guide them to the manual web UI method (see step 4 below).

4. **If refresh fails or user prefers manual creation:**
   - Guide user to: https://github.com/settings/tokens
   - Instruct them to:
     - Click "Generate new token" -> "Generate new token (classic)"
     - Name it (e.g., "n8n-workshop-token")
     - Select expiration
     - Select scopes: repo, workflow, admin:org, admin:repo_hook, admin:org_hook
     - Click "Generate token"
     - Copy the token immediately (only shown once!)

5. **Verify token (optional):**
   - Test the token: `gh auth token | gh api user` (if using CLI token)
   - Or verify scopes in GitHub settings

6. **Provide the token to the user:**
   - Display it clearly
   - Remind them it's needed for n8n GitHub node configuration

