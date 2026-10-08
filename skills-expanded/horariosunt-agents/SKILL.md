# 🏫 AGENTS.md — SiHorarios UNT

> **Contexto Global del Sistema de Horarios Académicos**
> Escuela de Ingeniería de Sistemas — Universidad Nacional de Trujillo

---

## 1. Descripción General

Sistema web de gestión de horarios académicos universitarios construido como **Next.js 16 Full Stack SPA**. Permite la administración de ciclos, cursos, docentes, aulas/laboratorios, y la asignación de horarios de forma manual o automática con validación de conflictos. Genera reportes PDF y mantiene un log de auditoría completo.

### Credenciales por defecto
| Rol | Email | Contraseña |
|-----|-------|------------|
| Admin | `admin@unt.edu.pe` | `password` |
| Secretaria | `secretaria@unt.edu.pe` | `password` |

---

## 2. Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| **Framework** | Next.js 16 (App Router, Turbopack) |
| **Frontend** | React 19, Recharts, jsPDF + jspdf-autotable, Lucide React |
| **Estilos** | Tailwind CSS 4 + Vanilla CSS (`globals.css`) |
| **Backend** | Next.js API Routes (`app/api/`) |
| **Base de datos** | PostgreSQL (driver `pg`, consultas SQL raw) |
| **Autenticación** | JWT custom (biblioteca `jose`) + cookies HttpOnly |
| **Hash passwords** | `bcryptjs` |
| **Lenguaje** | TypeScript 5 |

---

## 3. Arquitectura del Proyecto

```
horariosUNT/
├── app/
│   ├── page.tsx                    # Login (página raíz)
│   ├── layout.tsx                  # Root layout (metadata + globals.css)
│   ├── globals.css                 # Design system completo (CSS vanilla)
│   ├── (app)/                      # Route group autenticado
│   │   ├── layout.tsx              # Sidebar + UserContext + protección de rutas
│   │   ├── dashboard/page.tsx      # Dashboard con KPIs y gráficos
│   │   ├── horarios/page.tsx       # Cuadrícula + asignación manual/automática
│   │   ├── docentes/page.tsx       # CRUD completo de docentes
│   │   ├── cursos/page.tsx         # Gestión de cursos (agrupados por ciclo)
│   │   ├── aulas/page.tsx          # Gestión de aulas y laboratorios
│   │   ├── reportes/page.tsx       # Generación de reportes PDF
│   │   ├── usuarios/page.tsx       # Gestión de usuarios (solo admin)
│   │   └── auditoria/page.tsx      # Log de auditoría (solo admin)
│   └── api/
│       ├── auth/login/route.ts     # POST — Login con JWT
│       ├── auth/logout/route.ts    # POST — Logout + auditoría
│       ├── auth/me/route.ts        # GET — Sesión actual
│       ├── aulas/route.ts          # GET, POST — CRUD ambientes
│       ├── ciclos/route.ts         # GET, POST — Ciclos académicos
│       ├── cursos/route.ts         # GET, POST — Cursos
│       ├── docentes/route.ts       # GET, POST — Docentes (lista)
│       ├── docentes/[id]/route.ts  # GET, PUT, DELETE — Docente individual
│       ├── docentes/[id]/horario/route.ts  # GET — Horario de un docente
│       ├── horarios/route.ts       # GET, POST — Asignaciones
│       ├── horarios/[id]/route.ts  # DELETE — Eliminar asignación
│       ├── horarios/generar/route.ts   # POST — Generación automática
│       ├── horarios/grupos/route.ts    # GET, POST — Grupos por ciclo
│       ├── dashboard/route.ts      # GET — Estadísticas completas
│       ├── auditoria/route.ts      # GET — Registros de auditoría
│       └── usuarios/route.ts       # GET, POST — Usuarios
├── lib/
│   ├── db.ts                       # Pool PostgreSQL (query, queryOne, transaction)
│   ├── auth.ts                     # Login, getSession, hashPassword, verifyPassword
│   ├── jwt.ts                      # generateToken, verifyToken (jose/HS256)
│   ├── horarios.ts                 # Motor de asignación (conflictos + auto-generación)
│   ├── auditoria.ts                # registrarAuditoria, getAuditoria
│   └── schema.sql                  # DDL completo + datos iniciales
├── middleware.ts                   # Protección global de rutas (JWT en cookie)
├── .env / .env.local               # Variables de entorno
└── horarios-unt/                   # ⚠ Copia anterior/duplicada del proyecto
```

---

## 4. Modelo de Datos (PostgreSQL)

### Tablas principales
| Tabla | Descripción | PKs / UKs |
|-------|-------------|-----------|
| `usuarios` | Usuarios del sistema (admin, secretaria, docente) | PK: `id` (UUID), UK: `email` |
| `docentes` | Cuerpo docente con jerarquía y horas máximas | PK: `id`, UK: `codigo`, `dni` |
| `ciclos` | Ciclos académicos (2024-I, 2024-II, etc.) | PK: `id` |
| `ambientes` | Aulas, laboratorios, auditorios | PK: `id`, UK: `codigo` |
| `escuelas` | Escuelas/departamentos académicos | PK: `id`, UK: `codigo` |
| `cursos` | Plan de estudios por ciclo | PK: `id`, UK: `codigo` |
| `grupos` | Instancias de curso por ciclo académico | PK: `id`, UK: (`ciclo_id`, `curso_id`, `numero_grupo`) |
| `slots_tiempo` | Bloques horarios de 1 hora (07:00–21:00) | PK: `id`, UK: (`hora_inicio`, `hora_fin`) |
| `asignaciones` | **Tabla central** — docente+grupo+ambiente+slot+día | PK: `id` |
| `auditoria` | Log completo de todas las acciones | PK: `id` |

### Enums
- `rol_usuario`: `admin`, `secretaria`, `docente`
- `categoria_docente`: `principal`, `asociado`, `auxiliar`, `jefe_practica`
- `condicion_docente`: `nombrado`, `contratado`
- `tipo_grado`: `bachiller`, `licenciado`, `magister`, `doctor`
- `tipo_ambiente`: `aula`, `laboratorio`, `auditorio`
- `dia_semana`: `lunes`, `martes`, `miercoles`, `jueves`, `viernes`, `sabado`
- `tipo_sesion`: `teoria`, `practica`, `laboratorio`
- `accion_auditoria`: `CREATE`, `UPDATE`, `DELETE`, `LOGIN`, `LOGOUT`, `GENERATE_SCHEDULE`, `EXPORT_REPORT`, `ASSIGN`, `UNASSIGN`

### Índices únicos de conflicto (asignaciones)
- `idx_asig_docente_dia_slot` — Un docente no puede estar en dos lugares a la misma hora
- `idx_asig_ambiente_dia_slot` — Un ambiente no puede tener dos clases simultáneas
- `idx_asig_grupo_dia_slot` — Un grupo no puede tener dos clases simultáneas

---

## 5. Módulos y Estado de CRUDs

### 5.1 Autenticación
| Operación | Endpoint | Estado |
|-----------|----------|--------|
| Login | `POST /api/auth/login` | ✅ Completo |
| Logout | `POST /api/auth/logout` | ✅ Completo |
| Sesión actual | `GET /api/auth/me` | ✅ Completo |
| Middleware protección | `middleware.ts` | ✅ Completo |

### 5.2 Docentes — CRUD
| Operación | Endpoint | Estado |
|-----------|----------|--------|
| Listar (con filtros) | `GET /api/docentes` | ✅ Completo |
| Obtener por ID | `GET /api/docentes/[id]` | ✅ Completo |
| Crear | `POST /api/docentes` | ✅ Completo |
| Actualizar | `PUT /api/docentes/[id]` | ✅ Completo |
| Desactivar (soft delete) | `DELETE /api/docentes/[id]` | ✅ Completo |
| Horario del docente | `GET /api/docentes/[id]/horario` | ✅ Completo |
| Interfaz frontend | `(app)/docentes/page.tsx` | ✅ Completo |

### 5.3 Cursos
| Operación | Endpoint | Estado |
|-----------|----------|--------|
| Listar (con búsqueda) | `GET /api/cursos` | ✅ Completo |
| Crear | `POST /api/cursos` | ✅ Completo |
| Actualizar | — | ❌ **Falta PUT** |
| Eliminar/Desactivar | — | ❌ **Falta DELETE** |
| Interfaz frontend | `(app)/cursos/page.tsx` | ⚠️ Solo crear (no editar/eliminar) |

### 5.4 Aulas y Laboratorios (Ambientes)
| Operación | Endpoint | Estado |
|-----------|----------|--------|
| Listar (con filtros) | `GET /api/aulas` | ✅ Completo |
| Crear | `POST /api/aulas` | ✅ Completo |
| Actualizar | — | ❌ **Falta PUT** |
| Eliminar/Desactivar | — | ❌ **Falta DELETE** |
| Interfaz frontend | `(app)/aulas/page.tsx` | ⚠️ Solo crear (no editar/eliminar) |

### 5.5 Ciclos Académicos
| Operación | Endpoint | Estado |
|-----------|----------|--------|
| Listar | `GET /api/ciclos` | ✅ Completo |
| Crear | `POST /api/ciclos` | ✅ Completo |
| Actualizar | — | ❌ **Falta PUT** |
| Eliminar | — | ❌ **Falta DELETE** |
| Activar/Desactivar | — | ❌ **Falta endpoint para cambiar ciclo activo** |
| Interfaz frontend | — | ❌ **No existe página de gestión de ciclos** |

### 5.6 Grupos
| Operación | Endpoint | Estado |
|-----------|----------|--------|
| Listar (por ciclo/curso) | `GET /api/horarios/grupos` | ✅ Completo |
| Crear | `POST /api/horarios/grupos` | ✅ Completo |
| Actualizar | — | ❌ **Falta PUT** |
| Eliminar | — | ❌ **Falta DELETE** |
| Interfaz frontend | — | ❌ **No existe página dedicada para gestión de grupos** |

### 5.7 Horarios / Asignaciones
| Operación | Endpoint | Estado |
|-----------|----------|--------|
| Listar (con filtros) | `GET /api/horarios` | ✅ Completo |
| Crear (manual) | `POST /api/horarios` | ✅ Con validación de conflictos |
| Eliminar | `DELETE /api/horarios/[id]` | ✅ Soft delete (`estado='eliminado'`) |
| Generación automática | `POST /api/horarios/generar` | ✅ Motor por jerarquía |
| Actualizar asignación | — | ❌ **Falta PUT (mover asignación)** |
| Interfaz (grid + lista) | `(app)/horarios/page.tsx` | ✅ Completo |

### 5.8 Usuarios
| Operación | Endpoint | Estado |
|-----------|----------|--------|
| Listar | `GET /api/usuarios` | ✅ Completo |
| Crear | `POST /api/usuarios` | ✅ Completo |
| Actualizar | — | ❌ **Falta PUT (editar usuario/cambiar rol)** |
| Eliminar/Desactivar | — | ❌ **Falta DELETE** |
| Cambiar contraseña | — | ❌ **Falta endpoint** |
| Interfaz frontend | `(app)/usuarios/page.tsx` | ⚠️ Solo crear (no editar/eliminar) |

### 5.9 Escuelas
| Operación | Endpoint | Estado |
|-----------|----------|--------|
| CRUD completo | — | ❌ **No existe API de escuelas** |
| Interfaz frontend | — | ❌ **No existe página** |

### 5.10 Dashboard
| Operación | Endpoint | Estado |
|-----------|----------|--------|
| KPIs + estadísticas | `GET /api/dashboard` | ✅ Completo |
| Interfaz con gráficos | `(app)/dashboard/page.tsx` | ✅ Completo (Recharts) |

### 5.11 Reportes
| Operación | Endpoint | Estado |
|-----------|----------|--------|
| Reporte operacional | PDF client-side | ✅ Completo |
| Reporte por docente | PDF client-side | ✅ Completo |
| Reporte de gestión | PDF client-side | ✅ Completo |
| Interfaz frontend | `(app)/reportes/page.tsx` | ✅ Completo |

### 5.12 Auditoría
| Operación | Endpoint | Estado |
|-----------|----------|--------|
| Listar (con filtros y paginación) | `GET /api/auditoria` | ✅ Completo |
| Interfaz frontend | `(app)/auditoria/page.tsx` | ✅ Completo |

---

## 6. Roles y Permisos

| Módulo | Admin | Secretaria | Docente |
|--------|-------|------------|---------|
| Dashboard | ✅ | ✅ | ✅ |
| Horarios (ver) | ✅ | ✅ | ✅ |
| Horarios (crear/eliminar) | ✅ | ✅ | ❌ |
| Docentes | ✅ | ✅ | ❌ |
| Cursos | ✅ | ✅ | ❌ |
| Aulas y Labs | ✅ | ✅ | ❌ |
| Reportes | ✅ | ✅ | ❌ |
| Usuarios | ✅ | ❌ | ❌ |
| Auditoría | ✅ | ❌ | ❌ |
| Ciclos (crear) | ✅ | ❌ | ❌ |

---

## 7. Motor de Asignación Automática

**Archivo:** `lib/horarios.ts` → `generarHorarioAutomatico()`

### Jerarquía de asignación (orden de prioridad)
1. **Nombrados**: Principal → Asociado → Auxiliar → Jefe de Práctica
2. **Contratados**: Mismo orden
3. Dentro de cada nivel: por **antigüedad** (`fecha_ingreso ASC`)

### Algoritmo
1. Ordena docentes por jerarquía
2. Para cada docente, verifica horas disponibles vs horas requeridas
3. Selecciona el primer docente con disponibilidad suficiente
4. Asigna horas de teoría primero (recorre día × slot × ambiente)
5. Luego asigna horas de práctica/laboratorio
6. Valida conflictos triples: docente, ambiente, grupo

### Validaciones de conflicto (`verificarConflicto()`)
- ❌ Docente ya tiene clase en el mismo ciclo/día/slot
- ❌ Ambiente ya está ocupado en el mismo ciclo/día/slot
- ❌ Grupo ya tiene clase en el mismo ciclo/día/slot

---

## 8. ⚠️ Issues y Mejoras Pendientes para Funcionar al 100%

### 🔴 Críticas (bloquean funcionalidad)

1. **Password hash incompatible en seed**
   - El `schema.sql` inserta un hash `$2a$10$92IXU...` que corresponde a la palabra `"password"` en bcrypt con costo 10, pero fue generada externamente. Hay que verificar que `bcryptjs` la reconozca; de lo contrario, no se podrá hacer login.

2. **No existe página de gestión de Ciclos**
   - Los ciclos se crean vía API pero no hay interfaz para crearlos, editarlos, activarlos o desactivarlos.
   - Crear `app/(app)/ciclos/page.tsx` con CRUD completo.

3. **No existe página de gestión de Grupos**
   - Los grupos se necesitan antes de crear asignaciones. No hay UI para crearlos.
   - Se deben crear desde la UI, idealmente desde la página de horarios o cursos.

4. **CRUDs incompletos (faltan PUT y DELETE)**
   - **Cursos:** No se puede editar ni eliminar/desactivar.
   - **Aulas/Ambientes:** No se puede editar ni eliminar/deshabilitar.
   - **Usuarios:** No se puede editar, desactivar ni cambiar contraseña.
   - **Ciclos:** No se puede editar ni cambiar el ciclo activo.
   - **Grupos:** No se puede editar ni eliminar.

5. **Carpeta duplicada `horarios-unt/`**
   - Existe una copia completa del proyecto dentro de sí mismo. Podría causar confusión y problemas de importación. Se debe eliminar o ignorar.

### 🟡 Importantes (afectan usabilidad)

6. **No hay validación de formularios en el frontend**
   - Los modales de creación no validan campos requeridos antes de enviar.
   - El backend retorna errores de PostgreSQL crudos (ej: violaciones UNIQUE) sin mensajes amigables.

7. **La generación automática no pasa `horas_teoria` ni `horas_practica`**
   - El modal auto requiere seleccionar un grupo, pero el backend espera `horas_teoria` y `horas_practica` que se deberían extraer automáticamente del grupo/curso seleccionado.

8. **No hay endpoint para `escuelas`**
   - El formulario de cursos intenta obtener escuelas parseando la respuesta de cursos. Se necesita un `GET /api/escuelas`.

9. **Eliminar asignación con un click (sin confirmación clara)**
   - En la vista grid de horarios, hacer click en un bloque directamente dispara `confirm()` para eliminar. Esto es propenso a errores accidentales.

10. **La columna `Rol` en auditoría siempre muestra "—"**
    - La tabla de auditoría no almacena el rol del usuario. Debería unirse con la tabla de usuarios o almacenarse en el registro.

11. **Falta responsive design para móviles**
    - El sidebar es fijo a 260px y no colapsa en pantallas pequeñas.
    - Las tablas no son usables en móvil.

### 🟢 Mejoras deseables

12. **No hay paginación en las tablas principales**
    - Docentes, cursos, aulas y usuarios cargan todo de una vez. Funciona con pocos datos pero no escala.

13. **No hay exportación de reportes en otros formatos**
    - Solo PDF. Podrían agregarse CSV y XLSX.

14. **No hay vista de horario personal para el rol Docente**
    - El endpoint `GET /api/docentes/[id]/horario` existe pero no hay UI específica para el docente logueado.

15. **No hay manejo de sesión expirada en el frontend**
    - Si el token expira (8h), las llamadas API fallan silenciosamente. Debería redirigir al login.

16. **No hay "cambiar mi contraseña" para el usuario logueado**
    - No existe la funcionalidad de cambio de contraseña propio.

17. **Falta configuración de `equipamiento` en ambientes**
    - El campo `equipamiento TEXT[]` existe en el esquema pero no se gestiona en la UI.

18. **No hay manejo de `prerequisitos` en cursos**
    - El campo `prerequisitos UUID[]` existe en el esquema pero no tiene UI ni lógica.

19. **No se usa `num_alumnos` de grupos**
    - El conteo de alumnos existe pero no se refleja en la generación automática para validar capacidad del ambiente.

20. **No hay confirmación ni indicador visual de "ciclo activo"**
    - Debería poder cambiarse el ciclo activo desde la UI con confirmación, y marcar visualmente cuál está activo.

---

## 9. Reglas de Desarrollo

1. **Soft Delete siempre** — Nunca `DELETE FROM`. Usar campos `activo=false` o `estado='eliminado'`.
2. **Auditoría obligatoria** — Todo CREATE, UPDATE, DELETE debe llamar a `registrarAuditoria()`.
3. **Validación de roles** — Toda API que modifique datos debe verificar `getSession()` y el `rol` del usuario.
4. **SQL parametrizado** — Siempre usar `$1, $2...` con el array de parámetros. Nunca concatenar strings.
5. **Verificar conflictos** — Antes de crear/mover asignaciones, siempre llamar `verificarConflicto()`.
6. **Estilos centralizados** — Usar las clases definidas en `globals.css` (`.card`, `.btn-primary`, `.badge-*`, `.form-*`, `.modal-*`, etc.).
7. **Imports con alias** — Usar `@/lib/*` para importar módulos de la librería.

---

## 10. Variables de Entorno

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=horariosUNT
DB_USER=postgres
DB_PASSWORD=12345
JWT_SECRET=jwt-horarios-unt-2024
```

---

## 11. Comandos

```bash
# Instalar dependencias
npm install

# Crear base de datos, migrar el esquema y poblar datos iniciales
npx sequelize-cli db:create
npx sequelize-cli db:migrate
npx sequelize-cli db:seed:all

# Ejecutar en desarrollo
npm run dev   # → http://localhost:3000

# Build producción
npm run build
npm start
```

---

## 12. Distribución de Responsabilidades por Módulos (4 personas — Sin Interferencias)

> **Principio clave:** Cada persona es dueña completa de sus módulos (API + Frontend + estilos). Nadie edita archivos ajenos. Los archivos compartidos (`layout.tsx`, `globals.css`, `lib/`) tienen un dueño designado.

---

### 👤 Persona 1 — Módulos: Ciclos + Grupos + Escuelas + Limpieza Base
**Archivos exclusivos:** Todo lo nuevo que cree esta persona. Nadie más los toca.

| # | Tarea | Archivos (exclusivos) | Issue |
|---|-------|----------------------|-------|
| 1 | Crear API completa de **Ciclos** (`GET`, `POST`, `PUT`, `DELETE`, activar/desactivar) | `app/api/ciclos/route.ts` (ya existe, ampliar), `app/api/ciclos/[id]/route.ts` (nuevo) | #4, #20 |
| 2 | Crear página de gestión de **Ciclos** (tabla + modal crear/editar + botón activar) | `app/(app)/ciclos/page.tsx` (nuevo) | #2, #20 |
| 3 | Crear API completa de **Grupos** (`PUT`, `DELETE`) | `app/api/horarios/grupos/[id]/route.ts` (nuevo) | #4 |
| 4 | Crear página de gestión de **Grupos** (tabla por ciclo, crear/editar/eliminar) | `app/(app)/grupos/page.tsx` (nuevo) | #3 |
| 5 | Crear API de **Escuelas** (`GET`, `POST`) | `app/api/escuelas/route.ts` (nuevo) | #8 |
| 6 | Verificar compatibilidad del **hash bcrypt** del seed | `lib/schema.sql` | #1 |
| 7 | Eliminar o agregar a `.gitignore` la carpeta duplicada `horarios-unt/` | `.gitignore` | #5 |
| 8 | Agregar auditoría en todos sus endpoints nuevos | Sus propios `route.ts` | Regla #2 |

**🗂 Archivos que SOLO esta persona toca:**
- `app/api/ciclos/route.ts` y `app/api/ciclos/[id]/route.ts`
- `app/api/horarios/grupos/route.ts` y `app/api/horarios/grupos/[id]/route.ts`
- `app/api/escuelas/route.ts`
- `app/(app)/ciclos/page.tsx`
- `app/(app)/grupos/page.tsx`
- `lib/schema.sql`, `.gitignore`

---

### 👤 Persona 2 — Módulos: Docentes + Cursos + Aulas/Ambientes
**Archivos exclusivos:** Los módulos de docentes, cursos y aulas, tanto API como frontend.

| # | Tarea | Archivos (exclusivos) | Issue |
|---|-------|----------------------|-------|
| 1 | **Mantener y validar** el CRUD existente de **Docentes** (ya completo: GET, POST, PUT, DELETE) | `app/api/docentes/route.ts`, `app/api/docentes/[id]/route.ts` | — |
| 2 | Agregar **validación de formularios** en el modal de Docentes (campos requeridos, formato DNI, email) | `app/(app)/docentes/page.tsx` | #6 |
| 3 | Crear `PUT /api/cursos/[id]` y `DELETE /api/cursos/[id]` con auditoría | `app/api/cursos/[id]/route.ts` (nuevo) | #4 |
| 4 | Completar página de **Cursos**: botones Editar/Desactivar + modal de edición + usar `/api/escuelas` para el select | `app/(app)/cursos/page.tsx` | #4, #8 |
| 5 | Crear `PUT /api/aulas/[id]` y `DELETE /api/aulas/[id]` con auditoría | `app/api/aulas/[id]/route.ts` (nuevo) | #4 |
| 6 | Completar página de **Aulas**: botones Editar/Deshabilitar + modal edición | `app/(app)/aulas/page.tsx` | #4 |
| 7 | Agregar gestión de campo **equipamiento** (UI de tags/chips) en ambientes | `app/(app)/aulas/page.tsx`, `app/api/aulas/route.ts` | #17 |
| 8 | Agregar **validación de formularios** en modales de Cursos y Aulas | `app/(app)/cursos/page.tsx`, `app/(app)/aulas/page.tsx` | #6 |
| 9 | Agregar auditoría en todos sus endpoints nuevos | Sus propios `route.ts` | Regla #2 |

**🗂 Archivos que SOLO esta persona toca:**
- `app/api/docentes/route.ts` y `app/api/docentes/[id]/route.ts`
- `app/api/docentes/[id]/horario/route.ts`
- `app/(app)/docentes/page.tsx`
- `app/api/cursos/route.ts` y `app/api/cursos/[id]/route.ts`
- `app/api/aulas/route.ts` y `app/api/aulas/[id]/route.ts`
- `app/(app)/cursos/page.tsx`
- `app/(app)/aulas/page.tsx`

---

### 👤 Persona 3 — Módulos: Usuarios + Auditoría + Auth + Layout/UX
**Archivos exclusivos:** Usuarios, auditoría y el layout principal (sidebar, responsive, sesión).

| # | Tarea | Archivos (exclusivos) | Issue |
|---|-------|----------------------|-------|
| 1 | Crear `PUT /api/usuarios/[id]`, `DELETE /api/usuarios/[id]` y `PUT /api/usuarios/[id]/password` | `app/api/usuarios/[id]/route.ts` (nuevo), `app/api/usuarios/[id]/password/route.ts` (nuevo) | #4, #16 |
| 2 | Completar página de **Usuarios**: botones Editar/Desactivar/Cambiar contraseña | `app/(app)/usuarios/page.tsx` | #4, #16 |
| 3 | Corregir columna **Rol** en auditoría (JOIN con tabla usuarios) | `lib/auditoria.ts`, `app/api/auditoria/route.ts`, `app/(app)/auditoria/page.tsx` | #10 |
| 4 | Agregar enlaces de **Ciclos** y **Grupos** al sidebar | `app/(app)/layout.tsx` | #2, #3 |
| 5 | Agregar **sidebar colapsable** para móviles (hamburger menu) | `app/(app)/layout.tsx`, `app/globals.css` | #11 |
| 6 | Agregar **manejo de sesión expirada** (interceptor fetch → redirigir a login) | `app/(app)/layout.tsx` | #15 |
| 7 | Agregar **indicador visual** del ciclo activo en el sidebar | `app/(app)/layout.tsx` | #20 |
| 8 | Agregar botón **"Cambiar mi contraseña"** en el perfil del sidebar | `app/(app)/layout.tsx` | #16 |
| 9 | Hacer **tablas responsive** y estilos globales para móvil | `app/globals.css` | #11 |

**🗂 Archivos que SOLO esta persona toca:**
- `app/api/usuarios/route.ts` y `app/api/usuarios/[id]/route.ts`
- `app/(app)/usuarios/page.tsx`
- `app/(app)/auditoria/page.tsx`
- `app/api/auditoria/route.ts`
- `lib/auditoria.ts`
- `app/(app)/layout.tsx` ← **dueño único del sidebar/layout**
- `app/globals.css` ← **dueño único de estilos globales**

---

### 👤 Persona 4 — Módulos: Horarios + Reportes + Dashboard + Motor
**Archivos exclusivos:** El core de asignaciones, generación automática, reportes y dashboard.

| # | Tarea | Archivos (exclusivos) | Issue |
|---|-------|----------------------|-------|
| 1 | Corregir modal de **generación automática** para pasar `horas_teoria`/`horas_practica` desde el grupo | `app/(app)/horarios/page.tsx` | #7 |
| 2 | Reemplazar `confirm()` nativo por **modal de confirmación** para eliminar asignaciones | `app/(app)/horarios/page.tsx` | #9 |
| 3 | Crear **vista de horario personal** para el rol Docente (condicional en la misma página) | `app/(app)/horarios/page.tsx` | #14 |
| 4 | Crear `PUT /api/horarios/[id]` para **mover asignaciones** con re-validación de conflictos | `app/api/horarios/[id]/route.ts` | — |
| 5 | Validar **capacidad del ambiente** vs `num_alumnos` del grupo en la generación automática | `lib/horarios.ts` | #19 |
| 6 | Agregar exportación de reportes en **CSV** | `app/(app)/reportes/page.tsx` | #13 |
| 7 | Agregar **gráficos** o indicadores mejorados al Dashboard | `app/(app)/dashboard/page.tsx` | #20 |
| 8 | Agregar **validación de formularios** en los modales de Horarios | `app/(app)/horarios/page.tsx` | #6 |

**🗂 Archivos que SOLO esta persona toca:**
- `app/api/horarios/route.ts` y `app/api/horarios/[id]/route.ts`
- `app/api/horarios/generar/route.ts`
- `app/(app)/horarios/page.tsx`
- `app/(app)/reportes/page.tsx`
- `app/(app)/dashboard/page.tsx`
- `app/api/dashboard/route.ts`
- `lib/horarios.ts` ← **dueño único del motor de asignación**

---

### 📋 Mapa de Propiedad de Archivos (quién toca qué)

| Archivo / Módulo | P1 | P2 | P3 | P4 |
|------------------|:--:|:--:|:--:|:--:|
| `app/api/ciclos/**` | ✅ | | | |
| `app/api/horarios/grupos/**` | ✅ | | | |
| `app/api/escuelas/**` | ✅ | | | |
| `app/(app)/ciclos/page.tsx` | ✅ | | | |
| `app/(app)/grupos/page.tsx` | ✅ | | | |
| `app/api/docentes/**` | | ✅ | | |
| `app/(app)/docentes/page.tsx` | | ✅ | | |
| `app/api/cursos/**` | | ✅ | | |
| `app/api/aulas/**` | | ✅ | | |
| `app/(app)/cursos/page.tsx` | | ✅ | | |
| `app/(app)/aulas/page.tsx` | | ✅ | | |
| `app/api/usuarios/**` | | | ✅ | |
| `app/api/auditoria/**` | | | ✅ | |
| `app/(app)/usuarios/page.tsx` | | | ✅ | |
| `app/(app)/auditoria/page.tsx` | | | ✅ | |
| `app/(app)/layout.tsx` | | | ✅ | |
| `app/globals.css` | | | ✅ | |
| `lib/auditoria.ts` | | | ✅ | |
| `app/api/horarios/**` | | | | ✅ |
| `app/api/dashboard/**` | | | | ✅ |
| `app/(app)/horarios/page.tsx` | | | | ✅ |
| `app/(app)/reportes/page.tsx` | | | | ✅ |
| `app/(app)/dashboard/page.tsx` | | | | ✅ |
| `lib/horarios.ts` | | | | ✅ |
| `lib/schema.sql` | ✅ | | | |
| `lib/db.ts` | — | — | — | — |
| `lib/auth.ts` | — | — | — | — |
| `lib/jwt.ts` | — | — | — | — |
| `middleware.ts` | — | — | — | — |

> **—** = Archivo compartido de solo lectura. Si alguien necesita modificarlo, coordinar primero.

---

### 🔀 Orden de Trabajo Recomendado

```
Semana 1 (todos en paralelo, sin conflictos):
├── P1: APIs de Ciclos + Grupos + Escuelas + verificar bcrypt
├── P2: Validar Docentes + APIs de Cursos/[id] + Aulas/[id] + frontend
├── P3: APIs de Usuarios/[id] + layout responsive + sidebar
└── P4: Corregir modal auto + confirm → modal + vista docente

Semana 2 (integración):
├── P1: Páginas de Ciclos y Grupos (depende de sus APIs)
├── P2: Validación de forms + equipamiento en aulas
├── P3: Auditoría rol + sesión expirada + cambiar contraseña
└── P4: PUT horarios + capacidad ambiente + CSV + dashboard
```

### 📋 Resumen por Persona

| Persona | Módulos | Tareas | Archivos nuevos | Prioridad |
|---------|---------|--------|----------------|-----------|
| **P1** | Ciclos, Grupos, Escuelas | 8 | 5 archivos nuevos | 🔴 Crítica |
| **P2** | Docentes, Cursos, Aulas | 9 | 2 archivos nuevos | 🔴 Crítica |
| **P3** | Usuarios, Auditoría, Layout/UX | 9 | 2 archivos nuevos | 🔴 + 🟡 |
| **P4** | Horarios, Reportes, Dashboard | 8 | 0 archivos nuevos | 🟡 + 🟢 |
