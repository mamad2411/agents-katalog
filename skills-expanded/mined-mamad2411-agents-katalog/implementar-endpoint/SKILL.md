---
name: implementar-endpoint
description: "Implementa endpoints REST em NestJS com validação e tratamento de erros. Use quando o dev-backend ou o dev-bff vai adicionar uma rota a um serviço existente."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: implementar-endpoint

Adiciona um **novo endpoint** a um serviço NestJS existente: DTO de request/response, método no controller, lógica no service, registro no module e testes unitários — seguindo os contratos definidos pelo arquiteto.

**Agente:** dev-backend  
**Guardrails aplicáveis:** `00-core.md`, `backend.md`, `dados.md`, `seguranca.md`, `testes.md`

---

## Quando usar

- Para adicionar operação a serviço já existente (System ou Process API)
- Quando a especificação do endpoint já foi definida pelo arquiteto via `planejar-api` ou `mapear-contrato`
- Para implementar CRUD completo ou operação específica de domínio

---

## Pré-requisitos

- Contrato do endpoint definido: verbo HTTP, path, request shape, response shape, códigos de erro
- Serviço NestJS já inicializado (`criar-system-api` ou `criar-process-api`)
- Regras de negócio documentadas nos critérios de aceite

---

## Processo de execução

### Passo 1 — Criar DTOs

**DTO de request** (`dto/create-<recurso>.dto.ts`):
```typescript
import { IsString, IsEmail, IsOptional, IsUUID, MinLength } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class Create<Recurso>Dto {
  @IsString()
  @MinLength(2)
  name: string;

  @IsEmail()
  email: string;

  @IsUUID()
  @IsOptional()
  categoryId?: string;
}
```

Regras dos DTOs:
- Sempre usar `class-validator` — nunca validar manualmente na service
- Tipos TypeScript devem refletir exatamente o contrato do arquiteto
- `@IsOptional()` para campos opcionais; sem ele o campo é obrigatório por padrão
- Nunca usar `any` nos DTOs — todos os campos tipados explicitamente

**DTO de response** — quando a response difere da entidade do banco:
```typescript
export class <Recurso>ResponseDto {
  id: string;
  name: string;
  email: string; // mascarado se dado pessoal: seguranca.md §1
  createdAt: Date;
  // NUNCA incluir: passwordHash, tokenInterno, dados pessoais em claro
}
```

### Passo 2 — Implementar a service

Estrutura da service seguindo a responsabilidade da camada:

**System API — service com Prisma:**
```typescript
@Injectable()
export class <Recurso>Service {
  constructor(private readonly prisma: PrismaService) {}

  async create(dto: Create<Recurso>Dto): Promise<<Recurso>ResponseDto> {
    // 1. Verificar pré-condições de negócio
    const existing = await this.prisma.<recurso>.findUnique({
      where: { email: dto.email },
    });
    if (existing) throw new ConflictException('<Recurso> já existe com este email');

    // 2. Executar a operação
    const created = await this.prisma.<recurso>.create({ data: dto });

    // 3. Retornar apenas os campos necessários (não expor tudo do banco)
    return this.toResponseDto(created);
  }

  private toResponseDto(entity: <Recurso>): <Recurso>ResponseDto {
    return {
      id: entity.id,
      name: entity.name,
      createdAt: entity.createdAt,
    };
  }
}
```

**Process API — service que orquestra clients HTTP:**
```typescript
@Injectable()
export class <Fluxo>Service {
  constructor(
    private readonly systemAClient: SystemAClient,
    private readonly systemBClient: SystemBClient,
  ) {}

  async execute(dto: Execute<Fluxo>Dto): Promise<<Fluxo>ResponseDto> {
    // 1. Buscar dados necessários
    const resourceA = await this.systemAClient.findById(dto.aId);

    // 2. Aplicar regra de fluxo
    if (resourceA.status !== 'active') {
      throw new UnprocessableEntityException('Recurso A não está ativo');
    }

    // 3. Executar próximo passo do fluxo
    const result = await this.systemBClient.process(dto);

    return { success: true, resultId: result.id };
  }
}
```

### Passo 3 — Implementar o controller

```typescript
@Controller('<recursos>')
export class <Recurso>Controller {
  constructor(private readonly service: <Recurso>Service) {}

  @Post()
  @HttpCode(HttpStatus.CREATED)
  async create(@Body() dto: Create<Recurso>Dto): Promise<<Recurso>ResponseDto> {
    return this.service.create(dto);
  }

  @Get()
  async findAll(
    @Query('page', new DefaultValuePipe(1), ParseIntPipe) page: number,
    @Query('pageSize', new DefaultValuePipe(20), ParseIntPipe) pageSize: number,
  ) {
    // Nunca retornar lista sem paginação — dados.md §3
    return this.service.findAll({ page, pageSize: Math.min(pageSize, 100) });
  }

  @Get(':id')
  async findOne(@Param('id', ParseUUIDPipe) id: string) {
    return this.service.findOne(id);
  }
}
```

### Passo 4 — Registrar no module

```typescript
@Module({
  imports: [PrismaModule],
  controllers: [<Recurso>Controller],
  providers: [<Recurso>Service],
  exports: [<Recurso>Service], // exportar apenas se outro módulo precisar
})
export class <Recurso>Module {}
```

### Passo 5 — Escrever testes unitários da service

Usar `criar-teste-unitario` para os testes — não implementar sem testes.

### Passo 6 — Verificar checklist antes de concluir

- [ ] DTO valida todos os campos do contrato com `class-validator`
- [ ] Response não expõe campos sensíveis (`seguranca.md §1`)
- [ ] Nenhum `console.log` no código implementado (`backend.md §5`)
- [ ] Listas sempre paginadas (`dados.md §3`)
- [ ] Queries sempre parametrizadas (sem concatenação — `dados.md §1`)
- [ ] Erros usando exceções do NestJS (`ConflictException`, `NotFoundException`, etc.)
- [ ] Testes unitários da service escritos e passando

---

## Mapeamento de exceções NestJS para status HTTP

| Exceção NestJS | Status | Quando usar |
|---|---|---|
| `BadRequestException` | 400 | Validação de schema falhou |
| `UnauthorizedException` | 401 | Token ausente ou inválido |
| `ForbiddenException` | 403 | Sem permissão |
| `NotFoundException` | 404 | Recurso não encontrado |
| `ConflictException` | 409 | Duplicidade |
| `UnprocessableEntityException` | 422 | Regra de negócio violada |
| `InternalServerErrorException` | 500 | Nunca lançar explicitamente — deixar o filter tratar |

---

## Saída produzida

- `dto/create-<recurso>.dto.ts` e demais DTOs necessários
- `<recurso>.service.ts` com lógica implementada
- `<recurso>.controller.ts` com endpoints mapeados
- `<recurso>.module.ts` atualizado
- Testes unitários da service
