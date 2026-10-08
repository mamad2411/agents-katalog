# Cursor Rules - Software Development Standards
# Version: 2.2 (Language Correction + Migrations + AWS)
# Last Updated: October 2025

---

## 1. General Principles

### 1.1 Language Standards
- **Code**: Always use **English** for all code elements:
  - Variables, functions, methods, classes, interfaces
  - SQL table names, column names, stored procedures
  - Comments in code
  - Git commit messages
  - API endpoints and routes
  - Log messages and debug output
  
- **User-Facing Content**: Use **English by default** unless user specifies otherwise at project start:
  - UI labels, buttons, messages
  - Error messages shown to users
  - Help text and documentation for end users
  - Email templates
  - Push notifications
  
- **Multi-Language Support**:
  - Default UI language: **English**
  - Implement i18n/localization **only when user explicitly requests** multiple languages
  - Additional languages (Portuguese, Spanish, etc.) must be specified by user at project start
  - Never assume a specific non-English language without explicit user instruction

### 1.2 Project Organization
- **Root Folder Structure**: Use **PascalCase** for all project folders in the solution root:
  ```
  ProjectName/
  ├── Database/          # Database scripts and docker-compose
  ├── AppApi/            # Main API (.NET)
  ├── AdminApi/          # Admin API (.NET) [if applicable]
  ├── Website/           # Frontend website (Next.js/React)
  ├── Admin/             # Admin frontend [if applicable]
  ├── MobileApp/         # Mobile app (React Native) [if applicable]
  ├── Infrastructure/    # Terraform, deployment scripts, keys
  ├── MediaKit/          # Logos, branding assets
  ├── Scripts/           # Cross-project start/stop scripts
  ├── Resources/         # Shared resources (DLLs, config files)
  └── README.md          # Single source of truth documentation
  ```

### 1.3 README Policy
- **ONE README.md only** at the solution root
- **NEVER** create additional README files in subdirectories unless **EXPLICITLY requested**
- **NEVER** update the README.md without **EXPLICIT user request**
- README should contain:
  - Project overview and purpose
  - Architecture diagram (ASCII art)
  - How projects communicate (protocols, ports)
  - Main features
  - How to start, stop, restart services
  - How to reset database and clear logs

---

## 2. C# / .NET Development Standards

### 2.1 Technology Stack
- **.NET 9** (or latest LTS version)
- **C# 12** with nullable reference types enabled
- **Dapper** for database access (manual SQL queries)
- **NLog** for logging
- **BCrypt.Net-Next** for password hashing
- **Microsoft.Data.SqlClient** (for SQL Server) or **Npgsql** (for PostgreSQL)

### 2.2 Naming Conventions
- **Classes, Methods, Properties, Public Fields**: `PascalCase`
  ```csharp
  public class UserRepository { }
  public void GetUserById(int userId) { }
  public string FirstName { get; set; }
  ```

- **Local Variables, Parameters**: `camelCase`
  ```csharp
  var userName = "John";
  public void ProcessOrder(int orderId, string customerName) { }
  ```

- **Private Fields**: Prefix with `_` (underscore) + `camelCase`
  ```csharp
  private readonly ILogger<UsersRepository> _logger;
  private readonly string _connectionString;
  ```

- **Constructor Parameter Injection**: Use same name as field but without underscore
  ```csharp
  private readonly ILogger<UserService> _logger;
  
  public UserService(ILogger<UserService> logger)
  {
      _logger = logger;
  }
  ```

- **Constants**: Use dedicated `Constants.cs` file with `UPPER_SNAKE_CASE`
  ```csharp
  public static class Constants
  {
      public const int DESK_TYPE_ID = 10;
      public const string STATUS_ACTIVE = "Active";
      public const string STATUS_INACTIVE = "Inactive";
  }
  ```

### 2.3 Project Configuration (.csproj)
```xml
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="BCrypt.Net-Next" Version="4.0.3" />
    <PackageReference Include="Dapper" Version="2.1.66" />
    <PackageReference Include="NLog.Web.AspNetCore" Version="6.0.5" />
    <!-- SQL Server -->
    <PackageReference Include="Microsoft.Data.SqlClient" Version="6.1.2" />
    <!-- OR PostgreSQL -->
    <!-- <PackageReference Include="Npgsql" Version="8.0.0" /> -->
  </ItemGroup>
</Project>
```

### 2.4 Logging with NLog

#### nlog.config (place in project root)
```xml
<?xml version="1.0" encoding="utf-8" ?>
<nlog xmlns="http://www.nlog-project.org/schemas/NLog.xsd"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      autoReload="true"
      throwExceptions="false"
      internalLogLevel="Off">

  <variable name="appName" value="ProjectNameApi"/>

  <targets>
    <!-- All logs -->
    <target xsi:type="File" name="allfile"
            fileName="${basedir}/logs/${appName}-${shortdate}.log"
            layout="${longdate}|${level:uppercase=true}|${logger}|${message} ${exception:format=tostring}"
            archiveEvery="Day"
            maxArchiveFiles="30" />

    <!-- Error logs -->
    <target xsi:type="File" name="errorfile"
            fileName="${basedir}/logs/${appName}-error-${shortdate}.log"
            layout="${longdate}|${level:uppercase=true}|${logger}|${message} ${exception:format=tostring}"
            archiveEvery="Day"
            maxArchiveFiles="30" />

    <!-- Console -->
    <target xsi:type="Console" name="console"
            layout="${longdate}|${level:uppercase=true}|${logger}|${message}" />
  </targets>

  <rules>
    <logger name="*" minlevel="Info" writeTo="allfile" />
    <logger name="*" minlevel="Error" writeTo="errorfile" />
    <logger name="*" minlevel="Debug" writeTo="console" />
    <logger name="Microsoft.*" maxlevel="Info" final="true" />
  </rules>
</nlog>
```

#### Program.cs Setup
```csharp
using NLog;
using NLog.Web;

var logger = LogManager.Setup().LoadConfigurationFromFile("nlog.config").GetCurrentClassLogger();
logger.Info("Application starting...");

try
{
    var builder = WebApplication.CreateBuilder(args);

    // Configure NLog for ASP.NET Core
    builder.Logging.ClearProviders();
    builder.Host.UseNLog();

    // Configure port from settings
    var port = builder.Configuration.GetValue<int>("ApiSettings:Port", 10001);
    builder.WebHost.UseUrls($"http://0.0.0.0:{port}");

    // Add services, CORS, repositories, etc.
    // ... (see section 2.6)

    var app = builder.Build();

    // Configure middleware pipeline
    // ... (see section 2.7)

    logger.Info("Application started successfully on port {Port}", port);
    Console.WriteLine($"\n==========================================");
    Console.WriteLine($"  API is running");
    Console.WriteLine($"  Port: {port}");
    Console.WriteLine($"  Swagger: http://localhost:{port}/swagger");
    Console.WriteLine($"==========================================\n");

    app.Run();
}
catch (Exception ex)
{
    logger.Error(ex, "Application stopped due to exception");
    throw;
}
finally
{
    LogManager.Shutdown();
}
```

### 2.5 Configuration (appsettings.json)

**NEVER hard-code configuration values.** Always use `appsettings.json` or environment variables.

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*",
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost,10002;Database=mydb;User Id=sa;Password=MyPassword123!;TrustServerCertificate=True;"
  },
  "ApiSettings": {
    "Port": 10001,
    "SessionExpirationHours": 24
  },
  "Cors": {
    "AllowedOrigins": [
      "http://localhost:10000",
      "http://localhost:3000",
      "https://myapp.com"
    ]
  }
}
```

### 2.6 Dependency Injection Pattern

```csharp
// Register database connection
builder.Services.AddScoped<IDbConnection>(sp => 
{
    var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
    return new SqlConnection(connectionString); // or NpgsqlConnection for PostgreSQL
});

// Register repositories with interfaces
builder.Services.AddScoped<IUsersRepository, UsersRepository>();
builder.Services.AddScoped<IOrdersRepository, OrdersRepository>();

// Register services
builder.Services.AddSingleton<ICacheService, CacheService>();
builder.Services.AddScoped<IAuthService, AuthService>();

// Add Memory Cache
builder.Services.AddMemoryCache();

// Configure CORS
var allowedOrigins = builder.Configuration.GetSection("Cors:AllowedOrigins").Get<string[]>() 
    ?? new[] { "http://localhost:3000" };

builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend", policy =>
    {
        policy.WithOrigins(allowedOrigins)
              .AllowAnyMethod()
              .AllowAnyHeader()
              .AllowCredentials();
    });
});

// Add controllers
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
```

### 2.7 Middleware Pipeline

```csharp
var app = builder.Build();

// Swagger (development only)
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

// CORS
app.UseCors("AllowFrontend");

// Custom authentication middleware (if applicable)
app.UseTokenAuthentication();

app.UseHttpsRedirection();
app.UseAuthorization();

app.MapControllers();

app.Run();
```

### 2.8 Repository Pattern with Dapper

**Interface:**
```csharp
public interface IUsersRepository
{
    Task<UserEntity?> GetByEmailAsync(string email);
    Task<UserEntity?> GetByIdAsync(Guid userId);
    Task<SessionEntity> CreateSessionAsync(Guid userId, string token, DateTime expiresAt);
    Task<SessionWithUserEntity?> GetSessionByTokenAsync(string token);
}
```

**Implementation:**
```csharp
using Dapper;
using Microsoft.Data.SqlClient;

public class UsersRepository : IUsersRepository
{
    private readonly string _connectionString;
    private readonly ILogger<UsersRepository> _logger;

    public UsersRepository(IConfiguration configuration, ILogger<UsersRepository> logger)
    {
        _connectionString = configuration.GetConnectionString("DefaultConnection") 
            ?? throw new InvalidOperationException("Connection string not found");
        _logger = logger;
    }

    public async Task<UserEntity?> GetByEmailAsync(string email)
    {
        try
        {
            using var connection = new SqlConnection(_connectionString);
            
            const string sql = @"
                SELECT UserId, Email, PasswordHash, Name
                FROM Users
                WHERE Email = @Email";

            var user = await connection.QueryFirstOrDefaultAsync<UserEntity>(sql, new { Email = email });
            
            _logger.LogInformation("User lookup for {Email}: {Found}", email, user != null);
            
            return user;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error fetching user by email {Email}", email);
            throw;
        }
    }
    
    // Other methods...
}
```

### 2.9 API Controllers

```csharp
using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    private readonly IUsersRepository _usersRepository;
    private readonly ILogger<UsersController> _logger;

    public UsersController(IUsersRepository usersRepository, ILogger<UsersController> logger)
    {
        _usersRepository = usersRepository;
        _logger = logger;
    }

    /// <summary>
    /// Get user by ID
    /// </summary>
    [HttpGet("{id}")]
    [ProducesResponseType(typeof(UserDto), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ErrorResponse), StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetById(Guid id)
    {
        try
        {
            var user = await _usersRepository.GetByIdAsync(id);
            
            if (user == null)
            {
                return NotFound(new ErrorResponse { Message = "User not found" });
            }
            
            return Ok(user);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error retrieving user {UserId}", id);
            return StatusCode(500, new ErrorResponse { Message = "Internal server error" });
        }
    }
}
```

### 2.10 Error Handling

**ALWAYS implement robust error handling:**

1. **Global Exception Middleware** (optional but recommended):
```csharp
public class GlobalExceptionMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<GlobalExceptionMiddleware> _logger;

    public GlobalExceptionMiddleware(RequestDelegate next, ILogger<GlobalExceptionMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Unhandled exception occurred");
            
            context.Response.StatusCode = 500;
            context.Response.ContentType = "application/json";
            
            await context.Response.WriteAsJsonAsync(new ErrorResponse
            {
                Message = "An unexpected error occurred. Please try again later.",
                Details = ex.Message // Only in development
            });
        }
    }
}
```

2. **Try-catch in Controllers/Repositories** with meaningful logs
3. **Avoid crashing the application** except during startup for critical config errors

### 2.11 No Mock Data

**NEVER create mock data or fallbacks** unless explicitly requested by the user.

---

## 3. Database Standards

### 3.1 Database Technology

Support both:
- **SQL Server 2022** (preferred for complex projects with System Versioning)
- **PostgreSQL 14+** (preferred for simpler projects or when specified)

### 3.2 Docker Compose Setup

**Always create a `Database/` folder** with:

#### For SQL Server:
```yaml
# Database/docker-compose.yml
version: '3.8'

services:
  sqlserver:
    image: mcr.microsoft.com/mssql/server:2022-latest
    container_name: projectname-sqlserver
    environment:
      ACCEPT_EULA: Y
      SA_PASSWORD: ProjectName_StrongPassword123!
      MSSQL_PID: Developer
    ports:
      - "10002:1433"
    volumes:
      - sqlserver_data:/var/opt/mssql
      - ./create-database.sql:/scripts/create-database.sql:ro
      - ./initial-data.sql:/scripts/initial-data.sql:ro
      - ./entrypoint.sh:/scripts/entrypoint.sh:ro
    command: /bin/bash /scripts/entrypoint.sh
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P ProjectName_StrongPassword123! -C -Q 'SELECT 1'"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  sqlserver_data:
```

#### For PostgreSQL:
```yaml
# Database/docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:14-alpine
    container_name: projectname-postgres
    restart: unless-stopped
    ports:
      - "10002:5432"
    environment:
      POSTGRES_DB: projectname_db
      POSTGRES_USER: projectname_user
      POSTGRES_PASSWORD: projectname_pass_dev
      PGDATA: /var/lib/postgresql/data/pgdata
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./create-database.sql:/docker-entrypoint-initdb.d/01-create-database.sql:ro
      - ./initial-data.sql:/docker-entrypoint-initdb.d/02-initial-data.sql:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U projectname_user -d projectname_db"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

#### entrypoint.sh (SQL Server only)
```bash
#!/bin/bash

# Start SQL Server in background
/opt/mssql/bin/sqlservr &

# Wait for SQL Server to start
echo "Waiting for SQL Server to start..."
for i in {1..60}; do
    /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$SA_PASSWORD" -C -Q "SELECT 1" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "SQL Server started successfully"
        break
    fi
    sleep 1
done

# Check if database already exists
/opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$SA_PASSWORD" -C -Q "SELECT name FROM sys.databases WHERE name = 'projectname'" -h -1 | grep -q "projectname"
if [ $? -ne 0 ]; then
    echo "Running database initialization scripts..."
    
    if [ -f /scripts/create-database.sql ]; then
        echo "Executing create-database.sql..."
        /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$SA_PASSWORD" -C -i /scripts/create-database.sql
    fi
    
    if [ -f /scripts/initial-data.sql ]; then
        echo "Executing initial-data.sql..."
        /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "$SA_PASSWORD" -C -i /scripts/initial-data.sql
    fi
    
    echo "Database initialization completed"
else
    echo "Database already exists, skipping initialization"
fi

# Wait for SQL Server process
wait
```

### 3.3 Naming Conventions

#### Tables
- **Format**: `PascalCase` plural
- **Examples**: `Users`, `Orders`, `Pets`, `HealthIssues`
- **Junction Tables**: Use `X` separator: `UsersXProfiles`, `OrdersXProducts`

#### Columns
- **Format**: `PascalCase`, no underscores
- **Primary Key**: `<EntityName>Id`
  - Examples: `UserId`, `OrderId`, `PetId`
- **Foreign Keys**: `<ReferencedEntity>Id`
  - Examples: `UserId`, `CustomerId`, `ProductId`

#### Examples:
```sql
-- SQL Server
CREATE TABLE Users (
    UserId UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    Email NVARCHAR(255) NOT NULL,
    Name NVARCHAR(255) NOT NULL,
    CreatedBy NVARCHAR(255) NOT NULL,
    CreatedDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    ModifiedBy NVARCHAR(255) NULL,
    ModifiedDate DATETIME2 NULL,
    CONSTRAINT PK_Users PRIMARY KEY (UserId)
);

-- PostgreSQL
CREATE TABLE Users (
    UserId UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    Email VARCHAR(255) NOT NULL,
    Name VARCHAR(255) NOT NULL,
    CreatedBy VARCHAR(100) NOT NULL,
    CreatedDate TIMESTAMP NOT NULL DEFAULT NOW(),
    ModifiedBy VARCHAR(100),
    ModifiedDate TIMESTAMP
);
```

### 3.4 Primary Keys

Use appropriate PK types based on entity:

- **User/Account entities**: `UNIQUEIDENTIFIER` (SQL Server) or `UUID` (PostgreSQL)
- **Catalog/Lookup entities**: `INT IDENTITY` (SQL Server) or `SERIAL` (PostgreSQL)
- **Transaction entities**: `UNIQUEIDENTIFIER`/`UUID` or `BIGINT IDENTITY`/`BIGSERIAL`

```sql
-- SQL Server
CREATE TABLE Users (
    UserId UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    -- ...
    CONSTRAINT PK_Users PRIMARY KEY (UserId)
);

CREATE TABLE Profiles (
    ProfileId INT IDENTITY(1,1) NOT NULL,
    -- ...
    CONSTRAINT PK_Profiles PRIMARY KEY (ProfileId)
);

-- PostgreSQL
CREATE TABLE Users (
    UserId UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- ...
);

CREATE TABLE Profiles (
    ProfileId SERIAL PRIMARY KEY,
    -- ...
);
```

### 3.5 Audit Columns

**ALL domain tables** must include these audit columns:

```sql
-- SQL Server
CreatedBy NVARCHAR(255) NOT NULL,
CreatedDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
ModifiedBy NVARCHAR(255) NULL,
ModifiedDate DATETIME2 NULL

-- PostgreSQL
CreatedBy VARCHAR(100) NOT NULL,
CreatedDate TIMESTAMP NOT NULL DEFAULT NOW(),
ModifiedBy VARCHAR(100),
ModifiedDate TIMESTAMP
```

### 3.6 System Versioning (Temporal Tables) - SQL Server Only

For critical tables in SQL Server, use System Versioning:

```sql
CREATE TABLE Users (
    UserId UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    Email NVARCHAR(255) NOT NULL,
    Name NVARCHAR(255) NOT NULL,
    CreatedBy NVARCHAR(255) NOT NULL,
    CreatedDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    ModifiedBy NVARCHAR(255) NULL,
    ModifiedDate DATETIME2 NULL,
    
    -- System Versioning columns
    SysStartTime DATETIME2 GENERATED ALWAYS AS ROW START NOT NULL,
    SysEndTime DATETIME2 GENERATED ALWAYS AS ROW END NOT NULL,
    
    CONSTRAINT PK_Users PRIMARY KEY (UserId),
    PERIOD FOR SYSTEM_TIME (SysStartTime, SysEndTime)
)
WITH (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.UsersHistory));
```

### 3.7 Indexes

Create indexes on:
- Foreign keys
- Frequently queried columns (status, dates, email)
- Columns used in WHERE, JOIN, ORDER BY

```sql
-- SQL Server
CREATE NONCLUSTERED INDEX IX_Orders_CustomerId ON Orders(CustomerId);
CREATE NONCLUSTERED INDEX IX_Orders_Status ON Orders(Status);
CREATE NONCLUSTERED INDEX IX_Orders_CreatedDate ON Orders(CreatedDate);

-- PostgreSQL
CREATE INDEX IX_Orders_CustomerId ON Orders(CustomerId);
CREATE INDEX IX_Orders_Status ON Orders(Status);
CREATE INDEX IX_Orders_CreatedDate ON Orders(CreatedDate);
```

### 3.8 Port Allocation Strategy

Use **custom port ranges** per project to avoid conflicts:

| Service | Port Range Example | Notes |
|---------|-------------------|-------|
| Database | 10002, 20002, 30002 | Increment by 10000 per project |
| Main API | 10001, 20001, 30001 | Same port range as database |
| Website | 10000, 20000, 30000 | Usually port 0 of the range |
| Admin API | 10003, 20003, 30003 | Optional |
| Admin Web | 10005, 20005, 30005 | Optional |

**Examples:**
- **Project H2O**: DB=10002, API=10001, Website=10000
- **Project Orbytta**: DB=30002, API=30000, AdminAPI=30001, AdminWeb=30005
- **Project ViPet**: DB=10002, AppAPI=10001, AdminAPI=10003, AdminWeb=10000

### 3.9 Database Migrations System

**CRITICAL: Always use incremental migrations for database evolution in production.**

#### Migration Structure

```
Database/
├── docker-compose.yml
├── create-database.sql        # Initial schema (run once)
├── initial-data.sql            # Initial data (run once)
├── entrypoint.sh               # SQL Server only
└── Migrations/
    ├── 001_AddUserPhoneColumn.sql
    ├── 002_CreateOrdersTable.sql
    ├── 003_AddIndexToUsers.sql
    ├── 004_InsertDefaultProfiles.sql
    └── ...
```

#### Migration Control Table

**MUST be created in `create-database.sql`:**

```sql
-- SQL Server
CREATE TABLE DatabaseMigrations (
    MigrationId INT IDENTITY(1,1) NOT NULL,
    MigrationNumber INT NOT NULL,
    MigrationName NVARCHAR(255) NOT NULL,
    ExecutedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    ExecutedBy NVARCHAR(255) NOT NULL DEFAULT 'system',
    CONSTRAINT PK_DatabaseMigrations PRIMARY KEY (MigrationId),
    CONSTRAINT UK_DatabaseMigrations_Number UNIQUE (MigrationNumber)
);

CREATE INDEX IX_DatabaseMigrations_Number ON DatabaseMigrations(MigrationNumber);

-- PostgreSQL
CREATE TABLE DatabaseMigrations (
    MigrationId SERIAL PRIMARY KEY,
    MigrationNumber INT NOT NULL UNIQUE,
    MigrationName VARCHAR(255) NOT NULL,
    ExecutedAt TIMESTAMP NOT NULL DEFAULT NOW(),
    ExecutedBy VARCHAR(255) NOT NULL DEFAULT 'system'
);

CREATE INDEX IX_DatabaseMigrations_Number ON DatabaseMigrations(MigrationNumber);
```

#### Migration File Naming Convention

**Format**: `NNN_DescriptiveName.sql`

- **NNN**: 3-digit number (001, 002, 003...)
- **DescriptiveName**: PascalCase description
- **Examples**:
  - `001_AddUserPhoneColumn.sql`
  - `002_CreateOrdersTable.sql`
  - `003_AddIndexToUsersEmail.sql`
  - `004_InsertDefaultRoles.sql`

#### Migration File Structure

Each migration must be **idempotent** and **self-documenting**:

```sql
-- =============================================
-- Migration: 001_AddUserPhoneColumn
-- Description: Adds Phone column to Users table
-- Author: YourName
-- Date: 2025-10-28
-- =============================================

-- Check if already applied (for safety)
IF NOT EXISTS (SELECT 1 FROM DatabaseMigrations WHERE MigrationNumber = 1)
BEGIN
    -- Perform migration
    IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('Users') AND name = 'Phone')
    BEGIN
        ALTER TABLE Users ADD Phone NVARCHAR(20) NULL;
        PRINT 'Column Phone added to Users table';
    END
    
    -- Record migration
    INSERT INTO DatabaseMigrations (MigrationNumber, MigrationName, ExecutedBy)
    VALUES (1, 'AddUserPhoneColumn', 'system');
    
    PRINT 'Migration 001_AddUserPhoneColumn completed successfully';
END
ELSE
BEGIN
    PRINT 'Migration 001_AddUserPhoneColumn already applied, skipping';
END
GO
```

#### Migration Execution Script

Create `Database/run-migrations.sh` and `Database/run-migrations.bat`:

```bash
#!/bin/bash
# run-migrations.sh

echo "=========================================="
echo "Running Database Migrations"
echo "=========================================="

MIGRATION_DIR="./Migrations"

if [ ! -d "$MIGRATION_DIR" ]; then
    echo "No migrations directory found"
    exit 0
fi

# Get list of migration files sorted by number
for migration_file in $(ls $MIGRATION_DIR/*.sql | sort); do
    echo "Executing: $(basename $migration_file)"
    
    # SQL Server
    sqlcmd -S localhost,10002 -U sa -P "YourPassword" -d yourdatabase -i "$migration_file"
    
    # PostgreSQL
    # psql -h localhost -p 10002 -U youruser -d yourdatabase -f "$migration_file"
    
    if [ $? -eq 0 ]; then
        echo "✓ Success: $(basename $migration_file)"
    else
        echo "✗ Failed: $(basename $migration_file)"
        exit 1
    fi
done

echo "=========================================="
echo "All migrations completed successfully"
echo "=========================================="
```

#### AWS RDS Migration Deployment

**In AWS, migrations are run automatically by user-data script or manually:**

```bash
# user-data.sh snippet for EC2
# Download migration files from S3 or Git
aws s3 cp s3://mybucket/migrations/ /app/migrations/ --recursive

# Run migrations against RDS
cd /app/Database
./run-migrations.sh
```

### 3.10 Database Reset Procedure (Development Only)

To recreate database in **LOCAL development** (DROP and CREATE):

```bash
# Stop containers
docker-compose down

# Remove volumes (IMPORTANT!)
docker volume rm $(docker volume ls -q | grep projectname)

# Start again (will run initialization scripts)
docker-compose up -d
```

**NEVER run this in AWS/Production - use migrations only!**

---

## 4. React / Next.js Frontend Standards

### 4.1 Technology Stack
- **Next.js 15** with App Router
- **React 18+**
- **TypeScript 5+**
- **CSS Modules** or **pure CSS** for styling (**NEVER use TailwindCSS, Material UI, Ant Design, or any component library**)
- **Lucide React** for icons (preferred over other icon libraries)
- **All components must be created from scratch** for truly modern and unique designs

### 4.2 Project Structure

```
Website/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   └── register/
│   ├── dashboard/
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
├── components/
│   ├── Modal/
│   │   ├── Modal.tsx
│   │   └── Modal.module.css
│   ├── Button/
│   │   ├── Button.tsx
│   │   └── Button.module.css
│   └── ...
├── styles/
│   ├── variables.css      # CSS custom properties (colors, spacing, etc.)
│   ├── globals.css        # Global styles
│   └── mixins.css         # Reusable CSS patterns
├── contexts/
│   └── AuthContext.tsx
├── hooks/
│   └── useAuth.ts
├── lib/
│   ├── apiClient.ts
│   ├── utils.ts
│   └── constants.ts
├── public/
├── package.json
├── tsconfig.json
└── next.config.js
```

### 4.3 package.json

```json
{
  "name": "projectname-website",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev -p 10000",
    "build": "next build",
    "start": "next start -p 10000",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^15.0.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "lucide-react": "^0.294.0"
    // NEVER add: tailwindcss, @mui/material, antd, bootstrap, chakra-ui, or any UI library
    // All components must be created from scratch with CSS Modules
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "typescript": "^5.3.0"
  }
}
```

### 4.4 Centralized API Client

**ALWAYS create a centralized API client** in `lib/apiClient.ts`:

```typescript
// lib/apiClient.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:10001';

export interface ApiError {
  message: string;
  details?: string;
  timestamp: string;
}

export class ApiClientError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public details?: string
  ) {
    super(message);
    this.name = 'ApiClientError';
  }
}

function getAuthToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('authToken');
}

export function setAuthToken(token: string): void {
  if (typeof window === 'undefined') return;
  localStorage.setItem('authToken', token);
}

export function clearAuthToken(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('authToken');
}

async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const token = getAuthToken();

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token && !endpoint.includes('/auth/login')) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (response.ok) {
      return await response.json() as T;
    }

    let errorData: ApiError;
    try {
      errorData = await response.json();
    } catch {
      errorData = {
        message: `HTTP ${response.status}: ${response.statusText}`,
        timestamp: new Date().toISOString(),
      };
    }

    throw new ApiClientError(
      errorData.message || 'An unexpected error occurred',
      response.status,
      errorData.details
    );
  } catch (error) {
    if (error instanceof ApiClientError) {
      throw error;
    }

    throw new ApiClientError(
      'Network error: Unable to connect to the server',
      0,
      error instanceof Error ? error.message : 'Unknown error'
    );
  }
}

export const apiClient = {
  auth: {
    login: async (credentials: LoginRequest): Promise<LoginResponse> => {
      const response = await apiRequest<LoginResponse>('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify(credentials),
      });
      setAuthToken(response.token);
      return response;
    },

    logout: (): void => {
      clearAuthToken();
    },
  },

  // Add more API sections here...
};

export default apiClient;
```

### 4.5 Modal Component (Reusable)

**DO NOT use toast notifications for errors.** Create a reusable Modal component:

```typescript
// components/Modal.tsx
'use client'

import { useEffect, useRef } from 'react'
import { X } from 'lucide-react'

interface ModalProps {
  isOpen: boolean
  onClose: () => void
  children: React.ReactNode
  size?: 'md' | 'lg' | 'xl' | 'full'
  zIndex?: number
}

const openModals: number[] = []

export default function Modal({ 
  isOpen, 
  onClose, 
  children, 
  size = 'xl', 
  zIndex = 50 
}: ModalProps) {
  const idRef = useRef<number>(zIndex)

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        const highestZ = Math.max(...openModals)
        if (idRef.current === highestZ) {
          onClose()
        }
      }
    }

    if (isOpen) {
      if (!openModals.includes(zIndex)) {
        openModals.push(zIndex)
      }
      window.addEventListener('keydown', handleEscape)
    }

    return () => {
      if (isOpen) {
        const index = openModals.indexOf(zIndex)
        if (index > -1) {
          openModals.splice(index, 1)
        }
      }
      window.removeEventListener('keydown', handleEscape)
    }
  }, [isOpen, onClose, zIndex])

  if (!isOpen) return null

  const sizeClasses = {
    md: 'max-w-2xl',
    lg: 'max-w-4xl',
    xl: 'max-w-6xl',
    full: 'max-w-7xl',
  }

  return (
    <div className="fixed inset-0 flex items-center justify-center p-4" style={{ zIndex }}>
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal Content */}
      <div className={`relative w-full ${sizeClasses[size]} max-h-[90vh] bg-white rounded-2xl shadow-2xl overflow-hidden`}>
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 z-10 p-2 bg-black/10 hover:bg-black/20 rounded-lg"
        >
          <X className="w-6 h-6" />
        </button>

        {/* Scrollable Content */}
        <div className="overflow-y-auto max-h-[90vh] p-8">
          {children}
        </div>
      </div>
    </div>
  )
}
```

### 4.6 Error Display Pattern

```typescript
// Use Modal for errors, not toast
const [error, setError] = useState<string | null>(null);

try {
  await apiClient.users.create(userData);
} catch (err) {
  if (err instanceof ApiClientError) {
    setError(err.message);
  } else {
    setError('An unexpected error occurred');
  }
}

// In JSX:
{error && (
  <Modal isOpen={!!error} onClose={() => setError(null)}>
    <div className="text-center">
      <h2 className="text-xl font-bold text-red-600">Erro</h2>
      <p className="mt-4">{error}</p>
      <button onClick={() => setError(null)} className="mt-6 btn-primary">
        OK
      </button>
    </div>
  </Modal>
)}
```

### 4.7 CSS Modules and Custom Styling

**CRITICAL: All components must be styled from scratch. NEVER use TailwindCSS, Material UI, Ant Design, Bootstrap, or any UI library.**

#### CSS Variables (styles/variables.css)
```css
:root {
  /* Colors */
  --color-primary: #8c52ff;
  --color-secondary: #00bf63;
  --color-background: #ffffff;
  --color-surface: #f5f5f5;
  --color-text: #1a1a1a;
  --color-text-secondary: #666666;
  --color-border: #e0e0e0;
  --color-error: #dc2626;
  --color-success: #16a34a;
  --color-warning: #f59e0b;
  
  /* Spacing */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;
  
  /* Border Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  
  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 300ms ease;
  
  /* Font Sizes */
  --text-xs: 12px;
  --text-sm: 14px;
  --text-base: 16px;
  --text-lg: 18px;
  --text-xl: 20px;
  --text-2xl: 24px;
  --text-3xl: 30px;
  --text-4xl: 36px;
}
```

#### Component Example with CSS Modules
```typescript
// components/Button/Button.tsx
import styles from './Button.module.css'

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  children: React.ReactNode
  onClick?: () => void
  disabled?: boolean
}

export default function Button({
  variant = 'primary',
  size = 'md',
  children,
  onClick,
  disabled = false
}: ButtonProps) {
  return (
    <button
      className={`${styles.button} ${styles[variant]} ${styles[size]}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  )
}
```

```css
/* components/Button/Button.module.css */
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  border-radius: var(--radius-md);
  transition: all var(--transition-base);
  cursor: pointer;
  border: none;
  outline: none;
}

.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Variants */
.primary {
  background-color: var(--color-primary);
  color: white;
}

.primary:hover:not(:disabled) {
  filter: brightness(1.1);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.secondary {
  background-color: var(--color-secondary);
  color: white;
}

.outline {
  background-color: transparent;
  border: 2px solid var(--color-primary);
  color: var(--color-primary);
}

/* Sizes */
.sm {
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: var(--text-sm);
}

.md {
  padding: var(--spacing-md) var(--spacing-lg);
  font-size: var(--text-base);
}

.lg {
  padding: var(--spacing-lg) var(--spacing-xl);
  font-size: var(--text-lg);
}
```

#### Design Principles

1. **Modern and Unique**: Create designs that stand out, not generic UI
2. **Custom Components**: Every button, input, modal, card must be custom-made
3. **CSS Variables**: Use CSS custom properties for consistency
4. **Smooth Animations**: Use transitions and transforms for modern feel
5. **Responsive**: Mobile-first approach with media queries
6. **Accessibility**: Proper ARIA labels, keyboard navigation
7. **Dark Mode Ready**: Design with dark mode in mind (even if not implemented yet)

---

## 5. Scripts and Automation

### 5.1 Start/Stop Scripts

**Always create scripts** in a `Scripts/` folder at the root:

#### start.sh (Linux/macOS)
```bash
#!/bin/bash

echo "=========================================="
echo "Starting Project Services"
echo "=========================================="

# Start Database
echo "Starting database..."
cd Database
docker-compose up -d
cd ..
sleep 5

# Start API
echo "Starting API on port 10001..."
cd AppApi
dotnet run --launch-profile http > ../logs/api.log 2>&1 &
cd ..
sleep 3

# Start Website
echo "Starting Website on port 10000..."
cd Website
npm run dev > ../logs/website.log 2>&1 &
cd ..

echo "=========================================="
echo "✓ All services started"
echo "  Database: localhost:10002"
echo "  API: http://localhost:10001"
echo "  Website: http://localhost:10000"
echo "=========================================="
```

#### start.bat (Windows)
```batch
@echo off
echo ==========================================
echo Starting Project Services
echo ==========================================

echo Starting database...
cd Database
docker-compose up -d
cd ..
timeout /t 5 /nobreak > nul

echo Starting API on port 10001...
cd AppApi
start /B dotnet run --launch-profile http
cd ..
timeout /t 3 /nobreak > nul

echo Starting Website on port 10000...
cd Website
start /B npm run dev
cd ..

echo ==========================================
echo All services started
echo   Database: localhost:10002
echo   API: http://localhost:10001
echo   Website: http://localhost:10000
echo ==========================================
pause
```

#### stop.sh / stop.bat
Similar structure but using `docker-compose down`, `pkill`, or `taskkill`.

---

## 6. Infrastructure and Deployment

### 6.1 Infrastructure Folder

For production deployments, create an `Infrastructure/` folder with:
- **terraform/**: Terraform files for AWS (or other cloud provider)
  - EC2, S3, CloudFront, ACM, Route53, etc.
  - `terraform.tfvars.example` for reference
  - `user-data.sh` for EC2 initialization
- **scripts/**: Deployment scripts
- **keys/**: SSH keys (add to .gitignore)

### 6.2 Terraform Best Practices

- Use variables for all configurable values
- Separate environments (dev, staging, production)
- Use remote state (S3 + DynamoDB for locking)
- Use modules for reusable components

### 6.3 Environment Configuration

**CRITICAL: Development vs Production environments are COMPLETELY DIFFERENT**

#### Development Environment (Local)
```
┌─────────────────────────────────────────┐
│ Development Machine                      │
├─────────────────────────────────────────┤
│ • Docker Compose Database (port 10002)  │
│ • .NET API (port 10001) → localhost DB  │
│ • Next.js (port 10000) → localhost API  │
└─────────────────────────────────────────┘
```

#### Production Environment (AWS)
```
┌──────────────────────────────────────────────────────┐
│ AWS Cloud                                             │
├──────────────────────────────────────────────────────┤
│ • RDS Database (NOT Docker Compose)                  │
│ • EC2 Instance(s) with .NET API → RDS                │
│ • S3 + CloudFront for frontend → Subdomain          │
│ • Route53 DNS (api.domain.com, app.domain.com)       │
└──────────────────────────────────────────────────────┘
```

#### Configuration Management

**NEVER hard-code. Always use environment-specific config:**

##### appsettings.json (Development)
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost,10002;Database=mydb;User Id=sa;Password=DevPassword123!;TrustServerCertificate=True;"
  },
  "ApiSettings": {
    "Port": 10001,
    "BaseUrl": "http://localhost:10001"
  },
  "Frontend": {
    "Url": "http://localhost:10000"
  }
}
```

##### appsettings.Production.json (AWS)
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=mydb.abc123.us-east-1.rds.amazonaws.com,5432;Database=mydb;User Id=admin;Password=ProdPassword;TrustServerCertificate=True;"
  },
  "ApiSettings": {
    "Port": 5000,
    "BaseUrl": "https://api.mydomain.com"
  },
  "Frontend": {
    "Url": "https://app.mydomain.com"
  }
}
```

### 6.4 AWS Deployment Pattern

#### Step 1: Terraform Infrastructure

**Terraform creates:**
1. **RDS Instance** (replaces Docker Compose database)
2. **EC2 Instance(s)** for API(s)
3. **S3 Bucket(s)** for frontend static files
4. **CloudFront Distribution** for CDN
5. **Route53 DNS Records** for subdomains
6. **Security Groups** for access control
7. **IAM Roles** for permissions

#### Step 2: Configuration Replacement

**Deploy script MUST replace local config with AWS config:**

```bash
#!/bin/bash
# deploy.sh

# 1. Get RDS endpoint from Terraform output
RDS_ENDPOINT=$(terraform output -raw rds_endpoint)
RDS_DATABASE=$(terraform output -raw rds_database)
RDS_USERNAME=$(terraform output -raw rds_username)
RDS_PASSWORD=$(terraform output -raw rds_password)

# 2. Get subdomain URLs
API_URL=$(terraform output -raw api_url)
FRONTEND_URL=$(terraform output -raw frontend_url)

# 3. Replace appsettings.json for API
cat > AppApi/appsettings.Production.json <<EOF
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=${RDS_ENDPOINT};Database=${RDS_DATABASE};User Id=${RDS_USERNAME};Password=${RDS_PASSWORD};TrustServerCertificate=True;"
  },
  "ApiSettings": {
    "Port": 5000,
    "BaseUrl": "${API_URL}"
  },
  "Frontend": {
    "Url": "${FRONTEND_URL}"
  },
  "Cors": {
    "AllowedOrigins": ["${FRONTEND_URL}"]
  }
}
EOF

# 4. Replace .env for Frontend
cat > Website/.env.production <<EOF
NEXT_PUBLIC_API_URL=${API_URL}
EOF

# 5. Build and deploy API to EC2
cd AppApi
dotnet publish -c Release -o publish
# Upload to EC2 (via SCP, S3, or CodeDeploy)

# 6. Build and deploy Frontend to S3
cd ../Website
npm run build
aws s3 sync ./out s3://mybucket-frontend/ --delete
aws cloudfront create-invalidation --distribution-id XXXXX --paths "/*"
```

#### Step 3: Database Migration on Deploy

**user-data.sh (EC2) MUST run migrations:**

```bash
#!/bin/bash
# user-data.sh for EC2 instance

# Install .NET runtime
wget https://dot.net/v1/dotnet-install.sh
bash dotnet-install.sh --channel 9.0

# Download application from S3
aws s3 cp s3://mybucket-deploy/api.zip /app/api.zip
unzip /app/api.zip -d /app/

# Get RDS connection from environment variables (injected by Terraform)
export ConnectionStrings__DefaultConnection="${RDS_CONNECTION_STRING}"

# Run database migrations
cd /app/Database
chmod +x run-migrations.sh
./run-migrations.sh

# Setup systemd service
cat > /etc/systemd/system/myapi.service <<EOF
[Unit]
Description=MyAPI Service

[Service]
WorkingDirectory=/app/AppApi
ExecStart=/usr/bin/dotnet /app/AppApi/MyApi.dll
Restart=always
RestartSec=10
Environment=ASPNETCORE_ENVIRONMENT=Production
Environment="ConnectionStrings__DefaultConnection=${RDS_CONNECTION_STRING}"

[Install]
WantedBy=multi-user.target
EOF

systemctl enable myapi
systemctl start myapi
```

### 6.5 Terraform Configuration Example

**variables.tf**
```hcl
variable "project_name" {
  type = string
}

variable "domain_name" {
  type = string
}

variable "db_username" {
  type = string
  sensitive = true
}

variable "db_password" {
  type = string
  sensitive = true
}
```

**rds.tf**
```hcl
resource "aws_db_instance" "main" {
  identifier = "${var.project_name}-db"
  engine = "sqlserver-ex"  # or "postgres"
  engine_version = "15.00"  # or "14.7" for postgres
  instance_class = "db.t3.small"
  allocated_storage = 20
  
  db_name = var.project_name
  username = var.db_username
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  
  skip_final_snapshot = true
  publicly_accessible = false
  
  tags = {
    Name = "${var.project_name}-rds"
  }
}
```

**outputs.tf**
```hcl
output "rds_endpoint" {
  value = aws_db_instance.main.endpoint
  description = "RDS endpoint"
}

output "rds_database" {
  value = aws_db_instance.main.db_name
  description = "RDS database name"
}

output "api_url" {
  value = "https://api.${var.domain_name}"
  description = "API URL"
}

output "frontend_url" {
  value = "https://app.${var.domain_name}"
  description = "Frontend URL"
}
```

### 6.6 Deployment Checklist

**Before deploying to AWS:**

- [ ] **Database**: RDS created (NOT Docker Compose)
- [ ] **Connection Strings**: Updated to point to RDS
- [ ] **Migrations**: Tested and ready to run on RDS
- [ ] **Subdomains**: DNS configured (api.domain.com, app.domain.com)
- [ ] **Environment Variables**: Set in EC2 user-data or Parameter Store
- [ ] **CORS**: Updated to allow frontend subdomain
- [ ] **API Base URL**: Frontend configured to use https://api.domain.com
- [ ] **Secrets**: Stored in AWS Secrets Manager or Parameter Store
- [ ] **SSL Certificates**: Created via ACM and attached to CloudFront/ALB

---

## 7. FIX Protocol (When Applicable)

### 7.1 QuickFix Library
- **Always use QuickFix/N** for FIX 4.4 protocol
- **Never** parse or build FIX messages manually
- Store `QuickFix.dll` in a `Resources/` or `Lib/` folder

### 7.2 Configuration
```csharp
// Always use FIX dictionary file
var settings = new SessionSettings("path/to/FIX44.xml");
```

---

## 8. MediaKit and Branding

### 8.1 Organization
Create a `MediaKit/` folder with:
```
MediaKit/
├── png/
│   ├── logo-color-no-background.png
│   ├── logo-white-no-background.png
│   └── logo-with-background.png
├── svg/
│   └── ...
├── pdf/
│   └── ...
└── Favicons/
    ├── browser.png
    ├── iPhone.png
    └── Android.png
```

---

## 9. Best Practices Summary

### 9.1 DO

✅ **Code in English**, UI text in **English by default** (unless user specifies otherwise)
✅ Use PascalCase for folders, classes, methods
✅ Use camelCase for variables, parameters
✅ Prefix private fields with `_`
✅ Use Constants.cs for fixed IDs with UPPER_SNAKE_CASE
✅ Always use configuration files (appsettings.json) - never hard-code
✅ Use custom port ranges per project (e.g., 10000-10005, 20000-20005)
✅ Create ONE README.md at the solution root
✅ Use NLog with structured logging
✅ Use Dapper with manual SQL queries
✅ Implement robust error handling (try-catch + logging)
✅ Create repositories with interfaces
✅ Use dependency injection
✅ Create centralized API client for frontend
✅ Use reusable Modal component (not toast)
✅ **Create all UI components from scratch** with CSS Modules or pure CSS
✅ Use CSS custom properties (variables) for design consistency
✅ Design modern, unique interfaces (not generic)
✅ Create start.sh/bat and stop.sh/bat scripts
✅ Add audit columns (CreatedBy, CreatedDate, ModifiedBy, ModifiedDate) to all tables
✅ Use System Versioning (Temporal Tables) for critical tables in SQL Server
✅ Create indexes on foreign keys and frequently queried columns
✅ **Use incremental migrations** for database evolution (Database/Migrations/)
✅ **Separate development (Docker) and production (AWS RDS) configurations**
✅ **Deploy scripts must automatically replace configs** (connection strings, URLs)

### 9.2 DON'T

❌ Never mix languages (code must ALWAYS be in English, UI in English unless specified otherwise)
❌ Never hard-code configuration (ports, connection strings, URLs)
❌ Never use default/random ports
❌ Never create multiple README files
❌ Never update README without explicit request
❌ Never create mock data or fallbacks (unless explicitly requested)
❌ Never use Entity Framework (use Dapper with manual queries)
❌ Never connect directly to Docker for schema changes (always recreate with `docker-compose down -v`)
❌ Never use toast notifications for error messages (use Modal)
❌ **Never use TailwindCSS, Material UI, Ant Design, Bootstrap, Chakra UI, or ANY UI component library**
❌ **Never use pre-built component libraries** - all components must be custom-made
❌ Never copy generic designs - create modern, unique interfaces
❌ **Never use Docker Compose for database in AWS/Production** - always use RDS
❌ **Never run ALTER TABLE directly in production** - always use migrations
❌ **Never deploy with local connection strings** - deploy script must replace them
❌ **Never skip migrations** - all schema changes must go through migration system
❌ Never skip audit columns in domain tables
❌ Never skip try-catch in repository methods
❌ Never skip logging in error scenarios

---

## 10. Common Patterns and Conventions

### 10.1 Port Allocation Pattern

```
ProjectName/
├── Database      → Port: X0002 (e.g., 10002, 20002, 30002)
├── AppApi        → Port: X0001 (e.g., 10001, 20001, 30001)
├── Website       → Port: X0000 (e.g., 10000, 20000, 30000)
├── AdminApi      → Port: X0003 (e.g., 10003, 20003, 30003)
└── Admin         → Port: X0005 (e.g., 10005, 20005, 30005)
```

### 10.2 Authentication Flow

1. User sends credentials to `/api/auth/login`
2. API validates with BCrypt
3. API generates token and stores in Sessions table
4. API returns token + user data + permissions
5. Frontend stores token in localStorage
6. Frontend sends token in `Authorization: Bearer {token}` header
7. API middleware validates token and adds user to context

### 10.3 Password Hashing

```csharp
// Hash on registration
var passwordHash = BCrypt.Net.BCrypt.HashPassword(plainPassword);

// Verify on login
bool isValid = BCrypt.Net.BCrypt.Verify(plainPassword, storedHash);
```

### 10.4 Database Migration Pattern

**DO NOT use migrations**. Instead:

1. Edit `create-database.sql` directly
2. Stop containers: `docker-compose down`
3. Remove volumes: `docker volume rm ...`
4. Start again: `docker-compose up -d`

---

## 11. Troubleshooting Common Issues

### 11.1 Port Already in Use

```bash
# Linux/macOS
lsof -ti:10001 | xargs kill -9

# Windows
netstat -ano | findstr :10001
taskkill /PID <PID> /F
```

### 11.2 Database Connection Issues

- Check if container is running: `docker ps`
- Check logs: `docker logs projectname-sqlserver`
- Verify port mapping in docker-compose.yml
- Verify connection string in appsettings.json
- Check firewall settings

### 11.3 CORS Errors

- Verify `AllowedOrigins` in appsettings.json
- Ensure `app.UseCors("PolicyName")` is before `app.UseAuthorization()`
- Check browser console for exact origin

---

## 12. Version History

- **v2.0** (October 2025): Enhanced with real-world patterns from h2o, orbytta, vipet projects
- **v1.0** (Initial): Basic rules

---

**End of Cursor Rules v2.0**

