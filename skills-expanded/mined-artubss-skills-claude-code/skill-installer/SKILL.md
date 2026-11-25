---
name: skill-installer
description: Instala skills do Codex em $CODEX_HOME/skills a partir de uma lista curada ou um caminho de repositório GitHub. Use quando um usuário solicitar listar skills instaláveis, instalar uma skill curada ou instalar uma skill de outro repositório (incluindo repositórios privados).
metadata:
  short-description: Instala skills curadas do openai/skills ou outros repositórios
---

# Instalador de Skills

Ajuda a instalar skills. Por padrão, estas vêm de https://github.com/openai/skills/tree/main/skills/.curated, mas os usuários também podem fornecer outras localizações.

Use os scripts auxiliares com base na tarefa:
- Liste skills curadas quando o usuário perguntar o que está disponível, ou se o usuário usar esta skill sem especificar o que fazer.
- Instale a partir da lista curada quando o usuário fornecer um nome de skill.
- Instale de outro repositório quando o usuário fornecer um caminho/repositório GitHub (incluindo repositórios privados).

Instale skills com os scripts auxiliares.

## Comunicação

Ao listar skills curadas, produza aproximadamente como segue, dependendo do contexto da solicitação do usuário:
"""
Skills do {repo}:
1. skill-1
2. skill-2 (já instalada)
3. ...
Quais você gostaria de instalar?
"""

Após instalar uma skill, diga ao usuário: "Reinicie o Codex para carregar as novas skills."

## Scripts

Todos estes scripts usam rede, então ao executar na sandbox, solicite escalação ao executá-los.

- `scripts/list-curated-skills.py` (imprime lista curada com anotações de instalação)
- `scripts/list-curated-skills.py --format json`
- `scripts/install-skill-from-github.py --repo <owner>/<repo> --path <path/to/skill> [<path/to/skill> ...]`
- `scripts/install-skill-from-github.py --url https://github.com/<owner>/<repo>/tree/<ref>/<path>`

## Comportamento e Opções

- Padrão para download direto em repositórios públicos do GitHub.
- Se o download falhar com erros de autenticação/permissão, volta para sparse checkout com git.
- Aborta se o diretório de skill de destino já existe.
- Instala em `$CODEX_HOME/skills/<skill-name>` (padrão `~/.codex/skills`).
- Múltiplos valores `--path` instalam múltiplas skills em uma execução, cada uma nomeada a partir do basename do caminho, a menos que `--name` seja fornecido.
- Opções: `--ref <ref>` (padrão `main`), `--dest <path>`, `--method auto|download|git`.

## Notas

- A listagem curada é obtida de `https://github.com/openai/skills/tree/main/skills/.curated` via API do GitHub. Se estiver indisponível, explique o erro e saia.
- Repositórios privados do GitHub podem ser acessados via credenciais git existentes ou `GITHUB_TOKEN`/`GH_TOKEN` opcionais para download.
- Fallback git tenta HTTPS primeiro, depois SSH.
- As skills em https://github.com/openai/skills/tree/main/skills/.system vêm pré-instaladas, então não há necessidade de ajudar usuários a instalá-las. Se perguntarem, apenas explique isso. Se insistirem, você pode baixar e sobrescrever.
- Anotações instaladas vêm de `$CODEX_HOME/skills`.