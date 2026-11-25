# Reservas FdI

Plataforma de reservas de espacios para la Facultad de Informatica.

## Stack
- Nuxt 3 (Vue.js fullstack)
- Prisma ORM + SQLite
- FullCalendar (calendario interactivo)
- JWT para autenticacion (cookie httpOnly)

## Comandos
- `npm run dev` — Arranca el servidor de desarrollo (puerto 3000)
- `npm run db:reset` — Reinicia la base de datos y ejecuta el seed
- `npx prisma studio` — Interfaz visual para explorar la BD

## Estructura
- `server/api/` — Endpoints de la API (Nuxt server routes)
- `server/utils/` — Prisma client y utilidades de auth
- `pages/` — Paginas de la aplicacion (file-based routing)
- `components/` — Componentes Vue reutilizables
- `composables/` — Composables (useAuth)
- `prisma/schema.prisma` — Modelos de datos

## Usuarios de prueba
- Admin: admin@fdi.com / admin123
- Usuario: user1@fdi.com / user123
- Usuario: user2@fdi.com / user123

## Convenciones
- Server routes siguen la convencion Nuxt: `[recurso].method.ts`
- Validaciones de negocio en el backend, validaciones de UX en el frontend
- Usar Prisma transactions para operaciones con riesgo de race conditions
