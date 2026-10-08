---
name: vibe-coding-nestjs
description: >
  Hướng dẫn vibe-coding chuẩn cho stack NestJS (backend) + React (frontend) + PostgreSQL + TypeORM.
  Dùng skill này BẤT CỨ KHI NÀO người dùng yêu cầu: tạo module NestJS, viết entity/DTO/service/controller,
  thiết kế REST API, implement auth/JWT, xử lý error handling, tổ chức folder structure, viết migration,
  hoặc bất kỳ task coding nào liên quan đến project NestJS + React. Kể cả khi người dùng chỉ nói
  "tạo feature X", "thêm endpoint Y", "fix bug trong service Z" — đều dùng skill này để đảm bảo
  output đúng convention và không cần nhắc lại rule.
---

# Vibe-Coding Skill — NestJS + React + PostgreSQL/TypeORM

**Tối ưu token:** các quy tắc ngắn theo ngữ cảnh file nằm trong `.cursor/rules/*.mdc` (Clean Architecture, REST API, unit test, code review). Chỉ mở skill này khi cần template đầy đủ Entity/DTO/Service/Controller.

Skill này giúp Claude generate code nhất quán, đúng convention, và production-ready cho stack đã định nghĩa — không cần người dùng nhắc lại rules mỗi lần.

---

## 1. Stack & Convention Tổng Quan

| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | NestJS (TypeScript strict)        |
| Frontend   | React (functional components)     |
| Database   | PostgreSQL                        |
| ORM        | TypeORM với migration             |
| Auth       | JWT (access 15ph + refresh 7 ngày)|
| Validation | class-validator + class-transformer|
| Docs       | Swagger (@nestjs/swagger)         |
| Logging    | NestJS Logger                     |

---

## 2. Workflow Khi Nhận Task

Trước khi viết bất kỳ dòng code nào, Claude PHẢI:

1. **Xác định scope** — Task yêu cầu tạo mới hay sửa file đang có?
2. **Liệt kê files sẽ tạo/sửa** — Nói rõ cho người dùng trước khi generate.
3. **Hỏi nếu thiếu thông tin quan trọng** — Ví dụ: relation type, business rule, constraint đặc biệt.
4. **Generate theo thứ tự chuẩn**: Entity → Migration → DTO → Service → Controller → (Test nếu cần).
5. **Sau mỗi file**: nhắc người dùng review trước khi qua bước tiếp.

---

## 3. Template Chuẩn Theo File Type

### 3.1 Entity

```typescript
import {
  Entity, PrimaryGeneratedColumn, Column,
  CreateDateColumn, UpdateDateColumn, Index,
} from 'typeorm';

@Entity('[table_name]')         // snake_case, số nhiều
export class [EntityName] {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  // Columns đây — dùng name: 'snake_case' cho mọi column
  @Column({ name: 'field_name' })
  fieldName: string;

  @Column({ unique: true })
  @Index()
  email: string;                // Thêm @Index() cho các cột hay filter/search

  @CreateDateColumn({ name: 'created_at' })
  createdAt: Date;

  @UpdateDateColumn({ name: 'updated_at' })
  updatedAt: Date;
}
```

**Checklist entity:**
- [ ] Tên table: `snake_case`, số nhiều
- [ ] Tất cả column name: `snake_case`
- [ ] Có `createdAt` và `updatedAt`
- [ ] Các cột hay query/filter: có `@Index()`
- [ ] Sensitive fields (password...): có `@Exclude()` nếu cần

---

### 3.2 DTO

```typescript
import { IsString, IsEmail, IsOptional, MinLength } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class Create[Feature]Dto {
  @ApiProperty({ example: '...' })
  @IsString()
  fieldName: string;

  @ApiPropertyOptional()
  @IsOptional()
  @IsString()
  optionalField?: string;
}

export class Update[Feature]Dto {
  @ApiPropertyOptional()
  @IsOptional()
  @IsString()
  fieldName?: string;
}

export class Query[Feature]Dto {
  @ApiPropertyOptional({ default: 1 })
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  page?: number = 1;

  @ApiPropertyOptional({ default: 20 })
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  @Max(100)
  limit?: number = 20;

  @ApiPropertyOptional()
  @IsOptional()
  @IsString()
  search?: string;
}
```

**Checklist DTO:**
- [ ] Mọi field có decorator từ `class-validator`
- [ ] Mọi field có `@ApiProperty` hoặc `@ApiPropertyOptional`
- [ ] Optional fields dùng `@IsOptional()` + `?`
- [ ] Pagination DTO có `page`, `limit`, `search` nếu cần

---

### 3.3 Service

```typescript
import { Injectable, NotFoundException, ConflictException, Logger } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';

@Injectable()
export class [Feature]Service {
  private readonly logger = new Logger([Feature]Service.name);

  constructor(
    @InjectRepository([Entity])
    private readonly [entity]Repository: Repository<[Entity]>,
  ) {}

  async create(dto: Create[Feature]Dto): Promise<[Entity]> {
    this.logger.log(`Creating [entity]: ${JSON.stringify({ ...dto, password: undefined })}`);

    // Check duplicate nếu cần
    const existing = await this.[entity]Repository.findOne({ where: { email: dto.email } });
    if (existing) throw new ConflictException('[Entity] already exists');

    const entity = this.[entity]Repository.create(dto);
    const saved = await this.[entity]Repository.save(entity);
    this.logger.log(`[Entity] created: ${saved.id}`);
    return saved;
  }

  async findAll(query: Query[Feature]Dto): Promise<{ data: [Entity][]; total: number }> {
    const { page, limit, search } = query;
    const qb = this.[entity]Repository.createQueryBuilder('[alias]');

    if (search) {
      qb.andWhere('[alias].fieldName ILIKE :search', { search: `%${search}%` });
    }

    const [data, total] = await qb
      .skip((page - 1) * limit)
      .take(limit)
      .orderBy('[alias].createdAt', 'DESC')
      .getManyAndCount();

    return { data, total };
  }

  async findOne(id: string): Promise<[Entity]> {
    const entity = await this.[entity]Repository.findOne({ where: { id } });
    if (!entity) throw new NotFoundException(`[Entity] with id ${id} not found`);
    return entity;
  }

  async update(id: string, dto: Update[Feature]Dto): Promise<[Entity]> {
    const entity = await this.findOne(id);
    Object.assign(entity, dto);
    return this.[entity]Repository.save(entity);
  }

  async remove(id: string): Promise<void> {
    const entity = await this.findOne(id);
    await this.[entity]Repository.remove(entity);
    this.logger.log(`[Entity] removed: ${id}`);
  }
}
```

**Checklist service:**
- [ ] Logger ở đầu class
- [ ] Không query DB trực tiếp — luôn qua Repository
- [ ] Throw NestJS exception (NotFoundException, ConflictException...) — không return null
- [ ] Không log sensitive data (password, token...)
- [ ] Pagination dùng `getManyAndCount()`

---

### 3.4 Controller

```typescript
import {
  Controller, Get, Post, Patch, Delete,
  Body, Param, Query, UseGuards, HttpCode, HttpStatus,
  ParseUUIDPipe,
} from '@nestjs/common';
import { ApiBearerAuth, ApiTags, ApiOperation, ApiResponse } from '@nestjs/swagger';

@ApiTags('[feature]')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller({ path: '[feature]', version: '1' })
export class [Feature]Controller {
  constructor(private readonly [feature]Service: [Feature]Service) {}

  @Post()
  @ApiOperation({ summary: 'Create [entity]' })
  @ApiResponse({ status: 201, type: [Entity] })
  create(@Body() dto: Create[Feature]Dto) {
    return this.[feature]Service.create(dto);
  }

  @Get()
  @ApiOperation({ summary: 'Get all [entity]' })
  findAll(@Query() query: Query[Feature]Dto) {
    return this.[feature]Service.findAll(query);
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get [entity] by id' })
  findOne(@Param('id', ParseUUIDPipe) id: string) {
    return this.[feature]Service.findOne(id);
  }

  @Patch(':id')
  @ApiOperation({ summary: 'Update [entity]' })
  update(
    @Param('id', ParseUUIDPipe) id: string,
    @Body() dto: Update[Feature]Dto,
  ) {
    return this.[feature]Service.update(id, dto);
  }

  @Delete(':id')
  @HttpCode(HttpStatus.NO_CONTENT)
  @ApiOperation({ summary: 'Delete [entity]' })
  remove(@Param('id', ParseUUIDPipe) id: string) {
    return this.[feature]Service.remove(id);
  }
}
```

**Checklist controller:**
- [ ] `@ApiTags`, `@ApiBearerAuth`, `@ApiOperation`, `@ApiResponse` đầy đủ
- [ ] `@UseGuards(JwtAuthGuard)` — trừ endpoint public thì thêm `@Public()`
- [ ] `ParseUUIDPipe` cho mọi `:id` param
- [ ] DELETE trả `204 No Content`
- [ ] Không có business logic trong controller

---

### 3.5 Response Shape Chuẩn

Mọi API đều trả về format này — dùng Interceptor hoặc format thủ công trong service:

```typescript
// Success — single item
{ "success": true, "data": { ... } }

// Success — list
{
  "success": true,
  "data": [...],
  "meta": { "total": 100, "page": 1, "limit": 20, "totalPages": 5 }
}

// Error (do Global Exception Filter xử lý)
{
  "success": false,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User with id xyz not found",
    "statusCode": 404
  }
}
```

---

## 4. Auth & Security Rules

Khi generate code liên quan đến auth:

- Access token: 15 phút, gửi qua `Authorization: Bearer`
- Refresh token: 7 ngày, lưu trong `httpOnly cookie`
- Hash password: `bcrypt` với cost factor ≥ 12
- Không bao giờ trả `password` trong response — dùng `@Exclude()` trên entity + `ClassSerializerInterceptor`
- Public endpoints: dùng decorator `@Public()` thay vì bỏ guard

```typescript
// Exclude password khỏi response
@Exclude()
@Column()
password: string;
```

---

## 5. Error Handling Rules

- **Luôn throw NestJS exception** — không return null hay error object thủ công
- **Exception mapping chuẩn**:
  - Không tìm thấy → `NotFoundException`
  - Trùng dữ liệu → `ConflictException`
  - Input sai → `BadRequestException`
  - Không có quyền → `ForbiddenException`
  - Chưa đăng nhập → `UnauthorizedException`
- **Global Exception Filter** phải được setup ở `main.ts` để format response lỗi đồng nhất

---

## 6. Logging Rules

```typescript
// Đầu mỗi service
private readonly logger = new Logger([ClassName].name);

// Khi nào log gì
this.logger.log('...');    // Hành động thành công, flow bình thường
this.logger.warn('...');   // Unexpected nhưng không crash
this.logger.error('...', error.stack);  // Lỗi 5xx, lỗi DB
```

**Không bao giờ log**: password, token, credit card, thông tin nhạy cảm.

---

## 7. Git Commit Convention

Khi được yêu cầu suggest commit message, dùng format:

```
<type>(<scope>): <mô tả ngắn gọn bằng tiếng Anh>
```

| Type       | Dùng khi                        |
|------------|---------------------------------|
| `feat`     | Thêm tính năng mới              |
| `fix`      | Sửa bug                         |
| `refactor` | Refactor, không thêm feature    |
| `chore`    | Config, deps, CI/CD             |
| `docs`     | Cập nhật documentation          |
| `test`     | Thêm/sửa test                   |
| `perf`     | Cải thiện performance           |

Ví dụ: `feat(auth): add refresh token rotation`

---

## 8. React Frontend Rules

Khi generate React code:

- Functional component + hooks — không dùng class component
- Props phải có interface rõ ràng, không dùng `any`
- Không gọi API trong component — tách ra `services/` hoặc custom hook
- Custom hook bắt đầu bằng `use`

```typescript
// ✅ Đúng
interface Props { userId: string; onSelect: (id: string) => void; }
const UserCard: React.FC<Props> = ({ userId, onSelect }) => { ... }

// ❌ Sai
const UserCard = (props: any) => { ... }
```

---

## 9. Những Thứ Claude KHÔNG BAO GIỜ Làm

Dù người dùng có yêu cầu, Claude từ chối hoặc cảnh báo rõ nếu:

- `synchronize: true` trong TypeORM config production
- Trả raw DB error ra client
- Hardcode secret/URL/config trong code
- Dùng `any` trong TypeScript
- `console.log` trong production code (dùng Logger)
- Bỏ qua `// @ts-ignore` để ép qua TypeScript error
- SELECT * trong query quan trọng — phải chỉ định columns
- Logic business trong Controller

---

## 10. Checklist Trước Khi Deliver Code

Trước khi trả code cho người dùng, Claude tự review:

- [ ] TypeScript strict — không có `any`, không có lỗi type
- [ ] Đúng naming convention (file, class, variable, DB column)
- [ ] DTO có đầy đủ validator và Swagger decorator
- [ ] Service throw exception đúng loại, không return null
- [ ] Controller có đủ Swagger annotation
- [ ] Logger được dùng, không có console.log
- [ ] Không expose sensitive data trong response hay log
- [ ] File ≤ 300 dòng — nếu vượt thì tách