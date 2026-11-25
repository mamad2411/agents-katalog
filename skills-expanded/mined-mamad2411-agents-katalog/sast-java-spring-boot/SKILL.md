---
name: "sast-java-spring-boot"
description: "Run Static Application Security Testing (SAST) on LeadPerfection Java 17 / Spring Boot 3.2.x microservices — SpotBugs + Find-Sec-Bugs, OWASP Dependency Check, Checkstyle, and Azure DevOps pipeline integration with build-break gates."
version: 1
created: "2026-06-21"
updated: "2026-06-26"
---
## When to Use
Use this skill whenever you need to:
- Add SAST gates to a new or existing Spring Boot microservice (any LP epic)
- Configure OWASP Dependency Check (SCA) with CVSS >= 7 build-break threshold (ADR §12)
- Add SpotBugs + Find-Sec-Bugs for bytecode-level vulnerability detection (SQL injection paths, insecure deserialization, weak crypto)
- Add Checkstyle for code style enforcement (ADR §12)
- Wire all SAST tools into the Azure DevOps CI pipeline
- Generate SARIF/HTML/XML reports for security review artifacts
- Suppress known false positives with suppression files

Tool stack (aligned to ADR §12 + common_patterns NFR 3):
- OWASP Dependency Check 12.x — SCA (CVE scan of Maven dependencies)
- SpotBugs 4.x + Find-Sec-Bugs plugin — SAST bytecode analysis (400+ bug patterns, security-focused)
- Checkstyle 10.x — code style + basic security anti-pattern enforcement
- Azure DevOps YAML pipeline — orchestrates all gates in CI
- Threshold: CVSS >= 7 fails build (ADR §12)

## Procedure
1. STEP 1 — ADD OWASP DEPENDENCY CHECK to pom.xml: Add the plugin in <build><plugins>. Set failBuildOnCVSS to 7 per ADR §12. Add NVD API key as environment variable to avoid rate limiting.

<plugin>
  <groupId>org.owasp</groupId>
  <artifactId>dependency-check-maven</artifactId>
  <version>12.2.2</version>
  <configuration>
    <failBuildOnCVSS>7</failBuildOnCVSS>
    <suppressionFile>${project.basedir}/security/owasp-suppressions.xml</suppressionFile>
    <nvdApiKey>${env.NVD_API_KEY}</nvdApiKey>
    <formats>
      <format>HTML</format>
      <format>XML</format>
      <format>SARIF</format>
    </formats>
    <outputDirectory>${project.build.directory}/security-reports/owasp</outputDirectory>
  </configuration>
  <executions>
    <execution>
      <goals><goal>check</goal></goals>
    </execution>
  </executions>
</plugin>
2. STEP 2 — ADD SPOTBUGS + FIND-SEC-BUGS to pom.xml: SpotBugs scans compiled bytecode. Find-Sec-Bugs plugin adds 135+ security-specific detectors (SQL injection, XSS, path traversal, insecure crypto, etc.).

<plugin>
  <groupId>com.github.spotbugs</groupId>
  <artifactId>spotbugs-maven-plugin</artifactId>
  <version>4.8.6.6</version>
  <configuration>
    <effort>Max</effort>
    <threshold>Low</threshold>
    <failOnError>true</failOnError>
    <includeFilterFile>${project.basedir}/security/spotbugs-include.xml</includeFilterFile>
    <excludeFilterFile>${project.basedir}/security/spotbugs-exclude.xml</excludeFilterFile>
    <plugins>
      <plugin>
        <groupId>com.h3xstream.findsecbugs</groupId>
        <artifactId>findsecbugs-plugin</artifactId>
        <version>1.13.0</version>
      </plugin>
    </plugins>
    <xmlOutput>true</xmlOutput>
    <xmlOutputDirectory>${project.build.directory}/security-reports/spotbugs</xmlOutputDirectory>
    <sarifOutput>true</sarifOutput>
  </configuration>
  <executions>
    <execution>
      <id>spotbugs-check</id>
      <phase>verify</phase>
      <goals><goal>check</goal></goals>
    </execution>
  </executions>
</plugin>
3. STEP 3 — ADD CHECKSTYLE to pom.xml: Enforce ADR naming conventions and block anti-patterns (hardcoded passwords, System.out.println, etc.).

<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-checkstyle-plugin</artifactId>
  <version>3.5.0</version>
  <configuration>
    <configLocation>${project.basedir}/security/checkstyle.xml</configLocation>
    <suppressionsLocation>${project.basedir}/security/checkstyle-suppressions.xml</suppressionsLocation>
    <failsOnError>true</failsOnError>
    <violationSeverity>warning</violationSeverity>
    <outputFile>${project.build.directory}/security-reports/checkstyle/checkstyle-result.xml</outputFile>
  </configuration>
  <executions>
    <execution>
      <id>checkstyle-check</id>
      <phase>validate</phase>
      <goals><goal>check</goal></goals>
    </execution>
  </executions>
</plugin>
4. STEP 4 — CREATE SPOTBUGS INCLUDE FILTER (security/spotbugs-include.xml): Focus SpotBugs on security-critical bug categories relevant to Spring Boot REST APIs.

<?xml version='1.0' encoding='UTF-8'?>
<FindBugsFilter>
  <!-- SQL Injection -->
  <Match><Bug category='SECURITY'/></Match>
  <Match><Bug pattern='SQL_INJECTION,SQL_INJECTION_SPRING_JDBC,SQL_INJECTION_JPA'/></Match>
  <!-- Insecure deserialization -->
  <Match><Bug pattern='OBJECT_DESERIALIZATION'/></Match>
  <!-- Weak crypto -->
  <Match><Bug pattern='WEAK_MESSAGE_DIGEST_MD5,WEAK_MESSAGE_DIGEST_SHA1,DES_USAGE'/></Match>
  <!-- Hard-coded credentials -->
  <Match><Bug pattern='HARD_CODE_PASSWORD,HARD_CODE_KEY'/></Match>
  <!-- Path traversal -->
  <Match><Bug pattern='PATH_TRAVERSAL_IN,PATH_TRAVERSAL_OUT'/></Match>
  <!-- XXE -->
  <Match><Bug pattern='XXE_SAXPARSER,XXE_XMLREADER,XXE_DOCUMENT'/></Match>
  <!-- SSRF -->
  <Match><Bug pattern='URLCONNECTION_SSRF_FD'/></Match>
  <!-- Null dereference (high confidence only) -->
  <Match><Bug pattern='NP_NULL_ON_SOME_PATH_FROM_RETURN_VALUE' rank='1'/></Match>
</FindBugsFilter>
5. STEP 5 — CREATE OWASP SUPPRESSION FILE (security/owasp-suppressions.xml): Template for suppressing known false positives. Each suppression requires a justification comment and expiry date.

<?xml version='1.0' encoding='UTF-8'?>
<suppressions xmlns='https://jeremylong.github.io/DependencyCheck/dependency-suppression.1.3.xsd'>
  <!-- TEMPLATE: Copy and fill in for each false positive -->
  <!-- 
  <suppress until='2026-12-31Z'>
    <notes>False positive: CVE-XXXX-XXXX does not apply because [reason]. Reviewed by: [name] on [date]</notes>
    <packageUrl regex='true'>^pkg:maven/groupId/artifactId@.*$</packageUrl>
    <cve>CVE-XXXX-XXXX</cve>
  </suppress>
  -->
</suppressions>
6. STEP 6 — CREATE CHECKSTYLE CONFIG (security/checkstyle.xml): Enforce ADR §5.3 naming conventions and block hardcoded secrets pattern.

<?xml version='1.0'?>
<!DOCTYPE module PUBLIC '-//Checkstyle//DTD Checkstyle Configuration 1.3//EN'
  'https://checkstyle.org/dtds/configuration_1_3.dtd'>
<module name='Checker'>
  <property name='severity' value='warning'/>
  <!-- Naming conventions per ADR §5.3 -->
  <module name='TreeWalker'>
    <module name='PackageName'><property name='format' value='^[a-z]+(\.[a-z][a-z0-9]*)*$'/></module>
    <module name='TypeName'/>
    <module name='MethodName'/>
    <module name='ConstantName'/>
    <!-- Block System.out / System.err (use SLF4J) -->
    <module name='Regexp'>
      <property name='format' value='System\.(out|err)\.print'/>
      <property name='illegalPattern' value='true'/>
      <property name='message' value='Use SLF4J logger instead of System.out/err'/>
    </module>
    <!-- Block hardcoded password patterns -->
    <module name='Regexp'>
      <property name='format' value='(password|secret|apikey|api_key)\s*=\s*[&quot;&apos;][^&quot;&apos;]+[&quot;&apos;]'/>
      <property name='illegalPattern' value='true'/>
      <property name='ignoreCase' value='true'/>
      <property name='message' value='Hardcoded secret detected — use Azure Key Vault or env vars'/>
    </module>
    <!-- Missing @Override -->
    <module name='MissingOverride'/>
    <!-- Max method length -->
    <module name='MethodLength'><property name='max' value='80'/></module>
  </module>
  <!-- Max file length -->
  <module name='FileLength'><property name='max' value='500'/></module>
</module>
7. STEP 7 — AZURE DEVOPS PIPELINE SAST STAGE (azure-pipelines.yml): Add a dedicated SAST stage that runs after compile, before deploy. All three tools run in sequence; any failure breaks the pipeline.

# azure-pipelines.yml — SAST stage
stages:
- stage: Build
  jobs:
  - job: Compile
    steps:
    - task: Maven@4
      inputs:
        mavenPomFile: pom.xml
        goals: compile
        javaHomeOption: JDKVersion
        jdkVersionOption: '21'

- stage: SAST
  dependsOn: Build
  displayName: 'SAST Security Gates'
  jobs:
  - job: CheckstyleGate
    displayName: 'Checkstyle (code style + anti-patterns)'
    steps:
    - task: Maven@4
      displayName: 'Run Checkstyle'
      inputs:
        mavenPomFile: pom.xml
        goals: 'checkstyle:check'
        jdkVersionOption: '21'
    - task: PublishBuildArtifacts@1
      inputs:
        pathToPublish: target/security-reports/checkstyle
        artifactName: checkstyle-report

  - job: SpotBugsGate
    displayName: 'SpotBugs + Find-Sec-Bugs'
    dependsOn: CheckstyleGate
    steps:
    - task: Maven@4
      displayName: 'Run SpotBugs'
      inputs:
        mavenPomFile: pom.xml
        goals: 'spotbugs:check'
        jdkVersionOption: '21'
    - task: PublishBuildArtifacts@1
      inputs:
        pathToPublish: target/security-reports/spotbugs
        artifactName: spotbugs-report

  - job: OWASPGate
    displayName: 'OWASP Dependency Check (SCA)'
    dependsOn: SpotBugsGate
    steps:
    - task: Maven@4
      displayName: 'Run OWASP Dependency Check'
      inputs:
        mavenPomFile: pom.xml
        goals: 'dependency-check:check'
        jdkVersionOption: '21'
      env:
        NVD_API_KEY: $(NVD_API_KEY)   # stored in Azure DevOps pipeline variable group
    - task: PublishBuildArtifacts@1
      inputs:
        pathToPublish: target/security-reports/owasp
        artifactName: owasp-dependency-check-report

- stage: Test
  dependsOn: SAST   # Tests only run if SAST passes
  jobs:
  - job: UnitTests
    steps:
    - task: Maven@4
      inputs:
        goals: 'test'
        jdkVersionOption: '21'
8. STEP 8 — STORE NVD API KEY SECURELY: Register for a free NVD API key at https://nvd.nist.gov/developers/request-an-api-key. Store it in Azure DevOps pipeline variable group as a secret variable NVD_API_KEY. Reference it as $(NVD_API_KEY) in the pipeline YAML. NEVER commit it to source code.
9. STEP 9 — ADD JACOCO COVERAGE GATE alongside SAST: Ensure the 90% coverage gate (ADR §12) runs in the same SAST stage. Add to pom.xml:

<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution>
      <id>prepare-agent</id>
      <goals><goal>prepare-agent</goal></goals>
    </execution>
    <execution>
      <id>jacoco-check</id>
      <phase>verify</phase>
      <goals><goal>check</goal></goals>
      <configuration>
        <rules>
          <rule>
            <element>BUNDLE</element>
            <limits>
              <limit>
                <counter>LINE</counter>
                <value>COVEREDRATIO</value>
                <minimum>0.90</minimum>
              </limit>
            </limits>
          </rule>
        </rules>
      </configuration>
    </execution>
  </executions>
</plugin>
10. STEP 10 — SARIF REPORT UPLOAD TO AZURE DEVOPS: Publish SpotBugs and OWASP SARIF files to Azure DevOps Advanced Security for unified vulnerability tracking.

# In azure-pipelines.yml after each tool step:
- task: PublishBuildArtifacts@1
  displayName: 'Upload SpotBugs SARIF'
  inputs:
    pathToPublish: target/security-reports/spotbugs
    artifactName: CodeAnalysisLogs   # Azure DevOps Advanced Security picks up this artifact name

- task: PublishBuildArtifacts@1
  displayName: 'Upload OWASP SARIF'
  inputs:
    pathToPublish: target/security-reports/owasp
    artifactName: CodeAnalysisLogs

## Pitfalls
- OWASP Dependency Check first run downloads ~500MB from NVD — takes 20+ minutes. Always mirror the NVD database in a shared Azure DevOps cache or use an internal mirror for CI speed. Use the nvdDatafeedUrl config option to point to a cached mirror.
- NVD API key is REQUIRED from 2024 onwards — without it, Dependency Check is severely rate-limited and will fail or time out in CI. Register at https://nvd.nist.gov/developers/request-an-api-key and store as an Azure DevOps secret variable.
- SpotBugs runs on COMPILED bytecode — it MUST run after mvn compile, not on source. If you put it before the compile phase it will find nothing or fail.
- Find-Sec-Bugs version 1.13.0 is the latest compatible with SpotBugs 4.x. Do NOT mix versions — incompatible plugin versions cause ClassNotFoundException at scan time.
- failBuildOnCVSS is set to 7 per ADR §12. The OWASP site shows examples using 8 — override to 7 for this project. Do not silently change this threshold.
- Checkstyle violations are set to warning severity by default — change violationSeverity to 'warning' and failsOnError to true so any warning breaks the build. Do not set severity to 'error' only or you will miss warnings.
- OWASP suppression file entries MUST include an expiry date (until attribute) and a written justification. Suppressions without expiry are a security debt — they never get reviewed.
- SpotBugs with effort=Max + threshold=Low may produce a large number of false positives initially. Start with threshold=Medium for the first sprint, then lower to Low after establishing a baseline. Never set threshold=High in production gates.
- The SAST stage in Azure DevOps MUST be declared with dependsOn: Build and the Test stage MUST depend on SAST — this enforces the security gate ordering. If dependsOn is missing, stages run in parallel and tests can pass despite SAST failures.
- JaCoCo 0.8.12 is required for Java 17 bytecode support. Older versions (< 0.8.8) do not instrument Java 17 classes correctly and will report 0% coverage.

## Verification
1. mvn checkstyle:check — exits 0 with no violations
2. mvn spotbugs:check — exits 0; target/security-reports/spotbugs/spotbugsXml.xml exists
3. mvn dependency-check:check — exits 0; target/security-reports/owasp/dependency-check-report.html exists; no CRITICAL/HIGH CVEs >= 7 in report
4. mvn verify — all three tools + JaCoCo 90% gate pass in a single command
5. Azure DevOps pipeline SAST stage shows green; artifacts 'spotbugs-report' and 'owasp-dependency-check-report' are published
6. Deliberately introduce a hardcoded password string in a Java file — Checkstyle check should FAIL with 'Hardcoded secret detected' message
7. Add a known-vulnerable dependency (e.g., log4j 2.14.1) to pom.xml — OWASP check should FAIL with CVSS >= 7 finding
8. Azure DevOps Advanced Security tab shows findings from SARIF uploads under the CodeAnalysisLogs artifact