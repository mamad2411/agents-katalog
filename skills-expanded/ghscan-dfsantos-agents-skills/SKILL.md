---
name: clean-code-java
description: Aplica os princípios de Clean Code (Robert C. Martin) adotados na biblioteca pessoal do usuário para geração, revisão e refatoração de código Java, com exemplos concretos de antes/depois em cada princípio. Use sempre que for gerar, revisar ou refatorar código Java — não apenas quando solicitado explicitamente sobre "clean code". Contém as convenções específicas do usuário (nomenclatura, tamanho de função, tratamento de erro, testes), não apenas os princípios genéricos do livro.
---

Esta skill reúne as 37 regras de Clean Code que o usuário adota como padrão em projetos Java, organizadas em 11 categorias e cada uma ilustrada com exemplo de código antes/depois. APENAS em caso de dúvida sobre um princípio específico, leia o arquivo correspondente em `references/`.

# Princípios

## Nomes
Ver `references/nomes.md`.

## Funções
Ver `references/funcoes.md`.

## Comentários
Ver `references/comentarios.md`.

## Formatação
Ver `references/formatacao.md`.

## Objetos e Estruturas de Dados
Ver `references/objetos-e-estruturas-de-dados.md`.

## Tratamento de Erros
Ver `references/tratamento-de-erros.md`.

## Fronteiras (Boundaries)
Ver `references/fronteiras.md`.

## Testes
Ver `references/testes.md`.

## Classes
Ver `references/classes.md`.

## Emergent Design
Ver `references/emergent-design.md`.

## Geral
Ver `references/geral.md`.

# Critério de aplicação

- Em caso de conflito entre "função pequena" e "um nível de abstração por função", prefira extrair a função apenas se o nome resultante explicar por si só o que o trecho faz; caso contrário, mantenha o método único.
- Em caso de conflito entre DRY e legibilidade, não force abstração para eliminar duplicação de 2-3 linhas se o resultado tornar o fluxo mais difícil de seguir — duplicação pequena e estável é aceitável.
- "Poucos argumentos" tem precedência sobre manter assinaturas antigas: prefira introduzir um objeto de parâmetro (record) a acumular argumentos posicionais.
- Regras de Testes (`references/testes.md`) e Fronteiras (`references/fronteiras.md`) se aplicam tanto a código novo quanto a refatoração de testes existentes; não é aceitável ignorá-las "só para o teste passar mais rápido".
- É aceitável não aplicar um princípio quando o trade-off for explicitado ao usuário (ex: código de protótipo descartável, script de migração único).

# Fora de escopo

- Convenções de nomenclatura de métodos de teste (`should_quando_x`, `dado_quando_entao`, etc.): fica para uma futura skill `java-testes-unitarios` — pergunte ao usuário como proceder se ela ainda não existir.
- Padrões de arquitetura de camadas, empacotamento por feature vs. por camada, e escolha de frameworks: fora do escopo desta skill.
- Convenções de formatação automatizada (regras de um `.editorconfig` ou `spotless.xml` específico do projeto): siga a configuração do projeto quando existir; esta skill cobre apenas o princípio geral de consistência.
