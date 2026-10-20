---
name: entrevistar-usuario
description: "Fecha o gap entre o que o usuário pede e o que quer, com hipótese iterativa e score de confiança, uma pergunta por vez, parando perto de 95 por cento. Use quando o orquestrador ou o tech-lead precisa esclarecer requisitos."
author: "Pedro Andriow (https://github.com/Andriow)"
---

# Skill: entrevistar-usuario

Técnica para fechar o gap entre o que o usuário pede e o que ele realmente quer, usando hipóteses iterativas com uma única pergunta por vez.

**Agente:** `orquestrador`, `tech-lead`  

---

## Quando usar

- Antes de iniciar qualquer planejamento
- Quando a solicitação é ambígua ou tem escopo mal definido
- Quando o usuário usa linguagem vaga ("melhorar", "otimizar", "refazer")

---

## Processo

### Passo 1 — Formular a hipótese inicial
Leia a solicitação do usuário e formule internamente uma hipótese do que ele realmente quer. Atribua um número de confiança de 0 a 100% a essa hipótese. Não inicie nenhuma ação de implementação ou planejamento antes de completar a entrevista.

### Passo 2 — Fazer UMA única pergunta com o palpite embutido
Com base na hipótese, formule uma única pergunta que já contenha o seu melhor palpite. O formato recomendado é: "Imagino que você quer [hipótese] — é isso, ou tem alguma nuance diferente?" Nunca faça múltiplas perguntas ao mesmo tempo. Cada pergunta deve ser direta e específica, não genérica.

### Passo 3 — Atualizar a hipótese com a resposta
A cada resposta do usuário, revise a hipótese e o número de confiança. Identifique o que foi confirmado, o que foi corrigido e o que ainda está em aberto. Se a resposta revelar uma nova dimensão do problema, formule uma nova pergunta para cobrir essa dimensão.

### Passo 4 — Repetir até atingir ~95% de confiança
Continue o ciclo de hipótese → pergunta → atualização até que a confiança na compreensão da intenção real do usuário atinja aproximadamente 95%. Em média, isso ocorre em 2 a 4 rodadas. Se após 5 rodadas a confiança ainda não atingiu 90%, sinalize ao usuário que a solicitação pode precisar de maior clareza estrutural.

### Passo 5 — Entregar a declaração de intenção confirmada
Ao atingir o limiar de confiança, formule e apresente ao usuário a declaração de intenção no formato obrigatório abaixo. Aguarde confirmação explícita antes de passar o resultado para skills downstream.

**Formato obrigatório da declaração de intenção:**
> "Vou [ação concreta] para [objetivo mensurável], excluindo [o que ficou de fora]."

Exemplo: "Vou refatorar o módulo de autenticação para eliminar a duplicação entre os serviços de login e SSO, excluindo mudanças na camada de banco de dados e nos contratos de API públicos."

---

## Racionalizações bloqueadas

| Racionalização | Rebate |
|---|---|
| "A solicitação parece clara, posso começar" | "Parece clara" não é o mesmo que "está clara". O custo de 2 minutos de entrevista é zero; o custo de implementar a coisa errada pode ser dias. |
| "Fazer perguntas irrita o usuário" | Perguntas bem formuladas com palpite embutido mostram que você está engajado — não que está perdido. O que irrita é pergunta genérica sem hipótese. |
| "Vou implementar e o usuário ajusta" | Isso é iterar no escopo errado. Entrevista primeiro, implementa depois. Ajuste incremental só funciona quando a direção geral está correta. |
| "Já entendi o suficiente para começar" | Suficiente para começar não é suficiente para entregar. A entrevista não é sobre entender o pedido — é sobre entender o problema por trás do pedido. |

---

## Anti-padrões bloqueados

- Fazer múltiplas perguntas em uma única mensagem
- Fazer perguntas genéricas sem hipótese embutida ("O que exatamente você quer?")
- Iniciar implementação ou planejamento antes de atingir 95% de confiança
- Assumir que linguagem técnica implica clareza de intenção
- Passar para o próximo passo sem aguardar confirmação explícita da declaração de intenção
- Reformular a mesma pergunta de maneiras diferentes sem avançar a hipótese

---

## Checklist de conclusão

- [ ] Hipótese inicial formulada com número de confiança registrado
- [ ] Cada rodada usou apenas uma pergunta com palpite embutido
- [ ] A confiança atingiu pelo menos 95% antes de encerrar
- [ ] Declaração de intenção está no formato: "Vou [ação concreta] para [objetivo mensurável], excluindo [o que ficou de fora]"
- [ ] Usuário confirmou explicitamente a declaração de intenção
- [ ] Declaração de intenção foi entregue para uso pelos skills downstream
