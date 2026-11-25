---
name: write-cross-cutting-code
description: Use when writing a reusable request-pipeline primitive rather than feature logic — a custom decorator (param/metadata/method-wrapper + applyDecorators bundles), a guard (metadata-driven role/scope, or an OR-composition "any of these guards" guard), a pipe (polymorphic/variant DTO validation, or wrapping a built-in pipe to throw your typed error), an interceptor (metadata-driven audit/logging that fires after the response), middleware (correlation id), or a custom validation constraint (sync or async-with-DI via class-validator). NestJS reference, framework-flexible.
metadata:
  author: Ken Nguyễn <ntnpro@gmail.com>
---

# Write cross-cutting code

The request-pipeline / aspect layer — decorators, guards, pipes, interceptors, middleware, custom
validators — that lives in the shared lib and keeps auth, validation, logging, audit, and context out
of feature handlers. Examples NestJS/TS, neutral `@org` domain. principle → **▸ Example** → **▸ Other
stacks**. For *feature-body* code see `write-service-code`; for the **error model + exception filter**
see `design-an-error-model`; for where these live see `structure-a-shared-backend-lib`.

## Core principle
**A cross-cutting concern (auth, validation, context extraction, audit, tracing) belongs in ONE
reusable primitive, not copy-pasted into every handler.** Build it once as a decorator/guard/pipe/
interceptor/middleware, unit-test it once, and apply it declaratively. The handler stays pure feature
logic.

## 1. Custom decorators — the three shapes (+ bundling)
- **Param decorator** (`createParamDecorator`) — extract typed context from the request, and validate
  it there so handlers receive a ready, trusted object:
  ```ts
  export const CurrentCaller = createParamDecorator((_d, ctx: ExecutionContext): Nullable<Caller> => {
    const req = ctx.switchToHttp().getRequest();
    return req.headers['x-caller'] ? JSON.parse(req.headers['x-caller']) : null;   // typed, parsed once
  });
  // a header-DTO variant validates the headers as a class and throws your BadRequestError on failure
  ```
- **Metadata decorator** (`SetMetadata`) — annotate a handler/class so a guard/interceptor can read the
  requirement later via `Reflector`:
  ```ts
  export const Roles = (...roles: Role[]) => SetMetadata(ROLES_KEY, roles);
  ```
- **Method-wrapper decorator** — replace `descriptor.value` to wrap behavior (timing, log-and-swallow,
  caching). (The log-and-swallow `@CatchException` lives in `design-an-error-model` §5.)
- **Bundle related decorators with `applyDecorators`** so callers apply one decorator, not five:
  ```ts
  export const UseAnyGuards = (...guards: Type<CanActivate>[]) =>
    applyDecorators(SetMetadata(ANY_GUARDS_KEY, guards), UseGuards(AnyGuard));   // metadata + guard in one
  ```
▸ *Other stacks:* Python decorators, Java annotations + an aspect/`HandlerInterceptor`, Go middleware
closures. Principle: extract-and-validate context, or annotate-then-read-by-reflection, in one named
primitive.

## 2. Guards — metadata-driven, and OR-composition
- **A metadata-driven guard** reads the requirement set by a decorator via `Reflector`; **no metadata =
  allow** (the guard is opt-in per handler):
  ```ts
  canActivate(ctx: ExecutionContext) {
    const required = this.reflector.get<Role[]>(ROLES_KEY, ctx.getHandler()) ?? [];
    if (!required.length) return true;
    const have = (ctx.switchToHttp().getRequest().caller?.roles ?? []);
    if (required.some((r) => have.includes(r))) return true;
    throw new UnauthorizedError('missing role');
  }
  ```
- **OR-composition guard** — when an endpoint should accept *any* of several auth methods (API key
  **or** JWT **or** session), run them and pass if **one** passes; otherwise rethrow the last failure.
  Resolve each guard from the DI container (`ModuleRef`) so it keeps its injected deps:
  ```ts
  @Injectable() export class AnyGuard implements CanActivate {
    constructor(private reflector: Reflector, private moduleRef: ModuleRef) {}
    async canActivate(ctx: ExecutionContext) {
      const guards = this.reflector.get<Type<CanActivate>[]>(ANY_GUARDS_KEY, ctx.getHandler()) ?? [];
      const results = await Promise.all(guards.map(async (G) => {
        try { return { ok: true, pass: await this.moduleRef.get(G, { strict: false }).canActivate(ctx) }; }
        catch (e) { return { ok: false, e }; }
      }));
      if (results.some((r) => r.ok && r.pass)) return true;
      throw results.reverse().find((r) => !r.ok)?.e ?? new UnauthorizedError();
    }
  }
  ```
  (Concrete auth guards — API-key role, token introspection, tenant mapping — are in
  `integrate-external-services` §5; this is the *composition* mechanic.)
▸ *Other stacks:* policy middleware that short-circuits on first-allow; a composite authorization rule.

## 3. Pipes — validate/transform at the boundary
- **Polymorphic / variant validation pipe** — when a request body's shape depends on a discriminator
  field, pick the right DTO class by that field and validate against it (instead of one bloated
  optional-everything DTO):
  ```ts
  export class VariantValidationPipe implements PipeTransform {
    constructor(private field: string, private map: Record<string, ClassConstructor<unknown>>) {}
    transform(data: Record<string, unknown>) {
      const dto = this.map[String(data[this.field] ?? '')];
      if (!dto) throw new BadRequestError(`unknown ${this.field}`);
      const errs = validateSync(plainToInstance(dto, data));
      if (errs.length) throw BadRequestError.fromValidationErrors(errs);
      return data;
    }
  }
  ```
- **Wrap a built-in pipe to throw your typed error** — e.g. a parse-uuid pipe that raises your
  `BadRequestError` instead of the framework's generic one, so the error body stays uniform.
▸ *Other stacks:* a request-binding/validation layer that maps discriminated unions to the right schema
and emits your standard error.

## 4. Interceptors — wrap the response, driven by metadata
- An interceptor sees **before and after** the handler — use it for response shaping, timing, and
  **metadata-driven audit logging**: read `@SetObjectType('listing')` / `@SetActionType('create')` via
  `Reflector`, and **after** the handler completes, fire an audit event **asynchronously** (don't block
  the response):
  ```ts
  intercept(ctx: ExecutionContext, next: CallHandler) {
    if (this.reflector.get(SKIP_AUDIT, ctx.getClass())) return next.handle();
    const meta = { objectType: this.reflector.get(OBJECT_TYPE, ctx.getClass()),
                   actionType: this.reflector.get(ACTION_TYPE, ctx.getHandler()) };
    return next.handle().pipe(tap((data) => this.audit.dispatch({ ...meta, caller: req.caller, body: req.body })));
  }
  ```
  Gate optional behavior (audit on/off) behind **config**, not a `NODE_ENV` branch.
▸ *Other stacks:* an `around` aspect / `HandlerInterceptor#postHandle` / response middleware reading
route metadata.

## 5. Middleware — earliest, per-request context
- **Correlation id** — accept an inbound `x-correlation-id` or generate one, put it on the request and
  echo it on the response, so a request is traceable across hops (feeds the trace id in
  `design-an-error-model` §3 and context propagation in `integrate-internal-services` §5):
  ```ts
  use(req, res, next) { const id = req.header('x-correlation-id') || uuid(); req.headers['x-correlation-id'] = id; res.set('x-correlation-id', id); next(); }
  ```
- Request logging with timing lives once here too (see `write-service-code` §7). Middleware is the
  place for concerns that must run **before** guards/pipes.
▸ *Other stacks:* any web framework's middleware chain; the principle (earliest, per-request context +
tracing) is universal.

## 6. Custom validation constraints
- **Reusable field rules as decorators** via `class-validator` — a **sync** constraint for pure checks,
  and an **async + DI** constraint that validates against a service (existence, uniqueness):
  ```ts
  @ValidatorConstraint({ async: false })
  export class IsNoHtmlConstraint implements ValidatorConstraintInterface {
    validate(v: string) { return !/<\/?[a-z][^>]*>/i.test(v); }
    defaultMessage() { return 'must not contain HTML'; }
  }
  export const IsNoHtml = (o?: ValidationOptions) => (obj: object, p: string) => Validate(IsNoHtmlConstraint, o)(obj, p);

  @ValidatorConstraint({ name: 'isCountryCode', async: true }) @Injectable()
  export class IsCountryCodeConstraint implements ValidatorConstraintInterface {
    constructor(private countries: CountryService) {}
    async validate(code: unknown) { return typeof code === 'string' && !!(await this.countries.byCode(code)); }
  }
  ```
- Keep messages clear; prefer a reusable decorator over inline checks scattered across DTOs.
▸ *Other stacks:* a custom validator/annotation in your validation library; async validators hit a
repository/service.

## Verification
- Cross-cutting logic lives in a **named primitive** (decorator/guard/pipe/interceptor/middleware),
  applied declaratively — not duplicated in handlers.
- Metadata decorators are **read via `Reflector`**; guards are **opt-in** (no metadata = allow);
  OR-composition resolves guards through DI and passes on first success.
- Pipes throw your **typed** error (uniform body); variant bodies validate against the right DTO.
- Interceptors fire side effects **after** the handler, **async**, gated by **config** (not `NODE_ENV`).
- Custom validators are reusable decorators; async ones inject their dependency.

## Related
- `design-an-error-model` — exception filter (the cross-cutting error primitive) + `@CatchException`.
- `structure-a-shared-backend-lib` — where these primitives live (the `infra-common`/`infra-auth` packages).
- `integrate-external-services` §5 (concrete auth guards) · `integrate-internal-services` §5 (context propagation).
- `write-service-code` (§4 helpers/decorators, §7 logging) · `write-unit-tests` (test each primitive in isolation).
