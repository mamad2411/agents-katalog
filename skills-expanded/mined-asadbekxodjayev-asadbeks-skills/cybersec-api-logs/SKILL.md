# API Gateway Access Log Analysis Tool

This security operations resource provides guidance for investigating potential API exploits through log analysis.

## Primary Use Cases

The tool addresses scenarios where security teams need to examine API Gateway logs from platforms like AWS API Gateway, Kong, or Nginx. It's particularly valuable when investigating "broken object level authorization (BOLA), excessive data exposure, and injection attempts."

## Key Detection Methods

The analysis focuses on five main attack patterns:

1. **BOLA/IDOR attacks** - Identifying sequential resource ID enumeration attempts by individual users
2. **Rate limit circumvention** - Spotting header manipulation to bypass protections
3. **Authentication probing** - Detecting surges in 401 failures from single sources
4. **Injection attacks** - Analyzing query parameters for malicious payloads
5. **Unauthorized operations** - Flagging unusual HTTP methods on restricted endpoints

## Technical Approach

The methodology leverages pandas for statistical analysis, grouping requests by user and endpoint to identify suspicious patterns. For instance, detecting when a single user accesses over 50 different resource IDs on the same endpoint suggests potential enumeration activity.

## Relevant Context

The resource aligns with NIST cybersecurity frameworks (detection, monitoring, response) and MITRE ATT&CK techniques including exploitation and credential access approaches.
