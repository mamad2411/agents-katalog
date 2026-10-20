---
name: cwe-327-weak-cryptography
description: Use this skill when you need to remediate CWE-327 (Use of a Broken or Risky Cryptographic Algorithm) vulnerabilities in Java code. Triggers on SAST findings, security reviews, or when fixing use of a broken or risky cryptographic algorithm issues.
version: 1.0.0
license: MIT
tags:
- security
- java
- cwe-327
- remediation
- sast

- cryptography

- weak-crypto

---

# CWE-327 Use of a Broken or Risky Cryptographic Algorithm

## Description

Use of a Broken or Risky Cryptographic Algorithm

Reference:
https://cwe.mitre.org/data/definitions/327.html


**OWASP Category**: A02:2021 – Cryptographic Failures


---

## Vulnerable Pattern


### ❌ Example 1

```java
    private static final String LEVEL4_SECRET = "s3cretKey";
    private static final String LEVEL4_ENCODED =
            java.util.Base64.getEncoder().encodeToString(LEVEL4_SECRET.getBytes());

    private static final String LEVEL5_SECRET = "strongPass!";
    private static final String LEVEL5_SALT = "randomSalt123";
    private static final String LEVEL5_HASH;

    static {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            digest.update(LEVEL5_SALT.getBytes());
            byte[] hash = digest.digest(LEVEL5_SECRET.getBytes());
            LEVEL5_HASH = bytesToHex(hash);
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-256 not available", e);
        }
    }
```




### ❌ Example 2

```java
    public ResponseEntity<GenericVulnerabilityResponseBean<String>> getVulnerablePayloadLevel1(
            @RequestParam Map<String, String> queryParams) {
        String password = queryParams.get(PASSWORD_PARAM);

        // No password param: return the challenge hash
        if (password == null || password.isEmpty()) {
            return new ResponseEntity<>(
                    new GenericVulnerabilityResponseBean<>(
                            "CHALLENGE: A user's password is stored as MD5 hash: "
                                    + LEVEL1_HASH
                                    + " — Crack it and enter the original password!",
                            false),
                    HttpStatus.OK);
        }

        // Verify the guess
        String guessHash = DigestUtils.md5Hex(password);
        if (guessHash.equals(LEVEL1_HASH)) {
        // ... (truncated for brevity)
```





---

## Deterministic Fix


### ✅ Secure Implementation

```java
    public ResponseEntity<GenericVulnerabilityResponseBean<String>> getVulnerablePayloadLevel4(
            @RequestParam Map<String, String> queryParams) {
        String password = queryParams.get(PASSWORD_PARAM);

        if (password == null || password.isEmpty()) {
            return new ResponseEntity<>(
                    new GenericVulnerabilityResponseBean<>(
                            "CHALLENGE: The system 'encrypts' passwords using Base64 encoding. "
                                    + "The stored password is: "
                                    + LEVEL4_ENCODED
                                    + " — Decode it and enter the original password!",
                            false),
                    HttpStatus.OK);
        }

        if (password.equals(LEVEL4_SECRET)) {
            return new ResponseEntity<>(
                    new GenericVulnerabilityResponseBean<>(
                            "Correct! The password was '"
                                    + LEVEL4_SECRET
                                    + "'. Base64 is an encoding, NOT encryption."
                                    + " It provides zero security — anyone can decode it instantly.",
                            true),
                    HttpStatus.OK);
        } else {
        // ... (truncated for brevity)
```




### ✅ Secure Implementation

```java
    public ResponseEntity<GenericVulnerabilityResponseBean<String>> getVulnerablePayloadLevel4(
            @RequestParam Map<String, String> queryParams) {
        String password = queryParams.get(PASSWORD_PARAM);

        if (password == null || password.isEmpty()) {
            return new ResponseEntity<>(
                    new GenericVulnerabilityResponseBean<>(
                            "CHALLENGE: The system 'encrypts' passwords using Base64 encoding. "
                                    + "The stored password is: "
                                    + LEVEL4_ENCODED
                                    + " — Decode it and enter the original password!",
                            false),
                    HttpStatus.OK);
        }

        if (password.equals(LEVEL4_SECRET)) {
            return new ResponseEntity<>(
                    new GenericVulnerabilityResponseBean<>(
                            "Correct! The password was '"
                                    + LEVEL4_SECRET
                                    + "'. Base64 is an encoding, NOT encryption."
                                    + " It provides zero security — anyone can decode it instantly.",
                            true),
                    HttpStatus.OK);
        } else {
        // ... (truncated for brevity)
```





---

## Detection Pattern

Look for these patterns in your codebase:


```bash
# Find weak hash algorithms
grep -rn "MD5\|SHA-1\|SHA1" --include="*.java"
```


```bash
# Find weak ciphers
grep -rn "DES\|RC4\|ECB" --include="*.java"
```



---

## Remediation Steps


1. Replace MD5/SHA1 with SHA-256 or SHA-3 for hashing

2. Use bcrypt, scrypt, or Argon2 for password hashing

3. Replace DES/3DES with AES-256

4. Use GCM or CBC mode with proper IV instead of ECB

5. Use secure random for key generation


---

## Key Imports

```java

import javax.crypto.Cipher;

import java.security.MessageDigest;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

```

---

## Verification

After remediation:


- Re-run SAST scan - CWE-327 should be resolved

- Verify strong algorithms are used (AES-256, SHA-256)

- Check key lengths meet minimum requirements


---

## Trigger Examples

```
Fix CWE-327 vulnerability
Resolve Use of a Broken or Risky Cryptographic Algorithm issue
Secure this Java code against use of a broken or risky cryptographic algorithm
SAST reports CWE-327
```

---

## Common Vulnerable Locations

| Layer | Files | Patterns |
|-------|-------|----------|

| Security | `*Security*.java` | Password handling |

| Utility | `*Crypto*.java, *Hash*.java` | Encryption/hashing |

| Service | `*Service.java` | Data encryption |


---

## References


- [CWE-327: Broken Crypto](https://cwe.mitre.org/data/definitions/327.html)

- [OWASP Cryptographic Failures](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)


---

**Source**: Generated by [Java CWE Security Skills Generator](https://github.com/DevelopersCoffee/java-cwe-security-skills)
**Last Updated**: 2026-03-07
