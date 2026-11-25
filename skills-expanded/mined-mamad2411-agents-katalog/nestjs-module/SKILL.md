---
name: nestjs-module
description: "Convenciones para módulos NestJS: estructura module/controller/service/dto/entities, DI, DTOs con class-validator y class-transformer, ValidationPipe global, guards, interceptors, filters, @nestjs/config, errores y Swagger. Usar al crear o modificar recursos, endpoints o configuración en NestJS."
---

# nestjs-module

## Objetivo
Crear y mantener módulos NestJS coherentes, tipados y testeables: controllers delgados, lógica en services, validación estricta en la frontera, errores normalizados y OpenAPI generado desde el código.

## Cuándo aplicarla
- Crear un recurso nuevo o añadir endpoints a uno existente.
- Añadir guards, interceptors, pipes o exception filters.
- Configurar `main.ts` (ValidationPipe, Swagger, versionado, CORS) o `@nestjs/config`.
- Refactorizar módulos con dependencias circulares o lógica en controllers.

## Antes de empezar
1. Carga `core:project-context` y lee `package.json`: versiones de `@nestjs/core`, `@nestjs/swagger`, `@nestjs/config`, `class-validator`, ORM. **Verifica la versión en el manifiesto del proyecto**; esta skill apunta a NestJS 11 (Node ≥ 20, Express 5 por defecto).
2. Diferencias relevantes Nest 10 → 11: Express 5 cambia comodines de rutas (`'*splat'` o `'{*splat}'` en lugar de `'*'` en middlewares/`forRoutes`), `@nestjs/config` 4 cambia el orden de precedencia al resolver valores entre `process.env`, variables validadas y `load` (revisa la guía oficial de migración antes de actualizar), y `@nestjs/cache-manager` pasa a usar Keyv.
3. Toma un módulo existente como plantilla y replica nombres, rutas y estilo de errores.

## Estructura de carpetas
```
src/
├── main.ts
├── app.module.ts
├── config/                 # configuration.ts + validación de env
├── common/                 # filters/, guards/, interceptors/, decorators/, dto/ (paginación)
└── orders/
    ├── orders.module.ts
    ├── orders.controller.ts
    ├── orders.service.ts
    ├── orders.repository.ts          # opcional: si hay consultas complejas
    ├── dto/
    │   ├── create-order.dto.ts
    │   ├── update-order.dto.ts
    │   ├── list-orders-query.dto.ts
    │   └── order-response.dto.ts
    ├── entities/order.entity.ts      # TypeORM (con Prisma: sin entities, usa tipos generados)
    ├── orders.service.spec.ts
    └── (test/orders.e2e-spec.ts en la raíz test/)
```
Generación rápida: `npx nest g resource orders --no-spec` (elige REST) y luego ajusta a estas convenciones; o `nest g module|controller|service orders`.

## Pasos
1. **Module**: importa `TypeOrmModule.forFeature([Order])` (o un `PrismaModule` global), declara controller y providers, exporta solo el service si otros módulos lo usan.
2. **DTOs**: validación con `class-validator`, transformación con `class-transformer`, documentación con `@ApiProperty`. `UpdateDto` extiende `PartialType(CreateDto)` importado de `@nestjs/swagger` (no de `@nestjs/mapped-types`) para conservar metadata OpenAPI.
3. **Service**: inyecta repositorio/`PrismaService`; lanza `NotFoundException`, `ConflictException`, etc.; transacciones para escrituras múltiples.
4. **Controller**: rutas REST, pipes de parámetros, decoradores Swagger, `@HttpCode` cuando no sea el default.
5. **Registrar** el módulo en `AppModule` (o en el módulo padre).
6. **Tests**: unit del service y e2e (ver `backend:backend-testing`).
7. **Verificar**: `npx tsc --noEmit`, `npm run lint`, `npm test`.

Ejemplo completo de un recurso (entity, DTOs, service, controller, filter RFC 9457, `main.ts`): lee [references/resource-example.md](references/resource-example.md) cuando vayas a generar un recurso desde cero.

## DTOs: patrón base
```ts
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { Type } from 'class-transformer';
import { IsEnum, IsInt, IsOptional, IsString, IsUUID, Length, Max, Min } from 'class-validator';

export class CreateOrderDto {
  @ApiProperty({ format: 'uuid' })
  @IsUUID()
  customerId!: string;

  @ApiProperty({ minLength: 1, maxLength: 200 })
  @IsString()
  @Length(1, 200)
  description!: string;

  @ApiProperty({ minimum: 1, description: 'Importe en centavos' })
  @IsInt()
  @Min(1)
  amountCents!: number;
}

export class ListOrdersQueryDto {
  @ApiPropertyOptional({ default: 20, maximum: 100 })
  @IsOptional() @Type(() => Number) @IsInt() @Min(1) @Max(100)
  limit = 20;

  @ApiPropertyOptional()
  @IsOptional() @IsString()
  cursor?: string;

  @ApiPropertyOptional({ enum: OrderStatus })
  @IsOptional() @IsEnum(OrderStatus)
  status?: OrderStatus;
}
```
- Objetos anidados: `@ValidateNested()` + `@Type(() => ItemDto)`; arrays: `@IsArray() @ArrayMaxSize(50)`.
- Con `transform: true`, los query params llegan como string: usa `@Type(() => Number)` o `enableImplicitConversion` (con cuidado: `"false"` → `true` en booleanos; usa `@Transform` explícito para booleanos).

## Controller: patrón base
```ts
@ApiTags('orders')
@Controller({ path: 'orders', version: '1' })
export class OrdersController {
  constructor(private readonly ordersService: OrdersService) {}

  @Post()
  @ApiCreatedResponse({ type: OrderResponseDto })
  create(@Body() dto: CreateOrderDto): Promise<OrderResponseDto> {
    return this.ordersService.create(dto);
  }

  @Get(':id')
  @ApiOkResponse({ type: OrderResponseDto })
  @ApiNotFoundResponse()
  findOne(@Param('id', ParseUUIDPipe) id: string) {
    return this.ordersService.findOne(id);
  }

  @Delete(':id')
  @HttpCode(HttpStatus.NO_CONTENT)
  remove(@Param('id', ParseUUIDPipe) id: string): Promise<void> {
    return this.ordersService.remove(id);
  }
}
```

## main.ts mínimo
```ts
const app = await NestFactory.create(AppModule, { bufferLogs: true });
app.enableVersioning({ type: VersioningType.URI });      // /v1/orders
app.setGlobalPrefix('api');                               // /api/v1/orders
app.useGlobalPipes(new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true }));
app.useGlobalInterceptors(new ClassSerializerInterceptor(app.get(Reflector)));
app.useGlobalFilters(new ProblemDetailsFilter());
app.enableShutdownHooks();
const config = new DocumentBuilder().setTitle('API').setVersion('1.0').addBearerAuth().build();
SwaggerModule.setup('docs', app, () => SwaggerModule.createDocument(app, config));
await app.listen(app.get(ConfigService).getOrThrow<number>('PORT'));
```
Si el filtro/guard global necesita DI, regístralo como provider con `APP_FILTER`/`APP_GUARD`/`APP_PIPE` en `AppModule` en lugar de `useGlobal*`.

## Configuración con @nestjs/config
```ts
ConfigModule.forRoot({
  isGlobal: true,
  cache: true,
  load: [configuration],
  validate: (env) => envSchema.parse(env),   // zod, o validationSchema con Joi
}),
```
- Accede con `config.getOrThrow<string>('DATABASE_URL')` o con namespaces tipados (`registerAs('db', ...)` + `@Inject(dbConfig.KEY) cfg: ConfigType<typeof dbConfig>`).
- Falla al arrancar si falta una variable; nunca leas `process.env` fuera de `config/`.

## Guards, interceptors, filters, pipes
| Pieza | Úsala para | Ejemplo |
|---|---|---|
| Guard (`CanActivate`) | Autenticación/autorización | `JwtAuthGuard`, `RolesGuard` con `Reflector` + decorador `@Roles()` |
| Interceptor (`NestInterceptor`) | Transversal antes/después: logging, timeout, mapeo de respuesta, caché | `TimeoutInterceptor` con `timeout()` de RxJS |
| Pipe (`PipeTransform`) | Validar/transformar un argumento | `ParseUUIDPipe`, pipe de zod |
| Filter (`ExceptionFilter`) | Traducir excepciones a respuesta HTTP | `ProblemDetailsFilter` (RFC 9457) |
| Middleware | Nivel Express/Fastify: request-id, helmet | `app.use(helmet())` |

Guard de roles con metadata:
```ts
export const ROLES_KEY = 'roles';
export const Roles = (...roles: Role[]) => SetMetadata(ROLES_KEY, roles);

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private readonly reflector: Reflector) {}
  canActivate(ctx: ExecutionContext): boolean {
    const required = this.reflector.getAllAndOverride<Role[]>(ROLES_KEY, [ctx.getHandler(), ctx.getClass()]);
    if (!required?.length) return true;
    const { user } = ctx.switchToHttp().getRequest();
    return required.some((r) => user?.roles?.includes(r));
  }
}
```

## Manejo de errores
- Services lanzan excepciones de `@nestjs/common` (`NotFoundException(\`Order ${id} not found\`)`) o errores de dominio propios que un filter mapea.
- Traduce errores del ORM en el service o filter: TypeORM `QueryFailedError` con código `23505` → 409; Prisma `P2002` → 409, `P2025` → 404.
- Un único filter global produce `application/problem+json` con `type`, `title`, `status`, `detail`, `instance` y, para validación, `errors[]`.
- Loguea errores 5xx con contexto (request-id), nunca devuelvas el stack al cliente.

## Integración con LLMs (LangChain.js)
Encapsula el modelo o agente en un provider: `LlmModule` con `useFactory` que lee `ConfigService` y crea el modelo/agente una sola vez; los services lo inyectan por token. Para streaming, usa `@Sse()` devolviendo un `Observable<MessageEvent>` o escribe en `res` con `text/event-stream`. Detalle en `backend:langchain-chains`.

## Antipatrones
- Lógica de negocio o acceso a repositorio en el controller.
- DTOs sin decoradores (el `ValidationPipe` los deja pasar sin validar) o interfaces en lugar de clases como tipo de `@Body()`.
- Devolver entidades con campos sensibles (`passwordHash`) sin `@Exclude()` ni ResponseDto.
- `forwardRef` para "arreglar" dependencias circulares.
- `synchronize: true` fuera de local; `process.env.X` en services.
- `try { ... } catch { throw new InternalServerErrorException() }` que oculta la causa.
- Importar `PartialType` de `@nestjs/mapped-types` en proyectos con Swagger.

## Checklist final
- [ ] Estructura `module/controller/service/dto/entities` y nombres kebab-case.
- [ ] DTOs con class-validator + `@ApiProperty`; `UpdateDto` con `PartialType` de `@nestjs/swagger`.
- [ ] `ValidationPipe` global con `whitelist`, `forbidNonWhitelisted`, `transform`.
- [ ] Params con `ParseUUIDPipe`/`ParseIntPipe`; paginación con máximo.
- [ ] Status codes correctos (201, 204, 404, 409) y errores normalizados.
- [ ] Guards de auth/roles aplicados donde corresponde.
- [ ] Config vía `ConfigService` con validación al arrancar.
- [ ] Swagger: `@ApiTags`, respuestas tipadas.
- [ ] Tests unit + e2e; `tsc --noEmit`, lint y tests en verde.
