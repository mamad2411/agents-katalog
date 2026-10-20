# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Cool-Admin backend project built with Node.js, TypeScript, and the MidwayJS framework. It's an administrative management system with features like AI coding, permission management, multi-tenancy, and modular architecture.

- **Framework**: MidwayJS (Koa.js based)
- **Language**: TypeScript
- **Database**: PostgreSQL (previously MySQL), with TypeORM 0.3.20
- **Version**: 8.x
- **Admin Framework**: Cool-Admin MidwayJS

## Common Development Commands

### Development

```bash
npm run dev          # Start development server with local environment
npm run preview      # Start preview server with production environment
npm start            # Start production server
```

### Testing

```bash
npm test             # Run tests with local environment
npm run cov          # Run tests with coverage
```

### Code Quality

```bash
npm run lint         # Check code style with mwts
npm run lint:fix     # Fix code style issues
npm run format       # Format code with prettier
```

### Build & Deployment

```bash
npm run build        # Build for production
npm run build:obfuscate  # Build with code obfuscation
npm run pkg          # Package as executable
```

### Environment Management

```bash
npm run encrypt:local    # Encrypt local environment file
npm run encrypt:prod     # Encrypt production environment file
npm run decrypt:local    # Decrypt local environment file
npm run decrypt:prod     # Decrypt production environment file
```

## Project Architecture

### Directory Structure

```
src/
├── config/                    # Environment configurations
│   ├── config.default.ts     # Default config (all environments)
│   ├── config.local.ts       # Local development config
│   └── config.prod.ts        # Production config
├── modules/                   # Modular architecture
│   ├── base/                 # Core permission management
│   ├── demo/                 # Demo functionality
│   ├── dict/                 # Dictionary management
│   ├── plugin/               # Plugin system
│   ├── space/                # Space management
│   ├── task/                 # Task scheduling
│   └── user/                 # User management
├── comm/                     # Common utilities
└── configuration.ts          # MidwayJS configuration
```

### Module Structure

Each module follows this pattern:

```
modules/[module-name]/
├── controller/               # API endpoints
│   ├── admin/               # Admin panel APIs
│   └── app/                 # Application APIs
├── entity/                  # Database entities
├── service/                 # Business logic
├── dto/                     # Data validation
├── middleware/              # Module-specific middleware
├── config.ts                # Module configuration
├── db.json                  # Database initialization data
└── menu.json                # Menu initialization data
```

## Development Guidelines

### Database & Entities

- Use TypeORM 0.3.20 without foreign key relationships (@ManyToOne, @OneToMany are forbidden)
- Entity fields use camelCase naming (e.g., `studentNo`)
- All entities extend `BaseEntity` from `'../../base/entity/base'`
- Entities should be in `src/modules/[module]/entity/` directory

### Controllers

- Use `@CoolController` decorator for rapid CRUD generation
- Support automatic API generation: `['add', 'delete', 'update', 'info', 'list', 'page']`
- Do not override CRUD methods (`add`, `delete`, `update`, `info`, `list`, `page`) in Controller
- Controllers do not need `@Provide()` decorator
- Use camelCase for API endpoints, avoid nested paths like `/student/detail` → use `/studentDetail`

### Services

- Extend `BaseService` for common functionality
- Business logic should be in Service layer, not Controller
- Use TypeORM repository patterns for database operations
- Support for both TypeORM queries and raw SQL when needed

### File Naming

- Use snake_case for file names (e.g., `student_info.ts`)
- Keep file names concise within module context (e.g., `info.ts` not `student_info.ts`)

### Code Style

- Always respond in Chinese, including code comments
- Use `@midwayjs/core` instead of deprecated `@midwayjs/decorator`
- Avoid custom SQL for basic operations; use TypeORM APIs
- For statistics or complex queries, raw SQL is acceptable

## Configuration Notes

### Environment Files

- `.env.local` - Local development environment
- `.env.prod` - Production environment
- Environment files can be encrypted/decrypted using dotenvx

### Database Configuration

The project supports multiple databases (MySQL, PostgreSQL, SQLite). Database configuration is in `src/config/config.local.ts` and `src/config/config.prod.ts`.

### JWT Configuration

JWT settings are in the base module config with:

- Token expiry: 2 hours
- Refresh token expiry: 15 days
- Single sign-on support

## Module Development

When creating new modules, refer to the Cursor rules in `.cursor/rules/`:

- `module.mdc` - Module structure guidelines
- `controller.mdc` - Controller implementation patterns
- `service.mdc` - Service implementation patterns
- `db.mdc` - Database operation guidelines

## Testing

The project uses Jest with TypeScript support. Test files should be placed in the `test/` directory and follow the naming pattern `*.test.ts`.
