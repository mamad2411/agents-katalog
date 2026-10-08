# Contrato de trabajo para agentes de SDI

## Filosofía

- SDI es un producto, no una colección de scripts copiados.
- La arquitectura tiene prioridad sobre la velocidad de implementación.
- El alcance de SDI 0.1 está congelado.

## Fuente de verdad

La referencia principal es [docs/SDI_PRODUCT_ARCHITECTURE.md](docs/SDI_PRODUCT_ARCHITECTURE.md). Sus decisiones de alcance, contratos y roadmap prevalecen sobre inferencias o preferencias de implementación.

## Incorporación de un agente nuevo

Antes de escribir o modificar código, reconstruye el estado del proyecto leyendo, en este orden:

1. `README.md` — propósito, tecnologías, estado general.
2. [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md) — punto de entrada único: etapa en curso, última etapa completada, ADR relevantes, decisiones abiertas, trabajo pendiente y cómo validar.
3. `docs/SDI_PRODUCT_ARCHITECTURE.md` — fuente de verdad arquitectónica completa.
4. `docs/ADR/` — decisiones arquitectónicas formales, en orden.
5. Código en `src/` y pruebas en `tests/`.

No asumas la arquitectura ni el estado de implementación a partir de conversaciones previas o supuestos: reconstrúyelos leyendo el repositorio. Si algo en el código contradice lo documentado, repórtalo antes de corregirlo.

Este orden aplica para **desarrollar SDI mismo** (cambiar código en este repositorio). Si el objetivo de la tarea es **instalar o configurar `sdi-cli` en un proyecto consumidor** (no tocar el código de SDI), no hace falta leer la arquitectura completa: usá directamente [docs/guides/INSTALLATION.md](docs/guides/INSTALLATION.md) y, para Astro + Cloudflare, [docs/guides/ASTRO_CLOUDFLARE.md](docs/guides/ASTRO_CLOUDFLARE.md).

## Forma de trabajo

Los agentes deben implementar únicamente una etapa por chat, mantener los cambios pequeños y revisar el criterio de finalización de la etapa antes de avanzar. Todo cambio de comportamiento debe incluir pruebas proporcionales; se debe evitar la duplicación y respetar el roadmap aprobado.

## Restricciones

No se permite:

- rediseñar la arquitectura;
- ampliar el alcance de SDI 0.1;
- introducir funcionalidades futuras por anticipación;
- eliminar compatibilidad legacy antes de completar su migración.

## Gestión de deuda técnica

Si durante una etapa aparece una mejora fuera de alcance, no se implementa. Se registra como propuesta futura o ADR, según corresponda, y se continúa únicamente con la etapa actual.

## Calidad

Todo código nuevo debe ser modular, tipado, probado y fácil de mantener. Los agentes deben mantener la documentación coherente con los cambios aprobados, actualizar `CHANGELOG.md` en `Unreleased` cuando el cambio modifique el estado real del producto y no modificar silenciosamente la arquitectura congelada.

## Identidad Git de Terra

Para los commits y pushes de Terra en este repositorio se usa la identidad Git local `Terra (Codex) <terra@users.noreply.github.com>`. Los chats posteriores deben conservarla salvo instrucción explícita del usuario.
