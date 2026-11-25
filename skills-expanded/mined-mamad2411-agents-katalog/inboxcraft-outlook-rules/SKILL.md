---
name: inboxcraft-outlook-rules
description: Configures Outlook Inbox Rules leveraging COM for folders and Exchange Online for server rules.
license: MIT
metadata:
  author: "trivedi-vatsal<trivedivatsal005@gmail.com>"
  version: "1.0.0"
---

# InboxCraft Outlook Rules Generator

This skill instructs the agent on how to write the robust, idempotent PowerShell script used in **InboxCraft**. It is designed to work entirely standalone, without referencing local codebases.

## When to Use

Use this skill whenever the user asks to "generate an Outlook rules script", "create PowerShell script for inbox rules", or asks for help routing emails.

## Steps

1. **Be highly interactive!** Do not generate the script immediately. Start by using friendly, informative messages to guide the user. Output clear status messages indicating what you understand and what you are doing (e.g., "I've got the details, I will now generate the script to move emails from GitHub to the alerts folder").
2. **Clarify requirements:** Interactively ask the user for the following context before writing any code:
   - Do you want to create *only folders*, *only rules*, or *both*?
   - What are the sender email addresses or domains?
   - What folder should the emails be routed to? What is the parent folder (default to "team" if not specified)?
   - Do you want to **move** (remove from Inbox) or **copy** (keep in Inbox) the emails?
   
3. **Generate Script:** Once you have gathered and confirmed the requirements, use the following template exactly, filling in the rules provided. If the user opted to only create folders or only create rules, gracefully omit the irrelevant template sections. Do not hallucinate other PowerShell commands for this task.

### PowerShell Script Template Architecture

An InboxCraft script is robust because it attempts to use local `Outlook.Application` COM first (for folder creation), falling back to Exchange Online (`ExchangeOnlineManagement`). **Rule creation ALWAYS happens in Exchange Online**.

#### 1. Boilerplate Header
```powershell
#Requires -Version 5.1
$ErrorActionPreference = "Stop"

$confirm = Read-Host "Do you want to proceed? (Y/N)"
if ($confirm -notmatch '^[Yy]$') { exit 0 }

$outlook = $null; $namespace = $null; $inbox = $null; $userEmail = $null; $comAvailable = $false; $exoConnected = $false

Write-Host "Trying Outlook COM for folder creation..."
try {
    $outlook = New-Object -ComObject Outlook.Application
    $namespace = $outlook.GetNamespace("MAPI")
    $inbox = $namespace.GetDefaultFolder(6)
    $userEmail = $inbox.FolderPath.TrimStart('\').Split('\')[0]
    $comAvailable = $true
} catch {
    Write-Host "Outlook COM unavailable."
}

if (-not $comAvailable) {
    $userEmail = (whoami /upn 2>$null).Trim()
    if (-not $userEmail -or $userEmail -notmatch '@') {
        $userEmail = Read-Host "Enter your Exchange email address"
    }
}
```

#### 2. Folders (COM logic branch)
```powershell
if ($comAvailable) {
    # Create Parent Folder
    try {
        $parentFolderCom = $inbox.Folders.Item("YOUR_PARENT_FOLDER_NAME")
    } catch {
        $parentFolderCom = $inbox.Folders.Add("YOUR_PARENT_FOLDER_NAME")
    }

    # Create individual Subfolders loop
    # Repeat for each routing rule
    try {
        $inbox.Folders.Item("YOUR_SUBFOLDER_NAME") | Out-Null
    } catch {
        try {
            $tmp = $inbox.Folders.Item("YOUR_SUBFOLDER_NAME")
            $tmp.MoveTo($parentFolderCom)
        } catch {
            $new = $inbox.Folders.Add("YOUR_SUBFOLDER_NAME")
            $new.MoveTo($parentFolderCom)
        }
    }
}
```

#### 3. Folders (EXO Fallback branch)
```powershell
else {
    Import-Module ExchangeOnlineManagement -ErrorAction Stop
    Connect-ExchangeOnline -UserPrincipalName $userEmail -ShowBanner:$false
    $exoConnected = $true

    # We fetch the inbox folder explicitly to avoid string concatenation issues
    $inboxId = $userEmail + ":\Inbox"

    # Create Parent Folder
    $parentFolderPath = $inboxId + "\YOUR_PARENT_FOLDER_NAME"
    try {
        $parentFolderExo = Get-MailboxFolder -Identity $parentFolderPath -ErrorAction Stop
    } catch {
        $parentFolderExo = New-MailboxFolder -Name "YOUR_PARENT_FOLDER_NAME" -Parent $inboxId -ErrorAction Stop
    }

    # Create individual Subfolders loop
    # Repeat for each routing rule
    $subfolderPath = $parentFolderExo.Identity + "\YOUR_SUBFOLDER_NAME"
    try {
        Get-MailboxFolder -Identity $subfolderPath -ErrorAction Stop | Out-Null
    } catch {
        New-MailboxFolder -Name "YOUR_SUBFOLDER_NAME" -Parent $parentFolderExo.Identity -ErrorAction Stop | Out-Null
    }
}
```

#### 4. Rules Using Exchange Online
```powershell
if (-not $exoConnected) {
    Import-Module ExchangeOnlineManagement -ErrorAction Stop
    Connect-ExchangeOnline -UserPrincipalName $userEmail -ShowBanner:$false
    $exoConnected = $true
}

# Rule creation loop:
# Use -FromAddressContains if they specify a domain or specific email
# Use -MoveToFolder or -CopyToFolder depending on the requested action
# NOTE: DO NOT escape the backslashes in PowerShell with \\. Always use single \
try {
    $existing = Get-InboxRule -ErrorAction SilentlyContinue | Where-Object { $_.Name -eq "Move YOUR_EMAIL to YOUR_SUBFOLDER_NAME" }
    if (-not $existing) {
        $ruleFolderId = $userEmail + ":\Inbox\YOUR_PARENT_FOLDER_NAME\YOUR_SUBFOLDER_NAME"
        New-InboxRule -Name "Move YOUR_EMAIL to YOUR_SUBFOLDER_NAME" -FromAddressContains "YOUR_EMAIL_OR_DOMAIN" -MoveToFolder $ruleFolderId -ErrorAction Stop | Out-Null
    }
} catch {
    Write-Host "WARNING: Could not create rule."
}
```

#### 5. Cleanup
```powershell
if ($exoConnected) { Disconnect-ExchangeOnline -Confirm:$false -ErrorAction SilentlyContinue }
if ($null -ne $inbox) { [System.Runtime.InteropServices.Marshal]::ReleaseComObject($inbox) | Out-Null }
if ($null -ne $namespace) { [System.Runtime.InteropServices.Marshal]::ReleaseComObject($namespace) | Out-Null }
if ($null -ne $outlook) { [System.Runtime.InteropServices.Marshal]::ReleaseComObject($outlook) | Out-Null }
[System.GC]::Collect()
[System.GC]::WaitForPendingFinalizers()
```

3. **Output:** Combine the sections above chronologically to form one script. Deliver the fully synthesized script inside a `*.ps1` codeblock or write it to a `.ps1` file directly in the user's workspace for them to execute.
