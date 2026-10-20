---
description: Start a new engagement for a target — verifies scope, creates evidence directories, and launches recon agent
allowed-tools: Bash, Read, Write, Glob
---

Start a new penetration testing engagement for target: $ARGUMENTS

Follow these steps in order:

1. **Scope Verification**: Read `scope.txt` and verify that "$ARGUMENTS" is listed as an authorized target (exact IP, CIDR that includes the IP, or domain match). If NOT found in scope.txt, STOP immediately and output:
   ```
   ❌ SCOPE VIOLATION: "$ARGUMENTS" is not in scope.txt
   Add the target to scope.txt before proceeding.
   ```

2. **Create Evidence Directories**: Create the full directory structure:
   ```bash
   mkdir -p evidence/$(date +%Y%m%d)/$ARGUMENTS/{nmap,nuclei,web,creds,screenshots,post_ex,ad,cloud,wireless,mobile,api,re,osint,network,lateral,logs}
   ```

3. **Print Engagement Brief**:
   ```
   ═══════════════════════════════════════════════
   ENGAGEMENT START
   Target:    $ARGUMENTS
   Date:      $(date -u +%Y-%m-%dT%H:%M:%SZ)
   Operator:  $(whoami)
   Scope:     VERIFIED ✓
   Evidence:  evidence/$(date +%Y%m%d)/$ARGUMENTS/
   ═══════════════════════════════════════════════
   ```

4. **Delegate to Recon Agent**: Invoke the `recon` sub-agent with the target. The recon agent will:
   - Run nmap TCP full scan + service/version scan
   - Run nuclei CVE and exposure scans
   - Run httpx for web technology detection
   - Run feroxbuster for directory enumeration (if web ports found)
   - Run subfinder + amass if a domain target
   - Write `evidence/$(date +%Y%m%d)/$ARGUMENTS/recon_summary.md`

5. **Parse Recon Results**: After recon completes, read `recon_summary.md` and extract:
   - Open ports and services with versions
   - Web technologies detected
   - Discovered subdomains count

6. **Print Attack Vector Recommendations**: Based on the recon findings, output a prioritized list:
   ```
   ══ RECOMMENDED ATTACK VECTORS ══════════════════
   Priority 1: [e.g., "CVE-XXXX on Apache 2.4.49 (port 80)"]
   Priority 2: [e.g., "Default credentials on admin panel (/admin)"]
   Priority 3: [e.g., "SQL injection on login form"]
   Priority 4: [e.g., "Outdated OpenSSH — check for user enumeration"]
   ════════════════════════════════════════════════

   Ready. Run: /project:attack $ARGUMENTS <vector>
   ```
