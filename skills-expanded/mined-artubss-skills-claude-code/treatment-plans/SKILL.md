---
name: treatment-plans
description: "Gere planos de tratamento médico concisos (3-4 páginas), focados e em formato LaTeX/PDF para todas as especialidades clínicas. Suporta tratamento médico geral, terapia de reabilitação, saúde mental, controle de doenças crônicas, cuidados perioperatórios e controle da dor. Inclui estrutura de metas SMART, intervenções baseadas em evidências com citações mínimas, conformidade regulatória (HIPAA) e formatação profissional. Prioriza brevidade e acionabilidade clínica."
allowed-tools: [Read, Write, Edit, Bash]
---

# Redação de Plano de Tratamento

## Visão Geral

A redação de plano de tratamento é a documentação sistemática de estratégias de cuidado clínico destinadas a resolver condições de saúde do paciente por meio de intervenções baseadas em evidências, metas mensuráveis e acompanhamento estruturado. Esta competência fornece modelos LaTeX abrangentes e ferramentas de validação para criar **planos de tratamento concisos e focados** (padrão de 3-4 páginas) em todas as especialidades médicas com conformidade regulatória total.

**Princípios Críticos:**
1. **CONCISO & ACIONÁVEL**: Planos de tratamento padrão de 3-4 páginas máximo, focando apenas em informações clinicamente essenciais que impactam decisões de cuidado
2. **Centrado no Paciente**: Planos devem ser baseados em evidências, mensuráveis e conformes com regulamentações de saúde (HIPAA, padrões de documentação)
3. **Citações Mínimas**: Use citações no texto apenas quando necessário para apoiar recomendações clínicas; evite bibliografias extensas

Todo plano de tratamento deve incluir metas claras, intervenções específicas, cronogramas definidos, parâmetros de monitoramento e resultados esperados que se alinhem com preferências do paciente e diretrizes clínicas atuais — tudo apresentado da forma mais eficiente possível.

## Quando Usar Esta Competência

Esta competência deve ser usada quando:
- Criando planos de tratamento individualizados para cuidado ao paciente
- Documentando intervenções terapêuticas para controle de doença crônica
- Desenvolvendo programas de reabilitação (fisioterapia, terapia ocupacional, reabilitação cardíaca)
- Redigindo planos de tratamento de saúde mental e psiquiátricos
- Planejando vias de cuidado perioperatório e cirúrgico
- Estabelecendo protocolos de controle da dor
- Estabelecendo metas centradas no paciente usando critérios SMART
- Coordenando cuidado multidisciplinar entre especialidades
- Garantindo conformidade regulatória em documentação de tratamento
- Gerando planos de tratamento profissionais para registros médicos

## Aprimoramento Visual com Esquemas Científicos

**⚠️ OBRIGATÓRIO: Todo plano de tratamento DEVE incluir no mínimo 1 figura gerada por IA usando a competência scientific-schematics.**

Isto não é opcional. Planos de tratamento beneficiam-se muito de elementos visuais. Antes de finalizar qualquer documento:
1. Gere no mínimo UM esquema ou diagrama (por exemplo, fluxograma de via de tratamento, diagrama de coordenação de cuidados ou linha do tempo de terapia)
2. Para planos complexos: inclua fluxograma de algoritmo de decisão
3. Para planos de reabilitação: inclua diagrama de progressão de marcos

**Como gerar figuras:**
- Use a competência **scientific-schematics** para gerar diagramas de qualidade para publicação alimentados por IA
- Simplesmente descreva seu diagrama desejado em linguagem natural
- O Nano Banana Pro gerará automaticamente, revisará e refinará o esquema

**Como gerar esquemas:**
```bash
python scripts/generate_schematic.py "sua descrição de diagrama" -o figures/output.png
```

A IA gerará automaticamente:
- Imagens de qualidade para publicação com formatação apropriada
- Revisão e refinamento por meio de múltiplas iterações
- Acessibilidade garantida (amigável ao daltonismo, alto contraste)
- Salvamento de saídas no diretório figures/

**Quando adicionar esquemas:**
- Fluxogramas de via de tratamento
- Diagramas de coordenação de cuidados
- Cronogramas de progressão de terapia
- Diagramas de interação de equipe multidisciplinar
- Fluxogramas de gerenciamento de medicação
- Visualizações de protocolo de reabilitação
- Diagramas de algoritmo de decisão clínica
- Qualquer conceito complexo que se beneficie de visualização

Para orientação detalhada sobre criação de esquemas, consulte a documentação da competência scientific-schematics.

---

## Formato do Documento e Melhores Práticas

### Opções de Comprimento do Documento

Planos de tratamento vêm em três opções de formato baseadas em complexidade clínica e caso de uso:

#### Opção 1: Plano de Tratamento de Uma Página (PREFERIDO para a maioria dos casos)

**Quando usar**: Cenários clínicos diretos, protocolos padrão, ambientes clínicos ocupados

**Formato**: Página única contendo todas as informações essenciais de tratamento em seções escaneáveis
- Sem índice necessário
- Sem narrativas extensas
- Focado apenas em itens acionáveis
- Similar a relatórios de oncologia de precisão ou cartões de recomendação de tratamento

**Seções obrigatórias** (todas em uma página):
1. **Caixa de Cabeçalho**: Informação do paciente, diagnóstico, data, perfil molecular/risco se aplicável
2. **Regime de Tratamento**: Lista numerada de intervenções específicas
3. **Cuidados de Apoio**: Pontos de bala breves
4. **Fundamentação**: Justificativa de 1-2 frases (opcional para protocolos padrão)
5. **Monitoramento**: Parâmetros-chave e frequência
6. **Nível de Evidência**: Referência de diretriz ou grau de evidência (por exemplo, "Nível 1, aprovado pelo FDA")
7. **Resultado Esperado**: Cronograma e métricas de sucesso

**Princípios de design**:
- Use pequenas caixas/tabelas para organização (como formato de cartão de recomendação de tratamento clínico)
- Elimine todo texto não essencial
- Use abreviações familiares a clínicos
- Layout de informação denso — maximize informação por polegada quadrada
- Pense em "cartão de referência rápida" não em "documentação abrangente"

**Estrutura de exemplo**:
```latex
[Caixa de ID do Paciente/Diagnóstico no topo]

POPULAÇÃO DE PACIENTES-ALVO
  Número de pacientes, dados demográficos, características-chave

REGIME DE TRATAMENTO PRIMÁRIO
  • Medicação 1: dose, frequência, duração
  • Procedimento: detalhes específicos
  • Monitoramento: o quê e quando

CUIDADOS DE APOIO
  • Medicações de apoio-chave

FUNDAMENTAÇÃO
  Justificativa clínica breve

ALVOS MOLECULARES / FATORES DE RISCO
  Biomarcadores relevantes ou estratificação de risco

NÍVEL DE EVIDÊNCIA
  Referência de diretriz, dados de ensaio

REQUISITOS DE MONITORAMENTO
  Exames/sinais vitais-chave, frequência

BENEFÍCIO CLÍNICO ESPERADO
  Ponto final primário, cronograma
```

#### Opção 2: Formato Padrão de 3-4 Páginas

**Quando usar**: Complexidade moderada, necessidade de materiais de educação ao paciente, coordenação multidisciplinar

Usa o modelo de primeira página resumida da Foundation Medicine com 2-3 páginas adicionais de detalhes.

#### Opção 3: Formato Estendido de 5-6 Páginas

**Quando usar**: Comorbidades complexas, protocolos de pesquisa, monitoramento de segurança extenso necessário

### Resumo da Primeira Página (Modelo Foundation Medicine)

**EXIGÊNCIA CRÍTICA: Todos os planos de tratamento DEVEM ter um resumo executivo completo na primeira página SOMENTE, antes de qualquer índice ou seções detalhadas.**

Seguindo o modelo Foundation Medicine para relatórios de medicina de precisão e documentos de resumo clínico, planos de tratamento começam com um resumo executivo de uma página que fornece acesso imediato a informações-chave acionáveis. Este resumo inteiro deve caber na primeira página.

**Estrutura Obrigatória da Primeira Página (em ordem):**

1. **Título e Subtítulo**
   - Título principal: tipo de plano de tratamento (por exemplo, "Plano de Tratamento Abrangente")
   - Subtítulo: condição específica ou foco (por exemplo, "Diabetes Mellitus Tipo 2 — Paciente Adulto Jovem")

2. **Caixa de Informações do Relatório** (usando `\begin{infobox}` ou `\begin{patientinfo}`)
   - Tipo de relatório/propósito do documento
   - Data de criação do plano
   - Dados demográficos do paciente (idade, sexo, desidentificado)
   - Diagnóstico primário com código ICD-10
   - Autor do relatório/clínica (se aplicável)
   - Abordagem de análise ou framework usado

3. **Descobertas-Chave ou Destaques de Tratamento** (2-4 caixas coloridas usando tipos de caixa apropriados)
   - **Metas de Tratamento Primárias** (usando `\begin{goalbox}`)
     - 2-3 metas SMART em formato de bala
   - **Intervenções Principais** (usando `\begin{keybox}` ou `\begin{infobox}`)
     - 2-3 intervenções-chave (farmacológicas, não farmacológicas, monitoramento)
   - **Pontos de Decisão Críticos** (usando `\begin{warningbox}` se urgente)
     - Limiares de monitoramento importantes ou considerações de segurança
   - **Visão Geral do Cronograma** (usando `\begin{infobox}`)
     - Duração breve do tratamento/fases
     - Datas de marcos-chave

**Requisitos de Formato Visual:**
- Use `\thispagestyle{empty}` para remover números de página da primeira página
- Todo conteúdo deve caber na página 1 (antes de `\newpage`)
- Use caixas coloridas (pacote tcolorbox) com cores diferentes para tipos diferentes de informação
- As caixas devem ser visualmente proeminentes e fáceis de escanear
- Use formato conciso, de ponto de bala
- Índice de conteúdo (se incluído) começa na página 2
- Seções detalhadas começam na página 3

**Estrutura de Exemplo da Primeira Página:**
```latex
\maketitle
\thispagestyle{empty}

% Caixa de Informações do Relatório
\begin{patientinfo}
  Tipo de Relatório, Data, Informação do Paciente, Diagnóstico, etc.
\end{patientinfo}

% Descoberta-Chave #1: Metas de Tratamento
\begin{goalbox}[Metas de Tratamento Primárias]
  • Meta 1
  • Meta 2
  • Meta 3
\end{goalbox}

% Descoberta-Chave #2: Intervenções Principais
\begin{keybox}[Intervenções Essenciais]
  • Intervenção 1
  • Intervenção 2
  • Intervenção 3
\end{keybox}

% Descoberta-Chave #3: Monitoramento Crítico (se aplicável)
\begin{warningbox}[Pontos de Decisão Críticos]
  • Ponto de decisão 1
  • Ponto de decisão 2
\end{warningbox}

\newpage
\tableofcontents  % Índice na página 2
\newpage  % Conteúdo detalhado começa página 3
```

### Documentação Concisa

**CRÍTICO: Planos de tratamento DEVEM priorizar brevidade e relevância clínica. Padrão de 3-4 páginas máximo a menos que complexidade clínica absolutamente exija mais detalhe.**

Planos de tratamento devem priorizar **clareza e acionabilidade** em detrimento de detalhe exaustivo:

- **Focado**: Inclua apenas informação clinicamente essencial que impacte decisões de cuidado
- **Acionável**: Enfatize o que precisa ser feito, quando e por quê
- **Eficiente**: Facilite tomada de decisão rápida sem sacrificar qualidade clínica
- **Opções de comprimento-alvo**:
  - **Formato de 1 página** (preferido para casos diretos): Cartão de referência rápida com todas as informações essenciais
  - **Padrão de 3-4 páginas**: Formato padrão com resumo de primeira página + detalhes de apoio
  - **5-6 páginas** (raro): Apenas para casos altamente complexos com múltiplas comorbidades ou intervenções multidisciplinares

**Diretrizes de Simplificação:**
- **Resumo da Primeira Página**: Use caixas coloridas individuais para consolidar informação-chave (metas, intervenções, pontos de decisão) — isto sozinho frequentemente pode transmitir o plano de tratamento essencial
- **Elimine Redundância**: Se a informação está no resumo de primeira página, não a repita verbatim em seções detalhadas
- **Seção de Educação ao Paciente**: 3-5 pontos de bala-chave apenas em tópicos críticos e sinais de alerta
- **Seção de Mitigação de Risco**: Destaque apenas preocupações críticas de segurança de medicação e ações de emergência (não listas exaustivas)
- **Seção de Resultados Esperados**: 2-3 afirmações concisas sobre respostas antecipadas e cronogramas
- **Intervenções**: Foque em intervenções primárias; medidas secundárias/de apoio em formato de bala breve
- **Use tabelas e pontos de bala** extensivamente para apresentação eficiente
- **Evite prosa narrativa** onde listas estruturadas forem suficientes
- **Combine seções relacionadas** quando apropriado para reduzir contagem de páginas

### Qualidade em Vez de Quantidade

O objetivo é documentação clinicamente completa e profissional que respeite o tempo de clínicos enquanto garanta cuidado ao paciente abrangente. Cada seção deve adicionar valor; remova ou condense seções que não informem diretamente decisões de tratamento.

### Citações e Suporte de Evidência

**Use citações mínimas e direcionadas para apoiar recomendações clínicas:**

- **Citações no Texto Preferidas**: Use citações no texto breves (Autor Ano) ou referências simples em vez de bibliografias extensas a menos que especificamente solicitado
- **Quando Citar**:
  - Recomendações de diretrizes de prática clínica (por exemplo, "per diretrizes ADA 2024")
  - Dosagem específica de medicação ou protocolos (por exemplo, "recomendações ACC/AHA")
  - Intervenções novas ou controversas exigindo suporte de evidência
  - Ferramentas de estratificação de risco ou escalas de avaliação validadas
- **Quando NÃO Citar**:
  - Intervenções padrão de cuidado amplamente aceitas no campo
  - Fatos médicos básicos e práticas clínicas rotineiras
  - Conteúdo geral de educação ao paciente
- **Formato de Citação**: 
  - Inline: "Inicie metformina como terapia de primeira linha (Padrões de Cuidados ADA 2024)"
  - Mínimo: "Tratamento segue diretrizes de insuficiência cardíaca ACC/AHA"
  - Evite referências numeradas formais e seções de bibliografia extensas a menos que o documento seja para propósitos acadêmicos/pesquisa
- **Mantenha Breve**: Um plano de tratamento de 3-4 páginas deve ter 0-3 citações máximo, apenas onde essencial para credibilidade clínica ou recomendações novas

## Competências Principais

### 1. Planos de Tratamento Médico Geral

Planos de tratamento médico geral abordam condições crônicas comuns e problemas médicos agudos exigindo intervenções terapêuticas estruturadas.

#### Componentes Padrão

**Informação do Paciente (Desidentificada)**
- Dados demográficos (idade, sexo, antecedentes médicos relevantes)
- Condições médicas ativas e comorbidades
- Medicações atuais e alergias
- Histórico social e familiar relevante
- Status funcional e avaliações de baseline
- **Conformidade HIPAA**: Remova todos os 18 identificadores por método Safe Harbor

**Resumo de Diagnóstico e Avaliação**
- Diagnóstico primário com código ICD-10
- Diagnósticos secundários e comorbidades
- Classificação de severidade e estadiamento
- Limitações funcionais e impacto em qualidade de vida
- Estratificação de risco (por exemplo, risco cardiovascular, risco de queda)
- Indicadores prognósticos

**Metas de Tratamento (Formato SMART)**

Metas de curto prazo (1-3 meses):
- **Específica**: Resultado claramente definido (por exemplo, "Reduzir HbA1c para <7%")
- **Mensurável**: Métricas quantificáveis (por exemplo, "Diminuir PA sistólica em 10 mmHg")
- **Alcançável**: Realista dada capacidade do paciente
- **Relevante**: Alinhada com prioridades e valores do paciente
- **Limitada em Tempo**: Cronograma específico (por exemplo, "dentro de 8 semanas")

Metas de longo prazo (6-12 meses):
- Alvos de controle ou remissão de doença
- Objetivos de melhoria funcional
- Aprimoramento de qualidade de vida
- Prevenção de complicações
- Manutenção de independência

**Intervenções**

*Farmacológicas*:
- Medicações com dosagens, vias e frequências específicas
- Cronogramas de titulação e doses-alvo
- Considerações de interação droga-droga
- Monitoramento de efeitos adversos
- Reconciliação de medicação

*Não Farmacológicas*:
- Modificações de estilo de vida (dieta, exercício, cessação de tabagismo)
- Intervenções comportamentais
- Educação e automanejo do paciente
- Monitoramento e autorastreamento (glicose, pressão arterial, peso)
- Dispositivos adaptativos ou equipamento de assistência

*Procedurais*:
- Procedimentos ou intervenções planejadas
- Referências a especialistas
- Cronograma de testes diagnósticos
- Cuidados preventivos (vacinações, rastreamentos)

**Cronograma e Agenda**
- Fases de tratamento com cronogramas específicos
- Frequência de consultas (semanal, mensal, trimestral)
- Avaliações de marcos e avaliações de metas
- Cronograma de ajustes de medicação
- Duração esperada do tratamento

**Parâmetros de Monitoramento**
- Resultados clínicos a rastrear (sinais vitais, valores de laboratório, sintomas)
- Ferramentas de avaliação e escalas (por exemplo, PHQ-9, escalas de dor)
- Frequência de monitoramento
- Limiares para intervenção ou escalação
- Resultados informados pelo paciente

**Resultados Esperados**
- Medidas de resultado primário
- Critérios de sucesso e benchmarks
- Cronograma esperado para melhoria
- Critérios para modificação de tratamento
- Prognóstico de longo prazo

**Plano de Acompanhamento**
- Consultas agendadas e reavaliações
- Plano de comunicação (chamadas, mensagens seguras)
- Procedimentos de contato de emergência
- Critérios para avaliação urgente
- Planejamento de transição ou alta

**Educação do Paciente**
- Compreensão de condição e fundamentação de tratamento
- Treinamento de habilidades de automanejo
- Administração de medicação e aderência
- Sinais de alerta e quando procurar ajuda
- Recursos e serviços de apoio

**Mitigação de Risco**
- Efeitos adversos potenciais e manejo
- Interações de droga e contraindicações
- Prevenção de queda, prevenção de infecção
- Planos de ação de emergência
- Monitoramento de segurança

#### Aplicações Comuns

- Gerenciamento de diabetes mellitus
- Controle de hipertensão
- Tratamento de insuficiência cardíaca
- Manejo de DPOC
- Planos de cuidado de asma
- Tratamento de hipercolesterolemia
- Manejo de osteoartrite
- Doença renal crônica

### 2. Planos de Tratamento de Reabilitação

Planos de reabilitação focam em restaurar função, melhorar mobilidade e aprimorar qualidade de vida por meio de programas terapêuticos estruturados.

#### Componentes Principais

**Avaliação Funcional**
- Status funcional de baseline (AVD, AIVD)
- Amplitude de movimento, força, equilíbrio, resistência
- Análise de marcha e avaliação de mobilidade
- Medidas padronizadas (FIM, Índice de Barthel, Escala de Equilíbrio de Berg)
- Avaliação ambiental (segurança doméstica, acessibilidade)

**Metas de Reabilitação**

*Metas em nível de impedimento*:
- Melhorar flexão de ombro para 140 graus
- Aumentar força de quadríceps por 2/5 graus MMT
- Aprimorar equilíbrio (Escore de Berg >45/56)

*Metas em nível de atividade*:
- Deambulação independente 150 pés com dispositivo de assistência
- Subir 12 degraus com suporte de corrimão sob supervisão
- Transferência cama-cadeira independente

*Metas em nível de participação*:
- Retornar ao trabalho com modificações
- Retomar atividades recreacionais
- Mobilidade comunitária independente

**Intervenções Terapêuticas**

*Fisioterapia*:
- Exercícios terapêuticos (fortalecimento, alongamento, resistência)
- Técnicas de terapia manual
- Treinamento de marcha e atividades de equilíbrio
- Modalidades (calor, gelo, estimulação elétrica, ultrassom)
- Treinamento de dispositivo de assistência

*Terapia Ocupacional*:
- Treinamento de AVD (banho, vestiário, higiene pessoal, alimentação)
- Fortalecimento e coordenação de membro superior
- Equipamento adaptativo e modificações
- Técnicas de conservação de energia
- Reabilitação cognitiva

*Patologia da Fala e Linguagem*:
- Terapia de deglutição e manejo de disfagia
- Estratégias de comunicação e dispositivos aumentativos
- Terapia cognitivo-linguística
- Terapia de voz

*Outros Serviços*:
- Terapia recreacional
- Terapia aquática
- Reabilitação cardíaca
- Reabilitação pulmonar
- Reabilitação vestibular

**Cronograma de Tratamento**
- Frequência: FT 3x/semana, TO 2x/semana (exemplo)
- Duração da sessão: 45-60 minutos
- Durações de fase de tratamento (aguda, subaguda, manutenção)
- Duração esperada: 8-12 semanas
- Intervalos de reavaliação

**Monitoramento de Progresso**
- Avaliações funcionais semanais
- Medidas de resultado padronizadas
- Escala de realização de metas
- Rastreamento de dor e sintomas
- Satisfação do paciente

**Programa de Exercício Doméstico**
- Exercícios específicos com repetições/séries/frequência
- Precauções e instruções de segurança
- Critérios de progressão
- Estratégias de automomonitoramento

#### Reabilitação Especializada

- Reabilitação pós-acidente vascular cerebral
- Reabilitação ortopédica (substituição articular, fratura)
- Reabilitação cardíaca (pós-IM, pós-cirurgia)
- Reabilitação pulmonar
- Reabilitação vestibular
- Reabilitação neurológica
- Reabilitação de lesão esportiva

### 3. Planos de Tratamento de Saúde Mental

Planos de tratamento de saúde mental abordam condições psiquiátricas por meio de intervenções psicoterápicas, farmacológicas e psicossociais integradas.

#### Componentes Essenciais

**Avaliação Psiquiátrica**
- Diagnóstico psiquiátrico primário (critérios DSM-5)
- Severidade de sintomas e deficiência funcional
- Condições co-ocorrentes de saúde mental
- Avaliação de uso de substância
- Avaliação de risco de suicídio/homicídio
- Histórico de trauma e rastreamento de TEPT
- Determinantes sociais de saúde mental

**Metas de Tratamento**

*Redução de sintomas*:
- Diminuir severidade de depressão (escore PHQ-9 de 18 para <10)
- Reduzir sintomas de ansiedade (escore GAD-7 <5)
- Melhorar qualidade de sono (Índice de Qualidade do Sono de Pittsburgh)
- Estabilizar humor (episódios de humor reduzidos)

*Melhoria funcional*:
- Retornar ao trabalho ou escola
- Melhorar relacionamentos sociais e suporte
- Aprimorar habilidades de enfrentamento e regulação emocional
- Aumentar engajamento em atividades significativas

*Metas orientadas para recuperação*:
- Construir resiliência e autossuficiência
- Desenvolver habilidades de manejo de crise
- Estabelecer rotinas de bem-estar sustentáveis
- Alcançar metas de recuperação pessoal

**Intervenções Terapêuticas**

*Psicoterapia*:
- Modalidade baseada em evidências (TCC, DBT, ACT, psicodinâmica, IPT)
- Frequência de sessão (semanal, quinzenal)
- Duração do tratamento (12-16 semanas, contínuo)
- Técnicas específicas e alvos
- Participação em terapia de grupo

*Psicofarmacologia*:
- Classe de medicação e fundamentação
- Dose inicial e cronograma de titulação
- Sintomas-alvo
- Cronograma esperado de resposta (2-4 semanas para antidepressivos)
- Monitoramento de efeito colateral
- Considerações de terapia de combinação

*Intervenções Psicossociais*:
- Serviços de gerenciamento de caso
- Programas de suporte entre pares
- Terapia familiar ou psicodocação
- Reabilitação vocacional
- Habitação apoiada ou integração comunitária
- Tratamento de abuso de substância

**Planejamento de Segurança**
- Contatos de crise e serviços de emergência
- Sinais de alerta e gatilhos
- Estratégias de enfrentamento e técnicas de autossocorro
- Modificações de ambiente seguro
- Restrição de meios (armas de fogo, medicações)
- Ativação do sistema de suporte

**Monitoramento e Avaliação**
- Escalas de classificação de sintomas (semanal ou quinzenal)
- Aderência à medicação e efeitos colaterais
- Rastreamento de ideação suicida
- Avaliações de status funcional
- Engajamento no tratamento e aliança terapêutica

**Educação do Paciente e Familiar**
- Psicoeducação sobre diagnóstico
- Fundamentação de tratamento e expectativas
- Informação de medicação
- Estratégias de prevenção de recaída
- Recursos comunitários

#### Condições de Saúde Mental

- Transtorno depressivo maior
- Transtornos de ansiedade (GAD, pânico, ansiedade social)
- Transtorno bipolar
- Esquizofrenia e transtornos psicóticos
- TEPT e transtornos relacionados a trauma
- Transtornos alimentares
- Transtornos de uso de substância
- Transtornos de personalidade

### 4. Planos de Gerenciamento de Doença Crônica

Planos de cuidado abrangentes de longo prazo para doenças crônicas exigindo monitoramento contínuo, aj