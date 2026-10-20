---
name: Comunicador Backend
description: Enlace A2A del Grupo Backend. Gestiona la comunicación con otros grupos del Conglomerado.
metadata:
  model: inherit
  version: "1.0.0"
  type: group-communicator
  group: "10-backend-group"
---

# 🔗 Comunicador Backend

Skill de comunicación del Grupo Backend. Hereda del [Comunicador A2A Global](file:///d:/Users/julio/developer/Habilidades%20de%20Agentes/skills/99-common-utils/a2a-communicator/SKILL.md).

## Propósito

Gestionar la comunicación entre el Grupo Backend y otros grupos del Conglomerado cuando el Orquestador necesita información o servicios externos.

## Uso

Este skill es invocado por el Orquestador Backend cuando:
- Necesita información del Frontend (campos de formularios, requisitos UI)
- Requiere validación de Security (autenticación, autorización)
- Necesita coordinar con DevOps (deployment, infraestructura)
- Solicita tests del grupo Testing

## Grupos de Comunicación Frecuente

| Grupo | Casos de Uso Típicos |
|-------|---------------------|
| Frontend | Requisitos de UI, formatos de datos, validaciones cliente |
| Security | Autenticación, autorización, cifrado, compliance |
| DevOps | Variables de entorno, configuración, deployment |
| Testing | Tests de integración, mocks, fixtures |
| Data/ML | Pipelines de datos, modelos, embeddings |

## Protocolo

Consulta el [Protocolo A2A](file:///d:/Users/julio/developer/Habilidades%20de%20Agentes/skills/99-common-utils/a2a-communicator/SKILL.md) para detalles de implementación.

```yaml
source_group: "10-backend-group"
max_hops: 5
timeout_seconds: 30
```
