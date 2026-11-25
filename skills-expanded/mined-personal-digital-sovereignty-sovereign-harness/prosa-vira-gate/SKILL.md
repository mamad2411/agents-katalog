---
name: prosa-vira-gate
description: A doutrina central do método — toda lição que custou trabalho é convertida em mecanismo verificável (gate, hook, estado, teste), nunca deixada só como texto; e como fazer isso sem criar gate hostil ou gate construído sobre diagnóstico errado. Carregar quando um erro se repetir, ao propor um guardrail/hook/gate novo, ao endurecer ou afrouxar um existente, e ao revisar uma skill.
---

# Prosa vira gate — o erro que custou vira mecanismo

"Está escrito no AGENTS.md" não basta. No projeto de origem, na semana em que uma regra de segurança estava escrita e destacada, um `format!()` com SQL e uma rota nova entraram sem que a skill fosse aberta uma vez. A resposta não foi "tome mais cuidado" — foi construir o mecanismo.

O princípio: **o que é verificável por regra/script é automatizado; a prosa fica para o que exige julgamento.** Um invariante em prosa disputa atenção com todo o resto do contexto — e num modelo pequeno é praticamente invisível. Uma condição em código vale igual para qualquer modelo e qualquer humano.

## O ciclo de conversão

1. **Nomeie a classe**, não o caso. "Commit caiu em `main` porque o HEAD foi movido por outra sessão" é caso; "commit em branch protegida" é classe.
2. **Classifique** cada lição numa de três:
   - **mecanizável** → vira gate/hook/estado/teste;
   - **julgamento** → vira skill curta, ancorada nos mecanismos reais, com o caso de origem datado;
   - **rejeitada** → registrada com motivo, para não voltar como "melhoria óbvia".
3. **Refute antes de mecanizar.** Gate construído sobre diagnóstico não testado herda o erro e o impõe a todos com autoridade de ferramenta. Caso de origem: o gate "branch atrás de main reverte trabalho" foi de hipótese a skill, a regra escrita e a gate bloqueante em 8 repositórios em um dia, sem uma tentativa de refutação. A refutação levou quatro minutos. Virou aviso.
4. **Escolha o ponto de aplicação** mais cedo que ainda tem informação suficiente: guard do agente (antes da ação) → pre-commit → pre-push → merge gate (sobre o RESULTADO do merge) → esteira remota (ambiente limpo).
5. **Prove no sentido negativo** antes de propagar: o gate reprova o caso do incidente e libera o caso legítimo vizinho. Casos de origem: um gate novo era chamado antes de ser definido (o `command not found` foi engolido e o push autorizado sem o gate rodar); outro usava `comm` com ordenação de locale incompatível e passava verde com a colisão presente.
6. **Cite a origem** no próprio gate (data, documento) e registre a entrega nos dois registros (PENDING/CONCLUSION).

## Gate que sobrevive ao uso

- **Escape nomeado, nunca silencioso.** `HARNESS_SKIP=<regra>` / `SOVEREIGN_SKIP_GATES=<gate>` aparece no terminal e no registro. Override silencioso (`core.hooksPath=/dev/null`, `--no-verify`) é proibido.
- **Ferramenta ausente bloqueia** (fail-loud) e imprime como instalar. Um gate que vira "skipping" em silêncio é pior que nenhum, porque passa confiança.
- **Não hostil por padrão.** Gate que bloqueia trabalho legítimo é desligado na primeira semana e nunca reavaliado. Opções: nascer desligado com opt-in; nascer como aviso; escopar ao diff (dívida antiga não vira bloqueio retroativo).
- **Radar quando a sintaxe não decide.** Casamento sintático produz falso positivo por construção (todo `Command::new` é suspeito, quase nenhum é bug): aponte a seção da skill relevante e deixe a decisão com quem escreveu. Bloqueio só como modo consciente de auditoria.
- **Avalie o que está sendo enviado**, não a árvore inteira nem a branch em checkout (casos de origem: formatador checando o crate todo; gate rodando numa deleção de ref sobre a working tree errada).
- **Determinismo.** `echo | grep -q` com SIGPIPE tornou um radar não determinístico (3, 3 e 2 achados em três execuções idênticas). Radar que às vezes omite é pior que nenhum.
- **Meça antes de endurecer.** Registre bloqueios e escapes (sem dado sensível) e decida pelo número de falsos positivos, não pela impressão.

## Onde parar

Um gate cobre o caminho que conhece, não o julgamento. Horas depois de escrever o guardrail contra uma classe, a mesma sessão cometeu a classe por outro caminho (`cp` sobrescrevendo versão nova pela antiga). Por isso skill e gate convivem: o gate pega o mecânico, a skill treina o olhar para o resto — e o próximo incidente vira o próximo gate.
