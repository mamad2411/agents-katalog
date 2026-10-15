---
name: companify-ameacas
description: Analisa ameaças empresariais por categoria. Use para estruturar company/ameacas.md com probabilidade, impacto, mitigação e contingência.
---

# Analisar ameaças empresariais

## Protocolo operacional

- **Plano e progresso:** planejar a varredura por categoria antes de
  detalhar cada ameaça individualmente.
- **Fontes de verdade:** ler todos os artefatos já produzidos em `company/`
  e `.companify/assumptions.md`: premissas críticas não validadas são
  candidatas naturais a virar ameaça registrada.
- **Escopo e idempotência:** não substituir especialista jurídico, contábil,
  fiscal ou de compliance; sinalizar quando uma ameaça exige essa consulta.
- **Validação:** cada ameaça registrada tem probabilidade, impacto, sinal de
  alerta, mitigação, plano de contingência e responsável lógico.
- **Resumo final:** informar as ameaças críticas, as sem mitigação definida e
  as que exigem consulta profissional externa.

## Fluxo

1. Varrer as categorias: estratégica, de mercado, de produto, tecnológica,
   financeira, operacional, de pessoas, de fornecedor, regulatória, jurídica,
   de segurança, de privacidade, de reputação e de concentração (dependência
   excessiva de um cliente, fornecedor ou pessoa).
2. Para cada ameaça relevante identificada nos artefatos de `company/`,
   registrar: nome da ameaça, probabilidade, impacto, sinal de alerta,
   mitigação, plano de contingência, responsável lógico.
3. Priorizar as ameaças por combinação de probabilidade e impacto, não listar
   todas com o mesmo peso.
4. Sinalizar explicitamente quando uma ameaça (regulatória, jurídica,
   fiscal) exige consulta profissional fora do escopo do Companify.
5. Salvar em `company/ameacas.md`.

## Raciocínio do especialista

Uma ameaça sem sinal de alerta observável não é operacional, é uma
preocupação vaga. Exigir de cada ameaça registrada uma resposta à pergunta:
"como saberíamos que isso está começando a acontecer, antes de já ter
acontecido?". Ameaças de concentração (um cliente, um fornecedor, uma pessoa)
são frequentemente subestimadas porque não aparecem nas métricas de curto
prazo, e por isso exigem o mesmo rigor de uma ameaça financeira explícita.
