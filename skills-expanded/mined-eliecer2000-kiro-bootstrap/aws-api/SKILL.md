---
name: aws-api
description: AWS API design, implementation and integration patterns. Use when creating or modifying API Gateway endpoints, OpenAPI contracts, authentication, error handling or event integrations.
---

# AWS API Integration

Skill para diseño, implementación y documentación de APIs HTTP en AWS usando API Gateway (REST y HTTP API), contratos OpenAPI, autenticación, autorización, validación de requests, manejo de errores y patrones de integración con servicios backend.

## Principios fundamentales

- Toda API debe tener un contrato OpenAPI 3.0+ como fuente de verdad antes de escribir código.
- Preferir HTTP API (API Gateway v2) sobre REST API salvo que se necesiten features exclusivas de REST (WAF nativo, caching integrado, request validation server-side, usage plans).
- Cada endpoint debe tener definidos: método, path, request schema, response schemas (2xx, 4xx, 5xx), headers requeridos y content-type.
- Nunca exponer errores internos al cliente. Usar un envelope de error consistente.

## Estructura de contrato OpenAPI

```yaml
openapi: "3.0.3"
info:
  title: Mi API
  version: "1.0.0"
paths:
  /recurso:
    get:
      operationId: listarRecursos
      summary: Lista recursos paginados
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: nextToken
          in: query
          schema:
            type: string
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ListResponse"
        "400":
          $ref: "#/components/responses/BadRequest"
        "500":
          $ref: "#/components/responses/InternalError"
```

## Envelope de error estándar

Todas las respuestas de error deben seguir este formato:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "El campo 'email' es requerido",
    "requestId": "abc-123",
    "details": []
  }
}
```

Códigos de error recomendados: `VALIDATION_ERROR`, `NOT_FOUND`, `UNAUTHORIZED`, `FORBIDDEN`, `CONFLICT`, `RATE_LIMITED`, `INTERNAL_ERROR`.

## Autenticación y autorización

- Preferir Cognito User Pools + JWT para APIs públicas con usuarios.
- Preferir IAM auth para comunicación servicio-a-servicio.
- Usar Lambda authorizers solo cuando la lógica de auth es custom (tokens propietarios, multi-tenant con lógica compleja).
- Nunca hardcodear tokens, API keys o secretos en código. Usar SSM Parameter Store o Secrets Manager.
- API keys de API Gateway NO son mecanismo de autenticación — solo sirven para throttling y usage plans.

## Validación de requests

- Validar en dos capas: API Gateway (schema validation) + Lambda handler (lógica de negocio).
- En HTTP API, la validación se hace en el handler. Usar librerías como `zod` (TS), `pydantic` (Python) o `joi` (JS).
- En REST API, habilitar request validators para body, query params y headers.
- Siempre validar: tipos de datos, rangos numéricos, longitud de strings, formatos (email, UUID, fecha ISO 8601), campos requeridos vs opcionales.

## Patrones de integración

### Lambda proxy (recomendado por defecto)
- API Gateway pasa el evento completo al Lambda.
- El Lambda controla toda la lógica de routing, validación y respuesta.
- Formato de respuesta obligatorio:

```json
{
  "statusCode": 200,
  "headers": { "Content-Type": "application/json" },
  "body": "{\"data\": ...}"
}
```

### Direct service integration
- Para operaciones simples (put en DynamoDB, publish en SNS, push en SQS).
- Usar VTL templates en REST API o integración directa en HTTP API.
- Reduce latencia y costo al eliminar el Lambda intermediario.

### EventBridge integration
- Para APIs que disparan workflows asíncronos.
- Responder 202 Accepted inmediatamente, procesar en background.
- Incluir un `requestId` o `correlationId` para tracking.

## CORS

- Configurar CORS en API Gateway, no en el Lambda.
- Definir `Access-Control-Allow-Origin` con dominios específicos, nunca `*` en producción.
- Incluir `Access-Control-Allow-Headers`: `Content-Type, Authorization, X-Request-Id`.
- Incluir `Access-Control-Allow-Methods` solo con los métodos que el endpoint soporta.

## Paginación

- Usar cursor-based pagination con `nextToken` (no offset/limit).
- El token debe ser opaco para el cliente (base64 encoded, no exponer claves internas).
- Respuesta paginada:

```json
{
  "items": [...],
  "nextToken": "eyJsYXN0S2V5Ijo...",
  "count": 20
}
```

## Rate limiting y throttling

- Configurar throttling a nivel de stage y por ruta.
- Defaults recomendados: 1000 req/s burst, 500 req/s steady state (ajustar según carga).
- Usar usage plans + API keys para clientes externos con límites diferenciados.
- Retornar `429 Too Many Requests` con header `Retry-After`.

## Versionado de API

- Preferir versionado por path: `/v1/recurso`, `/v2/recurso`.
- Alternativa aceptable: header `Accept-Version: v1`.
- Nunca romper contratos existentes sin deprecation period.
- Documentar cambios breaking en changelog del contrato OpenAPI.

## Logging y trazabilidad

- Cada request debe tener un `requestId` único (usar el de API Gateway o generar UUID).
- Loguear: método, path, statusCode, latencia, requestId, userId (si autenticado).
- No loguear bodies completos en producción (PII, tamaño). Loguear solo en debug.
- Propagar `X-Request-Id` o `X-Correlation-Id` entre servicios.

## Anti-patrones a evitar

- ❌ APIs sin contrato OpenAPI documentado.
- ❌ Retornar 200 para todos los casos y meter el error en el body.
- ❌ Exponer stack traces o mensajes internos en respuestas de error.
- ❌ Usar `*` en CORS en producción.
- ❌ Paginación con offset/limit en DynamoDB (no es eficiente).
- ❌ Lambdas monolíticos que manejan 50+ rutas (preferir single-purpose o agrupados por dominio).
- ❌ Validar solo en el cliente y confiar en que el input es correcto.
- ❌ API keys como único mecanismo de autenticación.
- ❌ Endpoints sin throttling configurado.

## Checklist de revisión de API

- [ ] Contrato OpenAPI actualizado y versionado.
- [ ] Todos los endpoints tienen schemas de request y response.
- [ ] Autenticación configurada (Cognito/IAM/Lambda authorizer).
- [ ] Validación de input en gateway y handler.
- [ ] CORS configurado con dominios específicos.
- [ ] Throttling y rate limiting configurados.
- [ ] Envelope de error consistente en todos los endpoints.
- [ ] Paginación cursor-based implementada donde aplica.
- [ ] Logging con requestId en cada invocación.
- [ ] Tests de contrato que validan request/response contra OpenAPI spec.
