# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Acore is a Java-based Velocity Minecraft proxy server plugin that collects player data and stores it in a MySQL database, with QQ bot integration via MiraiMC.

## Technology Stack

- **Java 17** - Primary language
- **Gradle** - Build automation
- **Velocity API** - Minecraft proxy framework
- **MySQL** - Database storage
- **HikariCP** - Connection pooling
- **MiraiMC** - QQ bot integration
- **bStats** - Plugin metrics
- **Sponge Configurate** - Configuration management

## Build Commands

```bash
# Build the project (creates shadow JAR)
./gradlew build

# Run Velocity server for testing
./gradlew runVelocity

# Clean build artifacts
./gradlew clean

# Build without running tests
./gradlew shadowJar
```

## Architecture

### Core Components

1. **Main Plugin Class** (`Acore.java:27`)
   - Uses Velocity's dependency injection
   - Manages plugin lifecycle
   - Coordinates all subsystems

2. **Configuration System** (`config/`)
   - Type-safe configuration with Sponge Configurate
   - Default config in `src/main/resources/config.yml`
   - Runtime config loading with fallback values

3. **Database Layer** (`database/DatabaseManager.java`)
   - HikariCP connection pooling
   - Automatic connection cleanup on shutdown
   - Uses `ON DUPLICATE KEY UPDATE` for efficient updates

4. **Scheduled Tasks** (`task/PlayerListTask.java`)
   - Periodic player data collection
   - Configurable interval (default: 60s)
   - Collects player count and username list

5. **Bot Integration** (`bot/MessageListener.java`)
   - QQ bot message handling
   - Responds to `#ls` command with player info

### Key Design Patterns

- **Dependency Injection**: Velocity's Guice-based DI
- **Event-Driven**: Velocity event system
- **Connection Pooling**: HikariCP for database connections
- **Configuration as Code**: Type-safe config objects
- **Service Relocation**: Dependencies relocated to prevent conflicts

## Development Guidelines

### Adding New Configuration

1. Add fields to `PluginConfig.java` with `@Setting` annotations
2. Update default `config.yml`
3. Access via `Acore.getPluginConfig()`

### Database Operations

1. Use `DatabaseManager` for all database access
2. Connections are automatically managed
3. Implement proper error handling and logging

### Adding New Tasks

1. Create task class implementing `Runnable`
2. Schedule in `Acore.onProxyInitialization()`
3. Use configurable intervals from config

### Bot Commands

1. Extend `MessageListener.java`
2. Handle group messages via MiraiMC API
3. Use Velocity API for server interactions

## Build Output

- **Primary JAR**: `build/libs/Acore-1.0-SNAPSHOT.jar`
- **Shadow JAR**: Includes all dependencies
- **Relocated packages**: `cc.mcac.lib.*` for HikariCP and bStats

## Important Notes

- Java 17 is required
- Use Gradle wrapper for consistent builds
- Plugin ID: "acore"
- bStats plugin ID: 27159
- MySQL database required with schema "ac_info"
- Velocity 3.4.0-SNAPSHOT compatible