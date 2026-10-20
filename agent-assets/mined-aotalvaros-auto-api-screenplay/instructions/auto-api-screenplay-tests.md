---
applyTo: "backend/tests/**/*.py,frontend/src/__tests__/**/*.{js,jsx}"
---

> **Scope**: Las reglas de backend aplican a proyectos con tests en Python; las de frontend aplican a proyectos con tests en JS/JSX. En proyectos con otro stack, adaptar las herramientas y convenciones manteniendo los principios (independencia, aislamiento, AAA, cobertura ≥ 80%).

# Instrucciones para Archivos de Pruebas Unitarias

## Principios

- **Independencia**: cada test es 100% independiente — sin estado compartido entre tests.
- **Aislamiento**: mockear SIEMPRE dependencias externas (DB, Firebase, API REST, sistema de archivos).
- **Claridad**: nombre del test debe describir la función bajo prueba y el escenario (qué pasa cuando X).
- **Cobertura**: cubrir happy path, error path y edge cases para cada unidad.

## Backend (pytest)

### Estructura de archivos
```
backend/tests/
  conftest.py                        ← fixtures compartidas
  services/test_<feature>_service.py
  repositories/test_<feature>_repository.py
  routes/test_<feature>_router.py
```

### Convenciones
- Nombre: `test_[función]_[escenario]` (ej: `test_create_user_success`, `test_create_user_duplicate_email`)
- Usar `@pytest.mark.asyncio` para funciones asíncronas.
- Mockear repositorios en tests de servicios con `AsyncMock`.
- Usar `AsyncClient` + `ASGITransport` para tests de endpoints.

```python
# Ejemplo mínimo de test de servicio
@pytest.mark.asyncio
async def test_create_user_success():
    mock_repo = MagicMock()
    mock_repo.create = AsyncMock(return_value={"uid": "abc"})
    service = UserService(mock_repo)
    result = await service.create({"uid": "abc", "email": "a@b.com"})
    assert result["uid"] == "abc"
```

## Frontend (Vitest + Testing Library)

### Estructura de archivos
```
frontend/src/__tests__/
  [ComponentName].test.jsx
  use[HookName].test.js
```

### Convenciones
- Nombre del describe: nombre del componente/hook.
- Nombre del it/test: `[verbo] [qué hace] [condición]` (ej: `renders login button when unauthenticated`).
- Usar `vi.mock()` para mockear módulos externos (Firebase, fetch).
- Siempre limpiar mocks con `beforeEach(() => vi.clearAllMocks())`.

```jsx
// Ejemplo mínimo de test de componente
describe('LoginPage', () => {
  it('renders email input', () => {
    render(<LoginPage />);
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
  });
});
```

## Nunca hacer

- Tests que dependen del orden de ejecución.
- Llamadas reales a Firebase, MongoDB o APIs externas.
- `console.log` permanentes en tests.
- Lógica condicional dentro de un test (if/else).
- Usar `sleep` para sincronización temporal (cero tests "flaky").

---

> Para quality gates, pirámide de testing, TDD, CDC y nomenclatura Gherkin, ver `.github/docs/lineamientos/dev-guidelines.md` §7 y `.github/docs/lineamientos/qa-guidelines.md`.

### Estructura AAA obligatoria
```python
# GIVEN — preparar datos y contexto
# WHEN  — ejecutar la acción bajo prueba
# THEN  — verificar el resultado esperado
```

### DoR de Automatización
Antes de automatizar un flujo, verificar:
- [ ] Caso ejecutado exitosamente en manual sin bugs críticos
- [ ] Caso de prueba detallado con datos identificados
- [ ] Viabilidad técnica comprobada
- [ ] Ambiente estable disponible
- [ ] Aprobación del equipo

### DoD de Automatización
Un script finaliza cuando:
- [ ] Código revisado por pares (pull request review)
- [ ] Datos desacoplados del código
- [ ] Integrado al pipeline de CI
- [ ] Con documentación y trazabilidad hacia la HU
