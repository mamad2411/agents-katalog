<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-dan2melz
description: CTF writeups and security challenges by dan2melz.
---

# Writeups by dan2melz

Source repository: `/repos/dan2melz`

## Repository Index

- danielmelendez.github.io/README.md
- danielmelendez.github.io/ai-cloud-monitor/ai-cloud-monitor/README.md

## Writeup Content


### File: danielmelendez.github.io/README.md

Daniel Melendez AI and Cybersecurity Portfolio

About Me
CISSP-certified Cloud Security Engineer with expertise in AI cybersecurity and cloud automation Passionate about securing AI-driven systems detecting adversarial threats and automating compliance in AWS Azure and GCP environments

LinkedIn linkedincomindanielmelendez1  
GitHub githubcomdanielmelendez

Featured Projects

AI-Powered Cloud Security Monitor
Description
- Uses AI to analyze AWS logs for unauthorized access and anomalies
- Detects IAM misconfigurations privilege escalation and potential threats
- Sends alerts via SNS or Slack when security risks are detected

Tech Used Python AWS Boto3 CloudWatch OpenAI GPT  
GitHub Repo githubcomdanielmelendezai-cloud-monitor

AI Adversarial Attack Defense
Description
- Simulates adversarial attacks on ML models
- Demonstrates how AI models can be manipulated using evasion techniques
- Provides defense strategies for real-world AI security

Tech Used TensorFlow PyTorch CleverHans Library  
GitHub Repo githubcomdanielmelendezai-attack-defense

Cloud Pentesting Report AWS Security Audit
Description
- A professional AWS pentesting report on misconfigurations and attack vectors
- Includes IAM privilege escalation risks S3 misconfigurations and Lambda backdoors
- Features recommendations for hardening cloud security

Tools Used AWS IAM Analyzer Prowler Pacu  
Report PDF danielmelendezcomaws-pentest

Automated Security Compliance Checker
Description
- Scans AWS environments for compliance with NIST CIS and FedRAMP
- Uses Python and Boto3 to check for public S3 buckets weak IAM policies and MFA enforcement
- Generates an automated compliance report in markdown or PDF

Tech Used Python AWS Config Boto3 CloudFormation  
GitHub Repo githubcomdanielmelendezcompliance-checker

Certifications
AWS Certified Solutions Architect Professional  
AWS Certified DevOps Engineer Professional  
CISSP CCSP Azure AI Engineer Associate  
AI Security and Adversarial AI Research  

Contact Me
Email dan2melzgmailcom  
Website danielmelendezcom

How to Use This Portfolio
1 Check out the GitHub repos for code samples and security automation scripts
2 Download reports for security research and compliance insights
3 Connect on LinkedIn to discuss AI security cloud and compliance topics

Passionate about AI-driven security solutions Lets collaborate



### File: danielmelendez.github.io/ai-cloud-monitor/ai-cloud-monitor/README.md

# AI-Powered Cloud Security Monitor

## Overview
This project scans AWS IAM user activity and detects anomalies in access key usage. It flags unused keys older than 90 days to improve security.

## Installation & Setup
1. Install dependencies:
   ```bash
   pip install boto3
   ```
2. Configure AWS credentials:
   ```bash
   aws configure
   ```
3. Run the script:
   ```bash
   python ai_cloud_monitor.py
   ```

## How It Works
- Retrieves IAM users from AWS.
- Checks access key usage history.
- Flags access keys unused for **90+ days** as potential security risks.

## Example Output
```
Checking activity for user: admin-user
[ALERT] admin-user has an old access key that hasn't been used in 120 days!
```

## Future Enhancements
- Implement **machine learning-based** anomaly detection.
- Add **Slack/SNS notifications** for real-time alerts.

