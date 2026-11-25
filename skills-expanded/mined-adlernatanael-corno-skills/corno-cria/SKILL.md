---
name: corno-cria-skill
description: Cria uma skill nova do Corno ou dá o acabamento numa existente, no padrão do repositório - nome, descrição com gatilhos, estrutura curta com referências, voz em português direto, scripts testados e texto 100% próprio. Valida com o checador do repo e confere que ela aparece no site. Use quando pedirem "cria uma skill", "nova skill do corno", "transforma isso em skill", "dá um acabamento nessa skill" ou "revisa as skills".
---

# Corno cria skill

Uma skill boa é curta, dispara na hora certa e muda o que o agente faz. O resto é enfeite.

## Antes de escrever

1. **Qual comportamento muda?** Escreva em uma frase o que o agente faz diferente com a skill. Se não muda nada que ele já faria sozinho, não precisa de skill.
2. **Quando dispara?** Liste 4 a 6 frases que alguém diria pedindo isso, em português e, se fizer sentido, em inglês. Elas vão para a descrição.
3. **Já existe?** Procure em `skills/` algo que cubra o mesmo assunto. Melhorar a existente vence criar outra.

## Formato

```
skills/corno-<nome>/
  SKILL.md            # obrigatório, de preferência até ~80 linhas
  references/*.md     # detalhe que só é lido quando precisa
  scripts/*           # o que dá para rodar em vez de explicar
```

- Pasta e `name` iguais, sempre com prefixo `corno-`, em minúsculas e com hífen.
- `description` em uma linha: o que faz + "Use quando…" com as frases de gatilho. É a única parte que o agente lê antes de decidir usar, então os gatilhos importam mais que o estilo.
- `disable-model-invocation: true` só para skill que deve rodar apenas quando chamada pelo nome (revisão pesada, coisa destrutiva).
- O corpo responde, nesta ordem e só o que se aplica: a regra central em uma linha, o fluxo em passos numerados, **Quando não usar** (onde a skill atrapalha), o formato da entrega e **Pronto quando** (o que precisa estar provado para dizer que terminou).
- `SKILL.md` diz o fluxo e as regras; tabela grande, lista longa de caminhos e receita com número vão para `references/`, citadas pelo caminho relativo no ponto do fluxo em que são usadas.

## Voz

- Português do Brasil, frase curta, verbo no imperativo ("Rode", "Pergunte", "Não apague").
- Cada regra com o porquê em meia frase quando não for óbvio. Regra sem motivo vira ritual.
- Sem enchimento, sem "é importante notar", sem travessão como vírgula, sem emoji.
- Humor do Corno cabe no nome e no título, não nas instruções: instrução precisa ser inequívoca.

## Texto próprio

Todo texto do repositório é escrito por nós. Pode estudar qualquer material para entender o assunto, mas escreva do zero, com estrutura e exemplos seus. Não copie nem traduza trechos de skills, docs ou posts de terceiros, e não cite autores ou projetos de outras pessoas como fonte. Ferramenta que a skill manda instalar ou usar (um CLI, uma biblioteca) pode ser nomeada normalmente.

## Scripts

- Só leitura por padrão; o que apaga ou altera pede confirmação na própria skill.
- Rode em todos os sistemas que a skill promete (macOS, Linux, Windows) ou diga na skill onde não foi testado.
- Comentário no topo com uso e o que o script nunca faz.

## Antes de dizer que terminou

1. `node scripts/check-skills.mjs` passa sem erro.
2. `claude plugin validate .` passa.
3. A skill aparece no site: `cd site && npm run build` e procure a página `skills/<nome>/` no `dist`.
4. Teste de verdade: numa conversa nova, diga uma das frases de gatilho e confira que a skill foi usada e que o comportamento mudou.
5. Atualize a tabela de skills no `README.md`.
