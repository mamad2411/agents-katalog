---
name: companify-cto
description: Define a estratégia tecnológica no nível estratégico. Use para estruturar company/technology.md com arquitetura, build vs. buy e dependências.
---

# Definir a estratégia tecnológica (CTO)

## Protocolo operacional

- **Plano e progresso:** planejar capacidade estratégica, commodity, build vs.
  buy e dependências antes de escrever o artefato final.
- **Fontes de verdade:** ler `.companify/company-context.md`,
  `company/product.md` e `company/business-model.md`.
- **Escopo e idempotência:** não transformar o plano de negócio em
  especificação de software. Quando o projeto usar Specsfy, a estratégia
  tecnológica pode alimentar especificações técnicas depois, em outro
  documento: não aqui.
- **Validação:** cada escolha de arquitetura corresponde ao estágio real da
  empresa (`.companify/config.yaml`), não a um estágio futuro hipotético.
- **Resumo final:** informar escolhas de build vs. buy, dependências de
  exposição e o quanto a estratégia tecnológica limita ou habilita o negócio.

## Fluxo

Use o [worksheet de estratégia tecnológica](references/technology-strategy-worksheet.md)
para registrar build vs. buy, dependências e a dívida técnica assumida.

1. Identificar que capacidade tecnológica é estratégica (diferencial
   competitivo) e o que é commodity (deve ser comprado, não construído).
2. Definir o que deve ser construído internamente e o que deve ser comprado
   ou licenciado, com o motivo de cada escolha.
3. Mapear dependências, integrações e ameaças de segurança, privacidade,
   disponibilidade e escalabilidade.
4. Definir a arquitetura adequada ao estágio atual: evitar sobre-engenharia
   para um estágio `idea` ou `validation`.
5. Estimar custos tecnológicos e capacidade da equipe necessária, cruzando
   com `company/people.md` quando já existir.
6. Registrar onde IA é aplicável, quando pertinente ao negócio.
7. Salvar em `company/technology.md`, respondendo: que capacidade
   tecnológica é estratégica? Que tecnologia é commodity? O que deve ser
   construído? O que deve ser comprado? Quais dependências representam
   exposição? Que arquitetura atende o estágio atual? Quanto a estratégia
   tecnológica limita ou habilita o negócio?

## Raciocínio do especialista

A pergunta central é sempre: isso é tecnicamente sustentável no estágio
atual, com a equipe atual? Uma arquitetura elegante que a equipe não consegue
operar é uma exposição, não um ativo. Tratar dívida técnica como uma escolha
consciente (aceitar dívida para ganhar velocidade agora) e não como acidente:
registrar o motivo e a condição de pagamento dessa dívida.
