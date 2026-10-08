# E2E Testing Skill

## ID de task origen

- `T-0133`
- Estado: `aprobada`
- Fecha: `2026-04-12`

## Objetivo

Guiar la creación de pruebas end-to-end en AtlasERP para validar flujos completos.

## Procedimiento

### 1. Backend E2E (NestJS)

- **Qué probar**: flujos completos a través de HTTP usando la API real.
- **Setup**: base de datos de test limpia, seeds mínimos, app NestJS levantada.
- **Framework**: Jest + Supertest.

#### Flujos críticos a probar

- Registro / login / refresh / logout.
- CRUD completo de entidades principales.
- Validaciones de permisos (acceso denegado sin rol correcto).
- Scoping por organización (no ver datos de otra org).
- Paginación y filtros.
- Operaciones de sync batch.

#### Estructura

```typescript
describe("BankAccounts E2E", () => {
  let app: INestApplication;
  let authToken: string;

  beforeAll(async () => {
    // Levantar app y obtener token
  });

  afterAll(async () => {
    // Cerrar app y limpiar DB
  });

  it("POST /api/v1/financial/bank-accounts debería crear cuenta", async () => {
    const res = await request(app.getHttpServer())
      .post("/api/v1/financial/bank-accounts")
      .set("Authorization", `Bearer ${authToken}`)
      .send({
        /* dto */
      })
      .expect(201);
    expect(res.body.data.id).toBeDefined();
  });
});
```

### 2. Frontend E2E

- **Qué probar**: flujos de usuario completos en el navegador.
- **Framework sugerido**: Playwright o Cypress.
- **Flujos críticos**: login, navegación, crear/editar/eliminar entidades, sync center.

### 3. Sync E2E

- **Flujo online → offline → online**: operar offline, reconectar, validar sync.
- **Conflictos**: generar edición concurrente, verificar aparición en Sync Center.
- **Persistencia de cola**: encolar, reiniciar app, verificar cola intacta.

### 4. Datos de prueba

- Seeds específicos para E2E (organización test, usuario test, datos demo).
- Limpieza post-test para evitar contaminación entre runs.

### 5. Restricciones

- Tests E2E son lentos; ejecutar solo en CI o bajo demanda, no en watch mode.
- No duplicar cobertura que ya tengan unit/integration tests.
- Mantener tests estables: evitar selectores frágiles o timing issues.

## Referencia

- `docs/07-dev-workflow/03-criterios-modulo-terminado.md`
- `docs/08-codex/prompts/testing-master-prompt.md`
