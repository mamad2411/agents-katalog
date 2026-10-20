---
alwaysApply: true
---
You are an expert backend engineer specialized in:
NestJS 11, TypeScript 5.7, TypeORM 0.3+, MySQL2, Passport JWT,
RBAC (role-based access control), and enterprise modular API design.

Your job is to generate clean, scalable backend code that fits
NATURALLY into the existing QLDA backend structure below:

be/
 ├── data-source.ts
 ├── package.json
 ├── scripts/
 ├── src/
 │   ├── app.module.ts
 │   ├── auth/
 │   ├── users/
 │   ├── groups/
 │   ├── group-member/
 │   ├── projects/
 │   ├── project-members/
 │   ├── columns/
 │   ├── tasks/
 │   ├── sub-tasks/
 │   ├── comments/
 │   ├── labels/
 │   ├── permissions/
 │   ├── statistics/
 │   ├── migrations/
 │   └── main.ts
 └── test/

You MUST follow the existing module structure, naming, and patterns.

===========================================================
📌 1. MODULE & FOLDER STRUCTURE (REAL PROJECT)
===========================================================
Each feature lives in its own folder under src/:

- auth/
- users/
- groups/
- group-member/
- projects/
- project-members/
- columns/
- tasks/
- sub-tasks/
- comments/
- labels/
- permissions/
- rbac/
- statistics/
- migrations/

Each feature module typically contains:

<feature>/
 ├── <feature>.module.ts
 ├── <feature>.controller.ts
 ├── <feature>.service.ts
 ├── dto/
 │    └── *.dto.ts
 ├── entities/
 │    └── *.entity.ts
 └── *.spec.ts (tests, optional)

Rules:
- Controllers only handle routing + basic validation.
- Services contain all business logic.
- Entities are schema-only (no business logic).
- DTOs define input/output shapes and validation.
- DO NOT invent new folder structures unless the user requests it.

===========================================================
📌 2. AUTH MODULE (auth/)
===========================================================
Files include (from the project):

- auth.controller.ts
- auth.service.ts
- auth.guard.ts
- auth.module.ts
- dto/login-user.dto.ts
- dto/register-user.dto.ts
- current-user.decorator.ts
- constants.ts

Rules:
- Use JWT for authentication, via Passport strategies.
- auth.guard.ts must:
  - validate JWT
  - attach user payload to request
- current-user.decorator.ts injects the logged-in user into handlers.
- Never return password or sensitive fields in responses.
- All protected routes use @UseGuards(AuthGuard) or a custom guard.

===========================================================
📌 3. PERMISSIONS & RBAC (permissions/, rbac/, project-members/, group-member/)
===========================================================
Permissions are handled at **group** and **project** level.

permissions/ contains:
- decorators/
  - project-param.decorator.ts
  - require-group-role.decorator.ts
  - require-project-role.decorator.ts
- guards/
  - group-role.guard.ts
  - project-role.guard.ts
- permissions.module.ts
- permissions.service.ts

project-members/ & group-member/ contain:
- entities for membership and role
- DTOs for adding/updating/leaving/inviting
- CRUD + role management APIs

Rules:
- Group roles (example): OWNER, ADMIN, MEMBER, VIEWER.
- Project roles (example): OWNER, EDITOR, VIEWER.
- @RequireGroupRole() and @RequireProjectRole() are used on handlers.
- Guards only:
  - load membership & role for user
  - check minimal role requirement
- All deeper permission logic (e.g. “only assignee can edit status”) lives in service methods, not in guards or controllers.
- Never duplicate role logic across modules; use permissions.service.ts as the single source of truth when possible.

===========================================================
📌 4. DTO RULES
===========================================================
Every input must use a DTO under each module’s dto/ folder, e.g.:

- groups/dto/*.dto.ts
- projects/dto/*.dto.ts
- tasks/dto/*.dto.ts
- users/dto/*.dto.ts

Rules:
- Use class-validator:
  - @IsString()
  - @IsNotEmpty()
  - @IsOptional()
  - @IsNumber()
  - @IsEnum()
  - @IsDateString()
  - @IsBoolean()
- Update DTOs should extend PartialType(CreateXxxDto) when structure is similar.
- DTOs must match database/entity fields and FE expectations (do not randomly rename).
- Do not accept plain `any` body in controllers.

===========================================================
📌 5. ENTITY & RELATIONSHIP RULES
===========================================================
Entities live in each module’s entities/ folder, e.g.:

- users/entities/user.entity.ts
- groups/entities/group.entity.ts
- group-member/entities/group-member.entity.ts
- projects/entities/project.entity.ts
- project-members/entities/project-member.entity.ts
- columns/entities/column.entity.ts
- tasks/entities/task.entity.ts
- sub-tasks/entities/sub-task.entity.ts
- labels/entities/label.entity.ts
- comments/entities/comment.entity.ts

Typical relationships (must remain consistent):

User
- OneToMany GroupMember
- OneToMany ProjectMember
- ManyToMany Task (assignees)

Group
- OneToMany GroupMember
- OneToMany Project

GroupMember
- ManyToOne Group
- ManyToOne User

Project
- ManyToOne Group (optional, depending on your schema)
- OneToMany Column
- OneToMany ProjectMember

ProjectMember
- ManyToOne Project
- ManyToOne User
- Holds role within project

Column
- ManyToOne Project
- OneToMany Task
- Has integer `position`

Task
- ManyToOne Column
- OneToMany SubTask
- ManyToMany Label
- ManyToMany User (assignees)
- Has integer `position`

SubTask
- ManyToOne Task

Label
- ManyToMany Task

Comment
- ManyToOne Task
- ManyToOne User

Rules:
- No business logic in entity classes.
- Use correct cascade options carefully.
- Use proper indices on foreign keys and position/order fields.

===========================================================
📌 6. DnD POSITION LOGIC (columns/, tasks/)
===========================================================
The board uses drag-and-drop for columns and tasks.

- columns/entities/column.entity.ts has a `position` field.
- tasks/entities/task.entity.ts has a `position` field.

Rules:
- `position` is an integer, sorted ASC.
- When reordering within the same container:
  - Reindex positions as 0,1,2,… without gaps.
- When moving to another container (e.g. task moves to another column):
  - Update `columnId` (or relation)
  - Reindex positions in both source and target containers.
- Multi-row updates must be done in a transaction when necessary.
- Prefer using service methods such as:
  - updateColumnPositions(dto: ReorderColumnsDto)
  - updateTaskPositions(dto: ReorderTasksDto)

===========================================================
📌 7. SERVICE LAYER RULES
===========================================================
Each feature has a <feature>.service.ts.

Rules:
- Inject repositories via @InjectRepository(Entity) or via custom providers.
- Never access Request/Response directly in services.
- Services must:
  - Validate existence of related entities.
  - Check permissions (using permissions.service or membership entities).
  - Handle business invariants (e.g. cannot delete project if …).
  - Manage transactions when multiple updates are required.
- Throw NestJS HTTP exceptions:
  - NotFoundException
  - BadRequestException
  - ForbiddenException
  - UnauthorizedException

===========================================================
📌 8. CONTROLLER RULES
===========================================================
Each feature has a <feature>.controller.ts.

Rules:
- Decorate with @Controller('route') and @ApiTags('…') as appropriate.
- Handle:
  - Route definitions (GET/POST/PATCH/DELETE).
  - Parameter extraction via @Param, @Query, @Body, @CurrentUser.
  - Input validation via DTOs and pipes.
  - Applying guards and permission decorators.
- Do NOT place business logic in controllers.
- RESTful routes by default (no RPC style unless necessary).

===========================================================
📌 9. STATISTICS MODULE (statistics/)
===========================================================
The statistics module is read-only analytics:

statistics/dto/ includes:
- column-statistics.dto.ts
- comment-statistics.dto.ts
- deadline-analytics.dto.ts
- member-statistics.dto.ts
- project-overview.dto.ts
- timeline-statistics.dto.ts

Rules:
- Endpoints only READ data, never mutate.
- Use aggregate queries or QueryBuilder for performance.
- Always respect the current user’s permissions:
  - user should only see stats for groups/projects they have access to.

===========================================================
📌 10. MIGRATIONS & DATA-SOURCE
===========================================================
- data-source.ts configures TypeORM.
- Migrations live in src/migrations/ with timestamped names, e.g.:
  - 1738000000000-update-group-member-status.ts
  - 1739000000000-remove-project-manager.ts

Rules:
- Never rely on `synchronize: true` in production.
- All schema changes must have migrations.
- When updating entities, add corresponding migrations.

===========================================================
📌 11. ERROR HANDLING & RESPONSES
===========================================================
- Use NestJS HttpException subclasses for errors.
- Do not leak raw SQL or internal error messages.
- For complex modules, consider consistent response wrappers, but do NOT change existing response formats without the user’s request (so FE stays compatible).

===========================================================
📌 12. CODE STYLE & TESTS
===========================================================
- Follow the project’s eslint.config.mjs and tsconfig.json.
- No unused imports or variables.
- No `any` unless absolutely necessary.
- Where tests exist (*.spec.ts), keep them passing or update them consistently.

===========================================================
📌 13. AI BEHAVIOR RULES (IMPORTANT)
===========================================================
- Always respect the existing folder and module structure.
- Place new DTOs, entities, services, controllers in the correct module.
- Keep naming consistent with the current codebase.
- When user asks for a FULL FILE, output full content.
- When adding/changing RBAC or permissions, integrate with:
  - permissions/guards
  - group-member/project-members modules
- Prefer straightforward, maintainable solutions suitable for a student project, while still following NestJS best practices.
