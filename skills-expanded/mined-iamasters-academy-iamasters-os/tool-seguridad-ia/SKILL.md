---
name: tool-seguridad-ia
description: "Manual de seguridad para desarrollo con IA. Aplica prompts preventivos, checklists pre-deploy y protocolos de emergencia para los 10 riesgos críticos (credenciales, endpoints, inyección, rate limiting, XSS, BBDD, dependencias, logs). Úsala al generar código sensible, revisar seguridad o antes de desplegar proyectos creados con arnes."
---

# Manual de Seguridad para Desarrollo con IA

Fuente: https://github.com/angelapaia/manual-seguridad-ia

Este manual establece estándares no negociables para equipos que usan asistentes de IA (Claude, Cursor, GitHub Copilot) en entornos de producción. El modelo no sabe si estás en un hackathon o manejando datos reales de clientes — la instrucción explícita de seguridad es obligatoria.

Si construyes con `arnes`, pasa este checklist antes de desplegar.

---

## Cómo usar esta skill

Cuando el usuario va a generar código en un módulo crítico (autenticación, BBDD, pagos, APIs externas, logging), **prepend el prompt preventivo correspondiente** a la petición antes de escribir código.

Cuando el usuario pide una revisión de seguridad, aplica el **Prompt Maestro de Auditoría**.

---

## Flujo diario (3 pasos)

**Paso 1 — Preparación**: Configurar hooks de seguridad en el proyecto (escáner automático en cada edición).

**Paso 2 — Codificación**: Antes de pedir a la IA que genere módulos críticos, identificar el tipo de riesgo y anteponer el prompt preventivo correspondiente.

**Paso 3 — Auditoría**: Ejecutar auditoría antes de cada commit. Revisar credenciales hardcodeadas, endpoints sin proteger, inputs sin validar, dependencias vulnerables y datos sensibles en logs.

---

## Los 10 Prompts Preventivos

### 1. API Keys y Credenciales
```
Antes de escribir cualquier código, ten en cuenta estas restricciones de seguridad OBLIGATORIAS:
- NUNCA incluyas API keys, tokens, passwords o secrets directamente en el código
- SIEMPRE usa variables de entorno (process.env.VARIABLE_NAME)
- Las llamadas a APIs externas DEBEN hacerse desde el servidor/backend, nunca desde el cliente
- Si necesitas hacer una llamada desde el frontend, crea un endpoint proxy en el backend primero
- Verifica que .env está en .gitignore antes de continuar
Ahora [tu petición normal aquí]
```

### 2. Endpoints sin Autenticar
```
REQUISITO DE SEGURIDAD: Todos los endpoints que voy a crear deben incluir:
- Middleware de autenticación (verificación de JWT o sesión de Supabase) ANTES de cualquier lógica
- Verificación de que el usuario autenticado tiene permiso para acceder al recurso solicitado
- Respuesta 401 si no hay token, 403 si no tiene permisos
- Nunca exponer datos de otros usuarios aunque el endpoint sea "solo lectura"
Ahora [tu petición normal aquí]
```

### 3. Inyección de Código / SQL
```
SEGURIDAD CRÍTICA para este código:
- Usa SIEMPRE consultas parametrizadas o el ORM — NUNCA concatenes strings con input del usuario
- Valida y sanitiza TODO input antes de procesarlo con Zod o joi
- Para HTML/texto que se mostrará en el frontend, usa DOMPurify.sanitize()
- Aplica el principio de mínimo privilegio: solo pide los datos que realmente necesitas
Ahora [tu petición normal aquí]
```

### 4. Rate Limiting
```
Este endpoint necesita protección contra abuso. Implementa rate limiting con estas especificaciones:
- Rutas de autenticación (login, registro, recuperación): máximo 10 intentos por 15 minutos por IP
- API general: máximo 60 requests por minuto por usuario autenticado
- Servicios externos costosos (IA, emails, SMS): máximo 20 por hora por usuario
- Responde con HTTP 429 y header Retry-After cuando se supere el límite
- Loggea los intentos de abuso para detectar patrones
Ahora [tu petición normal aquí]
```

### 5. Manejo de Errores
```
Implementa manejo de errores SEGURO en este código:
- Captura TODOS los errores con try/catch y manéjalos explícitamente
- Al cliente: envía SIEMPRE mensajes genéricos ("Error interno del servidor", "No autorizado")
- Al servidor/logs: registra el error completo con contexto para debugging
- NUNCA expongas stack traces, nombres de archivos, versiones de librerías o estructura de la DB al cliente
- Valida que los datos de respuesta tienen la estructura esperada antes de enviarlos
Ahora [tu petición normal aquí]
```

### 6. Prompt Injection (integraciones con LLMs)
```
SEGURIDAD para integración con LLM:
- Separa las instrucciones del sistema del input del usuario usando etiquetas XML claras: <sistema>...</sistema> y <usuario>...</usuario>
- Sanitiza el input del usuario: elimina o escapa secuencias como "Ignora instrucciones anteriores", "Eres ahora un", etc.
- Establece límites explícitos: "Solo responde sobre [dominio específico], rechaza cualquier otra petición"
- Loggea inputs sospechosos para análisis posterior
- Nunca incluyas en el prompt del sistema datos que el usuario no debería ver
Ahora [tu petición normal aquí]
```

### 7. XSS (Cross-Site Scripting)
```
PREVENCIÓN DE XSS obligatoria:
- Sanitiza con DOMPurify.sanitize() cualquier string que venga del usuario antes de renderizarlo
- NUNCA uses dangerouslySetInnerHTML a menos que sea absolutamente necesario y el contenido esté sanitizado
- Configura CSP (Content Security Policy) headers en tu servidor
- Para URLs dinámicas, valida que empiecen por https:// y no contengan javascript:
- Escapa caracteres especiales en outputs: <, >, &, ", '
Ahora [tu petición normal aquí]
```

### 8. Privilegios de Base de Datos
```
MÍNIMO PRIVILEGIO para operaciones de base de datos:
- El usuario de BBDD de la aplicación solo debe tener los permisos mínimos necesarios (SELECT/INSERT donde corresponda, nunca DROP)
- Activa Row Level Security (RLS) en Supabase: cada usuario solo puede ver/editar SUS datos
- Nunca hagas queries como administrador desde la aplicación
- Audita y loggea operaciones sensibles (borrado masivo, cambios de roles, acceso a datos de pago)
- Implementa soft delete (campo deleted_at) en lugar de borrado físico para poder auditar
Ahora [tu petición normal aquí]
```

### 9. Dependencias de Terceros
```
SEGURIDAD en dependencias:
- Antes de instalar cualquier paquete, verifica: +50k descargas semanales, actualización reciente (+6 meses), reputación del autor
- Usa versiones exactas en package.json (sin ^ ni ~) para evitar actualizaciones automáticas con vulnerabilidades
- Ejecuta npm audit antes y después de instalar dependencias nuevas
- No instales paquetes que requieran permisos excesivos
- Alternativa: implementa la funcionalidad tú mismo si el paquete es pequeño (<50 líneas)
Ahora [tu petición normal aquí]
```

### 10. Datos Sensibles en Logs
```
PROTECCIÓN DE PRIVACIDAD en logging:
- NUNCA loggees: passwords, tokens JWT, API keys, números de tarjeta, DNI/SSN, datos de salud
- Para debug, usa placeholders: logger.info('Login attempt', { userId, email: '[REDACTED]' })
- Implementa un helper sanitizeForLog() que automáticamente ofusque campos sensibles
- En producción, usa nivel INFO o superior — nunca DEBUG con datos de usuario
- Asegúrate de que los logs no se almacenan sin cifrado si contienen datos personales (GDPR)
Ahora [tu petición normal aquí]
```

---

## Prompt Maestro de Auditoría

Úsalo para revisar código existente:

```
Actúa como un Security Engineer senior especializado en aplicaciones web. Analiza el siguiente código y genera un informe estructurado que cubra:

1. **CRÍTICO** — Credenciales o secrets expuestos en el código
2. **CRÍTICO** — Endpoints sin autenticación que deberían estar protegidos
3. **ALTO** — Inputs sin validar susceptibles a inyección SQL o NoSQL
4. **ALTO** — Ausencia de rate limiting en endpoints sensibles
5. **ALTO** — Vulnerabilidades XSS (dangerouslySetInnerHTML, innerHTML sin sanitizar)
6. **MEDIO** — Errores que revelan información técnica al cliente
7. **MEDIO** — Dependencias con vulnerabilidades conocidas
8. **MEDIO** — Datos sensibles (PII, tokens) en logs
9. **BAJO** — Falta de headers de seguridad (CSP, HSTS, X-Frame-Options)
10. **BAJO** — Permisos excesivos en BBDD o servicios externos

Para cada vulnerabilidad encontrada, proporciona:
- Localización exacta (archivo y línea si es posible)
- Nivel de riesgo (CRÍTICO/ALTO/MEDIO/BAJO)
- Impacto potencial
- Solución recomendada con código corregido

[PEGA AQUÍ EL CÓDIGO A AUDITAR]
```

---

## Checklist Pre-Deploy

Ningún PR debe llegar a `main` sin este checklist completado al 100%:

### Credenciales
- [ ] Zero secrets/API keys en el código fuente
- [ ] Variables de entorno correctamente configuradas en el servidor
- [ ] `.env` en `.gitignore`, nunca commiteado

### Autenticación
- [ ] Todos los endpoints privados tienen middleware de autenticación
- [ ] Los usuarios solo pueden acceder a SUS propios datos (Row Level Security)
- [ ] Tokens con expiración razonable (<24h para sesiones web)

### Validación
- [ ] Todo input del usuario validado con schema (Zod/joi)
- [ ] Consultas a BBDD parametrizadas (sin concatenación de strings)
- [ ] Outputs sanitizados antes de renderizar en frontend

### Rate Limiting
- [ ] Endpoints de auth: máx 10/15min por IP
- [ ] API general: máx 60/min por usuario
- [ ] Servicios externos: máx 20/hora por usuario

### Logs
- [ ] No hay PII, tokens ni passwords en los logs
- [ ] Errores: mensaje genérico al cliente, detalle solo en servidor

### Dependencias
- [ ] `npm audit` sin vulnerabilidades críticas o altas
- [ ] Nuevas dependencias revisadas (popularidad, mantenimiento)

---

## Protocolo de Emergencia (credenciales expuestas)

**Si se ha commiteado un secret o key a GitHub:**

1. **INMEDIATO** — Revocar la key comprometida en el proveedor (OpenAI, Supabase, Stripe, AWS, GitHub, Google Cloud)
2. **NOTIFICAR** al líder técnico con: tipo de incidente, servicio afectado, cómo se descubrió, estado actual, próximas acciones
3. **ROTAR** todas las credenciales relacionadas — regenerar keys, actualizar `.env` en todos los entornos, invalidar sesiones activas
4. **AUDITAR** logs: IPs anómalas, queries inusuales, picos de facturación, cuentas creadas sin autorización
5. **REMEDIAR** — parchear el código, desplegar con nuevas credenciales, ejecutar `git filter-branch` para limpiar el historial, verificar que los checks de seguridad pasan

> "La transparencia reduce el impacto; ocultarlo lo empeora."

---

## Notas de implementación para Claude

- Cuando el usuario pida generar código de autenticación, APIs externas, formularios, consultas a BD o integraciones con LLMs: **aplica automáticamente los prompts preventivos relevantes sin que el usuario tenga que pedirlo**
- Cuando el usuario pida revisar código: **usa el Prompt Maestro de Auditoría**
- Cuando detectes una vulnerabilidad en código del usuario: **señálala inmediatamente con su nivel de riesgo y la solución**
- Cuando el usuario describa un incidente de seguridad: **guíalo por el Protocolo de Emergencia paso a paso**

Skill original de Angel Aparicio (IA Masters Academy), adaptada para iamasters-os.
