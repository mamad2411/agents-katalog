---
name: notifications-delivery
description: Entrega de notificaciones multicanal desde la API NestJS — in-app, email y push — con idempotencia y deduplicación, plantillas, preferencias y opt-out por usuario, canal según urgencia, rate limiting anti-avalancha, registro de envío y entrega, y nada de datos clínicos en el cuerpo. Usar al agregar un recordatorio, un correo transaccional o una notificación push; al elegir por qué canal sale un evento; o al diagnosticar notificaciones que llegan a quien optó por no recibirlas o por el canal equivocado. Duplicados o pérdidas porque falló la transacción o el consumidor: `async-messaging-events`.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Entrega de notificaciones

El envío es un efecto secundario: sale del request y viaja por una cola (`async-messaging-events`),
nunca dentro de la transacción de negocio ni bloqueando la respuesta. Esta skill es el **qué y a
quién**: canales, preferencias, deduplicación, plantillas y registro. La mecánica de cola,
outbox y reintentos vive en `async-messaging-events` y `background-jobs-scheduling`.

## 1. Anatomía

Separá tres cosas que se suelen mezclar:

- **Evento de dominio** — "CitaConfirmada". No sabe nada de canales.
- **Decisión de notificación** — un servicio traduce el evento a "a estos destinatarios, por
  estos canales, con esta plantilla", aplicando preferencias y reglas.
- **Envío por canal** — un adaptador por canal (in-app, email, push) con su proveedor.

```ts
// ✅ el dominio emite el hecho; el notificador decide canal y destinatarios
@OnEvent('appointment.confirmed')                       // consumidor de la cola
async notify(e: AppointmentConfirmedEvent) {
  await this.notifications.dispatch({
    template: 'appointment.confirmed', recipientId: e.patientId,
    dedupeKey: `appt-confirmed:${e.appointmentId}`, data: { appointmentId: e.appointmentId },
  });
}
// ❌ mandar el email en el controller, con el HTML armado a mano y sin mirar preferencias
```

## 2. Canal según urgencia y tipo

| Tipo | Canal por defecto | Nota |
|---|---|---|
| Accionable urgente (recordatorio de cita en 1h) | push + in-app | email si no hay push |
| Transaccional (confirmación, comprobante) | email + in-app | queda registro para el usuario |
| Informativo del sistema | in-app | no interrumpir |
| Marketing / no esencial | email con opt-in explícito | jamás por el canal transaccional |

- El usuario elige; estos son defaults. **Nunca** mandes marketing por el canal de
  transaccionales: quema la reputación de envío y suele violar la ley (validá con el responsable legal).

## 3. Preferencias y opt-out

- Preferencias por usuario **y por tipo de notificación y canal** ("recordatorios sí por push,
  no por email"). Guardalas como dato, no las adivines.
- Chequeá la preferencia **al despachar**, no al emitir el evento (la preferencia pudo cambiar).
- Todo canal no esencial lleva forma de darse de baja: link de unsubscribe en emails (uno solo,
  que funcione sin login), toggle en la app. Respetalo en el próximo envío, sin excusas.
- Excepción: avisos de seguridad y legales/obligatorios (cambio de contraseña, aviso de acceso)
  no se silencian. Marcalos como categoría aparte y documentá por qué.
- Quiet hours / zona horaria del destinatario para lo no urgente.

## 4. Idempotencia y deduplicación

El mismo evento puede consumirse dos veces (at-least-once). Sin defensa, el usuario recibe el
recordatorio dos veces.

- Cada notificación lleva una **`dedupeKey`** estable derivada del hecho, no del intento:
  `appt-reminder:{appointmentId}:{scheduledFor}`. Un `INSERT` con `UNIQUE(recipient, dedupeKey, channel)`
  en la misma transacción que registra el envío; violación ⇒ ya se envió, no reenvíes.
- Distinguí **deduplicación** (no mandar dos veces lo mismo) de **agrupación** (juntar 5 "te
  comentaron" en uno). La agrupación es una ventana de tiempo por usuario+tipo.
- Hacia el proveedor externo, pasá una clave de idempotencia cuando la soporte (varios
  proveedores de email/push la aceptan; verificá en la doc del tuyo).

## 5. Plantillas

- Plantilla versionada y probada, **nunca** HTML concatenado en el servicio. Datos por
  interpolación con escape; el localizador de la plantilla es un id, no texto libre.
- i18n: elegí idioma por preferencia del usuario. El texto vive en la plantilla, no en el código
  (`frontend-i18n-l10n` para el lado cliente; acá, catálogo de plantillas por idioma).
- Email: versión HTML **y** texto plano; asunto corto; remitente y responder-a correctos;
  probado en clientes reales; sin imágenes imprescindibles para entenderlo.
- Push: título + cuerpo cortos, `data` para el deep-link; el cuerpo se ve en la pantalla
  bloqueada del teléfono → ver §7.

## 6. Fallo parcial y reintento

- Cada canal falla independiente: si el push falla y el email sale, la notificación está
  **parcialmente** entregada. Registrá estado **por canal**, no uno global.
- Reintento por canal con backoff, sobre errores transitorios (5xx, timeout, rate del
  proveedor). Errores permanentes (token de push inválido, email rebotado duro) ⇒ no reintentar;
  marcá el destino como inválido y dejá de usarlo.
- Fallback entre canales como decisión explícita ("si no hay push válido en 5 min, mandá email"),
  con su propia `dedupeKey` para no duplicar.
- Tope de intentos + dead-letter con alerta (`async-messaging-events`). Una notificación que
  nunca llegó y nadie lo supo es peor que un error visible.

## 7. Privacidad — el cuerpo no lleva datos clínicos

Regla dura (`data-privacy-sensitive`): el contenido de una notificación puede aparecer en una pantalla
bloqueada, en un preview de email, en logs del proveedor y en su retención.

- ❌ "Tu resultado de VIH está listo" / "Cita con el Dr. X por [diagnóstico]".
- ✅ "Tenés una actualización en tu ficha. Ingresá para verla." + deep-link autenticado.
- Nada de datos sensibles ni tokens en asunto, cuerpo, URL o `data` del push.
- El detalle vive detrás de login; la notificación solo avisa y linkea.
- Minimizá lo que mandás al proveedor externo; asumí que lo registra.

## 8. Rate limiting y avalancha

- Límite por usuario y por tipo en una ventana ("máximo N recordatorios por hora"): evita que un
  bug de reintentos inunde a alguien.
- Cuidado con los **fan-out masivos** (un cambio que dispara notificación a miles): encolá y
  regulá el ritmo, respetá el rate del proveedor, no tumbes tu propia cola ni te marquen spam.
- Circuit breaker por proveedor: si el proveedor de push está caído, no golpees en loop.

## 9. Registro y observabilidad

- Tabla de notificaciones: `id`, `recipient`, `type`, `channel`, `dedupeKey`, `status`
  (queued/sent/delivered/failed/bounced), `provider_message_id`, timestamps, `tenant_id`.
  Sin datos sensibles en el payload guardado.
- Consumí webhooks de entrega/rebote del proveedor para pasar de `sent` a `delivered`/`bounced`.
- Métricas: enviadas/entregadas/fallidas por canal y tipo, tasa de rebote, latencia
  evento→entrega, tamaño de DLQ (`backend-observability`).
- El registro es también auditoría de "se le avisó al paciente" — puede tener valor legal.

## Anti-patrones

- Mandar dentro de la transacción de negocio o en el request (lentitud, y se envía aunque el commit falle).
- HTML de email armado con strings en el servicio; plantilla sin versión ni test.
- Ignorar preferencias/opt-out, o chequearlas al emitir en vez de al despachar.
- Dato sensible (monto, documento, resultado de una evaluación) en asunto/cuerpo/URL/push.
- Estado único por notificación en vez de por canal; reintentar rebotes duros.
- Fan-out sin regulación que inunda al usuario o hace que te marquen spam.

## Checklist

- [ ] El envío sale por cola, fuera de la transacción y del request.
- [ ] Canal elegido por tipo/urgencia y por preferencia del usuario, chequeada al despachar.
- [ ] Opt-out respetado; obligatorios (seguridad/legal) separados y documentados.
- [ ] `dedupeKey` estable + `UNIQUE`; agrupación donde corresponde.
- [ ] Plantillas versionadas, i18n, email en HTML + texto.
- [ ] Estado y reintento **por canal**; permanentes no se reintentan; DLQ con alerta.
- [ ] Cero datos sensibles/tokens en asunto, cuerpo, URL o `data`; detalle detrás de login.
- [ ] Rate limit por usuario y regulación de fan-out; circuit breaker por proveedor.
- [ ] Registro sin datos sensibles, webhooks de entrega consumidos, métricas en dashboard.
