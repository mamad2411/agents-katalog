---
name: cloud-security
description: Pentest de infraestructura cloud (AWS/Azure/GCP) — metadata SSRF (IMDS), claves/credenciales expuestas, buckets/blobs públicos y escalada de privilegios por IAM. Úsala cuando el scope incluya cuentas/infra cloud o descubras endpoints o credenciales cloud.
---

# Seguridad ofensiva en cloud (AWS / Azure / GCP)

En cloud el perímetro es la **identidad**: la cadena suele ser metadata/credencial expuesta →
asunción de rol → privesc por política IAM laxa. Nada de tocar fuera de las cuentas en scope.

## Cuándo usarla
Cuando `contracts/scope.json` autorice cuentas/recursos cloud, o cuando en un assessment web
encuentres un SSRF, una clave `AKIA…`/token, o un bucket con nombre del cliente.

## Técnicas (con MITRE)
- **IMDS SSRF** (T1552.005): desde un SSRF, lee `http://169.254.169.254/…` (AWS IMDSv1),
  `http://169.254.169.254/metadata/instance?api-version=…` (Azure, cabecera `Metadata: true`),
  metadata GCP (cabecera `Metadata-Flavor: Google`) → credenciales temporales.
- **Credenciales expuestas** (T1552): claves en repos/JS/variables; valida con `sts get-caller-identity`.
- **Almacenamiento público** (T1530): S3/Blob/GCS listables o escribibles.
- **Privesc IAM** (T1078.004, T1098): `iam:PassRole`, `*:Create*Policy`, asunción de roles laxos.
- **Persistencia** (T1098): claves de acceso nuevas, políticas inline (solo si el RoE lo permite).

## Herramientas
- Recon/audit no destructivo: **CLI nativa** (`aws`/`az`/`gcloud`) + `curl` a IMDS como base. Para
  auditoría de postura a escala, `prowler` o `scoutsuite` (opcionales: instálalos en la VM si el
  engagement lo requiere — no van en el toolchain por defecto).
- Explotación guiada: `pacu` (AWS) — alto impacto, trátalo como **destructive** (aprobación humana).

## Evidencia y alcance
- Prueba mínima: salida de `get-caller-identity`/listado del recurso + la política que lo permite.
- Trabaja con credenciales **temporales** y revoca al cerrar (zona E3, sin egress de datos cliente).
- Mapea a `contracts/finding.schema.json`; **sin fuente no se explota** (una política "peligrosa"
  es candidato hasta demostrar la escalada). Acciones con impacto pasan por el gate del bot.
