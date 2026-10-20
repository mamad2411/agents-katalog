---
name: cwe-77-command-injection
description: Use this skill when you need to remediate CWE-77 (Improper Neutralization of Special Elements used in a Command (Command Injection)) vulnerabilities in Java code. Triggers on SAST findings, security reviews, or when fixing improper neutralization of special elements used in a command (command injection) issues.
version: 1.0.0
license: MIT
tags:
- security
- java
- cwe-77
- remediation
- sast

- command-injection

- injection

- os

---

# CWE-77 Improper Neutralization of Special Elements used in a Command (Command Injection)

## Description

Improper Neutralization of Special Elements used in a Command (Command Injection)

Reference:
https://cwe.mitre.org/data/definitions/77.html


**OWASP Category**: A03:2021 – Injection


---

## Vulnerable Pattern


### ❌ Example 1

```java
    private static final String IP_ADDRESS = "ipaddress";
    private static final Pattern SEMICOLON_SPACE_LOGICAL_AND_PATTERN = Pattern.compile("[;& ]");
    private static final Pattern IP_ADDRESS_PATTERN =
            Pattern.compile("\\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\\.|$)){4}\\b");

    StringBuilder getResponseFromPingCommand(String ipAddress, boolean isValid) throws IOException {
        boolean isWindows = System.getProperty("os.name").toLowerCase().startsWith("windows");
        StringBuilder stringBuilder = new StringBuilder();
        if (isValid) {
            Process process;
            if (!isWindows) {
                process =
                        new ProcessBuilder(new String[] {"sh", "-c", "ping -c 2 " + ipAddress})
                                .redirectErrorStream(true)
                                .start();
            } else {
                process =
                        new ProcessBuilder(new String[] {"cmd", "/c", "ping -n 2 " + ipAddress})
                                .redirectErrorStream(true)
                                .start();
            }
            try (BufferedReader bufferedReader =
                    new BufferedReader(new InputStreamReader(process.getInputStream()))) {
                bufferedReader.lines().forEach(val -> stringBuilder.append(val).append("\n"));
            }
        // ... (truncated for brevity)
```




### ❌ Example 2

```java
    StringBuilder getResponseFromPingCommand(String ipAddress, boolean isValid) throws IOException {
        boolean isWindows = System.getProperty("os.name").toLowerCase().startsWith("windows");
        StringBuilder stringBuilder = new StringBuilder();
        if (isValid) {
            Process process;
            if (!isWindows) {
                process =
                        new ProcessBuilder(new String[] {"sh", "-c", "ping -c 2 " + ipAddress})
                                .redirectErrorStream(true)
                                .start();
            } else {
                process =
                        new ProcessBuilder(new String[] {"cmd", "/c", "ping -n 2 " + ipAddress})
                                .redirectErrorStream(true)
                                .start();
            }
            try (BufferedReader bufferedReader =
                    new BufferedReader(new InputStreamReader(process.getInputStream()))) {
                bufferedReader.lines().forEach(val -> stringBuilder.append(val).append("\n"));
            }
        }
        return stringBuilder;
    }
```





---

## Deterministic Fix


### ✅ Secure Implementation

```java
    public ResponseEntity<GenericVulnerabilityResponseBean<String>> getVulnerablePayloadLevel5(
            @RequestParam(IP_ADDRESS) String ipAddress, RequestEntity<String> requestEntity)
            throws IOException {
        Supplier<Boolean> validator =
                () ->
                        StringUtils.isNotBlank(ipAddress)
                                && !SEMICOLON_SPACE_LOGICAL_AND_PATTERN
                                        .matcher(requestEntity.getUrl().toString())
                                        .find()
                                && !requestEntity.getUrl().toString().toUpperCase().contains("%26")
                                && !requestEntity.getUrl().toString().toUpperCase().contains("%3B")
                                && !requestEntity.getUrl().toString().toUpperCase().contains("%7C");
        return new ResponseEntity<GenericVulnerabilityResponseBean<String>>(
                new GenericVulnerabilityResponseBean<String>(
                        this.getResponseFromPingCommand(ipAddress, validator.get()).toString(),
                        true),
                HttpStatus.OK);
    }
```




### ✅ Secure Implementation

```java
    public ResponseEntity<GenericVulnerabilityResponseBean<String>> getVulnerablePayloadLevel5(
            @RequestParam(IP_ADDRESS) String ipAddress, RequestEntity<String> requestEntity)
            throws IOException {
        Supplier<Boolean> validator =
                () ->
                        StringUtils.isNotBlank(ipAddress)
                                && !SEMICOLON_SPACE_LOGICAL_AND_PATTERN
                                        .matcher(requestEntity.getUrl().toString())
                                        .find()
                                && !requestEntity.getUrl().toString().toUpperCase().contains("%26")
                                && !requestEntity.getUrl().toString().toUpperCase().contains("%3B")
                                && !requestEntity.getUrl().toString().toUpperCase().contains("%7C");
        return new ResponseEntity<GenericVulnerabilityResponseBean<String>>(
                new GenericVulnerabilityResponseBean<String>(
                        this.getResponseFromPingCommand(ipAddress, validator.get()).toString(),
                        true),
                HttpStatus.OK);
    }
```





---

## Detection Pattern

Look for these patterns in your codebase:


```bash
# Find Runtime.exec calls
grep -rn "Runtime.getRuntime().exec" --include="*.java"
```


```bash
# Find ProcessBuilder with concatenation
grep -rn "ProcessBuilder" --include="*.java" | grep "\+"
```



---

## Remediation Steps


1. Avoid executing shell commands with user input entirely

2. Use parameterized command arrays instead of shell strings

3. Validate input against strict allowlist of permitted values

4. Use ProcessBuilder with separate command and arguments

5. Escape special shell characters if command execution is required


---

## Key Imports

```java

import java.lang.ProcessBuilder;

import java.lang.Runtime;

```

---

## Verification

After remediation:


- Re-run SAST scan - CWE-77 should be resolved

- Test with command injection payloads: ; ls -la

- Verify commands cannot be chained or modified


---

## Trigger Examples

```
Fix CWE-77 vulnerability
Resolve Improper Neutralization of Special Elements used in a Command (Command Injection) issue
Secure this Java code against improper neutralization of special elements used in a command (command injection)
SAST reports CWE-77
```

---

## Common Vulnerable Locations

| Layer | Files | Patterns |
|-------|-------|----------|

| Service | `*Service.java` | System operations |

| Utility | `*Util.java, *Helper.java` | Shell commands |

| Controller | `*Controller.java` | Admin functions |


---

## References


- [CWE-77: Command Injection](https://cwe.mitre.org/data/definitions/77.html)

- [OWASP Command Injection](https://owasp.org/www-community/attacks/Command_Injection)


---

**Source**: Generated by [Java CWE Security Skills Generator](https://github.com/DevelopersCoffee/java-cwe-security-skills)
**Last Updated**: 2026-03-07
