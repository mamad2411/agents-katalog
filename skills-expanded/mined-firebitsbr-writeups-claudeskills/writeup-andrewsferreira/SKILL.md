<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-andrewsferreira
description: CTF writeups and security challenges by andrewsferreira.
---

# Writeups by andrewsferreira

Source repository: `/repos/andrewsferreira`

## Repository Index

- pentest-reports-examples/Pentest_Report_Template-PT-BR.md
- pentest-reports-examples/Pentest_Report_Template_EN.md
- pentest-reports-examples/README.md

## Writeup Content


### File: pentest-reports-examples/README.md

# Pentest Report Templates

This repository provides **professional penetration testing report templates** designed for security consultants, Red Team professionals, and internal security teams. The templates are structured for **Web, API, and Cloud** testing, including technical vulnerabilities, business impact analysis, and mitigation recommendations.

---

## Repository Contents

### 1. Pentest_Report_Template.md
- **Idioma:** Português
- **Escopo:** Web, API (REST/GraphQL), Cloud (AWS)
- **Contém:**
  - 5 vulnerabilidades fictícias detalhadas
  - Referência OWASP Top 10, CWE e CVSS
  - Impacto de negócio e linguagem executiva
  - Recomendações de mitigação e priorização
  

### 2. Pentest_Report_Template_EN.md
- **Language:** English
- **Scope:** Web, API, and Cloud
- **Includes:**
  - 5 detailed fictitious vulnerabilities
  - OWASP Top 10, CWE, and CVSS references
  - Business impact and executive-level language
  - Mitigation recommendations and prioritization

---

## Purpose of the Templates

- Streamline **professional Pentest documentation**
- Demonstrate **technical expertise and business impact awareness**
- Serve as a foundation for **client reports or internal projects**
- Allow **quick reuse and customization** for real-world authorized Pentest engagements

---

## Usage Instructions

1. Download the desired template (Portuguese or English).  
2. Copy it into your project or repository directory.  
3. Populate sections such as **Scope, Evidence, and Recommendations** with real authorized Pentest data.  
4. Save or export to PDF if needed for client delivery or internal documentation.

---

## Notes

- Templates are **fictitious** and meant for demonstration purposes only.  
- **Never perform security tests without formal authorization** and defined scope.

---

## License

This repository is released under the **MIT License**. You are free to adapt the templates for professional use.



### File: pentest-reports-examples/Pentest_Report_Template-PT-BR.md

# Relatório de Teste de Intrusão (Pentest) - Template

## Informações Gerais
- **Cliente:** Empresa Fictícia Tech&Finance
- **Escopo:** Aplicação Web, APIs expostas (REST), Infraestrutura em Cloud (AWS)
- **Data de Início:** 01/08/2025
- **Data de Término:** 15/08/2025
- **Equipe:** Red Team - Andrews Ferreira (Especialista Sênior)
- **Tempo Total de Teste:** ~120 horas (média utilizada em companhias de tecnologia e financeiras)

---

## Metodologia Utilizada
O teste foi realizado com base em:
- **OWASP Web Security Testing Guide**
- **OWASP API Security Top 10**
- **NIST SP 800-115 (Technical Guide to Information Security Testing and Assessment)**
- **Boas práticas de mercado utilizadas por consultorias brasileiras como Tempest e Pride**

---

## Vulnerabilidades Encontradas

### 1. Injeção em API (OWASP API1:2023 - Broken Object Level Authorization)
**Descrição Técnica:**  
Foi identificada a possibilidade de manipulação direta dos parâmetros enviados para a API. Durante o fuzzing avançado, utilizando **GraphQL Introspection Abuse** e **Mass Assignment**, foi possível alterar dados sensíveis de outros usuários.  
**Impacto de Negócio:**  
Acesso não autorizado a dados financeiros de clientes, levando a **quebra de confiança, multas regulatórias e riscos de fraude**.  
**Mitigação Recomendada:**  
- Implementar **validação de payloads** no backend.  
- Aplicar **verificação de autorização em nível de objeto**.  
- Desabilitar introspecção em GraphQL em ambientes produtivos.  

---

### 2. Exposição de Credenciais em Cloud (OWASP A05:2021 - Security Misconfiguration)
**Descrição Técnica:**  
Durante a análise de buckets S3, foi encontrado um bucket com permissões de leitura pública contendo **chaves de acesso AWS**.  
**Impacto de Negócio:**  
Uso indevido da infraestrutura em cloud, levando a custos financeiros inesperados e possível **sequestro de ambiente**.  
**Mitigação Recomendada:**  
- Restringir permissões de buckets S3 apenas a usuários/autenticações necessárias.  
- Rotacionar imediatamente as credenciais expostas.  
- Implementar **Cloud Security Posture Management (CSPM)** para monitoramento contínuo.  

---

### 3. SQL Injection em Aplicação Web (OWASP A03:2021 - Injection)
**Descrição Técnica:**  
Durante testes de parâmetros em formulários, foi identificado que o endpoint `/login` não fazia uso de prepared statements, permitindo **SQL Injection** com extração de informações de tabelas de usuários.  
**Impacto de Negócio:**  
Exposição de dados de clientes e **risco de sanções legais (LGPD)**.  
**Mitigação Recomendada:**  
- Adotar **ORMs seguros** ou **prepared statements**.  
- Monitorar consultas SQL suspeitas.  
- Implementar **WAF com regras específicas**.  

---

### 4. Falha em Autenticação Multifator (OWASP A07:2021 - Identification and Authentication Failures)
**Descrição Técnica:**  
Foi identificado que a autenticação multifator (MFA) era opcional e podia ser **bypassada via manipulação de headers**.  
**Impacto de Negócio:**  
Usuários maliciosos poderiam assumir contas administrativas, resultando em **sequestro de contas críticas**.  
**Mitigação Recomendada:**  
- Tornar MFA **obrigatória** para todos os usuários privilegiados.  
- Validar corretamente tokens de sessão e headers.  
- Adotar **hardening de autenticação** com análise de comportamento.  

---

### 5. Exposição de Dados Sensíveis em Logs (OWASP A09:2021 - Security Logging and Monitoring Failures)
**Descrição Técnica:**  
Logs de aplicação estavam armazenando **tokens JWT em plaintext**, permitindo que qualquer analista interno tivesse acesso a sessões ativas.  
**Impacto de Negócio:**  
Possibilidade de **ataques internos e comprometimento da confidencialidade de dados de clientes**.  
**Mitigação Recomendada:**  
- Sanitizar dados sensíveis antes de gravar em logs.  
- Implementar **criptografia de logs**.  
- Monitorar acessos suspeitos a sistemas de logging.  

---

## Sumário Executivo (Visão de Negócio)
O teste de intrusão demonstrou que a empresa possui **falhas críticas em suas APIs e configurações de cloud**, que podem levar a impactos financeiros severos, perda de confiança dos clientes e riscos regulatórios (LGPD, Bacen, PCI-DSS).  

As vulnerabilidades mais críticas foram relacionadas a **API Injection** e **Exposição de Credenciais em Cloud**, as quais poderiam resultar em **acesso não autorizado a dados financeiros** e **comprometimento da infraestrutura**.  

---

## Recomendação Final
- Priorizar a correção das vulnerabilidades críticas em até **15 dias**.  
- Estabelecer um programa de **Pentest recorrente (trimestral)**.  
- Adotar **DevSecOps** com integração de segurança no pipeline de desenvolvimento.  

---

## Tempo Total do Teste
- **Web Application Pentest:** 40 horas  
- **API Pentest:** 45 horas  
- **Cloud Security Review:** 35 horas  
**Total:** ~120 horas

---

## Observações
Este é um **template fictício** para ser utilizado como base em relatórios de Pentest no GitHub.  



### File: pentest-reports-examples/Pentest_Report_Template_EN.md

# Penetration Test Report  
**Client:** FinTechCloud Inc. (Fictional)  
**Date:** August 2025  
**Tested by:** Security Research Team  

---

## 1. Executive Summary  

This penetration test focused on the evaluation of **Web Applications, APIs, and Cloud Infrastructure** used by FinTechCloud Inc. The objective was to identify vulnerabilities that could affect the **confidentiality, integrity, and availability** of systems handling financial transactions and customer data.  

The following report provides:  
- Technical details of each vulnerability  
- Business-level risk analysis  
- Recommended mitigation strategies  

**Testing Duration:** 3 weeks (120 hours)  
**Industry Reference:** Based on average testing engagements for U.S. financial institutions and technology companies.  

---

## 2. Scope  

**In-Scope Targets:**  
- Web Application: `https://portal.fintechcloud.com`  
- API: `https://api.fintechcloud.com/v1/`  
- Cloud Environment: AWS-hosted infrastructure (EC2, S3, IAM)  

**Testing Types:**  
- Web application security testing  
- API security assessment (REST endpoints)  
- Cloud misconfiguration review (AWS)  

---

## 3. Vulnerabilities Identified  

### 3.1 API Injection (Advanced Finding)  
- **OWASP Category:** API8:2023 – Injection  
- **Risk Level:** Critical  

**Technical Details:**  
During testing of the `/transactions` endpoint, it was possible to manipulate a query parameter with **NoSQL injection** techniques. The crafted payload:  
```json
{ "account_id": { "$ne": null } }
```  
allowed unauthorized enumeration of transaction records across multiple accounts.  

**Business Impact:**  
- Direct exposure of financial data (PCI-DSS violation).  
- Potential for **fraudulent transaction manipulation**.  
- High reputational damage if exploited externally.  

**Mitigation:**  
- Use parameterized queries or ORM sanitization.  
- Enforce strict schema validation at API gateway.  
- Apply rate limiting and monitoring with anomaly detection.  

---

### 3.2 Cloud Misconfiguration – Public S3 Bucket  
- **OWASP Category:** A06:2021 – Security Misconfiguration  
- **Risk Level:** High  

**Technical Details:**  
An AWS S3 bucket (`fintechcloud-logs`) was found publicly accessible, exposing **application logs with sensitive PII**.  

**Business Impact:**  
- Violation of U.S. data privacy regulations (GLBA, CCPA).  
- Logs containing PII could aid attackers in account takeover.  

**Mitigation:**  
- Enforce **S3 Block Public Access**.  
- Implement AWS Config rules to continuously check for misconfigurations.  
- Encrypt logs and integrate with centralized SIEM.  

---

### 3.3 Weak Authentication Mechanism  
- **OWASP Category:** A07:2021 – Identification and Authentication Failures  
- **Risk Level:** High  

**Technical Details:**  
The login mechanism allowed **brute-force attacks** without CAPTCHA or IP throttling. Account lockout was not enforced after multiple failed attempts.  

**Business Impact:**  
- Credential stuffing attacks possible with leaked password lists.  
- Potential for **unauthorized access to customer accounts**.  

**Mitigation:**  
- Enforce MFA across all user accounts.  
- Implement IP-based throttling and lockout mechanisms.  
- Monitor login anomalies via SIEM.  

---

### 3.4 Cross-Site Scripting (XSS) – Web Portal  
- **OWASP Category:** A03:2021 – Injection (XSS)  
- **Risk Level:** Medium  

**Technical Details:**  
Reflected XSS was found on the **feedback form** of the portal:  
```html
<script>alert('XSS')</script>
```  

**Business Impact:**  
- Exploitation could allow session hijacking.  
- Regulatory implications for **data confidentiality breaches**.  

**Mitigation:**  
- Implement context-aware output encoding (CSP, sanitization).  
- Use modern frameworks with built-in XSS protection.  

---

### 3.5 Insufficient Logging & Monitoring  
- **OWASP Category:** A09:2021 – Security Logging and Monitoring Failures  
- **Risk Level:** Medium  

**Technical Details:**  
Critical API requests (e.g., transaction creation) were not logged adequately. Additionally, AWS CloudTrail had gaps in IAM activity tracking.  

**Business Impact:**  
- Delayed detection of fraud or insider threats.  
- Non-compliance with **financial regulatory standards** (SOX, PCI-DSS).  

**Mitigation:**  
- Enable centralized logging (SIEM integration).  
- Activate CloudTrail with full logging on all regions.  
- Implement automated alerting for suspicious activities.  

---

## 4. Business Risk Summary  

| Vulnerability                     | Technical Risk | Business Impact | Priority |
|----------------------------------|----------------|-----------------|----------|
| API Injection                    | Critical       | Customer data leakage & fraud | 🚨 Immediate |
| Cloud Misconfiguration (S3)      | High           | Privacy breach & compliance fines | 🔴 High |
| Weak Authentication              | High           | Unauthorized account access | 🔴 High |
| XSS (Web Portal)                 | Medium         | Session hijacking | 🟠 Medium |
| Insufficient Logging & Monitoring | Medium         | Fraud undetected | 🟠 Medium |

---

## 5. Testing Timeline  

**Total Engagement:** ~120 hours  
- Web Application Testing → 40 hours  
- API Testing (advanced injection) → 40 hours  
- Cloud Infrastructure (AWS) → 30 hours  
- Reporting & Executive Brief → 10 hours  

**Industry Benchmark:**  
This duration aligns with **financial and technology sector penetration testing** engagements in the U.S. (2–4 weeks).  

---

## 6. Conclusion  

The assessment revealed **critical vulnerabilities** in API handling and cloud configurations. Exploitation could result in **regulatory fines, financial fraud, and loss of customer trust**.  

Immediate remediation of **API injection and cloud misconfigurations** is strongly recommended, followed by reinforcement of authentication mechanisms and logging improvements.  

