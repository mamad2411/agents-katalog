---
name: nestjs-development
description: Mecánica del framework NestJS — módulos y scopes de DI, decoradores de controller, DTOs con class-validator y ValidationPipe, orden real de middleware/guards/interceptors/pipes/filters, ConfigModule con validación de env, exception filters, testing con Test.createTestingModule, documentación con @nestjs/swagger, lifecycle hooks y shutdown. Usar al crear un módulo, controller, provider o pipe en NestJS, cuando un endpoint acepta un body sin validar o campos de más, o al revisar por qué un guard/interceptor no se ejecuta en el orden esperado. Para separación en capas y dónde vive la lógica de negocio, ver `backend-development`.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Desarrollo en NestJS

Convenciones para NestJS, ORM-neutral (TypeORM, Prisma, MikroORM aplican igual a las
capas de dominio/infraestructura). Para arquitectura general ver `backend-development`;
para SOLID a nivel de clase, `solid-principles`.

## 1. Módulos y providers

- Un módulo por dominio/feature (`OrdersModule`, `UsersModule`), no un módulo gigante.
  Cada módulo expone solo lo necesario en `exports`; el resto es un detalle interno.
- Providers son `@Injectable()` — inyectá por interfaz/token de dominio, no la
  implementación concreta, para poder mockear en tests (`provide: ORDERS_REPOSITORY`).
- **Scope por defecto: singleton** (una instancia para toda la app). Usá `Scope.REQUEST`
  solo cuando de verdad necesitás estado por-request (ej. datos del usuario autenticado
  inyectados en toda la cadena) — cuesta performance porque Nest recrea el árbol de
  dependencias en cada request.
- Evitá dependencias circulares entre módulos/providers: si `A` necesita `B` y `B`
  necesita `A`, es una señal de que falta extraer una tercera pieza (interfaz o
  servicio compartido) — `forwardRef()` es el escape, no la solución de diseño.

## 2. Controllers finos

- El controller parsea la request (vía DTO + pipes), invoca un caso de uso/servicio, y
  devuelve la respuesta. Nada de lógica de negocio ni acceso directo a un repositorio
  con reglas de negocio adentro.
- Un método de controller por acción HTTP; si necesita orquestar varios servicios,
  esa orquestación es un caso de uso, no código suelto en el handler.

## 3. DTOs y validación

- Un DTO por cada payload de entrada, con decoradores de `class-validator`
  (`@IsString()`, `@IsEmail()`, `@IsOptional()`, etc.) — nunca `any`/`unknown` para el
  body de un endpoint.
- Registrá el `ValidationPipe` global con:

```typescript
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,            // descarta propiedades sin decorador
    forbidNonWhitelisted: true, // rechaza el request si vienen propiedades extra
    transform: true,            // castea el payload plano al tipo del DTO
  }),
);
```

- `whitelist: true` filtra en silencio lo no declarado en el DTO; combinado con
  `forbidNonWhitelisted: true` en vez de filtrar, **rechaza** el request — preferí esta
  combinación en APIs donde un campo extra puede indicar un error del cliente.
- Con `transform: true`, params de ruta/query (siempre `string` en la red) se convierten
  al tipo declarado en el DTO/firma del método (ej. a `number`).

## 4. Orden real del ciclo de vida de un request

No es un detalle menor: guards, interceptors y pipes se ejecutan en este orden exacto
(global → controller → ruta, salvo los filtros que son al revés):

```
1. Middleware (global → de módulo)
2. Guards (global → controller → ruta)
3. Interceptors, tramo previo al handler (global → controller → ruta)
4. Pipes (global → controller → ruta → de parámetro)
5. Controller (handler) → Service
6. Interceptors, tramo posterior (ruta → controller → global)
7. Exception filters — SOLO si hubo una excepción no capturada (ruta → controller → global)
8. Response
```

- Los **guards** corren después de todo middleware y antes de cualquier interceptor o
  pipe — son el lugar correcto para autenticación/autorización (`CanActivate`), no un
  interceptor.
- Los **filtros de excepción son la única pieza que resuelve del nivel más específico
  al más general** (ruta → controller → global): si un filtro de ruta captura la
  excepción, uno de controller o global no la vuelve a ver — no hay "propagación" entre
  filtros salvo herencia explícita.
- Una excepción atrapada con `try/catch` dentro del código nunca llega a los exception
  filters — los filtros solo actúan sobre excepciones no capturadas.

## 5. Exception filters

- Un `ExceptionFilter` global mapea excepciones de dominio a respuestas HTTP
  consistentes (problem details — ver `backend-development` § modelo de errores):

```typescript
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const status = exception instanceof HttpException
      ? exception.getStatus()
      : HttpStatus.INTERNAL_SERVER_ERROR;

    response.status(status).json({
      type: 'about:blank',
      title: exception instanceof HttpException ? exception.message : 'Internal error',
      status,
    });
  }
}
```

- No expongas el `exception.stack` ni el mensaje crudo de un error inesperado (5xx) en
  la respuesta — logueá el detalle completo del lado del servidor, devolvé algo genérico
  al cliente.

## 6. Configuración

- `ConfigModule.forRoot()` con `validationSchema` (Joi o Zod) para fallar en el arranque
  si falta una env var o tiene el tipo incorrecto, no a mitad de un request en producción.
- Tipá el acceso a configuración con un `ConfigService` inyectado y un
  `ConfigType`/schema propio — no `process.env.X` disperso por el código.

## 7. Testing

- `Test.createTestingModule({ providers: [...], imports: [...] })` para levantar el
  módulo real con mocks/stubs inyectados por token en las dependencias externas
  (repositorio, cliente HTTP), no toda la app.
- Un test de un `Controller` mockea el `Service`; un test de un `Service` mockea el
  repositorio/adapter — nunca el motor de base de datos real en un test unitario
  (ver `unit-testing` e `integrity-testing` para la frontera unitario/integración).

## 8. Documentación con @nestjs/swagger

- Decorá DTOs con `@ApiProperty()` y controllers con `@ApiTags()`/`@ApiOperation()`/
  `@ApiResponse()` — el spec sale del código, no se mantiene a mano por separado
  (ver `api-openapi-docs` para el resto del contrato: errores, versionado, linting).
- `SwaggerModule.createDocument()` + `SwaggerModule.setup()` solo en entornos donde
  tenga sentido exponerlo (no necesariamente producción pública sin autenticación).

## 9. Lifecycle hooks y shutdown

- `OnModuleInit`/`OnModuleDestroy` para inicializar/liberar recursos de un provider
  (conexión a un servicio externo, listener) — no lo hagas en el constructor.
- `app.enableShutdownHooks()` habilita que Nest invoque `onApplicationShutdown` en cada
  provider al recibir una señal de apagado del sistema operativo — necesario para drenar
  conexiones a DB/colas antes de salir (ver `backend-development` § graceful shutdown).

## Anti-patrones

- Lógica de negocio dentro del controller o de un guard.
- DTO tipado como `any` "para no pelear con el validador".
- Autenticación implementada como interceptor en vez de guard.
- `forwardRef()` como solución permanente a una dependencia circular de diseño.
- Loguear o devolver `exception.stack` al cliente en un filtro global.

## Checklist

- [ ] Un módulo por dominio; providers inyectados por interfaz/token, no por clase concreta.
- [ ] `ValidationPipe` global con `whitelist`, `forbidNonWhitelisted` y `transform`.
- [ ] Ningún controller con lógica de negocio; delega a un servicio/caso de uso.
- [ ] Autenticación/autorización en guards, no en interceptors ni middleware.
- [ ] Exception filter global sin fugar stack trace en respuestas 5xx.
- [ ] Config validada al boot vía `ConfigModule` + schema.
- [ ] Tests con `Test.createTestingModule` y mocks por token, no DB real en unitarios.
- [ ] DTOs documentados con `@nestjs/swagger`.
- [ ] `enableShutdownHooks()` habilitado si hay recursos que cerrar prolijamente.
