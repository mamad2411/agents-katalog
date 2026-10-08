Aplica estrictamente:

prompts/audita_skills_dominios_v2_terra.md

Proyecto:
C:/rutinas-local/gen-ai-skills-root/gen-ai-skills

Dominio:
seguridad-opsec

Ruta:
skills/seguridad-opsec

Fecha:
20260910

Estado PRECHECK:
FUNCTIONAL

Ejecuta únicamente la FASE 2B — AUDITORÍA FUNCIONAL.

Usa como evidencia de entrada:

docs/precheck_seguridad-opsec_20260910.md
docs/estado_seguridad-opsec_20260910.md

Audita el contenido real del dominio según:

workflows/workflow_skills_dominio_v1.md

Evalúa estrictamente:

- cobertura funcional;
- responsabilidades y límites entre skills;
- redundancias y solapamientos;
- contradicciones;
- granularidad;
- routing y carga selectiva;
- sobrecarga de instrucciones base;
- utilidad y ubicación del checklist;
- necesidad real de nuevas skills;
- necesidad real de fusiones;
- necesidad real de separar capacidades;
- conveniencia de mantener estructura plana o usar compound skills;
- límites y solapamientos con seguridad-appsec;
- límites y solapamientos con operaciones-tecnologia;
- riesgos de pérdida de conocimiento;
- mantenibilidad, portabilidad y eficiencia contextual.

Presta especial atención a:

- GRC, riesgo y cumplimiento;
- modelado de amenazas, ATT&CK e inteligencia;
- hardening de redes, endpoints y servidores;
- IAM;
- SOC, SIEM y EDR;
- DFIR, respuesta a incidentes y continuidad;
- cloud, contenedores y Kubernetes;
- vulnerabilidades, parchado y EOL;
- seguridad aplicativa/API como frontera con seguridad-appsec;
- terceros, concientización y métricas.

Respeta los principios del proyecto:

- no aplicar "concepto = skill";
- no crear skills para completar una taxonomía;
- no migrar a SKILL.md por uniformidad;
- no usar la arquitectura de geoespacial como estándar obligatorio;
- preferir estructura mínima suficiente;
- preferir carga progresiva:
  README + base + un módulo principal
  + secundarios solo por dependencia concreta
  + checklist solo cuando corresponda;
- no afirmar ahorro de tokens sin medición;
- no eliminar ni compactar contenido sin trazabilidad y validación previa.

Clasifica los hallazgos por prioridad:

P0
P1
P2
P3

Determina explícitamente:

ESTADO_AUDITORIA:
COBERTURA:
SOBRECARGA_BASE:
REDUNDANCIA:
SKILLS_FALTANTES:
FUSIONES_REQUERIDAS:
SEPARACIONES_REQUERIDAS:
ARQUITECTURA:
SUBDIRECTORIOS:
SKILL_MD:
P0:
P1:
P2:
P3:
PLAN_EJECUCION_LUNA:
GATE_TERRA_HIGH:

Si existen cambios necesarios, genera un plan determinista para Luna.

No ejecutes el refactor.
No modifiques archivos dentro de skills/seguridad-opsec/.
No avances automáticamente a la siguiente fase.

Genera o actualiza:

docs/auditoria_seguridad-opsec_20260910.md
docs/estado_seguridad-opsec_20260910.md

En el chat entrega únicamente el resumen de auditoría y la decisión de routing.