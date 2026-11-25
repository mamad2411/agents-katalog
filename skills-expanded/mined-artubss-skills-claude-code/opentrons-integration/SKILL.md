---
name: opentrons-integration
description: "Plataforma de automação laboratorial para robôs Flex/OT-2. Escreva protocolos Protocol API v2, manipulação de líquidos, módulos de hardware (heater-shaker, thermocycler), gestão de labware, para workflows de pipetagem automatizados."
---

# Integração Opentrons

## Visão Geral

Opentrons é uma plataforma de automação laboratorial baseada em Python para robôs Flex e OT-2. Escreva protocolos Protocol API v2 para manipulação de líquidos, controle de módulos de hardware (temperatura, magnético, heater-shaker, thermocycler), gestão de labware, para workflows de pipetagem automatizados.

## Quando Usar Esta Skill

Esta skill deve ser usada quando:
- Escrevendo protocolos Protocol API v2 da Opentrons em Python
- Automatizando workflows de manipulação de líquidos em robôs Flex ou OT-2
- Controlando módulos de hardware (temperatura, magnético, heater-shaker, thermocycler)
- Configurando layouts de labware e deck
- Implementando operações complexas de pipetagem (diluições seriadas, replicação de placas, setup de PCR)
- Gerenciando uso de tips e otimizando eficiência de protocolos
- Trabalhando com pipetas multicanal para operações em placas de 96 poços
- Simulando e testando protocolos antes da execução no robô

## Capacidades Principais

### 1. Estrutura de Protocolo e Metadados

Todo protocolo Opentrons segue uma estrutura padrão:

```python
from opentrons import protocol_api

# Metadados
metadata = {
    'protocolName': 'My Protocol',
    'author': 'Name <email@example.com>',
    'description': 'Protocol description',
    'apiLevel': '2.19'  # Use latest available API version
}

# Requisitos (opcional)
requirements = {
    'robotType': 'Flex',  # or 'OT-2'
    'apiLevel': '2.19'
}

# Função de execução
def run(protocol: protocol_api.ProtocolContext):
    # Protocol commands go here
    pass
```

**Elementos principais:**
- Importe `protocol_api` de `opentrons`
- Defina dicionário `metadata` com protocolName, author, description, apiLevel
- Dicionário `requirements` opcional para tipo de robô e versão da API
- Implemente função `run()` recebendo `ProtocolContext` como parâmetro
- Toda lógica do protocolo vai dentro da função `run()`

### 2. Carregando Hardware

**Carregando Instrumentos (Pipetas):**

```python
def run(protocol: protocol_api.ProtocolContext):
    # Carregue pipeta no mount específico
    left_pipette = protocol.load_instrument(
        'p1000_single_flex',  # Nome do instrumento
        'left',               # Mount: 'left' ou 'right'
        tip_racks=[tip_rack]  # Lista de objetos labware tip rack
    )
```

Nomes de pipeta comuns:
- Flex: `p50_single_flex`, `p1000_single_flex`, `p50_multi_flex`, `p1000_multi_flex`
- OT-2: `p20_single_gen2`, `p300_single_gen2`, `p1000_single_gen2`, `p20_multi_gen2`, `p300_multi_gen2`

**Carregando Labware:**

```python
# Carregue labware diretamente no deck
plate = protocol.load_labware(
    'corning_96_wellplate_360ul_flat',  # Nome API do labware
    'D1',                                # Slot do deck (Flex: A1-D3, OT-2: 1-11)
    label='Sample Plate'                 # Label opcional para exibição
)

# Carregue tip rack
tip_rack = protocol.load_labware('opentrons_flex_96_tiprack_1000ul', 'C1')

# Carregue labware em adaptador
adapter = protocol.load_adapter('opentrons_flex_96_tiprack_adapter', 'B1')
tips = adapter.load_labware('opentrons_flex_96_tiprack_200ul')
```

**Carregando Módulos:**

```python
# Módulo de temperatura
temp_module = protocol.load_module('temperature module gen2', 'D3')
temp_plate = temp_module.load_labware('corning_96_wellplate_360ul_flat')

# Módulo magnético
mag_module = protocol.load_module('magnetic module gen2', 'C2')
mag_plate = mag_module.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')

# Módulo heater-shaker
hs_module = protocol.load_module('heaterShakerModuleV1', 'D1')
hs_plate = hs_module.load_labware('corning_96_wellplate_360ul_flat')

# Módulo thermocycler (ocupa slots específicos automaticamente)
tc_module = protocol.load_module('thermocyclerModuleV2')
tc_plate = tc_module.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')
```

### 3. Operações de Manipulação de Líquidos

**Operações Básicas:**

```python
# Pegue um tip
pipette.pick_up_tip()

# Aspire (puxe líquido)
pipette.aspirate(
    volume=100,           # Volume em µL
    location=source['A1'] # Poço ou objeto location
)

# Dispense (libere líquido)
pipette.dispense(
    volume=100,
    location=dest['B1']
)

# Solte o tip
pipette.drop_tip()

# Retorne o tip ao rack
pipette.return_tip()
```

**Operações Complexas:**

```python
# Transfer (combina pick_up, aspirate, dispense, drop_tip)
pipette.transfer(
    volume=100,
    source=source_plate['A1'],
    dest=dest_plate['B1'],
    new_tip='always'  # 'always', 'once', ou 'never'
)

# Distribute (uma fonte para múltiplos destinos)
pipette.distribute(
    volume=50,
    source=reservoir['A1'],
    dest=[plate['A1'], plate['A2'], plate['A3']],
    new_tip='once'
)

# Consolidate (múltiplas fontes para um destino)
pipette.consolidate(
    volume=50,
    source=[plate['A1'], plate['A2'], plate['A3']],
    dest=reservoir['A1'],
    new_tip='once'
)
```

**Técnicas Avançadas:**

```python
# Mix (aspire e dispense no mesmo local)
pipette.mix(
    repetitions=3,
    volume=50,
    location=plate['A1']
)

# Air gap (previne gotejamento)
pipette.aspirate(100, source['A1'])
pipette.air_gap(20)  # 20µL air gap
pipette.dispense(120, dest['A1'])

# Blow out (expele líquido restante)
pipette.blow_out(location=dest['A1'].top())

# Touch tip (remove gotículas na parte externa do tip)
pipette.touch_tip(location=plate['A1'])
```

**Controle de Taxa de Fluxo:**

```python
# Configure taxas de fluxo (µL/s)
pipette.flow_rate.aspirate = 150
pipette.flow_rate.dispense = 300
pipette.flow_rate.blow_out = 400
```

### 4. Acessando Poços e Localizações

**Métodos de Acesso a Poços:**

```python
# Por nome
well_a1 = plate['A1']

# Por índice
first_well = plate.wells()[0]

# Todos os poços
all_wells = plate.wells()  # Retorna lista

# Por linhas
rows = plate.rows()  # Retorna lista de listas
row_a = plate.rows()[0]  # Todos os poços da linha A

# Por colunas
columns = plate.columns()  # Retorna lista de listas
column_1 = plate.columns()[0]  # Todos os poços da coluna 1

# Poços por nome (dicionário)
wells_dict = plate.wells_by_name()  # {'A1': Well, 'A2': Well, ...}
```

**Métodos de Localização:**

```python
# Topo do poço (padrão: 1mm abaixo do topo)
pipette.aspirate(100, well.top())
pipette.aspirate(100, well.top(z=5))  # 5mm acima do topo

# Fundo do poço (padrão: 1mm acima do fundo)
pipette.aspirate(100, well.bottom())
pipette.aspirate(100, well.bottom(z=2))  # 2mm acima do fundo

# Centro do poço
pipette.aspirate(100, well.center())
```

### 5. Controle de Módulos de Hardware

**Módulo de Temperatura:**

```python
# Configure temperatura
temp_module.set_temperature(celsius=4)

# Aguarde a temperatura
temp_module.await_temperature(celsius=4)

# Desative
temp_module.deactivate()

# Verifique status
current_temp = temp_module.temperature  # Temperatura atual
target_temp = temp_module.target  # Temperatura alvo
```

**Módulo Magnético:**

```python
# Engaje (levante os ímãs)
mag_module.engage(height_from_base=10)  # mm da base do labware

# Desengaje (abaixe os ímãs)
mag_module.disengage()

# Verifique status
is_engaged = mag_module.status  # 'engaged' ou 'disengaged'
```

**Módulo Heater-Shaker:**

```python
# Configure temperatura
hs_module.set_target_temperature(celsius=37)

# Aguarde a temperatura
hs_module.wait_for_temperature()

# Configure velocidade de agitação
hs_module.set_and_wait_for_shake_speed(rpm=500)

# Feche a trava do labware
hs_module.close_labware_latch()

# Abra a trava do labware
hs_module.open_labware_latch()

# Desative o aquecedor
hs_module.deactivate_heater()

# Desative o agitador
hs_module.deactivate_shaker()
```

**Módulo Thermocycler:**

```python
# Abra a tampa
tc_module.open_lid()

# Feche a tampa
tc_module.close_lid()

# Configure temperatura da tampa
tc_module.set_lid_temperature(celsius=105)

# Configure temperatura do bloco
tc_module.set_block_temperature(
    temperature=95,
    hold_time_seconds=30,
    hold_time_minutes=0.5,
    block_max_volume=50  # µL por poço
)

# Execute perfil (PCR cycling)
profile = [
    {'temperature': 95, 'hold_time_seconds': 30},
    {'temperature': 57, 'hold_time_seconds': 30},
    {'temperature': 72, 'hold_time_seconds': 60}
]
tc_module.execute_profile(
    steps=profile,
    repetitions=30,
    block_max_volume=50
)

# Desative
tc_module.deactivate_lid()
tc_module.deactivate_block()
```

**Leitor de Placa de Absorbância:**

```python
# Inicialize e leia
result = plate_reader.read(wavelengths=[450, 650])

# Acesse as leituras
absorbance_data = result  # Dicionário com chaves de comprimento de onda
```

### 6. Rastreamento de Líquidos e Etiquetagem

**Defina Líquidos:**

```python
# Defina tipos de líquido
water = protocol.define_liquid(
    name='Water',
    description='Ultrapure water',
    display_color='#0000FF'  # Código de cor hexadecimal
)

sample = protocol.define_liquid(
    name='Sample',
    description='Cell lysate sample',
    display_color='#FF0000'
)
```

**Carregue Líquidos em Poços:**

```python
# Carregue líquido em poços específicos
reservoir['A1'].load_liquid(liquid=water, volume=50000)  # µL
plate['A1'].load_liquid(liquid=sample, volume=100)

# Marque poços como vazios
plate['B1'].load_empty()
```

### 7. Controle de Protocolo e Utilitários

**Controle de Execução:**

```python
# Pause o protocolo
protocol.pause(msg='Replace tip box and resume')

# Atraso
protocol.delay(seconds=60)
protocol.delay(minutes=5)

# Comentário (aparece nos logs)
protocol.comment('Starting serial dilution')

# Retorne o robô à posição de repouso
protocol.home()
```

**Lógica Condicional:**

```python
# Verifique se está simulando
if protocol.is_simulating():
    protocol.comment('Running in simulation mode')
else:
    protocol.comment('Running on actual robot')
```

**Rail Lights (apenas Flex):**

```python
# Ligue as luzes
protocol.set_rail_lights(on=True)

# Desligue as luzes
protocol.set_rail_lights(on=False)
```

### 8. Pipetagem Multicanal e 8-Canais

Ao usar pipetas multicanal:

```python
# Carregue pipeta 8-canais
multi_pipette = protocol.load_instrument(
    'p300_multi_gen2',
    'left',
    tip_racks=[tips]
)

# Acesse a coluna inteira com referência de um único poço
multi_pipette.transfer(
    volume=100,
    source=source_plate['A1'],  # Acessa coluna inteira 1
    dest=dest_plate['A1']       # Dispensa para coluna inteira 1
)

# Use rows() para operações linha a linha
for row in plate.rows():
    multi_pipette.transfer(100, reservoir['A1'], row[0])
```

### 9. Padrões Comuns de Protocolo

**Diluição Seriada:**

```python
def run(protocol: protocol_api.ProtocolContext):
    # Carregue labware
    tips = protocol.load_labware('opentrons_flex_96_tiprack_200ul', 'D1')
    reservoir = protocol.load_labware('nest_12_reservoir_15ml', 'D2')
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 'D3')

    # Carregue pipeta
    p300 = protocol.load_instrument('p300_single_flex', 'left', tip_racks=[tips])

    # Adicione diluente para todos os poços exceto o primeiro
    p300.transfer(100, reservoir['A1'], plate.rows()[0][1:])

    # Diluição seriada através da linha
    p300.transfer(
        100,
        plate.rows()[0][:11],  # Fonte: poços 0-10
        plate.rows()[0][1:],   # Destino: poços 1-11
        mix_after=(3, 50),     # Mix 3x com 50µL após dispensar
        new_tip='always'
    )
```

**Replicação de Placa:**

```python
def run(protocol: protocol_api.ProtocolContext):
    # Carregue labware
    tips = protocol.load_labware('opentrons_flex_96_tiprack_1000ul', 'C1')
    source = protocol.load_labware('corning_96_wellplate_360ul_flat', 'D1')
    dest = protocol.load_labware('corning_96_wellplate_360ul_flat', 'D2')

    # Carregue pipeta
    p1000 = protocol.load_instrument('p1000_single_flex', 'left', tip_racks=[tips])

    # Transfira de todos os poços em source para dest
    p1000.transfer(
        100,
        source.wells(),
        dest.wells(),
        new_tip='always'
    )
```

**Setup de PCR:**

```python
def run(protocol: protocol_api.ProtocolContext):
    # Carregue thermocycler
    tc_mod = protocol.load_module('thermocyclerModuleV2')
    tc_plate = tc_mod.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')

    # Carregue tips e reagentes
    tips = protocol.load_labware('opentrons_flex_96_tiprack_200ul', 'C1')
    reagents = protocol.load_labware('opentrons_24_tuberack_nest_1.5ml_snapcap', 'D1')

    # Carregue pipeta
    p300 = protocol.load_instrument('p300_single_flex', 'left', tip_racks=[tips])

    # Abra a tampa do thermocycler
    tc_mod.open_lid()

    # Distribua master mix
    p300.distribute(
        20,
        reagents['A1'],
        tc_plate.wells(),
        new_tip='once'
    )

    # Adicione amostras (exemplo para os 8 primeiros poços)
    for i, well in enumerate(tc_plate.wells()[:8]):
        p300.transfer(5, reagents.wells()[i+1], well, new_tip='always')

    # Execute PCR
    tc_mod.close_lid()
    tc_mod.set_lid_temperature(105)

    # Perfil de PCR
    tc_mod.set_block_temperature(95, hold_time_seconds=180)

    profile = [
        {'temperature': 95, 'hold_time_seconds': 15},
        {'temperature': 60, 'hold_time_seconds': 30},
        {'temperature': 72, 'hold_time_seconds': 30}
    ]
    tc_mod.execute_profile(steps=profile, repetitions=35, block_max_volume=25)

    tc_mod.set_block_temperature(72, hold_time_minutes=5)
    tc_mod.set_block_temperature(4)

    tc_mod.deactivate_lid()
    tc_mod.open_lid()
```

## Melhores Práticas

1. **Sempre especifique nível de API**: Use a versão estável mais recente nos metadados
2. **Use labels significativos**: Etiquete labware para identificação mais fácil nos logs
3. **Verifique disponibilidade de tips**: Certifique-se de que há tips suficientes para conclusão do protocolo
4. **Adicione comentários**: Use `protocol.comment()` para debugging e logging
5. **Simule primeiro**: Sempre teste protocolos em simulação antes de executar no robô
6. **Trate erros corretamente**: Adicione pausas para intervenção manual quando necessário
7. **Considere timing**: Use atrasos quando protocolos requerem períodos de incubação
8. **Rastreie líquidos**: Use rastreamento de líquidos para melhor validação de setup
9. **Otimize uso de tips**: Use `new_tip='once'` quando apropriado para economizar tips
10. **Controle taxas de fluxo**: Ajuste taxas de fluxo para líquidos viscosos ou voláteis

## Solução de Problemas

**Problemas Comuns:**

- **Fora de tips**: Verifique se a capacidade do tip rack corresponde aos requisitos do protocolo
- **Colisão de labware**: Verifique o layout do deck para conflitos espaciais
- **Erros de volume**: Certifique-se de que volumes não excedem capacidades de poço ou pipeta
- **Módulo não responde**: Verifique se o módulo está conectado corretamente e o firmware está atualizado
- **Volumes imprecisos**: Calibre pipetas e verifique bolhas de ar
- **Protocolo falha em simulação**: Verifique compatibilidade de versão de API e definições de labware

## Recursos

Para documentação detalhada da API, consulte `references/api_reference.md` neste diretório de skill.

Para templates de protocolo de exemplo, consulte o diretório `scripts/`.