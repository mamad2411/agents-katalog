---
name: container-security
description: Escape de contenedores y abuso de Kubernetes — detección de entorno, capabilities/mounts peligrosos, docker.sock, y abuso de RBAC/service accounts. Úsala cuando obtengas ejecución dentro de un contenedor o frente a un clúster K8s en scope.
---

# Seguridad ofensiva de contenedores y Kubernetes

GAP crítico moderno: una RCE web a menudo aterriza **dentro de un contenedor**. El objetivo es
salir al host o pivotar por el clúster — siempre dentro de scope y con el kill-switch de E2 listo.

## Cuándo usarla
Tras conseguir ejecución de comandos en lo que parece un contenedor, o cuando el scope incluya
un API server de Kubernetes / kubeconfig autorizado.

## Técnicas (con MITRE)
- **Detección de contenedor**: `/.dockerenv`, cgroups (`/proc/1/cgroup`), `/proc/1/status` (CapEff).
- **Escape por capabilities** (T1611): `CAP_SYS_ADMIN`, `CAP_SYS_PTRACE`; contenedor `--privileged`.
- **Mounts peligrosos** (T1611): `/var/run/docker.sock` montado → control del daemon = root host;
  hostPath del FS del nodo; `/dev` expuesto.
- **Abuso de Kubernetes** (T1610, T1613): token de service account en
  `/var/run/secrets/kubernetes.io/serviceaccount/`, RBAC laxo (`create pods`, `exec`, `secrets`),
  pods privilegiados, acceso al API server, kubelet 10250 expuesto.
- **Pivot al nodo** (T1611): pod con `hostPID`/`hostNetwork`/`hostPath` → host del clúster.

## Herramientas (suite del repo)
- Enumeración manual desde el shell del contenedor (lo cubre `post-exploit`).
- `kubectl auth can-i --list` para mapear permisos del token; chequeos tipo amicontained.
- Movimiento posterior: `netexec`/Impacket si el pivot llega a Windows — tier **destructive**.

## Evidencia y alcance
- Prueba del escape: acceso a un recurso del host/nodo que el contenedor no debería ver
  (p.ej. listar procesos del host, leer un fichero del nodo) como `evidence`.
- Confirma que el nodo/clúster está en `contracts/scope.json` antes de pivotar.
- Mapea a `contracts/finding.schema.json`; **sin fuente no se explota**. Las acciones de impacto
  (escape efectivo, ejecución en otros pods) pasan por el gate humano del bot.
