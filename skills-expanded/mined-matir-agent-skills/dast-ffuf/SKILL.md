---
name: dast-ffuf
description: Dynamic Application Security Testing (DAST) using ffuf. Used for automated directory enumeration and virtual host discovery.
metadata:
  version: 0.2.0
  category: appsec
---
# ffuf - Fast Web Fuzzer

## Quick Start
```bash
# Basic directory discovery using a wordlist
ffuf -u https://example.com/FUZZ -w /path/to/wordlist.txt
```

## Workflow
1. **Target Identification**: Identify the base URL or specific endpoint for fuzzing.
2. **Wordlist Selection**: Choose an appropriate wordlist (e.g., from SecLists) for directories, parameters, or payloads.
3. **Fuzzing Execution**: Run `ffuf` with the `FUZZ` placeholder in the target URL, header, or POST data.
4. **Filtering Results**: Apply filters (e.g., `-fs`, `-fc`) or use auto-calibration (`-ac`) to remove noise and baseline responses.
5. **Discovery**: Analyze results with interesting status codes (e.g., 200, 403, 301) to find hidden resources or vulnerabilities.
6. **Documentation**: Save results in JSON or HTML format for reporting and further manual testing.

## Rules & Constraints
- **RULE-1**: Only fuzz applications where you have explicit authorization and permission.
- **RULE-2**: Use reasonable rate limits (`-t`, `-p`) to avoid causing a Denial of Service (DoS) on the target.
- **RULE-3**: Always filter out common or uninteresting response sizes (`-fs`) to reduce results noise.

## When to Use
- Discovering hidden directories, files, and undocumented API endpoints.
- Fuzzing GET and POST parameters for potential injection points.
- Enumerating subdomains or virtual hosts via HTTP headers.

## When NOT to Use
- Heavy vulnerability scanning that requires deep logic (use Burp Suite or dedicated scanners).
- Fuzzing non-HTTP services (use protocol-specific tools like `nmap` or `hydra`).

## References
- [Skill Manual](references/dast-ffuf-manual.md)
- [ffuf Official Repo](https://github.com/ffuf/ffuf)
