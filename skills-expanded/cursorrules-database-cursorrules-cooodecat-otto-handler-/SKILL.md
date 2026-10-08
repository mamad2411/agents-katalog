# Otto Handler - Cursor IDE 개발 규칙

Otto Handler는 NestJS 기반의 CI/CD 자동화 플랫폼입니다. 이 파일은 Cursor IDE에서 개발할 때 따라야 할 규칙과 가이드라인을 정의합니다.

## 기본 원칙

- 기존 파일 편집을 새 파일 생성보다 우선시합니다
- 명시적 요청 없이는 문서 파일(.md)을 생성하지 않습니다
- 타입 안전성을 최우선으로 합니다
- 일관된 코딩 스타일을 유지합니다
- **GitHub OAuth 전용**: password 인증은 완전히 제거됨

## 프로젝트 구조

```
src/
├── auth/           # JWT 인증, refresh token
├── user/           # 사용자 관리
├── projects/       # GitHub 저장소 연동
├── pipelines/      # CI/CD 파이프라인 정의/실행
├── environments/   # 배포 환경 설정
├── webhooks/       # GitHub 웹훅 처리
├── database/       # Prisma 설정
└── common/         # 공통 유틸리티
```

## 기술 스택 및 패턴

### 필수 기술
- **NestJS**: Fastify 어댑터 사용
- **Prisma**: PostgreSQL ORM, relationJoins 활용
- **Nestia**: 타입 안전 API SDK 생성
- **typia**: 런타임 타입 검증
- **Redis**: 캐싱 및 세션 관리
- **TypeScript**: Strict 모드

### 모듈 패턴
```typescript
// 표준 모듈 구조
@Module({
  imports: [PrismaModule], // 필요한 모듈
  controllers: [SomeController],
  providers: [SomeService],
  exports: [SomeService], // 다른 모듈에서 사용
})
export class SomeModule {}
```

### 컨트롤러 패턴
```typescript
// Nestia TypedRoute 사용 필수
@Controller('api-endpoint')
export class SomeController {
  constructor(private readonly service: SomeService) {}

  @TypedRoute.Post('create')
  async create(@TypedBody() dto: CreateDto): Promise<ResponseDto> {
    return this.service.create(dto);
  }
}
```

### 서비스 패턴
```typescript
@Injectable()
export class SomeService {
  constructor(private readonly prisma: PrismaService) {}

  async findWithRelations(): Promise<Entity[]> {
    // include 사용 시 N+1 문제 주의
    return this.prisma.entity.findMany({
      include: { relations: true },
    });
  }
}
```

## 데이터베이스 규칙

### Prisma 스키마
- 모든 테이블에 createdAt, updatedAt 포함
- 외래 키 관계에 인덱스 설정 필수
- 열거형(enum) 활용으로 타입 안전성 확보

### 중요한 관계
```
User → Project → Pipeline → PipelineRun → Job → Log/Error
```

### 주요 열거형
```prisma
enum TriggerType { MANUAL, WEBHOOK, SCHEDULE, API }  # PUSH는 제거됨
enum ExecutionStatus { PENDING, QUEUED, RUNNING, SUCCESS, FAILED, CANCELLED, SKIPPED }
enum NodeType { BUILD, TEST, DEPLOY, CUSTOM }
enum DeploymentStatus { PENDING, DEPLOYING, SUCCESS, FAILED, ROLLED_BACK }
```

## 개발 워크플로

### 필수 명령어
```bash
# 개발 서버 시작
pnpm run start:dev

# Prisma 클라이언트 생성
pnpm prisma generate

# 데이터베이스 마이그레이션
pnpm prisma migrate dev

# 린팅 및 포맷팅
pnpm run lint
pnpm run format

# 타입 안전 SDK 생성
pnpm nestia sdk
```

### 코드 스타일

#### Import 순서
```typescript
// 1. Node.js 내장 모듈
import { join } from 'path';

// 2. 외부 라이브러리
import { Injectable, Module } from '@nestjs/common';
import { TypedRoute, TypedBody } from '@nestia/core';

// 3. 내부 모듈 (상대 경로)
import { PrismaService } from '../database/prisma.service';
import { CreateDto } from './dto/create.dto';
```

#### 네이밍 컨벤션
- **파일명**: kebab-case (user-profile.service.ts)
- **클래스명**: PascalCase (UserProfileService)
- **변수/함수명**: camelCase (getUserProfile)
- **상수명**: SCREAMING_SNAKE_CASE (JWT_SECRET)
- **타입/인터페이스**: PascalCase (UserResponse)

#### DTO 구조
```typescript
// Request DTO (GitHub OAuth 전용)
export interface CreateUserRequest {
  email: string;
  name: string;
  githubId: string;  // password 대신 GitHub ID
  githubUsername: string;
}

// Response DTO (필드명 camelCase 주의)
export interface UserResponse {
  userId: string;  // userID가 아님!
  email: string;
  name: string;
  createdAt: Date;
}
```

## 에러 처리

### 예외 처리 패턴
```typescript
try {
  const result = await this.someAsyncOperation();
  return result;
} catch (error) {
  // 구체적인 에러 타입 확인
  if (error instanceof PrismaClientKnownRequestError) {
    throw new BadRequestException('데이터베이스 오류');
  }
  throw new InternalServerErrorException('예상치 못한 오류');
}
```

### HTTP 상태 코드 가이드
- **200**: 성공적인 조회/수정
- **201**: 리소스 생성 성공
- **400**: 잘못된 요청 (validation 실패)
- **401**: 인증 실패
- **403**: 권한 없음
- **404**: 리소스 없음
- **409**: 중복 리소스
- **500**: 서버 내부 오류

## 보안 가이드라인

### 인증/인가
- **GitHub OAuth 전용** (password 인증 제거됨)
- JWT Access Token (짧은 만료 시간)
- Refresh Token (긴 만료 시간, Session 모델에 저장)
- GitHub App 설치를 통한 레포지토리 접근

### 민감 정보 처리
```typescript
// ❌ 잘못된 예시
console.log('User password:', user.password);

// ✅ 올바른 예시
const { password, ...safeUser } = user;
console.log('User data:', safeUser);
```

### 환경 변수
- 모든 시크릿은 .env 파일로 관리
- 프로덕션에서는 절대 하드코딩 금지
- GitHub 토큰 만료 시간 추적 및 자동 갱신

## 성능 최적화

### 데이터베이스 쿼리
```typescript
// ❌ N+1 문제 발생 가능
const users = await prisma.user.findMany();
for (const user of users) {
  user.projects = await prisma.project.findMany({
    where: { userId: user.id }  // 필드명 주의!
  });
}

// ✅ include 사용하여 한 번에 조회
const users = await prisma.user.findMany({
  include: { projects: true }
});
```

### Redis 캐싱
```typescript
// 자주 조회되는 데이터 캐싱
const cacheKey = `user:${userId}`;  // camelCase!
const cached = await redis.get(cacheKey);
if (cached) {
  return JSON.parse(cached);
}

const userData = await this.prisma.user.findUnique({
  where: { id: userId }  // id 필드 사용
});

await redis.setex(cacheKey, 3600, JSON.stringify(userData));
return userData;
```

## 테스트 가이드라인

### 단위 테스트
```typescript
describe('UserService', () => {
  let service: UserService;
  let prisma: PrismaService;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [
        UserService,
        { provide: PrismaService, useValue: mockPrisma }
      ],
    }).compile();

    service = module.get<UserService>(UserService);
    prisma = module.get<PrismaService>(PrismaService);
  });

  it('should create user', async () => {
    // Given
    const createDto = { email: 'test@example.com', name: 'Test' };
    
    // When
    const result = await service.create(createDto);
    
    // Then
    expect(result).toBeDefined();
    expect(result.email).toBe(createDto.email);
  });
});
```

### E2E 테스트
```typescript
describe('Users (e2e)', () => {
  let app: INestApplication;

  beforeEach(async () => {
    const moduleFixture = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  it('/users (POST)', () => {
    return request(app.getHttpServer())
      .post('/users')
      .send({ email: 'test@example.com', name: 'Test' })
      .expect(201);
  });
});
```

## Git 컨벤션

### 커밋 메시지
```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 변경
style: 코드 포맷팅
refactor: 리팩토링
test: 테스트 코드
chore: 빌드 도구, 설정 변경
```

### 브랜치 전략
- `main`: 프로덕션 브랜치
- `dev`: 개발 브랜치
- `feat/기능명`: 기능 개발 브랜치
- `fix/버그명`: 버그 수정 브랜치

## 금지 사항

### 절대 하지 말 것
- TypeScript `any` 타입 사용
- console.log를 프로덕션 코드에 남기기
- 비밀번호를 평문으로 저장
- 하드코딩된 URL이나 API 키
- Prisma 스키마 직접 수정 (migration 사용)

### 권장하지 않는 패턴
```typescript
// ❌ 권장하지 않음
export class BadController {
  @Get()
  async getUsers(): Promise<any> { // any 타입 사용
    const users = await this.prisma.$queryRaw`SELECT * FROM users`; // raw SQL
    console.log(users); // console.log 사용
    return users;
  }
}

// ✅ 권장 패턴
export class GoodController {
  @TypedRoute.Get()
  async getUsers(): Promise<UserResponse[]> {
    return this.userService.findAll();
  }
}
```

## 문서화 규칙

### 코드 주석
```typescript
/**
 * 사용자 정보를 생성합니다.
 * @param createDto 사용자 생성 요청 데이터
 * @returns 생성된 사용자 정보
 * @throws BadRequestException 이메일이 중복된 경우
 */
async createUser(createDto: CreateUserRequest): Promise<UserResponse> {
  // 구현 내용...
}
```

### API 문서화
- Nestia를 사용하여 자동 생성
- Swagger는 개발 환경에서만 활성화
- 모든 엔드포인트에 적절한 예시 제공

이 규칙들을 따라 Otto Handler 프로젝트의 코드 품질과 일관성을 유지해주세요.