---
name: estructura-backend-roque
description: Diseña y organiza backends Node.js/TypeScript con APIs REST por funcionalidad, capas claras y funciones reutilizables documentadas. Úsala al crear un backend, módulo o endpoint, o al ordenar uno existente.
---

# Estructura Backend Roque

## Alcance

Construye un monolito modular por capacidades de negocio. Cada módulo es dueño de sus rutas, validación, coordinación e integraciones. No presupongas carpetas, módulos de ejemplo ni otras skills instaladas en el equipo. Para un backend nuevo puedes consultar [Roque-stack](https://github.com/Jonathan03R/Roque-stack); revisa su código vigente antes de usarlo. Su generador básico emplea `controller/`, `schemas/`, `services/` y un archivo `.route.ts`; adapta el módulo a la convención del proyecto cuando crezca.

Si están disponibles, usa `apis-roque` para detalles del contrato de errores y `esquema-roque` para SQL/RLS. Esta skill funciona sin ellas. Instrucciones del usuario y del repositorio prevalecen.

## Antes de crear o cambiar una API

1. Lee `AGENTS.md` aplicables. Localiza routers, módulos, validadores, servicios, clientes, contratos y documentación con búsqueda en el repositorio; no supongas rutas fijas.
2. Busca operaciones y funciones equivalentes, incluido `docs/REUTILIZABLES.md` cuando exista. Reutiliza dueño existente antes de crear otro helper o endpoint.
3. Define recurso, actor autorizado, entrada, salida, efectos, errores y compatibilidad. Conserva rutas, payloads, permisos y datos existentes si el pedido solo reorganiza código.
4. Compara estructura local con un módulo bien organizado si lo hay. Si no, usa la estructura orientativa siguiente; no añadas carpetas vacías.

## Estructura orientativa

```text
<raiz-de-modulos>/<capacidad>/
├── <capacidad>.routes.ts           # monta subrutas y middleware común
├── routes/                         # opcional al crecer: endpoints por subcapacidad
├── controllers/                    # entrada HTTP, validación y coordinación
├── schemas/                        # contratos de entrada/salida
├── services/                       # base de datos, APIs externas, archivos
├── utils/                          # funciones puras propias de la capacidad
└── README.md                       # opcional si el contrato necesita explicación

<raiz-compartida>/                  # helpers usados por varias capacidades
docs/REUTILIZABLES.md              # catálogo cuando haya helpers compartidos
```

- Nombra carpetas y archivos por negocio en `kebab-case`. El nombre visible puede diferir del identificador técnico: **AaaS** como marca, `aaas` como identificador si el producto lo conserva; `asistente-ia` si ese es el concepto aprobado. No cambies rutas o tablas por renombrar una carpeta.
- Una capacidad pequeña puede tener un router y un archivo por responsabilidad. Divide rutas y archivos cuando separen casos de uso reales. Evita archivos gigantes, una carpeta por función trivial y capas vacías.
- Coloca pruebas existentes junto a su unidad, siguiendo convención local. Una reorganización conserva esas pruebas y sus contratos.

## Límites entre capas

| Capa | Responsabilidad |
| --- | --- |
| Router | Declara método, path, middleware y controlador; no ejecuta negocio. |
| Controller | Valida path, query y body; coordina flujo; forma respuesta HTTP. |
| Schema | Define validación y tipos; no hace IO ni lee secretos. |
| Service | Consulta almacenamiento o sistemas externos; encapsula integración y errores técnicos. |
| Utilidad | Transforma o calcula sin IO ni estado de request. |
| Compartida | Resuelve un contrato usado por varias capacidades, con dueño y documentación. |

No importes un controlador desde otro controlador para compartir lógica. Extrae esa lógica al servicio o helper apropiado. Usa interfaces o repositorios adicionales solo si simplifican una dependencia real; no impongas Clean Architecture completa por defecto.

## Contrato REST

- Diseña URLs alrededor de recursos, usa plural y métodos HTTP según efecto: `GET` lee, `POST` crea o ejecuta una operación, `PUT` reemplaza, `PATCH` modifica parcialmente y `DELETE` elimina. Si el proyecto versiona rutas, respeta su versión.
- Valida `params`, `query` y `body` antes de efectos. Pagina colecciones potencialmente grandes; define filtros y orden estables. No inventes campos ni respuestas que el consumidor no pidió.
- Autentica y comprueba pertenencia/permisos en el servidor antes de consultar o modificar recursos de otro usuario. No confíes en IDs, roles o scopes enviados por el cliente.
- Mantén respuesta de éxito consistente con el proyecto. Para fallos, usa el helper común; `message` debe ser humano y seguro, `code` estable, `requestId` rastreable y detalles técnicos solo para diagnóstico. Conserva status/body de proveedores externos sin exponer HTML, cookies, tokens ni credenciales al cliente. Si existe `apiErrorResponse`, úsalo.
- En escrituras que puedan repetirse por reintento, decide y documenta idempotencia o detección de duplicados cuando el efecto lo requiera. No añadas este mecanismo a lecturas o acciones que no lo necesitan.

## Funciones reutilizables

Aplica esta regla de `go-feature-architecture` al backend TypeScript:

1. Busca primero en el código y en `docs/REUTILIZABLES.md` si existe.
2. Lógica exclusiva de una capacidad queda en su módulo. Solo mueve a carpeta compartida una función con uso real en varias capacidades o un contrato común ya confirmado; evita abstraer por posibilidad futura.
3. Documenta cada helper compartido en `docs/REUTILIZABLES.md`. Si no existe, créalo al incorporar el primer helper compartido. Registra **firma TypeScript exacta**, ruta/export, propósito, entradas, salida, efectos (IO/DB/red), errores y límites de uso. Incluye ejemplo breve solo si evita ambigüedad.
4. Actualiza catálogo al cambiar firma o eliminar helper. No dupliques funciones equivalentes entre módulos.

## Cierre

Revisa importaciones, rutas montadas, contratos y consumidores afectados. Usa comprobaciones acordes al pedido y a las instrucciones del usuario. Informa por separado revisión de código, compilación, pruebas y ejecución real; ninguna sustituye a otra.
