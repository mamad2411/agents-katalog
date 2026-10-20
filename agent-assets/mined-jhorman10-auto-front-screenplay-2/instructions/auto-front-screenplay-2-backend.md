---
applyTo: "backend/**/*.py"
---

> **Scope**: Se aplica a proyectos con capa backend. Si el proyecto usa un lenguaje o estructura diferente, adaptar la sección de convenciones y wiring al stack real definido en esta misma instrucción.

# Instrucciones para Archivos de Backend (Python/FastAPI)

## Arquitectura en Capas

Siempre sigue la arquitectura en capas del proyecto:

```
routes → services → repositories → MongoDB
```

- **`app/routes/`**: Solo parsear HTTP + instanciar dependencias + delegar al service.
- **`app/services/`**: Solo lógica de negocio. Recibe repository por constructor.
- **`app/repositories/`**: Único lugar con acceso a MongoDB via Motor.
- **`app/models/`**: Solo Pydantic schemas (no documentos DB).

## Wiring de Dependencias (patrón obligatorio en routers)

```python
# ✅ Correcto — Depends() en la firma del endpoint
@router.post("/")
async def create_item(body: ItemCreate, db=Depends(get_db)):
    repo = ItemRepository(db)
    service = ItemService(repo)
    return await service.create(body)
```

NUNCA inyectar `get_db()` directamente como `db = get_db()` fuera de `Depends()`.
NUNCA instanciar repositorios o servicios fuera del router.

## Convenciones de Código

- Todas las funciones que tocan la DB son `async def`.
- Nombres en `snake_case` para funciones y variables.
- Los endpoints FastAPI siempre tienen response model explícito o retornan dict serializable.
- Usar `uid` de Firebase como clave única en MongoDB.
- Importar configuración siempre desde `app.config.settings` o `app.config.database`.

## Nuevas Rutas / Controladores

Para agregar un nuevo endpoint:
1. Crear el archivo del router/controlador en la capa de entrada del proyecto
2. Registrar el router/controlador en el punto de montaje principal de la aplicación
3. Seguir el patrón de wiring de dependencias definido en la sección anterior

> Ver `README.md` para la estructura de carpetas específica del proyecto.

## Nunca hacer

- Inyectar la fuente de datos directamente en servicios o modelos (solo en la capa de entrada).
- Lógica de negocio en los routers.
- Operaciones MongoDB síncronas (siempre `await`).

---

> Para estándares de código limpio, SOLID, nombrado, API REST, seguridad y observabilidad, ver `.github/docs/lineamientos/dev-guidelines.md`.
