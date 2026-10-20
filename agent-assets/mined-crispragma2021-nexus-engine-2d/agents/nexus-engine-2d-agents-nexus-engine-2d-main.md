# Reglas operativas de Nexus Engine

Estas reglas se aplican a todo el trabajo realizado en este repositorio:

1. **Commits en español.** Usa mensajes claros, breves y en modo imperativo; describe el cambio principal.
2. **Dependencias bajo control.** No añadas, actualices ni reemplaces dependencias sin autorización previa y explícita. Prefiere las APIs y herramientas ya disponibles.
3. **Historial protegido.** Está prohibido reescribir, hacer force-push o eliminar historial de Git salvo petición explícita del responsable del repositorio.
4. **Verificación antes de entregar.** Ejecuta las comprobaciones relevantes (`tsc --noEmit`, `eslint` y `vite build`) y documenta cualquier excepción.
5. **Secretos fuera del repositorio.** No confirmes archivos `.env`, tokens, claves privadas ni credenciales. Usa `.env.example` como plantilla sin valores sensibles.
