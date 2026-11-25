---
name: quanto
description: Raio-x do contexto, mede quanto o setup do Claude Code consome antes da primeira palavra e mostra o que cortar. Gatilhos, /quanto, raio-x de contexto, o que está enchendo minha janela, meu setup está pesado. Só diagnostica, nunca altera o setup.
---

# Quanto (raio-x de contexto)

Todo turno da conversa reenvia o mesmo bloco fixo: CLAUDE.md, a lista de skills instaladas, o texto que os hooks injetam, as definições de subagentes e os schemas de MCP. Você paga isso em toda mensagem, não uma vez por sessão. Esta skill mede esse bloco e diz onde cortar.

Diagnóstico apenas. Não altere nada sem o usuário pedir.

## Como rodar

```bash
python3 ~/.claude/skills/quanto/scripts/raio_x.py
```

Opções:

| Flag | Para quê |
|---|---|
| `--janela 1000000` | Ajusta a janela do modelo em uso. O padrão é 200000. |
| `--medir-hooks` | Executa os hooks de SessionStart e UserPromptSubmit para medir o que injetam. Sem isso eles ficam indeterminados. |
| `--top 15` | Tamanho do ranking dos itens mais caros. |
| `--json` | Saída estruturada, para comparar antes e depois. |
| `--cwd CAMINHO` | Mede o setup de outro projeto. |

Comece sem `--medir-hooks`. Ofereça a flag depois, explicando que ela executa os hooks de verdade e que hooks podem ter efeito colateral. Só rode com o aval do usuário.

## Como apresentar o resultado

Mostre a saída do script como veio, ela já está formatada. Depois acrescente no máximo três frases: qual bloco domina, qual item isolado é o mais caro, e qual o corte de maior retorno.

Não repita a tabela em prosa. Não invente percentual de economia que o script não mediu.

## Como interpretar

**Skills (listagem).** Cada skill instalada paga nome mais description em todo turno, mesmo sem nunca ser usada. O corpo do SKILL.md só entra quando a skill é invocada. Description acima de 90 tokens quase sempre é description escrita como documentação, não como gatilho. Desinstalar skill que não se usa é o corte mais limpo.

**CLAUDE.md e imports.** Segue os `@arquivo`. Serve para regra permanente, que vale em toda mensagem. Procedimento que só importa às vezes custa menos como skill.

**Hooks.** Só SessionStart e UserPromptSubmit injetam texto no contexto. Os demais eventos não custam contexto. Um hook de UserPromptSubmit é o pior caso, porque reinjeta a cada mensagem.

**MCP.** Fica como indeterminado de propósito, porque o custo real depende de quantas tools o servidor expõe e de estarem diferidas ou não. Quando as tools são carregadas sob demanda, sobra só o nome no contexto. Servidor conectado e nunca usado é candidato natural a desligar.

**Agents.** As descriptions dos subagentes em `.claude/agents/` entram junto com a ferramenta Agent.

## Honestidade da medição

A contagem usa `tiktoken` quando disponível, com margem declarada de dez por cento, e cai para estimativa por caracteres quando não há. Nenhum dos dois é o tokenizador da Anthropic, então trate o número como ordem de grandeza confiável, não como fatura.

O script mede o custo fixo do setup. Ele não mede o que a conversa em si consome, nem o resultado de ferramentas, que costuma ser a maior fatia numa sessão longa.

Se for divulgar o número, meça antes e depois com `--json` no mesmo projeto e na mesma máquina.
