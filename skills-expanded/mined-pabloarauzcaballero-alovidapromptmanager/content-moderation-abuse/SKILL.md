---
name: content-moderation-abuse
description: Moderación y prevención de abuso en features sociales (publicaciones, comentarios, mensajes, reseñas) — reportes de usuarios, cola de moderación, filtros automáticos vs revisión humana, rate limiting y anti-spam, bloqueo y silencio entre usuarios, autoría verificada, protección de menores y rastro auditable de cada acción de moderación. Usar al construir o revisar cualquier superficie donde un usuario publica contenido que otros ven, al agregar reportar/bloquear/ocultar, o al diagnosticar spam, acoso o contenido que no debería estar visible.
---

# Moderación y prevención de abuso

Toda superficie donde un usuario publica contenido que otros ven es superficie de abuso: spam,
acoso, contenido dañino, suplantación. En un producto de salud el riesgo sube: desinformación
médica y datos sensibles expuestos por los propios usuarios. Complementa `authz-access-control`
(quién puede qué) y `social-feed-design` (el modelo del feed).

## 1. Principios

- **Autoría verificada e inmutable**: cada pieza de contenido guarda su autor real (del contexto
  autenticado), no uno declarado por el cliente. Nadie publica "como" otro.
- **El contenido del usuario es entrada hostil**: sanitizá y escapá al mostrar (XSS,
  `frontend-security`/`security-guardrails`); validá tamaño y formato al recibir.
- **Trazabilidad**: toda acción de moderación (ocultar, borrar, banear, restaurar) queda en un
  rastro auditable con quién, qué, cuándo y por qué (`audit-trail-history`). La moderación sin
  registro es arbitrariedad y no se puede revisar ni defender.
- **Reversibilidad y apelación**: preferí ocultar (reversible) a borrar (destructivo); dale al
  autor forma de saber qué pasó y apelar cuando corresponda.

## 2. Reportes de usuarios

- Cualquier usuario puede **reportar** una pieza: motivo (de una lista: spam, acoso, contenido
  sensible, desinformación, suplantación, otro), texto opcional, una vez por usuario por pieza
  (idempotente).
- El reporte crea/actualiza un caso en la **cola de moderación**, no oculta el contenido solo. No
  dejes que "N reportes = borrado automático": es censura por brigada. Los reportes **priorizan**
  la revisión, no la ejecutan (salvo señales muy fuertes y acotadas, definidas por política).
- El reportante no queda expuesto al reportado.

## 3. Cola de moderación

- Estado del caso como máquina explícita (`state-machines-workflows`):
  `pendiente → en_revisión → resuelto(acción) / descartado`, con dueño y timestamps.
- Prioridad por señal: severidad del motivo, cantidad de reportes, reputación/edad de la cuenta,
  si toca a un menor.
- Acciones posibles: sin acción, ocultar, borrar, advertir al autor, silenciar, banear, escalar.
  Cada una registrada y (donde aplique) notificada al autor (`notifications-delivery`, sin exponer
  al reportante).
- SLA de revisión para lo urgente; una cola que nadie mira es moderación de utilería.

## 4. Filtros automáticos vs revisión humana

| Capa | Rol | Límite |
|---|---|---|
| Filtro automático (heurísticas, listas, límites, detección de patrones) | frenar lo obvio y masivo (spam, enlaces, floods) en el acto | falsos positivos/negativos; no juzga contexto |
| Revisión humana | decidir lo ambiguo, el acoso, el matiz clínico | no escala a todo el volumen |

- Lo automático **filtra y prioriza**; lo humano **decide** lo dudoso. No delegues a un
  clasificador la decisión final sobre contenido borderline.
- Cuidado con el sesgo del filtro (dialectos, idiomas, términos médicos legítimos marcados como
  ofensivos). Medí falsos positivos.
- Contenido generado o clasificado por IA **no** es verdad clínica ni juicio definitivo
  (`medication-prescription-safety`, `anti-hallucination-guard`): es una señal para un humano.

## 5. Rate limiting y anti-spam

- Límites por usuario y por acción en ventanas de tiempo (publicaciones, comentarios, reportes,
  seguir, mensajes): frena floods y bots. `security-guardrails` para el marco.
- Señales anti-spam: cuentas nuevas que publican mucho, enlaces repetidos, mismo contenido a
  muchos destinos, patrones de bot. Elevá fricción (revisión previa, captcha) antes de banear.
- Verificación de identidad/edad de cuenta como gate para acciones sensibles.
- Protegé los endpoints de escritura social con las mismas reglas de autorización que el resto;
  la UI que oculta un botón no es control (`authz-access-control`).

## 6. Bloqueo y silencio entre usuarios

- **Bloquear**: A no ve a B y B no ve ni interactúa con A (ni comenta, ni menciona, ni mensajea).
  Aplicá el filtro **en el servidor**, en las queries del feed y de mensajes, no solo escondiendo
  en el cliente.
- **Silenciar (mute)**: A deja de ver a B, pero B no se entera ni pierde acceso general.
- El bloqueo es asimétrico y privado (B no recibe un cartel de "te bloquearon").
- Estas relaciones son datos con dueño y tenant; respetalas en cada listado, búsqueda y
  notificación (`search-and-filtering`).

## 7. Datos sensibles publicados por usuarios y menores

- Un usuario puede publicar **su propia** información de salud o la de otro. No puedes impedirlo
  del todo, pero: advertí antes de publicar en superficies públicas, permití borrar/ocultar rápido
  lo propio, y no amplifiques datos sensibles.
- No expongas en superficies públicas datos que el sistema conoce del usuario (que es paciente de
  X, su diagnóstico): eso es fuga tuya, no del usuario (`data-privacy-phi`).
- **Menores**: reglas más estrictas (consentimiento de representante, `consent-management`),
  prioridad máxima en moderación, límites de contacto. Validá el marco legal aplicable con el
  responsable legal (`regulatory-compliance-mapping`).

## Anti-patrones

- Autor declarado por el cliente; contenido mostrado sin escapar.
- N reportes → borrado automático; reportante expuesto al reportado.
- Filtro automático como juez final de contenido ambiguo; IA tratada como verdad clínica.
- Bloqueo aplicado solo en el cliente; relaciones de bloqueo ignoradas en búsqueda/feed/notificaciones.
- Acciones de moderación sin rastro; borrado destructivo por default; sin apelación.
- Endpoints sociales sin rate limit ni autorización server-side.

## Checklist

- [ ] Autoría del contexto autenticado, inmutable; contenido validado al entrar y escapado al mostrar.
- [ ] Reportar con motivos, idempotente, sin exponer al reportante; los reportes priorizan, no ejecutan.
- [ ] Cola de moderación con estados, dueño, prioridad por señal y SLA; acciones registradas.
- [ ] Filtro automático frena lo masivo; lo ambiguo lo decide un humano; falsos positivos medidos.
- [ ] Rate limit por usuario/acción; señales anti-spam con fricción escalada antes del baneo.
- [ ] Bloqueo/silencio aplicados en el servidor, en feed, búsqueda, mensajes y notificaciones.
- [ ] Datos sensibles: el sistema no los amplifica; menores con reglas reforzadas y marco legal validado.
- [ ] Toda acción de moderación auditada; preferencia por ocultar reversible y vía de apelación.
