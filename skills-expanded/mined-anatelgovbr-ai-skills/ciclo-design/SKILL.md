---
name: ciclo-design
description: Recebe um objetivo e uma referência real, identifica o que torna essa referência boa e executa um construtor com três críticos independentes até que todos aprovem o resultado ou o limite de rodadas seja atingido. Acione com "ciclo de design" ou quando o pedido for comparar um resultado com uma referência concreta.
---

# Ciclo de Design

Quatro fases, na ordem: entrevista, pré-verificação, desmontagem e ciclo. A construção começa na fase 4.

## Fase 1: Entrevista

Faça exatamente estas cinco perguntas juntas e depois pare e espere.

1. **O que você está construindo e qual será o tamanho ou duração?**

2. **Diga algo que já faça isso muito bem.** Pode ser um site, vídeo, documento, carrossel ou qualquer referência que eu consiga abrir. Se não tiver nenhuma, diga "pular".

3. **Existem arquivos que devo utilizar?** Sistema de design, guia de marca, roteiro, versão existente etc.

4. **Quais modelos você quer utilizar em cada agente?**

   Apresente sempre uma recomendação inicial:

   - **Construtor → Sonnet ou modelo equilibrado:** responsável por criar e corrigir. Normalmente oferece o melhor equilíbrio entre capacidade, velocidade e custo.
   - **Crítico do Briefing → Sonnet ou modelo equilibrado:** precisa interpretar corretamente o pedido e verificar se todos os requisitos foram cumpridos.
   - **Crítico do Sistema → Haiku ou modelo leve:** verifica regras mais objetivas, como cores, fontes, componentes e aderência ao sistema de design.
   - **Crítico Visual → modelo mais forte disponível:** realiza o julgamento mais subjetivo e exigente, comparando visualmente nosso resultado com a referência.

   Explique que modelos mais leves normalmente significam **mais velocidade e menor custo**, mas também podem reduzir a capacidade de análise e a qualidade final. Modelos mais fortes priorizam **performance e qualidade**, porém tendem a ser mais lentos e caros.

   Ofereça estas opções:

   - **Qualidade máxima:** use modelos mais fortes onde houver ganho relevante.
   - **Custo-benefício:** Construtor e Briefing equilibrados, Sistema leve e Crítico Visual forte.
   - **Rápido e econômico:** modelos mais leves sempre que isso não comprometer excessivamente a função.
   - **Personalizado:** o usuário escolhe individualmente o modelo de cada agente.

   Mantenha o modelo à altura da função mesmo quando o usuário quer economizar, e avise quando a escolha puder comprometer o resultado, especialmente no Crítico Visual.

5. **Qual é o número máximo de rodadas que o ciclo pode executar?**

   Explique que o método original não utiliza um número fixo: o ciclo continua até todos os críticos aprovarem ou o usuário interromper.

   O limite definido aqui funciona como uma proteção de custo e tempo, não como critério de aprovação.

   Se o limite for atingido e algum crítico ainda reprovar, pare e mostre:
   - quais críticos ainda reprovaram;
   - qual é a principal lacuna atual;
   - quantas rodadas foram executadas;
   - e pergunte se o usuário deseja continuar.

Se a referência for vaga ("site da Apple", "um SaaS bonito"), peça uma vez uma página, arquivo ou peça específica. Com referência vaga o crítico inventa o próprio padrão e aprova fácil, e é uma das principais razões para o método falhar.

Se o usuário responder "pular" na pergunta 2, proponha três possíveis referências, explicando em uma linha por que cada uma seria adequada, e espere. Se ele não escolher, utilize a mais exigente.

Depois das respostas, confirme em um único bloco:

- objetivo;
- referência;
- arquivos;
- modelo do Construtor;
- modelo do Crítico do Briefing;
- modelo do Crítico do Sistema;
- modelo do Crítico Visual;
- máximo de rodadas.

Só então continue.

## Fase 2: Pré-verificação

Uma checagem, não uma pergunta. Execute antes de qualquer trabalho e apresente tudo em um único bloco.

- Acesse a referência agora. Capture a página ou leia o arquivo. Se estiver bloqueado ou ausente, informe e peça outra.
- Confirme que será possível renderizar nosso resultado: screenshots para sites, sequência de frames para animações, PDF renderizado para documentos. Sem renderização, o Crítico Visual fica cego.
- Identifique ferramentas necessárias para o objetivo, como geração de imagem, vídeo ou voz, e confirme que estão disponíveis.
- Confirme que os arquivos necessários existem: `sistema-de-design.md`, guia de marca, roteiro etc.

Depois informe: o que está funcionando, o que está faltando e **qual crítico fica prejudicado** caso alguma coisa esteja ausente.

Um crítico só entra no ciclo enxergando aquilo que deve avaliar. Se algum ficar cego, diga isso antes de continuar.

## Fase 3: Desmontagem

Analise cuidadosamente a referência e escreva de 5 a 7 mecanismos em:

`criterios-de-qualidade.md`

Use mecanismos, que são o que um crítico consegue conferir olhando o resultado. "Tem aparência premium" é adjetivo e não serve.

Exemplos úteis:

- título tem cerca de 5x o tamanho do corpo; apenas três tamanhos tipográficos
- uma única cor de destaque, usada no máximo duas vezes por tela
- movimentos sempre terminam na mesma direção
- nenhuma animação dura menos de 400ms
- espaço vazio ocupa pelo menos 40% da primeira tela


Mostre `criterios-de-qualidade.md` ao usuário antes de continuar.

## Fase 4: Ciclo

Divida o objetivo nas menores peças que possam ser melhoradas e avaliadas individualmente. Você escolhe as peças. Mantenha normalmente três ou quatro, porque cada peça adicional multiplica as execuções.

Para cada peça: execute um **Construtor** e depois três críticos independentes, cada um com contexto novo e sem conhecimento de como o Construtor trabalhou.

Utilize os modelos definidos na entrevista.

- **Crítico do Briefing** avalia apenas o objetivo declarado. Fez aquilo que foi pedido? Ignore estética.
- **Crítico do Sistema** avalia apenas `sistema-de-design.md`. Verifique aderência objetiva.
- **Crítico Visual** avalia apenas `criterios-de-qualidade.md` e o resultado renderizado. Coloque nosso resultado ao lado da referência, sem identificação, escolha qual está melhor e indique a única maior diferença.

Escreva o briefing de cada crítico para o objetivo atual, do zero a cada projeto.

Regras:

- Críticos devem ser rigorosos e apontar o que está pior que a referência.
- Críticos avaliam o resultado renderizado. Ler a implementação faz o crítico avaliar intenção em vez de resultado.
- Use veredictos binários: **APROVADO** ou **REPROVADO**.
- Os três precisam aprovar.
- Qualquer reprovação volta para o Construtor com a principal lacuna identificada.
- Continue até todos aprovarem, o usuário interromper ou o limite de rodadas definido na entrevista ser atingido.
- Atingir o limite de rodadas nunca transforma uma reprovação em aprovação.

Mantenha uma página de progresso atualizada com: status das peças, resultado de cada crítico, histórico das principais lacunas e número de rodadas.

## Custo

O consumo real de tokens durante a execução não é estimável de forma confiável, então o controle é o número máximo de rodadas definido na entrevista.

Mostre o número de rodadas e peças concluídas.

Se o limite for atingido antes da aprovação completa, pause e deixe o usuário decidir se deseja continuar.

## O que faz este método falhar

- Uma referência vaga.
- O Construtor julgando o próprio trabalho.
- Críticos com contexto contaminado pelo processo de construção.
- Um crítico pouco rigoroso.
- Usar notas em vez de aprovação/reprovação.
- Tratar o limite de rodadas como aprovação automática.
- Usar um modelo fraco em uma função crítica sem considerar o impacto.
- Excesso de instruções que elimina a capacidade do modelo de tomar boas decisões.