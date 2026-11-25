---
name: cwe-89-sql-injection
description: Use this skill when you need to remediate CWE-89 (Improper Neutralization of Special Elements used in an SQL Command) vulnerabilities in Java code. Triggers on SAST findings, security reviews, or when fixing improper neutralization of special elements used in an sql command issues.
version: 1.0.0
license: MIT
tags:
- security
- java
- cwe-89
- remediation
- sast

- sql-injection

- injection

- database

---

# CWE-89 Improper Neutralization of Special Elements used in an SQL Command

## Description

Improper Neutralization of Special Elements used in an SQL Command

Reference:
https://cwe.mitre.org/data/definitions/89.html


**OWASP Category**: A03:2021 – Injection


---

## Vulnerable Pattern


### ❌ Example 1

```java
    public ResponseEntity<String> getCarInformationLevel1(
            @RequestParam Map<String, String> queryParams) {
        String id = queryParams.get(Constants.ID);
        BodyBuilder bodyBuilder = ResponseEntity.status(HttpStatus.OK);
        return applicationJdbcTemplate.query(
                "select * from cars where id=" + id,
                (rs) -> {
                    if (rs.next()) {
                        return bodyBuilder.body(CAR_IS_PRESENT_RESPONSE);
                    }
                    return bodyBuilder.body(
                            ErrorBasedSQLInjectionVulnerability.CAR_IS_NOT_PRESENT_RESPONSE);
                });
    }
```




### ❌ Example 2

```java
    public ResponseEntity<String> getCarInformationLevel2(
            @RequestParam Map<String, String> queryParams) {
        String id = queryParams.get(Constants.ID);
        BodyBuilder bodyBuilder = ResponseEntity.status(HttpStatus.OK);
        bodyBuilder.body(ErrorBasedSQLInjectionVulnerability.CAR_IS_NOT_PRESENT_RESPONSE);
        return applicationJdbcTemplate.query(
                "select * from cars where id='" + id + "'",
                (rs) -> {
                    if (rs.next()) {
                        return bodyBuilder.body(CAR_IS_PRESENT_RESPONSE);
                    }
                    return bodyBuilder.body(
                            ErrorBasedSQLInjectionVulnerability.CAR_IS_NOT_PRESENT_RESPONSE);
                });
    }
```





---

## Deterministic Fix


### ✅ Secure Implementation

```java
    public ResponseEntity<String> getCarInformationLevel2(
            @RequestParam Map<String, String> queryParams) {
        String id = queryParams.get(Constants.ID);
        BodyBuilder bodyBuilder = ResponseEntity.status(HttpStatus.OK);
        bodyBuilder.body(ErrorBasedSQLInjectionVulnerability.CAR_IS_NOT_PRESENT_RESPONSE);
        return applicationJdbcTemplate.query(
                "select * from cars where id='" + id + "'",
                (rs) -> {
                    if (rs.next()) {
                        return bodyBuilder.body(CAR_IS_PRESENT_RESPONSE);
                    }
                    return bodyBuilder.body(
                            ErrorBasedSQLInjectionVulnerability.CAR_IS_NOT_PRESENT_RESPONSE);
                });
    }
```




### ✅ Secure Implementation

```java
    public ResponseEntity<String> getCarInformationLevel2(
            @RequestParam Map<String, String> queryParams) {
        String id = queryParams.get(Constants.ID);
        BodyBuilder bodyBuilder = ResponseEntity.status(HttpStatus.OK);
        bodyBuilder.body(ErrorBasedSQLInjectionVulnerability.CAR_IS_NOT_PRESENT_RESPONSE);
        return applicationJdbcTemplate.query(
                "select * from cars where id='" + id + "'",
                (rs) -> {
                    if (rs.next()) {
                        return bodyBuilder.body(CAR_IS_PRESENT_RESPONSE);
                    }
                    return bodyBuilder.body(
                            ErrorBasedSQLInjectionVulnerability.CAR_IS_NOT_PRESENT_RESPONSE);
                });
    }
```





---

## Detection Pattern

Look for these patterns in your codebase:


```bash
# Find JdbcTemplate queries with concatenation
grep -rn "jdbcTemplate.query" --include="*.java" | grep -E "\+.*\"|\".*\+"
```


```bash
# Find raw Statement usage
grep -rn "createStatement\(\)" --include="*.java"
```



---

## Remediation Steps


1. Identify string concatenation in SQL query construction

2. Replace concatenated values with ? placeholders

3. Use PreparedStatement or equivalent parameterized API

4. Bind user input via setString(), setInt(), etc.

5. Validate input types match expected database column types


---

## Key Imports

```java

import java.sql.PreparedStatement;

import org.springframework.jdbc.core.JdbcTemplate;

```

---

## Verification

After remediation:


- Re-run SAST scan - CWE-89 should be resolved

- Test with injection payloads: ' OR '1'='1, 1; DROP TABLE--

- Verify query still returns expected results


---

## Trigger Examples

```
Fix CWE-89 vulnerability
Resolve Improper Neutralization of Special Elements used in an SQL Command issue
Secure this Java code against improper neutralization of special elements used in an sql command
SAST reports CWE-89
```

---

## Common Vulnerable Locations

| Layer | Files | Patterns |
|-------|-------|----------|

| Controller | `*Controller.java` | Query params to DB |

| Service | `*Service.java` | Business logic queries |

| Repository | `*Repository.java` | Custom queries |


---

## References


- [CWE-89: SQL Injection](https://cwe.mitre.org/data/definitions/89.html)

- [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)


---

**Source**: Generated by [Java CWE Security Skills Generator](https://github.com/DevelopersCoffee/java-cwe-security-skills)
**Last Updated**: 2026-03-07
