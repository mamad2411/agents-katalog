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

3. **Run the setup script:**
   - Windows: `powershell -ExecutionPolicy Bypass -File .\setup-github-template.ps1`
   - Mac/Linux: `pwsh -File ./setup-github-template.ps1`
   - Handle any authentication prompts or errors gracefully
   - Wait for user interaction if authentication is required

4. **Verify the setup:**
   - Confirm repository was created
   - Confirm issue was created
   - Provide the repository URL to the user

## Notes:
- Always check for prerequisites before running scripts
- Handle errors gracefully and provide clear feedback
- On Mac/Linux, PowerShell Core (pwsh) may need to be installed first
- The script will handle GitHub authentication interactively if needed
- Provide clear status updates at each step

