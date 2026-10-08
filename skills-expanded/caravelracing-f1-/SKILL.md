# CARAVEL RACING — Regras e Memória de AI
Use a informação abaixo sobre a equipa Caravel Racing para responder a perguntas e desenvolver código para este repositório.

---

## 1. IDENTIDADE DA EQUIPA

**Nome:** Caravel Racing
**Escola:** Colégio Paulo VI
**Competição:** STEM Racing (organizada pelo CATIM)
**Diretora da escola:** Dulce Machado
**Typeface principal:** Speed Demon
**Cores oficiais:** Exploration Red (#CC000E) e Sea Rose (#EB3963)
**Website:** caravelracing.com

**Origem do nome:** O nome combina o espírito de inovação e exploração associado às caravelas portuguesas com a natureza competitiva e tecnológica do STEM Racing. O logo é composto pela letra C de Caravel (que também se assemelha a uma onda) e uma caravela, com gradiente entre as duas cores oficiais. A equipa estudou logótipos icónicos como o da Nike e identificou prioridades fundamentais: criar um forte sentido de movimento para representar velocidade e aplicar o efeito Gestalt (o cérebro percebe formas como um todo e não como elementos separados). O nome foi escolhido em inglês para maior reconhecimento internacional e para ser fácil de lembrar e pronunciar.

**Origem e Formação da Equipa:** A equipa foi formada após assistir a uma apresentação inspiradora sobre STEM Racing realizada pelo CATIM. Muitos membros já eram fãs apaixonados de Fórmula 1. A primeira atividade em equipa foi go-karting — uma excelente forma de fortalecer o espírito de equipa e experimentar a corrida em primeira mão. O objetivo da equipa é vencer, mas também desfrutar do percurso, aprender novas competências e crescer em conjunto.

**Filosofia:** "From the very beginning, one thing was clear: our goal was to win."

---

## 2. MEMBROS DA EQUIPA E FUNÇÕES

| Nome | Função | Competências |
|---|---|---|
| Mariana Santos | Team Manager & Aerodinamicista | Física, aerodinâmica, escrita e investigação em F1 |
| Martim Ferreira | CAD Engineer & Graphic Designer | Blender, desenvolvimento web, programação |
| Martim Triunfante | All-Round Engineer | Física, engenharia, criação de negócios |
| Diogo Lopes | Finance & Business Development Manager | Conceitos de F1, gestão de negócios |
| Pedro Guedes | Marketing Director | Marketing, criação de negócios |
| Francisco Silva | Resource & Logistics Manager | Materiais, técnicas de fabrico |

---

## 3. GESTÃO DO PROJETO

**Orçamento total estimado:** 6.706€ (inclui reserva de contingência de 500€, ~10%)
**Custo real incorrido:** 2.155,71€
**Orçamento de marketing:** 1.555,06€

**Fases da competição:** Final Regional → Final Nacional

**Ferramentas de gestão utilizadas:**
- Notion (tarefas e calendário)
- Microsoft Teams (professores/supervisores)
- Discord e WhatsApp (membros e mentores)
- Gmail (sponsors — comunicação formal)
- Excel (gestão financeira)

**Estrutura de qualidade:** Quality Acceptance Criteria (QAC) — cada entregável é avaliado pelo responsável da área e validado pela Team Manager antes de avançar.

**WBS (Work Breakdown Structure):** dividido em 4 secções principais — Project Management, Enterprise, Car Design, Materials and Manufacturing.

**Gantt Chart:** outubro a março, dividido em semanas.

**RACI Chart:** define Responsible, Accountable, Consulted e Informed para cada área: Car design, Car materials, Car manufacture and assemble, Engineering Portfolio, Management and Enterprise Portfolio, Marketing.

**Objetivos SMART:**
- Melhorar eficiência da equipa
- Desenvolver um portfólio mais forte
- Aumentar performance do carro
- Manter foco nos objetivos da competição
- Melhorar gestão de tempo

**Desvio de Âmbito (Scope Creep):** tarefas ou requisitos adicionais adicionados sem ajustar o calendário, recursos ou aprovação — a equipa reviu e aprovou individualmente cada alteração antes da implementação.

**Relatórios de progresso (Status reports):** foram utilizados ao longo do desenvolvimento para rever tarefas concluídas, identificar atividades pendentes e avaliar se os objetivos e prazos estavam a ser cumpridos, evitando o desvio do âmbito (scope creep).

**Gestão de riscos:** Matriz de risco com categorias R (Resource), T (Timing), S (Scope), Q (Quality) e níveis H/M/L. Riscos inesperados identificados: guerra/instabilidade geopolítica, perda de ficheiros, problemas no dia da competição, difamação/sabotagem.

**Comunicação com stakeholders:**
- Formal (Gmail): sponsors
- Standard (Discord/WhatsApp): membros e mentores — diária
- Organizada (Notion/Teams): professores e supervisores — início do ano ou quando solicitado

---

## 4. ENGENHARIA — INVESTIGAÇÃO E DECISÕES

### Objetivos de engenharia
- Conformidade total com os regulamentos
- Máxima performance possível
- Viabilidade de fabrico
- Durabilidade para todas as corridas sem reparações

### Variáveis controláveis
Geometria do carro, design das rodas, setup na pista, peso do carro, tempos de reação, mecanismo de paragem.

### Variáveis não controláveis
Setup da pista, diferenças entre canisters de CO₂, condições atmosféricas, mecanismo de arranque, ruído.

### Canister de CO₂
- Única fonte de propulsão
- Aplica impulso durante ~0,3 segundos (~1/3 do comprimento da pista)
- O impulso deve ser direcionado pelo centro de gravidade do carro
- No carro dos Regionais: centro de massa 6mm abaixo do vetor de impulso
- No carro dos Nacionais: reduzido para 5,2mm
- Inclinação da câmara de 0,5° testada (reduzia para 4,86mm) mas descartada — cria componente normal de força

### Rolamentos (Bearings)
**Tipo selecionado:** Rolamentos cerâmicos híbridos — esferas de nitreto de silício (Si₃N₄) + anéis de zircónia (ZrO₂) + gaiola de PTFE
**Dimensão:** 4×9×2,5 mm
**Razão:** Menor densidade (reduz inércia rotacional), menor coeficiente de atrito, esferas mais leves reduzem forças centrífugas, anéis de zircónia garantem integridade durante as corridas

**Comparação de materiais (rolamentos):**
| Material | Densidade (g/cm³) | Módulo de Young (GPa) | Dureza (HV) | Coef. Atrito |
|---|---|---|---|---|
| Aço Inoxidável | ~7,8 | ~210 | 700–800 | 0,6–0,8 |
| Zircónia (ZrO₂) | ~6,0 | ~200 | 1200–1300 | 0,2–0,3 |
| Nitreto de Silício (Si₃N₄) | ~3,2 | ~310 | 1500–1800 | 0,1–0,2 |

### Rodas
**Material selecionado:** PEEK (Polyether ether ketone) — Ketron PEEK 1000
**Processo de fabrico:** CNC Machining (máxima concentricidade)
**Diâmetro:** 28mm (mínimo legal)
**Largura:** 13mm frente / 17mm traseiras
**Espessura da parede exterior:** 0,5mm

**Modelos de roda testados (FEA em Fusion 360 a 1600 rad/s ≈ 80km/h):**
| Design | Peso (g) | Inércia (g·mm²) | Deformação máx. (µm) | Tensão máx. (MPa) |
|---|---|---|---|---|
| 9 Colunas (Regionais) | 1,846 | 299,843 | 2,41 | 0,74 |
| Favo de mel | 1,87 | 302,473 | 1,585 | 0,743 |
| 6 Furos | 1,839 | 295,28 | 1,714 | 0,624 |
| 6 Colunas | 1,213 | 205,59 | 3,504 | 1,193 |
| **6 Colunas Finas (FINAL)** | **1,145** | **199,869** | **3,508** | **1,137** |

**Wheel caps:** adicionados após CFD mostrar turbulência sem eles — reduz drag.

---

## 5. ENGENHARIA — SOFTWARE E SIMULAÇÃO

**Software CAD:** Fusion 360
**Software CFD/FEA:** ANSYS Discovery

**Parâmetros das simulações CFD:**
- Velocidade do ar: 20 m/s
- Densidade do ar: 1,225 kg/m³
- Temperatura: 22°C
- Fidelidade: 2,26–2,28 mm

**Ferramentas CAD usadas:** Loft (com guide rails), Sweep, Intersection Curve

**Qualidade de superfície CAD:** objetivo G2/G3 (curvatura contínua). Regionais: G1 (padrão "V" em Zebra Stripes). Nacionais: melhorado para padrão "U".

**Offset entre superfícies:** 0,1mm para garantir montagem com cola.

---

## 6. ENGENHARIA — DESIGN DO CARRO

### Conceito — Biomimética (Nacionais): "Caravel Falcon"
Inspirado no Falcão-Peregrino (390 km/h) e no Martim-pescador (bico não cria ondas na água).

**Forma do corpo:** teardrop shape, ponto mais largo a ~33% do comprimento.

### Evolução CFD dos componentes:

**Corpo principal:**
| Versão | Drag (N) | Lift (N) |
|---|---|---|
| Regionais (base) | 0,298 | -0,0147 |
| Caravel Falcon (base Nacional) | 0,212 | -0,0182 |

**Sidepods testados:**
| Variante | Drag (N) | Lift (N) |
|---|---|---|
| Com asas | 0,214 | -0,0272 |
| Com túneis | 0,23 | -0,0177 |
| Sidepod mais largo | 0,221 | -0,0367 |
| Sidepod mais fino | — | — |
| Silhueta do Falcão (FINAL) | 0,192 | 0,00676 |

**Asa dianteira (com rampas):** 0,212N → 0,201N

**Nariz (alto e largo):** 0,212N → 0,196N

**Carro Final — Caravel Cabral:**
- Drag: 0,168 N | Lift: 0,0654 N
- Drag Coefficient: 0,33 (vs 0,53 nos Regionais) — **redução de 40%**
- Combinação: asa traseira e dianteira pontiagudas, dianteira com rampas, sem rearpods, silhueta de falcão

---

## 7. ENGENHARIA — FABRICO

### Impressão 3D
- **Material:** ASA (outsourcing)
- **Infill:** 20% para peças sem forças elevadas (asas, capacete, wheel caps); 100% para suportes de rodas e halo
- **Tipo de infill:** honeycomb
- **Vapor Smoothing:** aplicado com vapores de acetona nas asas, halo e capacete
- **Endplate da asa dianteira:** ângulo corrigido para 90° para viabilizar impressão

### CNC
- **Parceiro:** Ricardo & Barbosa, Lda.
- **Máquina:** 5 eixos
- **Tolerâncias:** +0,2mm adicionado a todas as superfícies
- **Material do corpo:** bloco de modelo (milled)
- **Rodas e suportes:** PEEK via CNC

### Processo de acabamento
1. Fresagem CNC → serrar excesso → lixar (400 → 1000 grit)
2. Primer (aplicado 3×, lixado com 600 e 1000 grit)
3. Tinta automóvel (preto + vermelho, com fita de máscara)
4. Decalques transferidos com água
5. Verniz final

### Jig de montagem
- Impresso em PLA
- Garante alinhamento das rodas (paralelas entre si e perpendiculares ao plano médio)
- Tolerâncias de -0,2mm onde necessário
- Verifica regulamentos de visibilidade de cima

### Jig de rolamentos (Nacionais)
- Pilar que encaixa o rolamento; a roda desliza sobre ele
- Tampa guia para pressão uniforme → evita desalinhamento

### Segurança no trabalho
| Risco | Causa | Prob. | Impacto | Score | Controlo |
|---|---|---|---|---|---|
| Irritação pele/olhos/pulmões | Acetona (vapor smoothing) | 3 | 4 | 12 | Área ventilada, óculos, luvas nitrilo, máscara com filtro orgânico |
| Inalação de fumos de tinta | Pintura e verniz | 3 | 3 | 9 | Área ventilada, máscara com filtro |
| Inalação de pó de lixagem | Lixagem a seco | 3 | 3 | 9 | Máscara de pó |
| Cortes na pele | Lâminas | 1 | 2 | 2 | Dedos afastados das lâminas |

---

## 8. ENTERPRISE — PATROCÍNIOS

**Hierarquia de patrocínio (nomes inspirados na tripulação de uma caravela):**
- **Sailor (0–150€):** menção e publicidade nas redes sociais
- **Helmsman (150–400€):** redes sociais + logo no uniforme
- **Master (400–700€):** redes sociais + logo no uniforme + logo no carro
- **Captain (+700€):** máxima visibilidade, logo destacado no carro, uniforme, stand, menções em apresentações

**Patrocinadores principais:**
- **Manuport Logistics** — apoio financeiro (compra de rolamentos, rodas, asas) + promoção da marca
- **Areus** — orientação técnica CNC + promoção da marca
- **Tintas Ponte Real** — fornecimento de tinta + promoção da marca
- A Oficina Gondomar, Gondoonda, TPGL Transportes Portuários, VHP, Umbicap, CACAO Civil Engineering, Invictad, Ricardo&Barbosa, Proporto, Challenge Team (entre outros)

**Estratégia de abordagem:** priorizar empresas ligadas a engenharia e tecnologia automóvel; argumento-chave: relevância da audiência (estudantes prestes a entrar no mercado automóvel).

**Posições no carro (por valor):** 7 posições (0–6); posição 0 reservada pelos regulamentos; posição 1 a mais valiosa para patrocinadores.

**ROI medido por:** área e visibilidade de logo no carro, menções nas redes sociais, presença no stand.

---

## 9. ENTERPRISE — MARKETING

### Estratégia
- Manter calendário consistente de publicações
- Conteúdo behind-the-scenes
- Parcerias com a escola (Associação de Estudantes — partilha de lucros em troca de divulgação)

### Canais
- **Instagram:** +300 seguidores; post mais bem-sucedido: 40,8K visualizações, 198 novos seguidores; estratégia: stories diários, conteúdo de valor, conteúdo interativo
- **LinkedIn:** 60 ligações, 276 impressões/semana; contactos com Mercedes-Benz e Porsche
- **Website:** caravelracing.com — portfólio, progresso, sponsors, jogo de tempo de reação (caravelracing.com/jogos), chatbot AI "NavAI" (caravelracing.com/chat)

### Atividades de marketing
- **Bake sale:** reaproveitamento de produtos de padaria; lucro superior ao esperado; visualizações maioritariamente de não-seguidores (75,2%)
- **Giveaway LEGO:** 3072 visualizações, 634 interações, 69,7% de não-seguidores
- **Canteens personalizadas:** vendidas e oferecidas a apoiantes e sponsors
- **Flyers impressos:** divulgação da final nacional e redes sociais
- **Visita ao FEUP (INEGI):** networking com engenheiros

### Ferramentas de conteúdo
Canva, Instagram, LinkedIn, CapCut (edição de vídeo)

### Persona
João Silva, estudante, 17 anos, Colégio Paulo VI, 12º ano, interesses em tecnologia, carros, projetos práticos, F1.

---

## 10. ENTERPRISE — SUSTENTABILIDADE

### Ambiental
- Materiais sustentáveis; reutilização de recursos
- Transporte público para reuniões com sponsors
- BIOfoam da BEWI para o stand (leve, moldável, sustentável)
- Limpeza de praia organizada pela equipa
- Plantação de árvores: *Liriodendron tulipifera* (crescimento rápido, alta absorção de CO₂)

### Económica
- Materiais de resíduo a preços reduzidos
- Reutilização de mesas e monitores de anos anteriores para o stand
- Reutilização de materiais do pit display dos Regionais

### Social
- Apresentações a equipas futuras da escola (após 1º lugar nos Regionais)
- Visita ao lar de acolhimento "Mãe D'Água": jogos, bolo, doação de produtos de higiene
- Contribuição para o UNICEF Special Survival Kit
- Combate a conta falsa no Instagram: denúncia rápida, aviso aos seguidores, conta removida com sucesso

---

## 11. STAND (Final Nacional)

**Conceito:** fusão de caravela portuguesa com motorsport moderno — formas fluidas (exploração/mar) + linhas angulares (velocidade).

**Elemento central:** estrutura de caravela construída sobre a mesa existente, coberta com BIOfoam esculpido e pintado — usada para expor e guardar os carros, com "buraco de canhão" como prateleira.

**Fundo do stand inclui:**
- Logo e identidade visual
- Design e desenvolvimento do carro
- Jig de rodas e processo de fabrico
- Marketing e sustentabilidade
- Timeline do projeto
- Chatbot AI personalizado
- Patrocinadores e parcerias
- Membros e funções
- Estatísticas de redes sociais

**Iluminação:** simula reflexo de água, reforçando o tema marítimo.

---

## 12. RESULTADOS E CONQUISTAS

- **1º Lugar na Final Regional** de STEM Racing
- Drag coefficient reduzido **40%** entre Regionais e Nacionais (0,53 → 0,33)
- Conta falsa no Instagram identificada e removida com sucesso
- NavAI atingiu capacidade máxima de engagement nas primeiras horas após lançamento
- Post mais visto: 40,8K visualizações
- Giveaway LEGO: 3.072 visualizações
- 198 novos seguidores ganhos em 1 mês
- Bake sale: procura superou as expectativas, produção expandida de urgência
- Manuport Logistics confirmou ROI dentro das expetativas e comprometeu-se a continuar para a Final Mundial
