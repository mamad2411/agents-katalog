---
name: package-nestjs
description: Boilerplate and patterns for new NestJS modules. Use when creating new packages or extending the @adatechnology/package-nestjs base.
---

# 📦 NestJS Package Standards

## 🏗️ Dynamic Module Pattern
```typescript
@Module({
  providers: [ExampleService],
  exports: [ExampleService],
})
export class ExampleModule {
  static forRoot(options: ExampleOptions): DynamicModule {
    return {
      module: ExampleModule,
      providers: [
        { provide: EXAMPLE_OPTIONS_TOKEN, useValue: options },
        ExampleService,
      ],
      exports: [ExampleService],
    };
  }
}
```

## 🛡️ Service Injection
```typescript
@Injectable()
export class ExampleService implements ExampleServiceInterface {
  constructor(
    @Inject(EXAMPLE_OPTIONS_TOKEN) private readonly options: ExampleOptions,
    @Inject(LOGGER_PROVIDER) private readonly logger: LoggerProviderInterface
  ) {}
}
```

## 🛠️ Exports Guidelines
- **index.ts**: Only export what is intended for public use (Modules, Interfaces, Tokens).
- **Internal**: Keep implementation details (private services, helpers) out of the main `index.ts`.

## 🚨 Standards
- Always use **CommonJS** output.
- Always include a `README.md` and `SKILL.md` (this file) in new packages.
