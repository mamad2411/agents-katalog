---
applyTo: "src/**/*.ts"
---

# Backend

- NestJS + Prisma.
- Mantener Controller → Service → Repository.
- Los controllers no deben contener lógica de negocio.
- Usar DTOs para entrada de datos.
- Mantener Prisma aislado en repositories/services.
- No modificar el schema sin explicar las migraciones necesarias.
- Manejar errores y excepciones adecuadamente en los servicios.
- Escribir pruebas unitarias para la lógica de negocio en los servicios.
- Codigo estructurado