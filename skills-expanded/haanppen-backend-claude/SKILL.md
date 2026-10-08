# 한편의 수학 Backend API - Comprehensive Project Documentation

## Project Overview

This is a monolithic Spring Boot REST API backend for "한편의 수학" (Hanpyeon Math), an online and offline academy management system. The project serves students, teachers, and managers by providing learning resources, course management, Q&A board, and video streaming capabilities.

**Tech Stack:**
- Spring Boot 3.2.2
- Spring Data JPA / Hibernate
- Spring Security with JWT
- MySQL 8 (InnoDB)
- Gradle
- Java 17
- AWS Integration (S3 for file storage)
- Logstash (structured logging)
- Swagger/OpenAPI 3.1.0

**Project Metrics:**
- Total Java files: 570+
- Modular architecture with clear separation of concerns
- Supports: H2 for testing, MySQL for production

---

## Architecture & Project Structure

### Module Organization

```
com.hanpyeon.academyapi/
├── account/           # User account management (members, auth)
├── board/            # Q&A board system (questions, comments)
├── course/           # Class management & memo system
├── online/           # Online course management (separate from regular courses)
├── dir/              # Directory & chunked file management
├── media/            # Media handling (upload, streaming, storage)
├── security/         # JWT, authentication, authorization
├── config/           # Spring configurations
├── aspect/           # Cross-cutting concerns (logging)
├── exception/        # Global exception handling
├── paging/           # Pagination utilities
└── webconfig/        # Web configuration
```

### Architectural Pattern

The project employs a **hexagonal architecture (ports & adapters)** in the course module while maintaining traditional layered architecture in other modules.

**Layering:**
1. **Controllers/Adapters (in)** - HTTP endpoints
2. **Services/Application** - Business logic
3. **Domain** - Core business rules (for course module)
4. **Repositories/DAOs** - Data access
5. **Entities** - JPA-mapped database objects
6. **DTOs** - Data transfer objects
7. **Models** - Domain value objects

---

## Entity Models & Relationships

### Core Entities

#### 1. **Member** (`account/entity/Member.java`)
**Purpose:** Represents users (students, teachers, managers, admins)

**Key Fields:**
```java
- id (Long): Primary key
- phoneNumber (String): Unique identifier for users
- name (String): Member name
- password (String): BCrypt encrypted password
- grade (Integer): Student grade (0-11)
- role (Role enum): STUDENT, TEACHER, MANAGER, ADMIN
- removed (Boolean): Soft delete flag
- registeredDate (LocalDateTime): Account creation timestamp
- verificationCode (String): SMS verification code
- verifyMessageSendCount (Integer): Tracking SMS attempts
- isVerifying (Boolean): Verification status
- loginTryCount (Integer): Failed login attempts
- locked (Boolean): Account lock status
- lockedStartTime (LocalDateTime): When account was locked
```

**Key Methods:**
- `setVerificationCode()` - Sets code and tracks send count
- `increaseLoginTryCount()` - Increments failed login attempts
- `canLoginAt(currentTime, lockMinutes)` - Checks if lock period expired
- `lock(startTime)` / `unlock()` - Lock/unlock mechanism
- `remove()` - Soft delete with cascading operations

**Relationships:**
- OneToMany → CourseStudent (student enrollment)
- ManyToOne (implicit) ← Question (as owner and target)
- ManyToOne (implicit) ← Comment (as registered member)
- OneToMany (implicit) ← Media (ownership)

#### 2. **Question** (`board/entity/Question.java`)
**Purpose:** Q&A board questions with image support

**Key Fields:**
```java
- id (Long): Primary key
- title (String): Question title
- content (String): Question content
- registeredDateTime (LocalDateTime): Creation time
- solved (Boolean): Resolution status
- viewCount (Long): View count
- ownerMember (Member): Question author
- targetMember (Member): Question recipient (teacher)
- images (List<Image>): Attached images (cascade delete)
- comments (List<Comment>): Related answers
```

**Key Methods:**
- `changeTitle()` / `changeContent()` - Update question
- `addComment(comment)` - Add answer with bidirectional linking
- `solved()` / `clearSolved()` - Mark resolution status
- `addViewCount()` - Increment views

**Relationships:**
- ManyToOne → Member (ownerMember, targetMember) - NO_CONSTRAINT FK
- OneToMany → Image (cascade delete)
- OneToMany → Comment (mapped by "question")

#### 3. **Comment** (`board/entity/Comment.java`)
**Purpose:** Answers to questions with adoption system

**Key Fields:**
```java
- id (Long): Primary key
- content (String): Comment text
- adopted (Boolean): Whether chosen as best answer
- registeredDateTime (LocalDateTime): Creation time
- registeredMember (Member): Commenter
- question (Question): Parent question
- images (List<Image>): Attached images
```

**Key Methods:**
- `adopt()` / `deAdopt()` - Mark as best answer, updates question solved status
- `setContent()` - Update comment text
- `delete()` - Nullify relationships for safe deletion

**Relationships:**
- ManyToOne → Member (registeredMember) - NO_CONSTRAINT FK
- ManyToOne → Question (required)
- OneToMany → Image

#### 4. **Media** (`media/entity/Media.java`)
**Purpose:** Track uploaded files with soft-delete support

**Key Fields:**
```java
- id (Long): Primary key (column name: media_id)
- mediaName (String): User-friendly filename
- src (String): Unique file path/identifier
- createdTime (LocalDateTime): Upload timestamp
- member (Member): File owner
- duration (Long): Video duration in milliseconds
- size (Long): File size in bytes
- deleted (Boolean): Soft delete flag
```

**Special Features:**
- **Soft Delete Pattern:** Uses Hibernate `@SQLDelete` and `@Where` annotations
  - DELETE operations translated to UPDATE deleted=true
  - Queries automatically filter out deleted=true rows
- Indexed on `src` for fast lookups
- Lazy loading of member relationship
- **CRITICAL:** Column name is `media_id`, not `id`

```java
@SQLDelete(sql = "UPDATE media SET deleted = true WHERE media_id = ?")
@Where(clause = "deleted = false")
```

#### 5. **Image** (`media/entity/Image.java`)
**Purpose:** Simple image reference holder

**Key Fields:**
```java
- id (Long): Primary key
- src (String): Unique image path (unique constraint)
```

**Usage:** Embedded in questions and comments for image attachments

#### 6. **Directory** (`dir/dao/Directory.java`)
**Purpose:** File system directory structure

**Key Fields:**
```java
- id (Long): Primary key
- owner (Member): Directory owner
- path (String): Directory path (unique, must end with /)
- canViewByEveryone (Boolean): Public visibility
- canAddByEveryone (Boolean): Public write access
- createdTime (LocalDateTime): Creation timestamp
- medias (List<Media>): Files in directory
```

**Important Notes:**
- Directory paths MUST end with `/` (e.g., `/teachers/`)
- Default directories: `/` (root), `/teachers/`
- Created automatically by DataInitializer on startup

---

## Important Configuration Details

### Application Properties

#### Database
```properties
spring.datasource.url=jdbc:mysql://localhost:3306/academydb
spring.datasource.username=${SPRING_DATASOURCE_USERNAME}
spring.datasource.password=${SPRING_DATASOURCE_PASSWORD}
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQLDialect
spring.jpa.hibernate.ddl-auto=validate  # Prod: validate, Dev: update
```

#### File Storage (Local)
```properties
server.local.storage=C:/MyProgram/backend/storage
server.local.chunk.storage=C:/MyProgram/backend/storage/chunks
memo.attachment.directory.path=/attachment/
```

#### Multipart Upload
```properties
spring.servlet.multipart.max-request-size=10MB
spring.servlet.multipart.max-file-size=3MB
```

#### Admin Account (Auto-created by DataInitializer)
```properties
application.admin.account.id=01000000000
application.admin.account.password=admin
```

---

## Security & Authentication

### Authentication Flow

**JWT-Based Authentication:**
- Access token: 6 hours expiry
- Refresh token: 7 days expiry, HttpOnly cookie
- Claims include memberId, name, role

**Password Security:**
```properties
server.password.encryption.version=$2B  # BCrypt version
server.password.encryption.strength=10  # Cost factor
```

**Role Hierarchy:**
```java
STUDENT    -> "ROLE_STUDENT"
TEACHER    -> "ROLE_TEACHER"
MANAGER    -> "ROLE_MANAGER"
ADMIN      -> "ROLE_ADMIN"
```

**Account Lock Mechanism:**
```properties
login.lock.minutes=60       # Lock duration
login.lock.maxTryCount=5    # Max failed attempts
```

---

## Key Implementation Details

### 1. Soft Delete Pattern

**Implementation:**
```java
@SQLDelete(sql = "UPDATE media SET deleted = true WHERE media_id = ?")
@Where(clause = "deleted = false")
public class Media {
    private boolean deleted = false;
}
```

**Effect:**
- DELETE operations become UPDATE statements
- All SELECT queries automatically filter `deleted = false`
- Data preserved for audit trails

### 2. Chunked File Upload System

**Storage Strategy:**
```
Temp Directory: /chunks/{uploadSessionId}/
├── chunk_0
├── chunk_1
└── chunk_2

Final Directory: /storage/{fileName}
```

**Response Codes:**
```
202 Accepted        → Chunk received, more needed
201 Created         → All chunks received, merge complete
406 Not Acceptable  → Invalid chunk (wrong order/size)
```

### 3. Directory & Media Management

**Duplicate File Handling:**
- Same filename in same directory → Old file deleted (soft delete)
- New file replaces old file
- Implemented in `DirectoryMediaUpdateManager`

**File Naming:**
- Pattern: `result_{UUID}.{extension}`
- Example: `result_1fee707b-b7fe-4ac5-9fe7-19a9bb3acc89.mp4`
- UUID ensures uniqueness across uploads

---

## DataInitializer (Automatic Setup)

**Purpose:** Auto-create initial data on application startup

**What it creates:**
1. **Admin Account** (if not exists)
   - Phone: 01000000000
   - Password: admin (BCrypt encrypted)
   - Role: ADMIN

2. **Storage Directories** (if not exist)
   - `C:/MyProgram/backend/storage`
   - `C:/MyProgram/backend/storage/chunks`

3. **Default Directories** (if not exist)
   - `/` (root directory)
   - `/teachers/` (teacher resources)

**Location:** `com.hanpyeon.academyapi.config.DataInitializer`

---

## Common Pitfalls & Things to Remember

### Critical Points

1. **Soft Delete Everywhere**
   - Member: Always check `removed = false`
   - Media: Repository handles via `@Where`
   - Don't hardcode WHERE clauses

2. **Member Phone Number is Unique Identifier**
   - Used for login instead of username
   - NOT the ID when identifying users

3. **Foreign Key Constraints = NO_CONSTRAINT**
   ```java
   @ForeignKey(ConstraintMode.NO_CONSTRAINT)
   ```
   - Developers must ensure referential integrity
   - No cascading deletes at DB level

4. **Media Entity Column Name**
   - Java field: `id`
   - Database column: `media_id`
   - MUST use `media_id` in native SQL queries

5. **Directory Paths Must End with /**
   - `/teachers/` ✅
   - `/teachers` ❌
   - Required for proper directory matching

6. **Password Encryption**
   - Always use PasswordHandler for encoding
   - Never compare raw passwords directly

7. **Transaction Boundaries**
   - Service methods marked @Transactional
   - Use @Transactional(readOnly=true) for queries

### Security Considerations

1. **Authentication Filter**
   - JwtAuthenticationFilter runs before every request
   - Checks Authorization header for "Bearer {token}"

2. **Storage Directory**
   - `storage/` folder is in `.gitignore`
   - Never commit uploaded files to git

3. **Sensitive Data**
   - Password never logged (masked in toString)
   - JWT key should be environment variable

---

## Development Workflow

### Adding a New Endpoint

1. **Create Controller**
2. **Define DTO/Request**
3. **Implement Service**
4. **Add Security Rule** in SecurityConfig
5. **Add Tests**

### Database Changes
- Development: `spring.jpa.hibernate.ddl-auto=update`
- Production: `spring.jpa.hibernate.ddl-auto=validate`

### Environment Variables Required
```
SPRING_DATASOURCE_USERNAME
SPRING_DATASOURCE_PASSWORD
SPRING_DATASOURCE_URL
```

---

## Useful Commands

### Build & Run
```bash
./gradlew build          # Build project
./gradlew bootRun        # Run application
```

### Database Reset (Development)
```sql
USE academydb;
SET SQL_SAFE_UPDATES = 0;
DELETE FROM directory;
DELETE FROM member;
SET SQL_SAFE_UPDATES = 1;
-- Restart application to auto-create via DataInitializer
```

### Git Operations
```bash
git status
git add .
git commit -m "message"
git push origin main
```

---

## Project Statistics

- **Total Java Files:** 570+
- **Database:** MySQL 8 (InnoDB)
- **API Endpoints:** 50+ REST endpoints
- **Roles:** 4 (STUDENT, TEACHER, MANAGER, ADMIN)

---

**Last Updated:** 2026-06-15
**Spring Boot Version:** 3.2.2
**Java Version:** 17