---
name: mobile-offline-sync
description: Modo offline y sincronización en la app móvil — almacenamiento local, cola de operaciones pendientes, sincronización idempotente, resolución de conflictos, indicador de estado de red y cifrado en reposo de los datos sensibles. Usar al construir cualquier flujo que deba funcionar sin conexión o tolerar cortes, al diseñar la caché local de una pantalla, al sincronizar cambios hechos offline, o cuando "si se corta el internet se pierde lo que cargó". Los datos sensibles se rigen por `data-privacy-sensitive`.
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Offline y sincronización — Flutter

En móvil la conexión se corta. Offline es un estado de diseño, no un error. Definí por pantalla
si es **solo lectura cacheada**, **lectura + escritura diferida** o **requiere conexión** (y decilo
claro en la UI).

## 1. Almacenamiento local

- Base local para datos estructurados: `drift` (SQL tipado sobre SQLite) o `sqflite`. `shared_preferences`
  solo para preferencias chicas, no para datos de dominio. Verificá la API del paquete en pub.dev.
- Modelá la caché con una marca de tiempo de sincronización y el origen del dato (servidor vs local
  pendiente), para saber qué mostrar y qué falta subir.
- Datos sensibles en reposo: **cifrados** (ver §5). No los dejes en claro en el dispositivo.

## 2. Lectura offline

- Patrón cache-then-network: mostrá lo cacheado al instante y refrescá desde el servidor si hay red;
  si no hay, quedate con la caché y marcala como "sin conexión / actualizado hace X".
- Nunca pantalla en blanco por falta de red: si hay caché, mostrala; si no, estado offline explícito
  con reintento (ver `mobile-ux-design`, `frontend-ux-states`).

## 3. Escritura diferida — cola de operaciones

- Las mutaciones hechas offline se persisten en una **cola** local (una tabla): tipo de operación,
  payload, timestamp, estado (pendiente/enviando/fallida) e **idempotency key** generada en el cliente.
- Al recuperar conexión, procesá la cola en orden. UI optimista: reflejá el cambio localmente y
  marcá el registro como "pendiente de sincronizar".
- Reintentos con backoff ante fallo de red; una operación no reintentable (rechazo de negocio 4xx)
  sale de la cola y se le informa al usuario, no se reintenta para siempre.

## 4. Sincronización idempotente y conflictos

- El servidor debe aceptar la **idempotency key** para que reenviar la misma operación no la duplique
  (coordiná con `concurrency-and-locking` e `integrity-testing` del backend). Reenviar es normal en móvil.
- Conflictos (el registro cambió en el servidor mientras estabas offline): definí la política por dato
  — last-write-wins con marca de versión, merge por campos, o "gana el servidor y avisá al usuario".
  Usá la versión de fila del backend para detectarlo; no pises a ciegas.
- No borres el ítem de la cola hasta confirmar el resultado del servidor.

## 5. Cifrado en reposo (datos sensibles)

- Datos de pacientes en la base local deben estar cifrados (SQLCipher con drift/sqflite, o cifrado a
  nivel de campo). La clave va en el almacenamiento seguro del sistema, no en el código ni en la base
  (ver `mobile-release-security`).
- Minimizá lo que se guarda offline: solo lo necesario para el flujo, con retención acotada; purgá al
  cerrar sesión. Ver `data-privacy-sensitive`.

## 6. Estado de red visible

- Escuchá la conectividad (paquete `connectivity_plus` u equivalente; verificá) y mostrá un banner
  persistente cuando no hay red y cuántos cambios quedan por sincronizar.
- Al volver la red, indicá el progreso de sincronización y el resultado (éxito / N fallaron).

## Anti-patrones
- Perder lo que el usuario cargó porque falló el POST.
- Reintentar indefinidamente una operación que el servidor rechazó por regla de negocio.
- Duplicar registros al reenviar por no usar idempotency key.
- Guardar datos sensibles en claro en la base local o en `shared_preferences`.
- "Sincronizado" mostrado antes de confirmar la respuesta del servidor.

## Checklist
- [ ] Cada pantalla declara su modo offline (lectura cacheada / escritura diferida / requiere red).
- [ ] Lectura cache-then-network; nunca blanco por falta de conexión.
- [ ] Mutaciones offline en cola persistente con idempotency key y estado por ítem.
- [ ] Sincronización idempotente; política de conflictos definida por dato con versión del backend.
- [ ] Dato sensible local cifrado, minimizado y purgado al cerrar sesión.
- [ ] Estado de red y progreso de sincronización visibles.
