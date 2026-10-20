# Vinylmania

## HU desde Jira

- Sitio: `fortizfe.atlassian.net` · Proyecto Jira: `VINYLMANIA` (tickets `VINYLMANIA-XXX`).
- Si el argumento de `/speckit-specify` (o de clarify/plan/tasks) es una clave `VINYLMANIA-XXX`, o una URL de ese Jira,
  lee el ticket con las herramientas MCP `atlassian` (`getJiraIssue` / `searchJiraIssuesUsingJql`) y usa como
  descripción de la feature: summary + description + criterios de aceptación + comentarios relevantes.
  No pidas al usuario que pegue el contenido.
- Sin argumento explícito, no consultes Jira.
- Las HU refinadas siguen viviendo en `.hu/` con las reglas de `.hu/AGENTS.md` (BDD Given-When-Then, constitución).

## Hooks de spec-kit

Configurados en `.specify/extensions.yml` (los hooks obligatorios los ejecuta el agente automáticamente):

- **Commit por fase**: cada `after_*` dispara `speckit.git.commit` (obligatorio). El mensaje sale de
  `auto_commit.<evento>.message` en `.specify/extensions/git/git-config.yml`, en formato conventional commit;
  `{scope}` → número de feature y `{name}` → slug, resueltos desde `.specify/feature.json`.
  Para cambiar el formato de un commit de fase, edita esa config, no el mensaje a mano.
  Los `before_*` siguen desactivados. La PR (`speckit.git.pr`) sigue siendo opcional/manual.
- **Tarjeta de Jira**: `speckit.jira.start` (hook `after_specify`) mueve la tarjeta a *En curso* si el
  argumento de `/speckit-specify` traía una clave/URL `VINYLMANIA-XXX`, y guarda la clave en
  `<feature_dir>/.jira`. `speckit.jira.review` (hook `after_implement`, también vía
  `/speckit-implement-with-agents`) la mueve a *En revisión*. Sin `.jira`, ambos no hacen nada.
