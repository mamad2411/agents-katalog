import { Callout } from "nextra/components"

# Odoo Skill

Después de instalar el módulo, corré esta rutina con tu agente (Claude Code, Cursor, Codex, etc.) para validar que `payment_talo` quedó bien instalado y operativo en tu Odoo.

<Callout emoji="💡">
	Copiá el skill completo con el botón de copiar del bloque de abajo, guardalo
	como un skill de tu agente (por ejemplo `install-and-validate/SKILL.md`) y
	pedile que lo ejecute contra tu instancia.
</Callout>

## Skill: `install-and-validate`

```markdown copy
---
name: install-and-validate
description: Instala el módulo payment_talo en una instancia Odoo 17 propia y valida que la integración con Talo quedó operativa. Usar cuando el usuario pide instalar, configurar o diagnosticar el módulo de pagos Talo.
---

# Instalación y validación de `payment_talo`

Guía para instalar este módulo en un Odoo propio (no en el repo demo de Talo) y confirmar que quedó
funcionando de punta a punta. Está pensada para que la use el agente/desarrollador del cliente, cuyo
entorno puede ser Docker, apt/deb, código fuente, Odoo.sh, o gestionado por un partner — por eso no
prescribe comandos fijos, sino qué lograr en cada paso. Adaptá cada acción al entorno real que
encuentres.

## Qué es este módulo

`payment_talo` agrega un proveedor de pago para Odoo que permite cobrar por transferencia bancaria
con acreditación automática vía Talo: el cliente ve un Alias/CVU en el checkout, transfiere, y cuando
Talo confirma el pago (vía webhook) la orden de venta se confirma sola, sin intervención manual.

## 1. Requisitos a confirmar antes de instalar

- Odoo **17.0** (Community o Enterprise).
- Los módulos `payment`, `account` y `l10n_ar` deben estar disponibles (son `depends` del manifest;
  Odoo los instala solos si faltan, pero confirmá que existen en el `addons_path`).
- Credenciales de API de Talo: `user_id`, `client_id`, `client_secret` (de sandbox y/o producción).
- El sitio Odoo debe ser accesible públicamente por **HTTPS**. El webhook de Talo no puede llegar a
  `localhost` ni a una IP privada — sin esto la orden nunca se confirma sola.
- Moneda **ARS** configurada en la compañía.

## 2. Instalación (adaptá al tipo de despliegue)

Primero identificá cómo está desplegado ese Odoo — Docker/docker-compose, apt/deb, instalación desde
código fuente, Odoo.sh, o administrado por un tercero — porque cambia dónde vive el `addons_path` y
cómo se reinicia el servicio.

1. **Ubicá el `addons_path` real.** Como referencia orientativa (puede variar):

   | Tipo de instalación | Path típico de addons custom |
   |---|---|
   | Docker oficial (docker-compose) | Un volumen montado en `/mnt/extra-addons` dentro del contenedor |
   | apt/deb (Debian/Ubuntu) | `/opt/odoo/custom-addons` o similar — nunca dentro de la carpeta `addons` del core |
   | Código fuente (`git clone odoo/odoo`) | Una carpeta separada agregada aparte, no dentro de `odoo/addons` del core |
   | Odoo.sh | El módulo va directo en el repo del proyecto, junto a otros addons — no aplica copiar a mano |

   Nunca mezcles módulos custom dentro de la carpeta `addons` del core: usá siempre una carpeta
   separada agregada al `addons_path`, para no romper upgrades del core.

2. **Copiá `payment_talo/`** (esta carpeta) a esa ubicación y confirmá que el path está listado en
   `addons_path` del `odoo.conf`.

3. **Reiniciá el servicio de Odoo** para que detecte el módulo nuevo. El mecanismo depende del
   entorno (reinicio de contenedor, `systemctl`, proceso propio, redeploy en Odoo.sh, etc.) — el
   objetivo es que el proceso de Odoo vuelva a arrancar leyendo el `addons_path` actualizado.

4. **Instalá el módulo:**
   - Por UI: **Apps → Update Apps List**, buscar **"Payment Provider: Talo"** e instalar.
   - Por línea de comandos (si hay acceso): `-i payment_talo` al arrancar Odoo.

## 3. Configuración

En **Sitio web/Contabilidad → Configuración → Proveedores de pago → Talo**:

- Cargar `talo_user_id`, `talo_client_id`, `talo_client_secret`.
- Elegir **Estado**: *Modo de prueba* (sandbox) o *Habilitado* (producción) — define contra qué API
  de Talo se opera.
- **Publicar** el proveedor. Si no está publicado, no aparece en el checkout.
- Opcional: color de marca del encabezado de la página de instrucciones (`talo_brand_color`).

En **Ajustes → Sitio web**: configurar la **URL base pública** del sitio. Es crítico — de ahí sale el
`webhook_url` que el módulo le manda a Talo en cada pago. Si apunta a `localhost` o a un dominio
incorrecto, los pagos nunca se confirman solos.

## 4. Checklist de validación post-instalación

Esta es la parte que responde a "¿quedó todo funcionando?". Verificá cada punto con el medio que
tengas disponible en ese entorno (UI de Odoo, XML-RPC, acceso a shell/DB, logs) — el skill no asume
uno en particular:

- [ ] El módulo figura como **instalado** (en Apps, o el estado correspondiente del módulo).
- [ ] Existe un proveedor de pago con código `talo` y tiene un método de pago asociado creado
      automáticamente al instalar (si falta, la instalación quedó a medias — revisar logs de
      instalación).
- [ ] El proveedor está **publicado** y en el estado esperado (test o enabled, según las credenciales
      cargadas).
- [ ] El checkout del sitio muestra **"Transferencia Talo"** como opción de pago.
- [ ] Una compra de prueba en sandbox llega a la página de instrucciones con Alias, monto y
      vencimiento visibles.
- [ ] La URL base configurada es pública y HTTPS (no `localhost` ni una IP interna) — condición
      necesaria para que el webhook de Talo pueda llegar.
- [ ] Al simular el pago en el simulador de sandbox de Talo, la transacción pasa a **confirmada** y la
      **orden de venta se confirma sola**, sin intervención manual. Esta es la prueba end-to-end real
      de que la integración funciona.
- [ ] Los logs con prefijo `TALO` no muestran errores de autenticación (401) ni de conexión.

## 5. Troubleshooting

| Síntoma | Causa probable | Qué revisar |
|---|---|---|
| El pago queda pendiente para siempre aunque se transfirió | El webhook no llega: URL base en `localhost` o incorrecta | URL pública HTTPS en Ajustes → Sitio web. Para desarrollo local, usar un túnel tipo ngrok |
| "No suitable payment method" en el checkout | Proveedor no publicado | Publicarlo desde el formulario del proveedor |
| Error de autenticación / credenciales inválidas | Credenciales incorrectas o de un entorno distinto al configurado (sandbox vs producción) | Revisar `user_id`/`client_id`/`client_secret` y que coincidan con el Estado del proveedor |
| No se pudo conectar con Talo | Sin salida a internet desde el servidor de Odoo, o API de Talo caída | Probar conectividad HTTP saliente desde el servidor hacia la API de Talo; revisar logs con prefijo `TALO` |
| Error de campos requeridos en el checkout | Campos de `l10n_ar` obligatorios del partner (CUIT, responsabilidad AFIP) sin completar | Completar tipo y número de identificación en el formulario de dirección del checkout |

## 6. Más allá de este skill

Este skill es deliberadamente acotado a instalar y validar. Para arquitectura interna, diagramas de
flujo y mapeo completo de estados, pedile a Talo la documentación completa o consultá
docs.talo.com.ar.
```

## Cómo usarlo

1. Copiá el contenido del bloque.
2. Pegalo en la carpeta de skills de tu agente (o pegaselo directo en el prompt).
3. Pedile algo como: *"Corré el skill install-and-validate contra mi Odoo y confirmá que Talo quedó operativo."*
4. El agente debería seguir el checklist de validación (módulo instalado, proveedor publicado, checkout, webhook, sandbox).

Cuando el skill termina en verde, tu integración está lista para probar end-to-end (o pasar a producción).
