---
name: pylabrobot
description: Kit de ferramentas de automação laboratorial para controlar manipuladores de líquidos, leitores de placas, bombas, agitadores com aquecimento, incubadoras, centrífugas e equipamentos analíticos. Use essa habilidade ao automatizar fluxos de trabalho laboratoriais, programar robôs manipuladores de líquidos (Hamilton STAR, Opentrons OT-2, Tecan EVO), integrar equipamentos de laboratório, gerenciar layouts de plataforma e recursos (placas, ponteiras, containers), ler placas ou criar protocolos laboratoriais reproduzíveis. Aplicável para protocolos simulados e controle de hardware físico.
---

# PyLabRobot

## Visão Geral

PyLabRobot é um Software Development Kit Python puro agnóstico quanto ao hardware para laboratórios automatizados e autônomos. Use essa habilidade para controlar robôs manipuladores de líquidos, leitores de placas, bombas, agitadores com aquecimento, incubadoras, centrífugas e outros equipamentos de automação laboratorial através de uma interface Python unificada que funciona em diferentes plataformas (Windows, macOS, Linux).

## Quando Usar Essa Habilidade

Use essa habilidade quando:
- Programar robôs manipuladores de líquidos (Hamilton STAR/STARlet, Opentrons OT-2, Tecan EVO)
- Automatizar fluxos de trabalho laboratoriais envolvendo pipetagem, preparação de amostras ou medições analíticas
- Gerenciar layouts de plataforma e recursos laboratoriais (placas, ponteiras, containers, calhas)
- Integrar múltiplos dispositivos de laboratório (manipuladores de líquidos, leitores de placas, agitadores com aquecimento, bombas)
- Criar protocolos laboratoriais reproduzíveis com gerenciamento de estado
- Simular protocolos antes de executar em hardware físico
- Ler placas usando BMG CLARIOstar ou outros leitores de placas suportados
- Controlar temperatura, agitação, centrifugação ou outras operações de manipulação de materiais
- Trabalhar com automação laboratorial em Python

## Capacidades Principais

PyLabRobot oferece automação laboratorial abrangente através de seis áreas de capacidade principais, cada uma detalhada no diretório references/:

### 1. Manipulação de Líquidos (`references/liquid-handling.md`)

Controle robôs manipuladores de líquidos para aspirar, dispensar e transferir líquidos. As operações principais incluem:
- **Operações Básicas**: Aspirar, dispensar, transferir líquidos entre poços
- **Gerenciamento de Ponteiras**: Apanhar, descartar e rastrear ponteiras de pipeta automaticamente
- **Técnicas Avançadas**: Pipetagem multi-canal, diluições seriadas, replicação de placas
- **Rastreamento de Volume**: Rastreamento automático de volumes de líquido em poços
- **Suporte a Hardware**: Hamilton STAR/STARlet, Opentrons OT-2, Tecan EVO e outros

### 2. Gerenciamento de Recursos (`references/resources.md`)

Gerencie recursos laboratoriais em um sistema hierárquico:
- **Tipos de Recursos**: Placas, racks de ponteiras, calhas, tubos, carriers e labware customizado
- **Layout de Plataforma**: Atribua recursos a posições da plataforma com sistemas de coordenadas
- **Gerenciamento de Estado**: Rastreie presença de ponteiras, volumes de líquido e estados de recursos
- **Serialização**: Salve e carregue layouts de plataforma e estados de arquivos JSON
- **Descoberta de Recursos**: Acesse poços, ponteiras e containers através de APIs intuitivas

### 3. Backends de Hardware (`references/hardware-backends.md`)

Conecte-se a equipamentos laboratoriais diversos através de abstração de backend:
- **Manipuladores de Líquidos**: Hamilton STAR (suporte completo), Opentrons OT-2, Tecan EVO
- **Simulação**: ChatterboxBackend para teste de protocolos sem hardware
- **Suporte de Plataforma**: Funciona em Windows, macOS, Linux e Raspberry Pi
- **Alternância de Backend**: Altere robôs trocando backend sem reescrever protocolos

### 4. Equipamentos Analíticos (`references/analytical-equipment.md`)

Integre leitores de placas e instrumentos analíticos:
- **Leitores de Placas**: BMG CLARIOstar para absorbância, luminescência, fluorescência
- **Balanças**: Integração com Mettler Toledo para medições de massa
- **Padrões de Integração**: Combine manipuladores de líquidos com equipamentos analíticos
- **Fluxos de Trabalho Automatizados**: Mova placas entre dispositivos automaticamente

### 5. Manipulação de Materiais (`references/material-handling.md`)

Controle equipamentos de manipulação de materiais e ambientais:
- **Agitadores com Aquecimento**: Hamilton HeaterShaker, Inheco ThermoShake
- **Incubadoras**: Incubadoras Inheco e Thermo Fisher com controle de temperatura
- **Centrífugas**: Agilent VSpin com posicionamento de balde e controle de rotação
- **Bombas**: Cole Parmer Masterflex para operações de bombeamento de fluidos
- **Controle de Temperatura**: Configure e monitore temperaturas durante protocolos

### 6. Visualização & Simulação (`references/visualization.md`)

Visualize e simule protocolos laboratoriais:
- **Visualizador em Navegador**: Visualização 3D em tempo real do estado da plataforma
- **Modo Simulação**: Teste protocolos sem hardware físico
- **Rastreamento de Estado**: Monitore presença de ponteiras e volumes de líquido visualmente
- **Editor de Plataforma**: Ferramenta gráfica para projetar layouts de plataforma
- **Validação de Protocolo**: Verifique protocolos antes de executar em hardware

## Início Rápido

Para começar com PyLabRobot, instale o pacote e inicialize um manipulador de líquidos:

```python
# Instale PyLabRobot
# uv pip install pylabrobot

# Configuração básica de manipulação de líquidos
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import STAR
from pylabrobot.resources import STARLetDeck

# Inicialize manipulador de líquidos
lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
await lh.setup()

# Operações básicas
await lh.pick_up_tips(tip_rack["A1:H1"])
await lh.aspirate(plate["A1"], vols=100)
await lh.dispense(plate["A2"], vols=100)
await lh.drop_tips()
```

## Trabalhando com Referências

Essa habilidade organiza informações detalhadas em múltiplos arquivos de referência. Carregue a referência relevante quando:
- **Manipulação de Líquidos**: Escrever protocolos de pipetagem, gerenciamento de ponteiras, transferências
- **Recursos**: Definir layouts de plataforma, gerenciar placas/ponteiras, labware customizado
- **Backends de Hardware**: Conectar a robôs específicos, alternar plataformas
- **Equipamentos Analíticos**: Integrar leitores de placas, balanças ou dispositivos analíticos
- **Manipulação de Materiais**: Usar agitadores com aquecimento, incubadoras, centrífugas, bombas
- **Visualização**: Simular protocolos, visualizar estados da plataforma

Todos os arquivos de referência podem ser encontrados no diretório `references/` e contêm exemplos abrangentes, padrões de uso de API e melhores práticas.

## Melhores Práticas

Ao criar protocolos de automação laboratorial com PyLabRobot:

1. **Comece com Simulação**: Use ChatterboxBackend e o visualizador para testar protocolos antes de executar em hardware
2. **Ative Rastreamento**: Ative rastreamento de ponteiras e rastreamento de volume para gerenciamento preciso de estado
3. **Nomenclatura de Recursos**: Use nomes claros e descritivos para todos os recursos (placas, racks de ponteiras, containers)
4. **Serialização de Estado**: Salve layouts de plataforma e estados em JSON para reproduzibilidade
5. **Tratamento de Erros**: Implemente tratamento apropriado de erros assíncronos para operações de hardware
6. **Controle de Temperatura**: Configure temperaturas cedo pois aquecimento/resfriamento leva tempo
7. **Protocolos Modulares**: Divida fluxos de trabalho complexos em funções reutilizáveis
8. **Documentação**: Consulte docs oficiais em https://docs.pylabrobot.org para recursos mais recentes

## Fluxos de Trabalho Comuns

### Protocolo de Transferência de Líquido

```python
# Configuração
lh = LiquidHandler(backend=STAR(), deck=STARLetDeck())
await lh.setup()

# Defina recursos
tip_rack = TIP_CAR_480_A00(name="tip_rack")
source_plate = Cos_96_DW_1mL(name="source")
dest_plate = Cos_96_DW_1mL(name="dest")

lh.deck.assign_child_resource(tip_rack, rails=1)
lh.deck.assign_child_resource(source_plate, rails=10)
lh.deck.assign_child_resource(dest_plate, rails=15)

# Protocolo de transferência
await lh.pick_up_tips(tip_rack["A1:H1"])
await lh.transfer(source_plate["A1:H12"], dest_plate["A1:H12"], vols=100)
await lh.drop_tips()
```

### Fluxo de Trabalho de Leitura de Placa

```python
# Configure leitor de placa
from pylabrobot.plate_reading import PlateReader
from pylabrobot.plate_reading.clario_star_backend import CLARIOstarBackend

pr = PlateReader(name="CLARIOstar", backend=CLARIOstarBackend())
await pr.setup()

# Configure temperatura e leia
await pr.set_temperature(37)
await pr.open()
# (carregue placa manualmente ou roboticamente)
await pr.close()
data = await pr.read_absorbance(wavelength=450)
```

## Recursos Adicionais

- **Documentação Oficial**: https://docs.pylabrobot.org
- **Repositório GitHub**: https://github.com/PyLabRobot/pylabrobot
- **Fórum da Comunidade**: https://discuss.pylabrobot.org
- **Pacote PyPI**: https://pypi.org/project/PyLabRobot/

Para uso detalhado de capacidades específicas, consulte o arquivo de referência correspondente no diretório `references/`.