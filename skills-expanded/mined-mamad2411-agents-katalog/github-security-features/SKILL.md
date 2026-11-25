---
name: github-security-features
description: Gate de seguridad de la plataforma GitHub para repos con datos sensibles — Dependabot (alerts, security updates, version updates y `dependabot.yml`), secret scanning con push protection, code scanning/CodeQL, dependency review en PRs, SECURITY.md y canal privado de reporte, auditoría de accesos de equipos y colaboradores, tokens fine-grained vs clásicos, GitHub Apps y deploy keys. Usar al crear un repo, al auditar la postura de seguridad de uno existente, al emitir o rotar un token, al dar acceso a una persona o bot, o cuando aparece una alerta de secreto o de dependencia.
allowed-tools: Read Grep Glob Bash
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Seguridad de la plataforma GitHub

Los repos de la casa contienen código que maneja datos de salud. Un repo mal configurado filtra
por tres vías: **secretos commiteados**, **dependencias vulnerables** y **accesos de más**.
Esta skill audita la plataforma; la seguridad del código vive en `security-guardrails`, la del
pipeline en `github-actions-ci` §5, la de los datos en `data-privacy-sensitive`.

## 1. Mapa de features y disponibilidad

Verificado en docs.github.com. La disponibilidad cambia con los planes: confirmá la tuya antes
de prometer una feature en un repo **privado**.

| Feature | Qué hace | Disponibilidad |
|---|---|---|
| Dependency graph | Inventario de dependencias y dependientes | Todos los planes |
| Dependabot alerts | Avisa dependencias con vulnerabilidades conocidas | Todos los planes |
| Dependabot security updates | PRs automáticos que corrigen dependencias vulnerables | Todos los planes |
| Dependabot version updates | PRs para mantener dependencias al día | Todos los planes |
| SBOM | Exporta el grafo en formato compatible con SPDX | Todos los planes |
| Security policy (`SECURITY.md`) | Dice cómo reportar una vulnerabilidad | Todos los planes |
| Secret scanning alerts | Detecta credenciales ya commiteadas | Gratis en públicos; en privados requiere **GitHub Secret Protection** |
| Push protection | **Bloquea** el push que contiene un secreto | Ídem |
| Code scanning / CodeQL | Análisis estático de vulnerabilidades | Gratis en públicos; en privados requiere **GitHub Code Security** |
| Dependency review | Muestra el impacto de cambios de dependencias antes de mergear | Ídem |
| Private vulnerability reporting | Formulario privado para investigadores | Solo repos **públicos** |

Si el plan no cubre secret scanning o code scanning en privados, **no quedás eximido**: corré
un escáner de secretos y SAST equivalentes en CI (`static-analysis-linting`, `security-guardrails`).

## 2. Dependabot

`.github/dependabot.yml` — `version: 2` siempre. Un bloque por ecosistema y directorio.

```yaml
version: 2
updates:
  - package-ecosystem: "npm"            # cubre proyectos npm y Yarn
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    groups:
      dev-minor-patch:
        dependency-type: "development"
        update-types: ["minor", "patch"]
    commit-message:
      prefix: "chore(deps)"
    labels: ["tipo:deps"]
    cooldown:
      default-days: 7
  - package-ecosystem: "pip"
    directory: "/"
    schedule: { interval: "weekly" }
  - package-ecosystem: "pub"            # Dart / Flutter
    directory: "/"
    schedule: { interval: "weekly" }
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule: { interval: "weekly" }
  - package-ecosystem: "docker"
    directory: "/"
    schedule: { interval: "weekly" }
```

- Claves útiles: `directories` (varios paths, admite `*`), `groups` (`patterns`,
  `dependency-type`, `update-types`), `ignore` (`dependency-name`, `versions`), `allow`,
  `target-branch`, `registries`, `versioning-strategy`, `cooldown` (`default-days`,
  `semver-major-days`, `semver-minor-days`, `semver-patch-days`).
- `schedule.interval`: `daily`, `weekly`, `monthly`, `quarterly`, `semiannually`, `yearly`, `cron`.
- `target-branch`: apuntá a la rama de **integración** si no es la default. Ojo: al usarla, la
  configuración de ese bloque deja de aplicar a las security updates; verificar el detalle en la doc oficial.
- **`cooldown`** retrasa la adopción de versiones recién publicadas: reduce exposición a paquetes
  comprometidos que se detectan en los primeros días.
- **Agrupá** minor/patch de desarrollo; los **major** y todo lo de producción, de a uno, con
  lectura del changelog (`dependency-management`).
- Actions pinneadas por SHA: confirmá en la doc cómo las trata Dependabot antes de confiar en
  que el bump llega solo.
- Un PR de Dependabot pasa por los **mismos gates** que uno humano. Auto-merge solo para
  patch de desarrollo con CI completo y verde.
- Alertas: SLA por severidad definido en el CLAUDE.md del proyecto. "Descartar" una alerta
  exige motivo escrito (no explotable / sin fix / riesgo aceptado por quién).

## 3. Secret scanning y push protection

1. Activá **ambos**. Detectar después sirve; **bloquear antes** evita la rotación.
   `gh repo edit --enable-secret-scanning --enable-secret-scanning-push-protection`
   (push protection requiere secret scanning activo primero).
2. Un secreto que llegó al remoto está **comprometido**, aunque borres el commit o reescribas la
   historia: forks, clones y cachés ya lo tienen.
   Orden: **revocar/rotar → verificar uso indebido en el proveedor → limpiar → postmortem**.
   Nunca al revés (`incident-response-postmortem`).
3. Saltear push protection ("es un falso positivo", "es de test") deja registro: exige motivo
   real. Los secretos de test también se rotan si tienen forma de credencial válida.
4. Prevención local: `.gitignore` para `.env*`, hooks de pre-commit con escáner de secretos,
   plantillas `.env.example` sin valores (`environment-secrets-config`).
5. Un secreto **no** es solo una API key: connection strings, claves privadas, tokens de sesión,
   dumps de base y capturas con datos de pacientes también son fuga.

## 4. Code scanning y dependency review

- **CodeQL**: "default setup" desde Settings es el camino corto; "advanced setup" (workflow
  propio) cuando necesitás controlar build, lenguajes o queries. El job que sube resultados
  necesita `security-events: write`. Configuración exacta del workflow: verificar en la doc oficial.
- Regla de ruleset "Require code scanning results" para que una alerta nueva de severidad alta
  **bloquee** el merge (`github-branch-protection-rulesets`).
- **Dependency review** en PRs:

```yaml
name: dependency-review
on: [pull_request]
permissions:
  contents: read
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha-completo>
      - uses: actions/dependency-review-action@<sha-completo>
        with:
          fail-on-severity: high
```

  Entradas: `fail-on-severity` (`critical|high|moderate|low`), `allow-licenses` /
  `deny-licenses` (SPDX), `allow-ghsas`, `fail-on-scopes`.
- Falsos positivos de SAST: se descartan **con motivo**, no se apaga la query.

## 5. Política y reporte privado

- `SECURITY.md` en todo repo (o por defecto desde el repo `.github` de la organización:
  `github-repo-standards`): versiones soportadas, **canal privado** de reporte, tiempo de
  respuesta, qué no hacer (no abrir un issue público).
- "Private vulnerability reporting" es solo para repos **públicos**. En repos privados el canal
  es un buzón de seguridad monitoreado. Definilo en el CLAUDE.md del proyecto.
- Una vulnerabilidad **nunca** se discute en un issue o PR público antes del fix. Para repos
  públicos, los security advisories permiten trabajar el fix en privado.
- Si el incidente pudo exponer datos personales o de salud: escalar al responsable legal y de
  privacidad. Los plazos y obligaciones de notificación **no** los decide ingeniería
  (`regulatory-compliance-mapping`).

## 6. Accesos

1. **Mínimo privilegio por equipo, no por persona.** Roles del repo: read, triage, write,
   maintain, admin. Admin: los menos posibles.
2. **Colaboradores externos**: acceso por repo, con fecha de revisión. Al terminar el contrato,
   se quita **ese día**.
3. 2FA obligatorio a nivel organización. SSO si el plan lo permite.
4. Auditoría trimestral: quién tiene acceso y por qué; apps y tokens instalados; deploy keys;
   webhooks (¿a qué URL mandan eventos del repo?); secrets de Actions sin uso.
5. Offboarding: quitar de la organización, revocar tokens y claves SSH autorizados, rotar
   secretos compartidos que la persona conocía.

## 7. Tokens y credenciales de máquina

| Necesidad | Usá | Evitá |
|---|---|---|
| Un workflow toca su propio repo | `GITHUB_TOKEN` con `permissions` mínimos | PAT en secrets |
| Automatización duradera / entre repos | **GitHub App** (permisos finos, tokens cortos, no atada a una persona) | PAT de un empleado |
| Un servidor clona **un** repo | **Deploy key** de solo lectura | Clave SSH personal |
| Persona desde CLI o script | **Fine-grained PAT**: un solo dueño de recursos, repos específicos, permisos granulares, con vencimiento | PAT clásico con scope `repo` |
| Nube desde Actions | OIDC | Claves de larga vida en secrets |

- Fine-grained PAT: la organización puede **exigir aprobación**. Limitaciones documentadas: no
  acceden a varias organizaciones a la vez, ni a Packages, ni a la Checks API, ni a repos donde
  sos colaborador externo; para esos casos, GitHub App o, como último recurso, PAT clásico acotado.
- **Todo token con vencimiento.** Inventario: dueño, propósito, permisos, fecha de expiración.
- Deploy key con escritura: solo si es imprescindible, documentada, y una por repo (no reutilizar).
- Un token **jamás** va en el código, en un issue, en un log de CI ni en el prompt de un agente.
- Agentes: operan con el token de menor alcance que sirva; no crean ni amplían tokens.

## Anti-patrones

- Alertas de Dependabot con meses de antigüedad "porque son de dev".
- Borrar el commit con el secreto y no rotar.
- Un PAT clásico `repo` de una persona sosteniendo el CI de cinco repos.
- Deploy key con escritura reutilizada en varios servidores.
- Ex-colaboradores con acceso vigente.
- Apagar push protection porque "molesta".
- Descartar alertas en masa sin motivo.

## Evidencia / DoD

Para afirmar "el repo cumple la postura de seguridad", pegá salida literal de (en PowerShell,
los `{owner}` `{repo}` entre comillas):

```bash
gh api repos/{owner}/{repo} --jq '.security_and_analysis'
gh api repos/{owner}/{repo}/dependabot/alerts --paginate --jq '[.[] | select(.state=="open")] | length'
gh api repos/{owner}/{repo}/secret-scanning/alerts --paginate --jq '[.[] | select(.state=="open")] | length'
gh api repos/{owner}/{repo}/collaborators --paginate --jq '.[] | {login, role_name}'
gh api repos/{owner}/{repo}/keys --jq '.[] | {title, read_only, created_at}'
```

Más: contenido de `.github/dependabot.yml`, existencia de `SECURITY.md`, y el inventario de
tokens/apps con vencimientos. Un endpoint que devuelve 403/404 por plan o permisos se reporta
**BLOCKED**, no se asume "sin alertas" (`evidence-and-verification`).

## Checklist

- [ ] Dependency graph, Dependabot alerts y security updates activos.
- [ ] `dependabot.yml` cubre todos los ecosistemas del repo, incluido `github-actions`.
- [ ] Secret scanning + push protection activos (o escáner equivalente en CI si el plan no cubre).
- [ ] Code scanning o SAST equivalente; alerta alta bloquea el merge.
- [ ] Dependency review en PRs con `fail-on-severity`.
- [ ] `SECURITY.md` con canal privado real y monitoreado.
- [ ] Accesos por equipo, mínimo privilegio, 2FA, externos con fecha de revisión.
- [ ] Sin PAT clásicos sosteniendo automatizaciones; tokens con vencimiento e inventario.
- [ ] Deploy keys de solo lectura, una por repo.
- [ ] Cero alertas críticas/altas abiertas fuera de SLA; descartes con motivo.
- [ ] Evidencia literal pegada.
