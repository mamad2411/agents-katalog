---
name: cloud-project-standard
description: "Estándar obligatorio para trabajar en AWS o Google Cloud: cuentas/proyectos y entornos, identidad (roles por workload, OIDC, sin llaves estáticas), secretos, red privada, cómputo, datos, IaC con Terraform, CI/CD, etiquetas, observabilidad y auditoría, costos y resiliencia, más reglas de operación segura para agentes y un checklist final. Usar siempre que la tarea cree o modifique infraestructura cloud, despliegues a AWS/GCP, IAM o integraciones con servicios cloud, y al verificar que cumple el estándar antes de entregar."
---

# cloud-project-standard

Estándar **obligatorio** para todo lo que toque AWS o Google Cloud. Es la contraparte cloud de `frontend:nextjs-project-standard` y `mobile:expo-project-standard`: reglas concretas, precedencia clara y un **Final Checklist** que `/standard` recorre al terminar.

> **Infraestructura existente**: si el proyecto ya define convenciones (`CLAUDE.md`, módulos, naming, estructura de cuentas o proyectos), **síguelas**. Este estándar manda en lo nuevo y en lo no definido; las desviaciones del código existente se anotan, no se migran fuera del alcance. Los límites, precios y versiones cambian: verifícalos en la documentación oficial del proveedor antes de afirmarlos.

---

## 1. Cuándo es obligatorio y qué proveedor aplica

Es obligatorio (en `/standard`, en la especialidad `devops` y para los agentes `devops:*`) cuando la tarea:

- crea o modifica infraestructura cloud: IAM, redes, cómputo, datos, colas, buckets, DNS, certificados;
- cambia cómo se construye, despliega o ejecuta un servicio en AWS/GCP (Dockerfile hacia ECS/Cloud Run, workflows con deploy, manifiestos hacia EKS/GKE);
- usa SDKs de servicios cloud en código de aplicación (S3, SQS, Secrets Manager, GCS, Pub/Sub, Secret Manager...): ahí aplican las secciones 3, 4, 6 y 7.

Detección del proveedor (lee la referencia del que corresponda):

| Señal en el repo | Proveedor | Referencia |
|---|---|---|
| `provider "aws"`, `@aws-sdk/*`, `boto3`, `aws-cdk`, `cdk.json`, `samconfig.toml`, `aws-actions/*`, `.aws/` | AWS | [references/aws.md](references/aws.md) |
| `provider "google"`, `@google-cloud/*`, `google-cloud-*`, `cloudbuild.yaml`, `app.yaml`, `google-github-actions/*` | Google Cloud | [references/gcp.md](references/gcp.md) |

- Las dos señales a la vez → cada recurso sigue la referencia de su proveedor.
- Ninguna señal o ambigüedad → **pregunta** el proveedor; no lo elijas por defecto.
- Azure u otra nube: este estándar no lo cubre; aplica solo las secciones agnósticas y avisa de la limitación.

Equivalencias rápidas (los detalles están en las referencias):

| Necesidad | AWS | Google Cloud |
|---|---|---|
| Aislamiento por entorno | Cuentas en Organizations | Proyectos en folders |
| Identidad de un workload | Rol (task role, IRSA/Pod Identity, rol de Lambda) | Service account propia (adjunta o Workload Identity) |
| Identidad de CI | OIDC → rol IAM | Workload Identity Federation |
| Acceso de personas | IAM Identity Center | Cloud Identity / Workspace SSO |
| Secretos | Secrets Manager / SSM SecureString | Secret Manager |
| Cifrado con llave propia | KMS | Cloud KMS |
| Contenedores sin servidores | ECS Fargate, App Runner, Lambda | Cloud Run, Cloud Functions |
| Registro de imágenes | ECR | Artifact Registry |
| Base relacional | RDS / Aurora | Cloud SQL / AlloyDB |
| Objetos | S3 | Cloud Storage |
| Logs y métricas | CloudWatch | Cloud Logging / Monitoring |
| Auditoría | CloudTrail | Cloud Audit Logs |
| Presupuestos | AWS Budgets | Billing budgets |

---

## 2. Cuentas, proyectos y entornos

- Mínimo **tres entornos**: `dev`, `staging`, `production`. Producción **aislada** en su propia cuenta (AWS) o proyecto (GCP); no compartas cuenta/proyecto entre producción y no producción.
- Una organización con estructura por entorno (OU en AWS, folders en GCP) donde se aplican las **guardas** (SCP / Organization Policies): sin llaves estáticas, sin acceso público a almacenamiento, regiones permitidas, auditoría imposible de apagar.
- **Región única** por defecto, declarada de forma explícita en el código (nunca implícita por el CLI); multirregión solo con requisito de DR documentado.
- Nada de recursos creados a mano en staging/producción: todo lo persistente nace de IaC (sección 8). La consola es para leer y diagnosticar.
- Cuenta/proyecto de **logs y auditoría** separados del de las cargas de trabajo cuando la organización lo permita.

## 3. Identidad y acceso (IAM)

- **Mínimo privilegio**: permisos por recurso y acción concretos. Prohibido `Action: "*"`, `Resource: "*"`, `roles/owner` y `roles/editor` sin una justificación escrita en el PR.
- **Una identidad por workload** (rol o service account propia). No reutilices la identidad por defecto de la plataforma (p. ej. la service account por defecto de Compute) ni compartas una entre servicios.
- **Cero credenciales de larga vida**: no crees access keys de IAM users ni llaves JSON de service accounts. Los workloads usan su identidad adjunta; el CI usa **OIDC / Workload Identity Federation** restringido al repositorio y, en producción, al environment; las personas entran con SSO y MFA.
- Los roles de CI de **producción** solo se asumen desde el environment protegido; el de `plan` (lectura) es distinto del de `apply`.
- No uses el usuario root (AWS) ni cuentas de organización-admin para el trabajo diario.
- Revisa permisos con el analizador del proveedor (IAM Access Analyzer / Policy Analyzer + Recommender) y elimina lo no usado.

## 4. Secretos y configuración

- Los secretos viven en el gestor del proveedor (Secrets Manager o SSM SecureString / Secret Manager). **Nunca** en el repositorio, en `*.tfvars`, en variables de entorno de la imagen ni en el estado de Terraform si se puede evitar (referencia el secreto por ARN/ID, no por valor).
- El workload recibe el secreto por referencia en tiempo de ejecución (inyección de la plataforma o lectura con su identidad) y con acceso solo a **sus** secretos.
- Rotación para credenciales de bases de datos y claves de terceros; usa autenticación IAM a la base cuando el motor la soporte (tokens de vida corta).
- Datos especialmente sensibles: llave propia (KMS) con política de acceso mínima.
- Configuración no secreta (URLs, flags, región) por parámetros o variables, validada al arrancar; falla rápido si falta.
- Nunca imprimas secretos, tokens ni credenciales en logs, salidas de Terraform o mensajes de error.

## 5. Red

- Cómputo y datos en **subredes privadas**. Lo público es solo el balanceador o CDN, con **TLS** y **WAF** (WAF / Cloud Armor) cuando aplique.
- Reglas de entrada mínimas: ningún `0.0.0.0/0` salvo 80/443 en el balanceador público. Entre servicios, referencia grupos de seguridad / etiquetas de red, no rangos abiertos.
- **Sin SSH ni RDP abiertos**: acceso administrativo por SSM Session Manager (AWS) o IAP / OS Login (GCP).
- Tráfico hacia servicios del proveedor por **endpoints privados** (VPC endpoints / Private Google Access, Private Service Connect) y egreso controlado: es más seguro y suele ser más barato que NAT.
- GCP: red en modo personalizado, nunca la red `default`. AWS: no uses la VPC por defecto para cargas reales.
- Logs de flujo de red activos en producción.

## 6. Cómputo y entrega

- Elige la opción **más simple** que cumpla: contenedores sin servidores (ECS Fargate / App Runner / Cloud Run) o funciones primero; Kubernetes (EKS/GKE) solo con varios servicios, necesidad de portabilidad y un equipo que lo opere. Decídelo con `devops:cloud-architect`.
- Imágenes en el registro del proveedor con **escaneo de vulnerabilidades** activo, y desplegadas **por digest**, no por tag mutable. Imágenes base mínimas y sin root (`devops:docker`).
- Límites explícitos: CPU/memoria, mínimo y máximo de instancias, concurrencia y **timeouts**. Para streaming (LLM, SSE) revisa el timeout del balanceador y del servicio.
- Health checks reales (liveness/readiness) y despliegues con **rollback automático** (circuit breaker, revisiones/tráfico gradual).
- Servicios privados por defecto: sin invocación pública anónima salvo que sea un requisito.
- Aplicaciones con LangChain/LangGraph: persistencia de checkpoints en un servicio gestionado, timeouts y reintentos alineados con los límites de tasa del proveedor del modelo (`devops:cloud-architect`).

## 7. Datos

- Servicios **gestionados** (RDS/Aurora/DynamoDB/S3, Cloud SQL/Firestore/Cloud Storage) antes que bases autoadministradas en VMs.
- **Cifrado** en reposo (llaves gestionadas o propias) y en tránsito (TLS obligatorio; en buckets, denegar tráfico sin TLS).
- Producción con **alta disponibilidad** (Multi-AZ / regional), **backups y recuperación a un punto en el tiempo**, y **protección contra borrado**. Un backup que nunca se restauró no cuenta: documenta y prueba la restauración.
- Bases de datos solo en red privada; sin IP pública.
- Buckets **privados** con bloqueo de acceso público a nivel de cuenta/proyecto, versionado y reglas de ciclo de vida; los datos expuestos pasan por URLs prefirmadas/firmadas de corta duración o por CDN.
- Define y documenta RPO/RTO de cada almacén de datos.

## 8. Infraestructura como código

- Todo lo persistente se define en **Terraform/OpenTofu** siguiendo `devops:terraform`: un directorio por entorno, estado remoto con bloqueo y cifrado, versiones de providers fijadas, módulos pequeños. CDK/CloudFormation/Pulumi solo si el proyecto ya los usa; no mezcles herramientas en el mismo recurso.
- **Protección contra cuenta equivocada**: el provider fija la cuenta/proyecto permitido (`allowed_account_ids` en AWS; `project` explícito en GCP) y la región.
- `fmt`, `validate`, `tflint` y un escáner de políticas (`checkov` o `trivy config`) limpios antes del `plan`; el `plan` se **revisa** antes del `apply`.
- `apply`, `destroy`, `import` y manipulación de estado **solo con confirmación explícita del usuario** y, de preferencia, desde el pipeline con environment protegido.
- Cambios manuales de emergencia: se reconcilian en IaC el mismo día (importar o revertir) y se anotan en el PR.
- Habilita las APIs de GCP de forma explícita en IaC (`google_project_service`); no dependas de que alguien las haya activado.

## 9. CI/CD

- Pipelines con `devops:github-actions`: permisos mínimos, actions fijadas por SHA, OIDC (sección 3), `plan` en cada PR y `apply`/deploy con **environment** y aprobación para producción.
- Se promueve el **mismo artefacto** (digest) entre entornos; no se reconstruye para producción.
- Un solo camino a producción: los despliegues manuales con credenciales personales no son el flujo normal.
- Escaneos en CI: secretos, dependencias, imagen e IaC.

## 10. Etiquetas, naming y gobierno

- Etiquetas (AWS `tags`) / labels (GCP `labels`) **obligatorias** en todo recurso que las soporte: `project`, `environment`, `owner`, `managed_by=terraform`, `repo`, y `cost_center` si la organización lo usa. Aplícalas por defecto desde el provider (`default_tags` / `default_labels`) y activa las de asignación de costos.
- GCP: las labels solo admiten minúsculas, dígitos, `_` y `-`; usa los mismos nombres de clave que en AWS.
- Naming predecible: `<proyecto>-<entorno>-<recurso>` en minúsculas; el entorno siempre en el nombre.
- Nada de recursos huérfanos: todo recurso tiene `owner` y un motivo trazable al repositorio.

## 11. Observabilidad y auditoría

- **Auditoría activa y no apagable**: CloudTrail multirregión (con validación de integridad) / Cloud Audit Logs (Data Access en servicios sensibles), centralizada y con retención definida.
- Logs **estructurados** a CloudWatch / Cloud Logging con **retención explícita** (nunca "sin expiración"), sin PII ni secretos.
- Métricas, alarmas y alertas ligadas a un canal de guardia para lo que afecta al usuario (errores, latencia, saturación, trabajos fallidos); trazas con OpenTelemetry cuando haya varios servicios.
- Detección de amenazas activada en producción (GuardDuty/Security Hub en AWS; Security Command Center en GCP) cuando el plan de la organización lo incluya.

## 12. Costos y resiliencia

- **Presupuestos con alertas** (80 % y 100 %) por cuenta/proyecto y entorno; estima el costo mensual **antes** de crear (`devops:cloud-architect`).
- Vigila los costos silenciosos: NAT y egreso, ingesta de logs, instancias o clusters ociosos, snapshots huérfanos. Apaga o reduce no producción fuera de horario cuando sea posible.
- Producción en **varias zonas de disponibilidad**, con autoscaling acotado y sin puntos únicos de fallo; DR multirregión solo si hay requisito.
- Cada servicio crítico tiene runbook: cómo desplegar, revertir, restaurar y a quién escalar (`core:documentation-standards`).

## 13. Operación segura (agentes y personas)

Reglas para todo agente que trabaje con este estándar:

1. **Solo lectura por defecto.** Se permiten comandos de inspección (`aws sts get-caller-identity`, `aws ... describe-*|list-*|get-*`, `gcloud config list`, `gcloud ... describe|list`, `terraform plan`). Todo lo que cree, modifique o borre recursos requiere **confirmación explícita del usuario** en esa acción; el hook de `core` lo pide.
2. **Antes de cualquier cambio, confirma el destino**: cuenta/proyecto, región y entorno (`aws sts get-caller-identity`, `gcloud config get-value project`). Si es producción, dilo en voz alta y espera un "sí" explícito.
3. **Nunca** pidas, muestres, guardes ni escribas en archivos credenciales, llaves o tokens. Si el usuario pega unas, no las repitas y recomiéndale rotarlas.
4. **No ejecutes** `apply`, `destroy`, borrados de buckets/bases/snapshots ni cambios de IAM por tu cuenta; prepara el `plan` o el comando y deja la decisión al usuario.
5. Un cambio de IAM, de red pública o de cifrado se **destaca** en el resumen final aunque sea pequeño.

---

## Final Checklist

Antes de entregar. Marca ✅ / ❌ (con archivo y motivo) / N/A para cada ítem sobre lo que cambió:

- [ ] Proveedor detectado o confirmado con el usuario; se aplicó la referencia correcta (AWS/GCP)
- [ ] Producción aislada de no producción (cuenta/proyecto) y tres entornos como mínimo
- [ ] Región declarada de forma explícita; provider protegido contra cuenta/proyecto equivocado
- [ ] Una identidad por workload, mínimo privilegio y sin `*`/owner/editor sin justificación
- [ ] Sin llaves estáticas: workloads con identidad adjunta, CI con OIDC/WIF restringido al repo (y environment en producción)
- [ ] Secretos en el gestor del proveedor; ninguno en repo, `tfvars`, imagen ni logs
- [ ] Cómputo y datos en red privada; sin `0.0.0.0/0` salvo 80/443 del balanceador; sin SSH/RDP abierto
- [ ] Datos cifrados en reposo y tránsito; producción con HA, backups, PITR y protección contra borrado; restauración documentada
- [ ] Buckets privados con bloqueo de acceso público, versionado y ciclo de vida
- [ ] Imágenes escaneadas y desplegadas por digest; límites, timeouts y health checks definidos; rollback automático
- [ ] Todo lo persistente en IaC (`devops:terraform`); `fmt`/`validate`/`tflint`/escáner de políticas limpios; `plan` revisado
- [ ] Pipeline con permisos mínimos, actions fijadas por SHA y `apply`/deploy a producción con environment aprobado
- [ ] Etiquetas/labels obligatorias aplicadas por defecto desde el provider
- [ ] Auditoría activa (CloudTrail / Audit Logs), logs estructurados con retención explícita y alarmas hacia un canal
- [ ] Presupuesto con alertas y costo mensual estimado en el PR
- [ ] Ningún comando mutante ni credencial manejados sin confirmación del usuario; destino (cuenta/región/entorno) verificado

## Referencias

- [references/aws.md](references/aws.md): cuentas y SCP, roles y OIDC de GitHub, Secrets Manager/SSM, VPC endpoints, ECS/Lambda/EKS, RDS, S3, CloudTrail, Budgets y preflight de CLI. Léelo cuando el proveedor sea AWS.
- [references/gcp.md](references/gcp.md): folders y Organization Policies, service accounts y Workload Identity Federation de GitHub, Secret Manager, VPC y Cloud NAT, Cloud Run/GKE, Cloud SQL, Cloud Storage, Audit Logs, billing y preflight de CLI. Léelo cuando el proveedor sea Google Cloud.
- `devops:terraform`: estructura de módulos y entornos, estado remoto, OIDC de GitHub y plantillas.
- `devops:github-actions`, `devops:docker`, `devops:kubernetes`: pipeline, imágenes y manifiestos.
- `devops:cloud-architect`: diseño y estimación de costos **antes** de implementar.
