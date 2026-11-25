---
name: clinical-reports
description: "Escreva relatórios clínicos abrangentes incluindo relatos de casos (diretrizes CARE), relatórios diagnósticos (radiologia/patologia/laboratório), relatórios de ensaios clínicos (ICH-E3, SAE, CSR) e documentação de pacientes (SOAP, H&P, resumos de alta). Suporte completo com modelos, conformidade regulatória (HIPAA, FDA, ICH-GCP) e ferramentas de validação."
allowed-tools: [Read, Write, Edit, Bash]
---

# Escrita de Relatórios Clínicos

## Visão Geral

A escrita de relatórios clínicos é o processo de documentação de informações médicas com precisão, exatidão e conformidade com padrões regulatórios. Esta habilidade abrange quatro categorias principais de relatórios clínicos: relatos de casos para publicação em periódicos, relatórios diagnósticos para prática clínica, relatórios de ensaios clínicos para submissão regulatória e documentação de pacientes para registros médicos. Aplique esta habilidade para documentação em saúde, disseminação de pesquisa e conformidade regulatória.

**Princípio Crítico: Os relatórios clínicos devem ser precisos, completos, objetivos e conformes com regulamentações aplicáveis (HIPAA, FDA, ICH-GCP).** A privacidade do paciente e a integridade dos dados são primordiais. Toda documentação clínica deve apoiar a tomada de decisão baseada em evidências e atender aos padrões profissionais.

## Quando Usar Esta Habilidade

Esta habilidade deve ser usada quando:
- Redigir relatos de casos clínicos para submissão em periódicos (diretrizes CARE)
- Criar relatórios diagnósticos (radiologia, patologia, laboratório)
- Documentar dados de ensaios clínicos e eventos adversos
- Preparar relatórios de estudo clínico (CSR) para submissão regulatória
- Escrever notas de progresso do paciente, notas SOAP e resumos clínicos
- Redigir resumos de alta, documentos H&P ou notas de consulta
- Garantir conformidade HIPAA e de-identificação apropriada
- Validar documentação clínica quanto à integridade e completude
- Preparar relatórios de eventos adversos graves (SAE)
- Criar relatórios do comitê de monitoramento de segurança de dados (DSMB)

## Aprimoramento Visual com Esquemas Científicos

**⚠️ OBRIGATÓRIO: Todo relatório clínico DEVE incluir pelo menos 1 figura gerada por IA usando a habilidade scientific-schematics.**

Isso não é opcional. Relatórios clínicos se beneficiam muito de elementos visuais. Antes de finalizar qualquer documento:
1. Gere no mínimo UM esquema ou diagrama (ex.: cronograma do paciente, algoritmo diagnóstico ou fluxo de tratamento)
2. Para relatos de casos: inclua cronograma de progressão clínica
3. Para relatórios de ensaios: inclua diagrama de fluxo CONSORT

**Como gerar figuras:**
- Use a habilidade **scientific-schematics** para gerar diagramas com qualidade de publicação alimentados por IA
- Simplesmente descreva seu diagrama desejado em linguagem natural
- O Nano Banana Pro gerará, revisará e refinará automaticamente o esquema

**Como gerar esquemas:**
```bash
python scripts/generate_schematic.py "descrição do seu diagrama" -o figures/output.png
```

A IA gerará automaticamente:
- Imagens com qualidade de publicação com formatação apropriada
- Revisão e refinamento através de múltiplas iterações
- Garantia de acessibilidade (amigável para daltônicos, alto contraste)
- Salvamento de resultados no diretório figures/

**Quando adicionar esquemas:**
- Cronogramas e diagramas de progressão clínica do paciente
- Fluxogramas de algoritmo diagnóstico
- Fluxos de trabalho de protocolo de tratamento
- Diagramas anatômicos para relatos de casos
- Diagramas de fluxo de participantes de ensaios clínicos (CONSORT)
- Árvores de classificação de eventos adversos
- Qualquer conceito complexo que se beneficie de visualização

Para orientação detalhada sobre criação de esquemas, consulte a documentação de habilidade scientific-schematics.

---

## Capacidades Essenciais

### 1. Relatos de Casos Clínicos para Publicação em Periódicos

Os relatos de casos clínicos descrevem apresentações clínicas incomuns, diagnósticos novos ou complicações raras. Contribuem para o conhecimento médico e são publicados em periódicos revisados por pares.

#### Conformidade com Diretrizes CARE

As diretrizes CARE (CAse REport) fornecem um framework padronizado para redação de relatórios de casos. Todos os relatos de casos devem seguir este checklist:

**Título**
- Inclua as palavras "relato de caso" ou "estudo de caso"
- Indique a área de foco
- Exemplo: "Apresentação Incomum de Infarto Agudo do Miocárdio em Paciente Jovem: Um Relato de Caso"

**Palavras-chave**
- 2-5 palavras-chave para indexação e capacidade de busca
- Use termos MeSH (Medical Subject Headings) quando possível

**Resumo** (estruturado ou não estruturado, 150-250 palavras)
- Introdução: O que é único ou novo sobre o caso?
- Preocupações do paciente: Sintomas primários e histórico médico relevante
- Diagnósticos: Diagnósticos primários e secundários
- Intervenções: Tratamentos e procedimentos-chave
- Resultados: Resultado clínico e acompanhamento
- Conclusões: Ponto principal ou lição clínica

**Introdução**
- Breve contexto sobre a condição médica
- Por que este caso é novo ou importante
- Revisão de literatura de casos semelhantes (breve)
- O que torna este caso digno de relato

**Informações do Paciente**
- Dados demográficos (idade, sexo, raça/etnia se relevante)
- Histórico médico, histórico familiar, histórico social
- Comorbidades relevantes
- **De-identificação**: Remova ou altere 18 identificadores HIPAA
- **Consentimento do paciente**: Documente consentimento informado para publicação

**Achados Clínicos**
- Queixa principal e sintomas apresentados
- Achados do exame físico
- Cronograma de sintomas (considere figura de cronograma ou tabela)
- Observações clínicas relevantes

**Cronograma**
- Resumo cronológico de eventos-chave
- Datas de sintomas, diagnóstico, intervenções, resultados
- Pode ser apresentado como tabela ou figura
- Formato exemplo:
  - Dia 0: Apresentação inicial com sintomas X, Y, Z
  - Dia 2: Teste diagnóstico A realizado, revelou descoberta B
  - Dia 5: Tratamento iniciado com droga C
  - Dia 14: Melhora clínica notada
  - Mês 3: Exame de acompanhamento mostra resolução completa

**Avaliação Diagnóstica**
- Testes diagnósticos realizados (labs, imagem, procedimentos)
- Resultados e interpretação
- Diagnóstico diferencial considerado
- Justificativa do diagnóstico final
- Desafios no diagnóstico

**Intervenções Terapêuticas**
- Medicamentos (nomes, dosagens, vias, duração)
- Procedimentos ou cirurgias realizadas
- Intervenções não farmacológicas
- Raciocínio para escolhas de tratamento
- Tratamentos alternativos considerados

**Acompanhamento e Resultados**
- Resultado clínico (resolução, melhora, inalterado, piorado)
- Duração e frequência do acompanhamento
- Resultados a longo prazo se disponíveis
- Resultados relatados pelo paciente
- Aderência ao tratamento

**Discussão**
- Força e novidade do caso
- Como este caso se compara à literatura existente
- Limitações do relato de caso
- Possíveis mecanismos ou explicações
- Implicações clínicas e lições aprendidas
- Questões não respondidas ou áreas para pesquisa futura

**Perspectiva do Paciente** (opcional mas encorajado)
- Experiência e ponto de vista do paciente
- Impacto na qualidade de vida
- Resultados relatados pelo paciente
- Citação do paciente se apropriado

**Consentimento Informado**
- Declaração documentando consentimento do paciente para publicação
- Se paciente falecido ou incapaz de consentir, descreva consentimento por procurador
- Para casos pediátricos, consentimento de pais/tutor
- Exemplo: "Consentimento informado por escrito foi obtido do paciente para publicação deste relato de caso e imagens acompanhantes. Uma cópia do consentimento escrito está disponível para revisão pelo Editor-Chefe deste periódico."

Para diretrizes detalhadas de CARE, consulte `references/case_report_guidelines.md`.

#### Requisitos Específicos de Periódicos

Diferentes periódicos têm requisitos de formatação específicos:
- Limites de contagem de palavras (tipicamente 1500-3000 palavras)
- Número de figuras/tabelas permitidas
- Estilo de referência (AMA, Vancouver, APA)
- Resumo estruturado vs. não estruturado
- Políticas de materiais suplementares

Verifique as instruções do periódico para autores antes da submissão.

#### De-identificação e Privacidade

**18 Identificadores HIPAA a Remover ou Alterar:**
1. Nomes
2. Subdivisões geográficas menores que estado
3. Datas (exceto ano)
4. Números de telefone
5. Números de fax
6. Endereços de email
7. Números de seguro social
8. Números de registros médicos
9. Números de beneficiários de plano de saúde
10. Números de conta
11. Números de certificado/licença
12. Identificadores de veículos e números de série
13. Identificadores de dispositivos e números de série
14. URLs
15. Endereços IP
16. Identificadores biométricos
17. Fotografias em close do rosto
18. Qualquer outra característica de identificação única

**Melhores Práticas:**
- Use "o paciente" em vez de nomes
- Relate faixas etárias (ex.: "uma mulher em seus 60 anos") ou idade exata se relevante
- Use datas aproximadas ou intervalos de tempo (ex.: "3 meses antes")
- Remova nomes de instituições a menos que necessário
- Desfoque ou corte características de identificação em imagens
- Obtenha consentimento explícito para qualquer informação potencialmente identificável

### 2. Relatórios Diagnósticos Clínicos

Relatórios diagnósticos comunicam achados de estudos de imagem, exames patológicos e testes laboratoriais. Devem ser claros, precisos e acionáveis.

#### Relatórios de Radiologia

Os relatórios de radiologia seguem uma estrutura padronizada para garantir clareza e integridade.

**Estrutura Padrão:**

**1. Dados Demográficos do Paciente**
- Nome do paciente (ou ID em contextos de pesquisa)
- Data de nascimento ou idade
- Número de registro médico
- Data e hora do exame

**2. Indicação Clínica**
- Razão do exame
- Histórico clínico relevante
- Pergunta clínica específica a ser respondida
- Exemplo: "Descartar embolia pulmonar em paciente com dispneia aguda"

**3. Técnica**
- Modalidade de imagem (raio-X, TC, RM, ultrassom, PET, etc.)
- Região anatômica examinada
- Administração de contraste (tipo, via, volume)
- Protocolo ou sequência usada
- Qualidade técnica e limitações
- Exemplo: "TC com contraste de tórax, abdômen e pelve foi realizada usando 100 mL de contraste iodado intravenoso. Contraste oral não foi administrado."

**4. Comparação**
- Estudos de imagem prévia disponível para comparação
- Datas de estudos anteriores
- Estabilidade ou mudança em relação à imagem prévia
- Exemplo: "Comparação: TC tórax de [data]"

**5. Achados**
- Descrição sistemática de achados de imagem
- Abordagem por órgão ou por região
- Achados positivos primeiro, depois negativos pertinentes
- Medições de lesões ou anormalidades
- Uso de terminologia padronizada (léxico ACR, RadLex)
- Exemplo:
  - Pulmões: Opacidades em vidro fosco bilaterais, predominantes nos lobos inferiores. Sem consolidação ou derrame pleural.
  - Mediastino: Sem linfadenopatia. Tamanho cardíaco normal.
  - Abdômen: Fígado, baço, pâncreas sem alterações. Sem líquido livre.

**6. Impressão/Conclusão**
- Resumo conciso dos achados-chave
- Respostas à questão clínica
- Diagnóstico diferencial se aplicável
- Recomendações para acompanhamento ou estudos adicionais
- Nível de suspeita ou certeza diagnóstica
- Exemplo:
  - "1. Opacidades em vidro fosco bilaterais consistentes com pneumonia viral ou infecção atípica. COVID-19 não pode ser excluído. Correlação clínica recomendada.
  - 2. Sem evidência de embolia pulmonar.
  - 3. Recomenda-se acompanhamento de imagem em 4-6 semanas para avaliar resolução."

**Relatórios Estruturados:**

Muitos departamentos de radiologia usam modelos de relatórios estruturados para exames comuns:
- Relatório de nódulo pulmonar (Lung-RADS)
- Imagem de mama (BI-RADS)
- Imagem de fígado (LI-RADS)
- Imagem de próstata (PI-RADS)
- TC de colonografia (C-RADS)

Os relatórios estruturados melhoram a consistência, reduzem ambiguidade e facilitam extração de dados.

Para padrões de relatório de radiologia, consulte `references/diagnostic_reports_standards.md`.

#### Relatórios de Patologia

Os relatórios de patologia documentam achados microscópicos de espécimes teciduais e fornecem conclusões diagnósticas.

**Estrutura do Relatório de Patologia Cirúrgica:**

**1. Informações do Paciente**
- Nome do paciente e identificadores
- Data de nascimento, idade, sexo
- Médico solicitante
- Número de registro médico
- Data de recebimento do espécime

**2. Informações do Espécime**
- Tipo de espécime (biópsia, excisão, ressecção)
- Local anatômico
- Lateralidade se aplicável
- Número de espécimes/blocos/lâminas
- Exemplo: "Pele, antebraço esquerdo, biópsia excisional"

**3. Histórico Clínico**
- Informação clínica relevante
- Indicação de biópsia
- Diagnósticos anteriores
- Exemplo: "Histórico de melanoma. Lesão pigmentada nova, descartar recorrência."

**4. Descrição Macroscópica**
- Aparência macroscópica do espécime
- Tamanho, peso, cor, consistência
- Marcadores de orientação se presentes
- Abordagem de corte e amostragem
- Exemplo: "O espécime consiste em uma elipse de pele medindo 2,5 x 1,0 x 0,5 cm. Uma lesão pigmentada medindo 0,6 cm de diâmetro está presente na superfície. O espécime foi cortado em série e integralmente submetido em cassetes A1-A3."

**5. Descrição Microscópica**
- Achados histológicos
- Características celulares
- Padrões arquiteturais
- Presença de malignidade
- Status de margens se aplicável
- Resultados de colorações especiais ou imunoistoquímica

**6. Diagnóstico**
- Diagnóstico primário
- Grau e estágio se aplicável (câncer)
- Status de margens
- Status de linfonodos se aplicável
- Relatório sinóptico para cânceres (protocolos CAP)
- Exemplo:
  - "MELANOMA MALIGNO, TIPO DISSEMINAÇÃO SUPERFICIAL
  - Espessura de Breslow: 1,2 mm
  - Nível de Clark: IV
  - Taxa mitótica: 3/mm²
  - Ulceração: Ausente
  - Margens: Negativas (margem mais próxima 0,4 cm)
  - Invasão linfovascular: Não identificada"

**7. Comentário** (se necessário)
- Contexto ou interpretação adicional
- Diagnóstico diferencial
- Recomendações para estudos adicionais
- Sugestões para correlação clínica

**Relatório Sinóptico:**

O College of American Pathologists (CAP) fornece modelos de relatório sinóptico para espécimes de câncer. Estes checklists garantem que todos os elementos diagnósticos relevantes sejam documentados.

Elementos-chave para relatório de câncer:
- Local do tumor
- Tamanho do tumor
- Tipo histológico
- Grau histológico
- Extensão de invasão
- Invasão linfovascular
- Invasão perineural
- Margens
- Linfonodos (número examinado, número positivo)
- Estágio patológico (classificação TNM)
- Estudos auxiliares (marcadores moleculares, biomarcadores)

#### Relatórios Laboratoriais

Os relatórios laboratoriais comunicam resultados de testes para espécimes clínicos (sangue, urina, tecido, etc.).

**Componentes Padrão:**

**1. Informações do Paciente e do Espécime**
- Identificadores do paciente
- Tipo de espécime (sangue, soro, urina, LCR, etc.)
- Data e hora de coleta
- Data e hora de recebimento
- Provedor solicitante

**2. Nome e Método do Teste**
- Nome completo do teste
- Metodologia (imunoensaio, espectrofotometria, PCR, etc.)
- Número de acesso do laboratório

**3. Resultados**
- Resultado quantitativo ou qualitativo
- Unidades de medição
- Intervalo de referência (valores normais)
- Sinalizadores para valores anormais (H = alto, L = baixo)
- Valores críticos destacados
- Exemplo:
  - Hemoglobina: 8,5 g/dL (L) [Referência: 12,0-16,0 g/dL]
  - Contagem de Leucócitos: 15,2 x10³/μL (H) [Referência: 4,5-11,0 x10³/μL]

**4. Interpretação** (quando aplicável)
- Significância clínica dos resultados
- Testes de acompanhamento sugeridos
- Correlação com diagnóstico
- Níveis de drogas e intervalos terapêuticos

**5. Informações de Controle de Qualidade**
- Adequação do espécime
- Problemas de qualidade de espécime (hemolisado, lipêmico, coagulado)
- Atrasos no processamento
- Limitações técnicas

**Relatório de Valor Crítico:**
- Resultados que ameaçam a vida requerem notificação imediata
- Exemplos: glicose <40 ou >500 mg/dL, potássio <2,5 ou >6,5 mEq/L
- Documente hora de notificação e destinatário

Para padrões laboratoriais e terminologia, consulte `references/diagnostic_reports_standards.md`.

### 3. Relatórios de Ensaios Clínicos

Os relatórios de ensaios clínicos documentam a conduta, resultados e segurança de estudos de pesquisa clínica. Esses relatórios são essenciais para submissões regulatórias e publicação científica.

#### Relatórios de Eventos Adversos Graves (SAE)

Os relatórios de SAE documentam reações adversas inesperadas graves durante ensaios clínicos. Os requisitos regulatórios obrigam relatório oportuno para IRBs, patrocinadores e órgãos regulatórios.

**Definição de Evento Adverso Grave:**
Um evento adverso é grave se:
- Resulta em morte
- Ameaça a vida
- Requer hospitalização inpatiente ou prolongamento de hospitalização existente
- Resulta em incapacidade/incapacidade persistente ou significativa
- É uma anomalia congênita/defeito de nascimento
- Requer intervenção para prevenir comprometimento ou dano permanente

**Componentes do Relatório de SAE:**

**1. Informações do Estudo**
- Número e título do protocolo
- Fase do estudo
- Nome do patrocinador
- Investigador principal
- Número IND/IDE (se aplicável)
- Número de registro de ensaio clínico (número NCT)

**2. Informações do Paciente (De-identificadas)**
- ID do sujeito ou número de randomização
- Idade, sexo, raça/etnia
- Braço do estudo ou grupo de tratamento
- Data de consentimento informado
- Data da primeira intervenção do estudo

**3. Informações do Evento**
- Descrição do evento (narrativa)
- Data de início
- Data de resolução (ou em andamento)
- Severidade (leve, moderada, grave)
- Critérios de seriedade atendidos
- Resultado (recuperado, se recuperando, não recuperado, fatal, desconhecido)

**4. Avaliação de Causalidade**
- Relação com intervenção do estudo (não relacionada, improvável, possível, provável, definida)
- Relação com procedimentos do estudo
- Relação com doença subjacente
- Justificativa da determinação de causalidade

**5. Ação Tomada**
- Modificação de intervenção do estudo (redução de dose, bloqueio temporário, descontinuação permanente)
- Medicamentos ou tratamentos concomitantes administrados
- Detalhes de hospitalização
- Resultado e plano de acompanhamento

**6. Esperabilidade**
- Esperado conforme protocolo ou folheto do investigador
- Evento inesperado requerendo relatório expedido
- Comparação com perfil de segurança conhecido

**7. Narrativa**
- Descrição detalhada do evento
- Cronograma de eventos
- Curso clínico e manejo
- Resultados de testes laboratoriais e diagnósticos
- Diagnóstico final ou conclusão

**8. Informações do Relator**
- Nome e contato do relator
- Data do relatório
- Assinatura

**Linhas de Tempo Regulatórias:**
- SAEs fatais ou que ameaçam a vida inesperados: 7 dias para relatório preliminar, 15 dias para relatório completo
- Outros eventos graves inesperados: 15 dias
- Notificação do IRB: conforme política institucional, tipicamente dentro de 5-10 dias

Para orientação detalhada sobre relatório de SAE, consulte `references/clinical_trial_reporting.md`.

#### Relatórios de Estudo Clínico (CSR)

Os relatórios de estudo clínico são documentos abrangentes que resumem o design, conduta e resultados de ensaios clínicos. Eles são submetidos a órgãos regulatórios como parte de aplicações de aprovação de drogas.

**Estrutura ICH-E3:**

A diretriz ICH E3 define a estrutura e conteúdo dos relatórios de estudo clínico.

**Seções Principais:**

**1. Página de Título**
- Título do estudo e número do protocolo
- Informações do patrocinador e investigador
- Data do relatório e versão

**2. Sinopse** (5-15 páginas)
- Resumo breve de todo o estudo
- Objetivos, métodos, resultados, conclusões
- Achados-chave de eficácia e segurança
- Pode estar independente

**3. Índice**

**4. Lista de Abreviações e Definições**

**5. Ética** (Seção 2)
- Aprovações de IRB/IEC
- Processo de consentimento informado
- Declaração de conformidade com GCP

**6. Investigadores e Estrutura Administrativa do Estudo** (Seção 3)
- Lista de investigadores e sites
- Organização do estudo
- Monitoramento e garantia de qualidade

**7. Introdução** (Seção 4)
- Contexto e justificativa
- Objetivos e propósito do estudo

**8. Objetivos do Estudo e Plano** (Seção 5)
- Design e plano geral
- Objetivos (primários e secundários)
- Endpoints (eficácia e segurança)
- Determinação de tamanho de amostra

**9. Pacientes do Estudo** (Seção 6)
- Critérios de inclusão e exclusão
- Disposição do paciente
- Desvios de protocolo
- Características demográficas e basais

**10. Avaliação de Eficácia** (Seção 7)
- Conjuntos de dados analisados (ITT, PP, segurança)
- Características demográficas e basais
- Resultados de eficácia para endpoints primários e secundários
- Análises de subgrupos
- Desistências e dados faltantes

**11. Avaliação de Segurança** (Seção 8)
- Extensão de exposição
- Eventos adversos (tabelas de resumo)
- Eventos adversos graves (narrativas)
- Valores laboratoriais
- Sinais vitais e achados físicos
- Mortes e outros eventos graves

**12. Discussão e Conclusões Gerais** (Seção 9)
- Interpretação de resultados
- Avaliação risco-benefício
- Implicações clínicas

**13. Tabelas, Figuras e Gráficos** (Seção 10)

**14. Lista de Referências** (Seção 11)

**15. Apêndices** (Seção 12)
- Protocolo do estudo e emendas
- Amostra de formulários de coleta de dados
- Lista de investigadores e comitês de ética
- Informações do paciente e formulários de consentimento
- Referências do folheto do investigador
- Publicações baseadas no estudo

**Princípios-Chave:**
- Objetividade e transparência
- Apresentação de dados abrangente
- Adesão ao plano de análise estatística
- Apresentação clara de dados de segurança
- Integração de apêndices

Para modelos de ICH-E3 e orientação detalhada, consulte `references/clinical_trial_reporting.md` e `assets/clinical_trial_csr_template.md`.

#### Desvios de Protocolo

Os desvios de protocolo são afastamentos do protocolo aprovado do estudo. Devem ser documentados, avaliados e relatados.

**Categorias:**
- **Desvio menor**: Não impacta significativamente a segurança do paciente ou integridade dos dados
- **Desvio maior**: Pode impactar a segurança do paciente, integridade dos dados ou conduta do estudo
- **Violação**: Desvio grave requerendo ação e relatório imediatos

**Requisitos de Documentação:**
- Descrição do desvio
- Data de ocorrência
- ID do sujeito afetado
- Impacto em segurança e dados
- Ações corretivas e preventivas (CAPA)
- Análise de causa raiz
- Medidas preventivas implementadas

### 4. Documentação Clínica do Paciente

A documentação do paciente registra encontros clínicos, progresso e planos de cuidado. A documentação precisa apoia a continuidade do cuidado, faturamento e proteção legal.

#### Notas SOAP

As notas SOAP são o formato mais comum para notas de progresso na prática clínica.

**Estrutura:**

**S - Subjetivo**
- Sintomas e preocupações relatados pelo paciente
- História da doença atual (HDA)
- Revisão de sistemas (ROS) relevante à consulta
- Palavras do próprio paciente (use aspas quando útil)
- Exemplo: "Paciente relata piora de falta de ar nos últimos 3 dias, particularmente com esforço. Nega dor no peito, febre ou tosse."

**O - Objetivo**
- Achados clínicos mensuráveis
- Sinais vitais (temperatura, pressão arterial, frequência cardíaca, frequência respiratória, saturação de oxigênio)
- Achados do exame físico (organizados por sistema)
- Resultados laboratoriais e de imagem
- Exemplo:
  - Sinais: T 98,6°F, PA 142/88, FC 92, FR 22, SpO2 91% em ar ambiente
  - Geral: Leve desconforto respiratório
  - Cardiovascular: Ritmo regular,