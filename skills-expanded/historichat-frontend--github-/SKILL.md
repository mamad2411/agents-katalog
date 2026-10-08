# Reglas OBLIGATORIAS para Asistentes de IA en este proyecto

1. **LEER SIEMPRE LA ARQUITECTURA**: Antes de proponer o escribir cualquier código, sugerencia de refactorización o adición de nuevas funcionalidades, DEBES leer, comprender y basar tus decisiones en el archivo `ARCHITECTURE.md` y los archivos en `docs/`. Son la fuente de verdad inamovible del proyecto.
2. **RESPETAR PRINCIPIOS OBLIGATORIOS**: Sigue estrictamente los principios de arquitectura de `ARCHITECTURE.md` (Separación estricta de responsabilidades, proxy BFF protegido, evitar lógica de negocio en componentes, nomenclatura de archivos/variables, etc.).
3. **ACTUALIZAR LA DOCUMENTACIÓN**: Si añades una nueva página principal, recurso REST importante, cambias los flujos de datos o añades una nueva convención, DEBES agregar y documentar esos cambios en el propio archivo `ARCHITECTURE.md` para mantenerlo siempre actualizado.
4. **NO INVENTAR PATRONES**: Si `ARCHITECTURE.md` ya define cómo se conectan las cosas (ej. WebSocket, proxy para el Backend, normalización de datos snake_case a camelCase), no propongas patrones alternativos o atajos. Apégate a la documentación estricta.
