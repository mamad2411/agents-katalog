---
name: "security-best-practices"
description: "Realize análises de segurança específicas de linguagem e framework e sugira melhorias. Ative apenas quando o usuário solicitar explicitamente orientação sobre segurança, uma análise/relatório de segurança ou ajuda com codificação segura por padrão. Ative apenas para linguagens suportadas (python, javascript/typescript, go). Não ative para análise geral de código, depuração ou tarefas não relacionadas a segurança."
author: openai
---

# Segurança — Melhores Práticas

## Visão Geral

Esta skill fornece uma descrição de como identificar as linguagens e frameworks usadas pelo contexto atual e, em seguida, carregar informações do diretório de referências da skill sobre as melhores práticas de segurança para essa linguagem e/ou frameworks.

Essas informações, se presentes, podem ser usadas para escrever código novo seguro por padrão, para detectar passivamente problemas graves em código existente ou (se solicitado pelo usuário) fornecer um relatório de vulnerabilidades e sugerir correções.

## Fluxo de Trabalho

O primeiro passo para esta skill é identificar TODAS as linguagens e TODOS os frameworks que você está sendo solicitado a usar ou que já existem no escopo do projeto em que está trabalhando. Concentre-se nos frameworks principais. Muitas vezes você precisará identificar tanto linguagens e frameworks frontend quanto backend.

Em seguida, verifique o diretório de referências da skill para ver se há documentação relevante para a linguagem e/ou frameworks. Certifique-se de ler TODOS os arquivos de referência relacionados ao framework ou linguagem específica. O formato dos nomes de arquivo é `<language>-<framework>-<stack>-security.md`. Você também deve verificar se existe um `<language>-general-<stack>-security.md` que seja agnóstico ao framework que você pode estar usando.

Se estiver trabalhando em uma aplicação web que inclua frontend e backend, certifique-se de ter verificado documentos de referência para AMBOS frontend e backend!

Se você for solicitado a fazer uma web app que incluirá tanto frontend quanto backend, mas o framework frontend não for especificado, verifique também `javascript-general-web-frontend-security.md`. É importante que você entenda como proteger tanto o frontend quanto o backend.

Se nenhuma informação relevante estiver disponível no diretório de referências da skill, pense um pouco sobre o que você sabe sobre a linguagem, o framework e todas as melhores práticas de segurança bem conhecidas para ele. Se não tiver certeza, você pode tentar procurar online por documentação sobre melhores práticas de segurança.

A partir daí, ele pode funcionar de algumas maneiras.

1. O modo primário é simplesmente usar as informações para escrever código seguro por padrão a partir deste ponto. Isso é útil para iniciar um novo projeto ou ao escrever novo código.

2. O modo secundário é detectar passivamente vulnerabilidades enquanto trabalha no projeto e escreve código para o usuário. Vulnerabilidades críticas ou muito importantes ou problemas graves que vão contra a orientação de segurança podem ser sinalizados e o usuário pode ser informado. Este modo passivo deve se concentrar nas vulnerabilidades de maior impacto e padrões seguros.

3. O usuário pode solicitar um relatório de segurança ou melhorar a segurança da base de código. Neste caso, um relatório completo deve ser produzido descrevendo de quais maneiras o projeto falha em seguir a orientação de melhores práticas de segurança. O relatório deve ser priorizado e ter seções claras de severidade e urgência. Em seguida, ofereça-se para começar a trabalhar nas correções para esses problemas. Veja #fixes abaixo.

## Árvore de Decisão do Fluxo de Trabalho

- Se a linguagem/framework estiver pouco clara, inspecione o repositório para determiná-la e liste suas evidências.
- Se a orientação correspondente existir em `references/`, carregue apenas os arquivos relevantes e siga suas instruções.
- Se nenhuma orientação correspondente existir, considere se você conhece alguma melhores práticas de segurança bem conhecidas para a linguagem e/ou frameworks escolhida, mas se solicitado a gerar um relatório, deixe o usuário saber que orientações concretas não estão disponíveis (você ainda pode gerar o relatório ou detectar com certeza vulnerabilidades críticas)

# Substituições

Embora essas referências contenham as melhores práticas de segurança para linguagens e frameworks, os clientes podem ter casos em que precisam contornar ou substituir essas práticas. Preste atenção em regras específicas e instruções na documentação do projeto e arquivos de prompt que podem exigir que você substitua certas melhores práticas. Ao substituir uma melhor prática, VOCÊ PODE relatá-la ao usuário, mas não discuta com ele. Se uma melhor prática de segurança precisa ser contornada/ignorada por alguma razão específica do projeto, você também pode sugerir adicionar documentação sobre isso ao projeto para deixar claro por que a melhor prática não está sendo seguida e para seguir esse contorno no futuro.

# Formato do Relatório

Ao produzir um relatório, você deve escrever o relatório como um arquivo markdown em `security_best_practices_report.md` ou outro local se fornecido pelo usuário. Você pode perguntar ao usuário onde gostaria que o relatório fosse escrito.

O relatório deve ter um breve sumário executivo no topo.

O relatório deve ser claramente dividido em várias seções baseadas na severidade da vulnerabilidade. O relatório deve se concentrar nos achados mais críticos, pois estes têm o maior impacto para o usuário. Todos os achados devem ser anotados com um ID numérico para facilitar a referência.

Para achados críticos, inclua uma declaração de impacto de uma sentença.

Após escrever o relatório, relate também ao usuário diretamente, embora você possa ser menos detalhado. Você pode oferecer-se para explicar qualquer um dos achados ou as razões por trás da orientação de melhores práticas de segurança, se o usuário quiser mais informações sobre qualquer um dos achados.

Importante: Ao referenciar código no relatório, certifique-se de encontrar e incluir números de linha para o código que está referenciando.

Após escrever o arquivo de relatório, resuma os achados para o usuário.

Também diga ao usuário onde o relatório final foi escrito.

# Correções

Se você produziu um relatório, deixe o usuário ler o relatório e peça para começar a realizar correções.

Se você encontrou passivamente um achado crítico, notifique o usuário e pergunte se ele gostaria que você corrigisse esse achado.

Ao produzir correções, concentre-se em corrigir um achado por vez. As correções devem ter comentários concisos e claros explicando que o novo código é baseado na melhor prática de segurança específica e, talvez, uma razão muito breve sobre por que seria perigoso não fazê-lo desta forma.

Sempre considere se as alterações que você deseja fazer impactarão a funcionalidade do código do usuário. Considere se as alterações podem causar regressões na forma como o projeto funciona atualmente. Frequentemente é o caso que código inseguro é confiável por outras razões (e esta é a razão pela qual código inseguro persiste por tanto tempo). Evite quebrar o projeto do usuário, pois isso pode fazer com que ele não queira aplicar correções de segurança no futuro. É melhor escrever uma correção bem pensada e bem informada pelo resto do projeto, do que uma mudança rápida e improvisada.

Sempre siga qualquer fluxo normal de alteração ou commit que o usuário tenha configurado. Se fizer commits git, forneça mensagens de commit claras explicando que isso é para alinhar-se com melhores práticas de segurança. Tente evitar agrupar vários achados não relacionados em um único commit.

Sempre siga qualquer fluxo de teste normal que o usuário tenha configurado (se houver) para confirmar que suas alterações não estão introduzindo regressões. Considere os impactos de segunda ordem que as alterações podem ter e informe o usuário antes de fazê-las se houver algum.

# Orientação Geral de Segurança

Abaixo estão alguns conselhos de codificação segura que se aplicam a quase qualquer linguagem ou framework.

### Evite Usar IDs Incrementais para IDs Públicos de Recursos

Ao atribuir um ID para algum recurso, que será então exposto à internet, evite usar pequenos IDs auto-incrementais. Use UUID4 mais longo ou string hex aleatória. Isso impedirá que usuários aprendam a quantidade de um recurso e consigam adivinhar IDs de recursos.

### Uma observação sobre TLS

Embora TLS seja importante para implantações de produção, a maioria do trabalho de desenvolvimento será com TLS desativado ou fornecido por algum proxy TLS fora do escopo. Por isso, tenha muito cuidado para não relatar a falta de TLS como um problema de segurança. Também tenha muito cuidado com o uso de cookies "secure". Eles devem ser definidos apenas se a aplicação estiver realmente sobre TLS. Se forem definidos em aplicações não-TLS (como ao serem implantadas para dev local ou testes), isso quebrará a aplicação. Você pode fornecer uma env ou outro sinalizador para substituir a configuração de secure para mantê-lo desativado até estar em uma implantação de produção TLS. Além disso, evite recomendar HSTS. Não é recomendado usar sem compreensão total dos impactos duradouros (pode causar grandes interrupções e bloqueio de usuários) e geralmente não é recomendado para o escopo de projetos sendo revisados por codex.