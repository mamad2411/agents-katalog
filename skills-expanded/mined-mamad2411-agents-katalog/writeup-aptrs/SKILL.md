<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-aptrs
description: CTF writeups and security challenges by APTRS.
---

# Writeups by APTRS

Source repository: `/repos/APTRS`

## Repository Index

- APTRS/CODE_OF_CONDUCT.md
- APTRS/CONTRIBUTING.md
- APTRS/LICENSE.md
- APTRS/README.md
- APTRS/SECURITY.md
- APTRS/frontend/README.md
- APTRS/.github/ISSUE_TEMPLATE/bug_report.md
- APTRS/.github/ISSUE_TEMPLATE/feature_request.md

## Writeup Content


### File: APTRS/README.md



# APTRS
<p align="center">
  <img src="https://repository-images.githubusercontent.com/558932728/6a0fb8ea-a539-4ba6-8ef8-2ee7fb0b3f17" width="500" height="400"/>
</p>
APTRS (Automated Penetration Testing Reporting System) is a Python and Django-based automated reporting tool designed for penetration testers and security organizations. This tool streamlines the report generation process by enabling users to create PDF and Excel reports directly, eliminating the need for manual approaches. Additionally, APTRS offers a systematic way to monitor and manage vulnerabilities within various projects. Keep your penetration testing projects organized and efficient with APTRS.
<br/><br/>

[![sponsors](https://img.shields.io/github/sponsors/Anof-cyber)](https://github.com/sponsors/Anof-cyber)
[![Python Version](https://img.shields.io/badge/Python-3.9+-brightgreen)](https://www.python.org/downloads/release/python-391/)
[![NodeJS Version](https://img.shields.io/badge/NodeJS-18+-brightgreen)](https://nodejs.org/en/download/package-manager)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/APTRS/APTRS?include_prereleases)
![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/APTRS/aptrs)
[![platform](https://img.shields.io/badge/platform-osx%2Flinux%2Fwindows-green.svg)](https://github.com/APTRS/APTRS)
[![Django Build](https://github.com/Anof-cyber/APTRS/actions/workflows/django.yml/badge.svg)](https://github.com/Anof-cyber/APTRS/actions/workflows/django.yml)
[![Frontend Test and Build](https://github.com/APTRS/APTRS/actions/workflows/frontend.yml/badge.svg)](https://github.com/APTRS/APTRS/actions/workflows/frontend.yml)
[![Docker Image CI](https://github.com/APTRS/APTRS/actions/workflows/docker.yml/badge.svg)](https://github.com/APTRS/APTRS/actions/workflows/docker.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/fce97190bae94040823a2994c0722ea8)](https://app.codacy.com/gh/Anof-cyber/APTRS/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=Anof-cyber_APTRS&metric=security_rating&branch=main)](https://sonarcloud.io/summary/new_code?id=Anof-cyber_APTRS&branch=API)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=Anof-cyber_APTRS&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=Anof-cyber_APTRS)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Anof-cyber_APTRS&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Anof-cyber_APTRS)
[![CodeQL](https://github.com/Anof-cyber/APTRS/actions/workflows/codeql.yml/badge.svg)](https://github.com/Anof-cyber/APTRS/actions/workflows/codeql.yml)
[![Build and Publish to GitHub Container Registry](https://github.com/APTRS/APTRS/actions/workflows/ghcr-latest.yml/badge.svg)](https://github.com/APTRS/APTRS/actions/workflows/ghcr-latest.yml)
[![Twitter](https://img.shields.io/twitter/follow/ano_f_)](https://twitter.com/Ano_F_)
![GitHub contributors from allcontributors.org](https://img.shields.io/github/all-contributors/aptrs/aptrs)


## Documentation

> [!Note]
> Please ensure to review the Installation and Deployment Guide from the documentation.



[<img src="https://i.ibb.co/qnssqbJ/doc.png" alt="APTRS Documentation" width="220" height="45">](https://aptrs.com)
[<img src="https://fetch.usebruno.com/button.svg" alt="Fetch in Bruno" style="width: 220; height: 45;" width="220" height="45">](https://fetch.usebruno.com?url=https%3A%2F%2Fgithub.com%2FAPTRS%2FAPI-Doc "target=_blank rel=noopener noreferrer")



- Try APTRS Live - [https://live.aptrs.com](https://live.aptrs.com)

> [!NOTE]
> Default creds are sourav.kalal@aptrs.com & I-am-Weak-Password-Please-Change-Me

Quick Installation

> [!Warning]
> Please ensure to review the documentation for Security Configuration for ENV and other Installation methods.

```bash
git clone https://github.com/APTRS/APTRS
cd APTRS
cp env.docker .env
nano .env
docker-compose up
```



<!-- GitAds-Verify: C2E2P14Y337DTQ2X2BGXTNJW5Y4LVWUP -->

## Features
- Manage Vulnerabilities
- Custom Report Template in Docx or HTML/CSS
- Manage All Projects in one place
- Maintain the Vulnerability Database
- Customer Dashboard, allow customer to login and check projects and download reports
- Easily Generate PDF, DOCX and Excel Report
- Easily Customize PDF and DOCX Report Template
- Dynamically add POC, Description and Recommendations
- Manage Customers and Companies
- Manage Project Status, Schedules and Retest


## Support APTRS

APTRS is an open-source project that takes significant time and effort to maintain. If you're using APTRS in your work or find it valuable, please consider supporting its development.

<div align="center">
  <table>
    <tr>
      <td align="center">
        <h3>🚀 Why Support?</h3>
        <ul align="left">
          <li>Ensure active development of new features</li>
          <li>Help maintain and improve existing functionality</li>
          <li>Support faster bug fixes and timely updates</li>
          <li>Enable better documentation and tutorials</li>
          <li>Show appreciation for a tool you use professionally</li>
        </ul>
      </td>
      <td align="center" width="350">
        <div style="border: 1px solid #e1e4e8; border-radius: 6px; padding: 16px; background-color: #f6f8fa;">
          <h3>Bitcoin Donations</h3>
          <img src="https://raw.githubusercontent.com/APTRS/APTRS-Changelog/refs/heads/main/images/BTC.png" alt="BTC Wallet QR Code" width="200" height="200" style="border-radius: 10px;">
          <p><code>bc1qusxngf2w5gl2g8hw82ggct59227k4963f9fwhm</code></p>
        </div>
      </td>
    </tr>
  </table>

  <div style="margin-top: 20px;">
    <a href="https://github.com/sponsors/APTRS">
      <img src="https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&style=for-the-badge&color=%23fe8e86" alt="Sponsor APTRS">
    </a>
  </div>

  <p><em>Your support makes a meaningful difference in keeping this project alive and evolving!</em> 💖</p>
</div>

## Sponsor

<p>This project is supported by:</p>
<p>
  <a href="https://m.do.co/c/daa899c901f2">
    <img src="https://opensource.nyc3.cdn.digitaloceanspaces.com/attribution/assets/SVG/DO_Logo_horizontal_blue.svg" width="201px">
  </a>
</p>



## Security

If you discover any security vulnerabilities in this open-source project, please responsibly disclose it by referring to our [Security Policy](https://github.com/Anof-cyber/APTRS/security/policy). We appreciate and value your efforts to improve the security of this project.

## GitAds Sponsored
[![Sponsored by GitAds](https://gitads.dev/v1/ad-serve?source=aptrs/aptrs@github)](https://gitads.dev/v1/ad-track?source=aptrs/aptrs@github)



## Contributors ✨

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://souravkalal.tech/"><img src="https://avatars.githubusercontent.com/u/39705906?v=4?s=100" width="100px;" alt="Sourav Kalal"/><br /><sub><b>Sourav Kalal</b></sub></a><br /><a href="#maintenance-anof-cyber" title="Maintenance">🚧</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/djscruggs"><img src="https://avatars.githubusercontent.com/u/41671?v=4?s=100" width="100px;" alt="DJ Scruggs"/><br /><sub><b>DJ Scruggs</b></sub></a><br /><a href="https://github.com/APTRS/APTRS/commits?author=djscruggs" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/noraj"><img src="https://avatars.githubusercontent.com/u/16578570?v=4?s=100" width="100px;" alt="Alexandre ZANNI"/><br /><sub><b>Alexandre ZANNI</b></sub></a><br /><a href="https://github.com/APTRS/APTRS/commits?author=noraj" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/0xdeviner"><img src="https://avatars.githubusercontent.com/u/61959752?v=4?s=100" width="100px;" alt="Hitesh Patra"/><br /><sub><b>Hitesh Patra</b></sub></a><br /><a href="https://github.com/APTRS/APTRS/commits?author=0xdeviner" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->


## Authors

- [Sourav Kalal](https://twitter.com/Ano_F_)



### File: APTRS/frontend/README.md


## What is this?

aptrs-react is a React front end to the [Automated Penetration Testing Reporting System](https://github.com/Anof-cyber/APTRS)

Written in TypeScript, this app uses no server resources except to deliver the JavaScript bundle. The back end relies on the APTRS [API](https://www.postman.com/anof-cyber/workspace/aptrs/collection/24236036-131e5e02-32e5-45be-9c15-02c91fe9230a)

## Installation

`npm install`

Note that this will also install a custom build of CK Editor in the `/packages/ckeditor` director

There is a file called `env.example` in the root of the project that you will need to customize. Copy it to `.env` or `.env.local` and add the API url.

## Available Scripts

In the project directory, you can run:

`npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

`npm test`

Launches the test runner in the interactive watch mode.\


`npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the docs about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.





### File: APTRS/.github/ISSUE_TEMPLATE/bug_report.md

---
name: Bug report
about: Create a report to help us improve
title: ''
labels: bug
assignees: ''

---

# Make sure you have gone through the Documentation
https://anof-cyber.github.io/APTRS/#/

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Desktop (please complete the following information):**
 - OS: [e.g. iOS]
 - Browser [e.g. chrome, safari]
 - Python Version [e.g. 3.10]
 - Pip Version[e.g. 20]
 - wkhtmltopdf Version [e.g. 0.12.6-3]
 
**Additional context**
Add any other context about the problem here.



### File: APTRS/.github/ISSUE_TEMPLATE/feature_request.md

---
name: Feature request
about: Suggest an idea for this project
title: ''
labels: enhancement
assignees: ''

---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.



### File: APTRS/CODE_OF_CONDUCT.md

# Contributor Covenant Code of Conduct

## Our Pledge

We as members, contributors, and leaders pledge to make participation in our
community a harassment-free experience for everyone, regardless of age, body
size, visible or invisible disability, ethnicity, sex characteristics, gender
identity and expression, level of experience, education, socio-economic status,
nationality, personal appearance, race, religion, or sexual identity
and orientation.

We pledge to act and interact in ways that contribute to an open, welcoming,
diverse, inclusive, and healthy community.

## Our Standards

Examples of behavior that contributes to a positive environment for our
community include:

* Demonstrating empathy and kindness toward other people
* Being respectful of differing opinions, viewpoints, and experiences
* Giving and gracefully accepting constructive feedback
* Accepting responsibility and apologizing to those affected by our mistakes,
  and learning from the experience
* Focusing on what is best not just for us as individuals, but for the
  overall community

Examples of unacceptable behavior include:

* The use of sexualized language or imagery, and sexual attention or
  advances of any kind
* Trolling, insulting or derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or email
  address, without their explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

## Enforcement Responsibilities

Community leaders are responsible for clarifying and enforcing our standards of
acceptable behavior and will take appropriate and fair corrective action in
response to any behavior that they deem inappropriate, threatening, offensive,
or harmful.

Community leaders have the right and responsibility to remove, edit, or reject
comments, commits, code, wiki edits, issues, and other contributions that are
not aligned to this Code of Conduct, and will communicate reasons for moderation
decisions when appropriate.

## Scope

This Code of Conduct applies within all community spaces, and also applies when
an individual is officially representing the community in public spaces.
Examples of representing our community include using an official e-mail address,
posting via an official social media account, or acting as an appointed
representative at an online or offline event.

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported to the community leaders responsible for enforcement at
.
All complaints will be reviewed and investigated promptly and fairly.

All community leaders are obligated to respect the privacy and security of the
reporter of any incident.

## Enforcement Guidelines

Community leaders will follow these Community Impact Guidelines in determining
the consequences for any action they deem in violation of this Code of Conduct:

### 1. Correction

**Community Impact**: Use of inappropriate language or other behavior deemed
unprofessional or unwelcome in the community.

**Consequence**: A private, written warning from community leaders, providing
clarity around the nature of the violation and an explanation of why the
behavior was inappropriate. A public apology may be requested.

### 2. Warning

**Community Impact**: A violation through a single incident or series
of actions.

**Consequence**: A warning with consequences for continued behavior. No
interaction with the people involved, including unsolicited interaction with
those enforcing the Code of Conduct, for a specified period of time. This
includes avoiding interactions in community spaces as well as external channels
like social media. Violating these terms may lead to a temporary or
permanent ban.

### 3. Temporary Ban

**Community Impact**: A serious violation of community standards, including
sustained inappropriate behavior.

**Consequence**: A temporary ban from any sort of interaction or public
communication with the community for a specified period of time. No public or
private interaction with the people involved, including unsolicited interaction
with those enforcing the Code of Conduct, is allowed during this period.
Violating these terms may lead to a permanent ban.

### 4. Permanent Ban

**Community Impact**: Demonstrating a pattern of violation of community
standards, including sustained inappropriate behavior,  harassment of an
individual, or aggression toward or disparagement of classes of individuals.

**Consequence**: A permanent ban from any sort of public interaction within
the community.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage],
version 2.0, available at
https://www.contributor-covenant.org/version/2/0/code_of_conduct.html.

Community Impact Guidelines were inspired by [Mozilla's code of conduct
enforcement ladder](https://github.com/mozilla/diversity).

[homepage]: https://www.contributor-covenant.org

For answers to common questions about this code of conduct, see the FAQ at
https://www.contributor-covenant.org/faq. Translations are available at
https://www.contributor-covenant.org/translations.



### File: APTRS/CONTRIBUTING.md

# Contributing to APTRS

Thank you for your interest in contributing to APTRS! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
  - [Setting Up Development Environment](#setting-up-development-environment)
  - [Project Structure](#project-structure)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Pull Requests](#pull-requests)
- [Development Workflow](#development-workflow)
  - [Branching Strategy](#branching-strategy)
  - [Commit Guidelines](#commit-guidelines)
  - [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [Community](#community)

## Code of Conduct

This project follows our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

### Setting Up Development Environment

> **Note:** It is recommended to use Linux or macOS for development. Windows can work for code development, but Redis will not work properly on Windows.

#### Prerequisites

- **PostgreSQL**: Install and configure a PostgreSQL database
- **Redis**: Required for task queuing and caching
- **Poetry**: Required for dependency management (do not use pip)
- **Node.js & npm**: Required for frontend development

#### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/APTRS.git
   cd APTRS
   ```

2. **Install backend dependencies with Poetry**
   ```bash
   poetry install
   ```

3. **Configure environment variables**
   ```bash
   cp APTRS/env.example .env
   # Edit .env with your configuration including PostgreSQL and Redis details
   # Refer to the installation documentation page for detailed environment configuration
   ```

4. **First-time setup (initializes accounts, permissions, migrations, etc.)**
   ```bash
   poetry run python APTRS/manage.py first_setup
   ```

5. **Start the development server**
   ```bash
   poetry run python APTRS/manage.py runserver
   ```

#### Frontend Setup

1. **Navigate to the frontend directory**
   ```bash
   cd frontend
   ```

2. **Install frontend dependencies**
   ```bash
   npm install
   ```

3. **Configure frontend environment**
   ```bash
   cp env.example .env
   # Edit .env to include backend API domain/IP address
   ```

4. **Start the frontend development server**
   ```bash
   npm start
   ```

#### Important Domain/Port Considerations

- Backend and frontend should ideally run on the same domain and port (using a reverse proxy in production)
- In development, they can run on different ports/domains, but make sure to configure the frontend `.env` with the correct backend API address
- Certain features may not work properly when running on separate domains/ports:
  - Loading images in CKEditor after upload
  - Rendering vulnerability or project data with embedded images
  - Loading report CSS files
  - And others (refer to documentation for details)

- **Before submitting a PR**: Test your changes with both frontend and backend running on the same port/IP to ensure you don't break any domain-dependent features

### Project Structure

- `APTRS/` - Main Django project
- `accounts/` - User authentication and management
- `project/` - Project management functionality
- `vulnerability/` - Vulnerability tracking
- `utils/` - Shared utility functions
- `templates/` - HTML templates
- `frontend/` - Frontend code

## How to Contribute

### Reporting Bugs

When reporting bugs, please include:

- A clear, descriptive title
- Steps to reproduce the bug
- Expected behavior vs. actual behavior
- Screenshots if applicable
- Environment details (OS, browser, etc.)

To report a bug, open an issue using the bug report template.

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

- A clear description of the enhancement
- Rationale (why this would be useful)
- Possible implementation approaches if you have suggestions

### Pull Requests

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes following our [commit guidelines](#commit-guidelines)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Workflow

### Branching Strategy

- `main` - Production-ready code
- `develop` - Development branch, base for feature branches
- `feature/*` - New features or improvements
- `fix/*` - Bug fixes
- `hotfix/*` - Critical fixes for production

### Commit Guidelines

- Use concise, descriptive commit messages
- Start with a verb in imperative mood (e.g., "Add", "Fix", "Update")
- Reference issue numbers when applicable

Example:
```
Add image upload functionality for project POCs

- Implement MultiPartParser for handling image uploads
- Generate unique filenames with UUID
- Store images in designated 'poc' directory
- Return URL for retrieving the image

Fixes #123
```

### Code Style

- Follow PEP 8 guidelines for Python code
- Use 4 spaces for indentation (not tabs)
- Use meaningful variable and function names
- Keep lines under 100 characters where possible
- Include docstrings for classes and functions

## Testing

- Write tests for new functionality
- Ensure all tests pass before submitting a pull request
- Run tests using:
  ```bash
  poetry run python APTRS/manage.py test
  ```

## Documentation

- Update documentation when changing functionality
- Document new features, APIs, and configuration options
- Use clear, concise language accessible to all users

## Community

- Join our community discussions
- Help answer questions from other contributors
- Share your experiences using the project

Thank you for contributing to APTRS!


### File: APTRS/LICENSE.md

MIT License

Copyright (c) 2022 APTRS

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


### File: APTRS/SECURITY.md

# Security Policy

## Supported Versions

Please refer to this table to understand the currently supported versions of the project that receive security updates.

| Version | Supported          |
| ------- | ------------------ |
| 0.x.x   | :x:                |
| 1.x.x   | :x:                |
| 2.x.x   | :white_check_mark: |


## Reporting a Vulnerability

We appreciate and encourage responsible disclosure of security vulnerabilities within this open-source project. If you discover any vulnerabilities or security issues, please report them to us by emailing kalalsourav20@gmail.com. We value your efforts to enhance the security of this project and kindly request that you provide details on the vulnerability discovered.

Please note that this project is an open-source initiative and, as such, we do not offer monetary rewards for reported vulnerabilities. However, contributors who responsibly disclose valid issues will be acknowledged and credited within the project.


**Important Security Considerations for APTRS:**

- **Rate Limiting:** The application includes features that could be affected by rate limiting; however, reports on rate limiting will not be considered security issues unless they demonstrate further exploitation that could lead to significant impact or compromise of the system.

- **High-Priority Vulnerabilities:** APTRS utilizes features that may lead to the following security concerns:
  - **Server-Side Template Injection (SSTI):** Due to dynamic template rendering features for HTML to PDF and DOCX reports using Jinja2 with `docxtpl`.
  - **Path Traversal:** Because of the file access functionalities, especially in the delete image API.
  - **File Upload Vulnerabilities:** Given the application's support for file uploads, particularly for Proof of Concept (POC) image uploads.
  - **Server-Side Request Forgery (SSRF):** Due to the application’s interaction with external URLs in HTML to PDF and DOCX reports.

- **User Configuration Requirements:** Some security implementations require configuration from users, such as whitelisted IPs or domains. Bypassing such restrictions will be considered a security issue, whereas misconfigured settings from the user end will not be treated as a vulnerability.

  These areas are critical for APTRS, and we have implemented robust security checks to prevent exploitation. However, due to the inherent risks associated with these features, we are particularly concerned about potential bypasses or misconfigurations. Reports identifying vulnerabilities or bypasses in these categories will be treated with the highest priority.

