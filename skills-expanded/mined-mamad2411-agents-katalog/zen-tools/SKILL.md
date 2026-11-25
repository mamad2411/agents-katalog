# Zen Tools Integration Skill

How to use and integrate the 72+ security tools in Zen-Ai-Pentest.

## Tool Categories

### Network Scanning
```bash
# Port scanning (via deep-recon)
nmap -sV -sC -p- -T4 target.com
masscan -p1-65535 --rate=1000 target.com

# Service enumeration
whatweb target.com
wafw00f target.com
```

### Web Security
```bash
# Directory busting
gobuster dir -u https://target.com -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
ffuf -u https://target.com/FUZZ -w wordlist.txt

# Vulnerability scanning
nuclei -u https://target.com -t ~/nuclei-templates/
sqlmap -u "https://target.com/page?id=1" --batch
```

### Exploitation
```bash
# Via metasploit MCP
metasploit_module_search search_term="apache log4j"
metasploit_module_execute module_type=exploit module_name="exploit/multi/http/log4j" options='{"RHOSTS":"target.com"}'
```

### Active Directory
```bash
# Enumeration
bloodhound-python -d domain.local -u user -p pass -dc dc.domain.local
netexec smb target.com -u user -p pass --shares
responder -I eth0 -wrf
```

### Container Security
```bash
trivy image myapp:latest --severity CRITICAL,HIGH
docker scout quickview myapp:latest
kubectl audit --namespace=default
```

## Tool Execution via API

```python
import requests
from typing import Any


class ZenToolExecutor:
    def __init__(self, base_url: str = "http://localhost:8000", token: str = ""):
        self.base = base_url
        self.headers = {"Authorization": f"Bearer {token}"}

    def execute(self, tool: str, target: str, params: dict[str, Any] = None):
        return requests.post(
            f"{self.base}/tools/execute",
            headers=self.headers,
            json={"tool_name": tool, "target": target, "parameters": params or {}},
        ).json()

    def list_tools(self):
        return requests.get(f"{self.base}/tools", headers=self.headers).json()


executor = ZenToolExecutor()
result = executor.execute("nmap_scan", "scanme.nmap.org", {"ports": "22,80,443"})
```

## Report Generation

```python
from reports.generator import ReportGenerator

gen = ReportGenerator()
report = gen.create(
    scan_id=123,
    format="pdf",
    template="pentest",
    findings=[{"severity": "critical", "title": "SQL Injection", ...}],
)
# Output: reports/output/scan-123-report.pdf
```
