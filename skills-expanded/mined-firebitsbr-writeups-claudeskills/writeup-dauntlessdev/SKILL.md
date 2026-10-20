<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-dauntlessdev
description: CTF writeups and security challenges by DauntlessDev.
---

# Writeups by DauntlessDev

Source repository: `/repos/DauntlessDev`

## Repository Index

- bug-bounty-platform/README.md

## Writeup Content


### File: bug-bounty-platform/README.md

# Bug Bounty Platform

A microservices-based bug bounty platform built with Go, enabling secure bug reporting and bounty management.

## Overview

This platform connects security researchers with organizations through a streamlined bug bounty process. Built using microservices architecture, it demonstrates modern Go development practices including gRPC communication, event-driven patterns, and secure payment handling.

## Architecture

The platform consists of three core microservices:

- **Auth Service** - Handles user authentication, authorization, and profile management
- **Bounty Service** - Manages bug reports, bounty lifecycle, and claim processing
- **Wallet Service** - Processes payments, escrow management, and fund transfers

## Tech Stack

- **Backend**: Go 1.21+
- **API**: gRPC and REST
- **Database**: PostgreSQL
- **Cache**: Redis
- **Message Queue**: RabbitMQ
- **Containerization**: Docker
- **Deployment**: Docker Compose (local) / Kubernetes (production)

## Project Structure

```
bug-bounty-platform/
├── services/
│   ├── auth/
│   ├── bounty/
│   └── wallet/
├── pkg/           # Shared packages
├── deployments/   # Docker and K8s configs
├── docs/          # API and architecture documentation
└── scripts/       # Build and deployment scripts
```

## Core Features

### Bounty Service (Current Focus)
- Create and manage bug bounties
- Claim and track bounty progress
- Submit bug fixes with proof
- Automated status management
- Dispute resolution system

### Planned Features
- Multi-factor authentication
- Real-time notifications
- Reputation system
- Automated payouts
- Analytics dashboard

## Getting Started

### Prerequisites
- Go 1.21 or higher
- Docker and Docker Compose
- PostgreSQL 15
- Redis 7

### Installation

```bash
# Clone the repository
git clone https://github.com/DauntlessDev/bug-bounty-platform.git
cd bug-bounty-platform

# Run with Docker Compose
docker-compose up

# Or run individual services
cd services/bounty
go run cmd/main.go
```

### Configuration

Environment variables:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bugbounty
REDIS_URL=localhost:6379
JWT_SECRET=your-secret-key
```

## API Documentation

API documentation is available at:
- REST API: `/api/v1/docs`
- gRPC: See proto files in `services/*/api/proto/`

## Development

### Running Tests
```bash
make test
```

### Code Standards
- Follow standard Go project layout
- Use table-driven tests
- Maintain >80% test coverage
- Run `golangci-lint` before commits

## Roadmap

- [x] Core bounty service implementation
- [ ] Authentication service
- [ ] Wallet service integration
- [ ] Admin dashboard
- [ ] Mobile application
- [ ] Advanced analytics

## Contributing

This is a personal portfolio project, but suggestions and feedback are welcome through issues.

## License

MIT License - see LICENSE file for details

## Author

Rom Braveheart Leuterio
- Email: leuteriobrave@gmail.com
- LinkedIn: [braveleuterio](https://www.linkedin.com/in/braveleuterio)
- Portfolio: [dauntlessdev](https://dauntlessdev.netlify.app/)
