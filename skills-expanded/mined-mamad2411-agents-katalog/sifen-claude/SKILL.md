# pysifen — Diretrizes do Projeto

## Visão Geral

Biblioteca Python que gera automaticamente bindings (dataclasses) a partir dos schemas XSD oficiais do **SIFEN** (Sistema Integrado de Facturación Electrónica Nacional) do Paraguai, usando **xsdata**, no mesmo padrão da [nfelib](https://github.com/akretion/nfelib) da Akretion.

**Princípio central:** Zero código manual para o schema. Todo binding é gerado pelo xsdata a partir dos XSD oficiais da SET. Código escrito à mão se limita ao `CommonMixin`, `assinatura`, `transmissao`, testes e scripts de geração.

## Metadados

- **Licença:** MIT
- **Copyright:** KMEE
- **Autor:** mileo
- **GitHub:** `KMEE/pysifen`
- **Python:** >=3.10
- **Dependência principal:** xsdata

## Estrutura do Projeto

```
pysifen/
├── .xsdata.xml                    # Configuração do xsdata (originalCase, CommonMixin extension)
├── pyproject.toml                 # Build config (setuptools)
├── script.sh                      # Script de geração de bindings
├── README.md
├── MIT-LICENSE
├── pysifen/
│   ├── __init__.py                # __version__ = "0.1.0"
│   ├── CommonMixin.py             # Mixin: from_xml, to_xml, from_path, validate_xml, sign_xml
│   ├── assinatura.py              # sign_xml() — signxml direto com RSA-SHA256
│   ├── de/                        # Documento Electrónico
│   │   ├── schemas/v150/          # XSD originais da SET (com schemaLocation local)
│   │   ├── bindings/v150/         # Bindings gerados pelo xsdata (NÃO editar manualmente)
│   │   └── samples/v150/          # XMLs de exemplo para testes
│   └── transmissao/               # Transmissão SOAP ao SIFEN
│       ├── __init__.py            # Exports: TransmissaoDE, ConsultaSIFEN, TransmissaoEvento
│       ├── base.py                # TransmissaoBase: SOAP client, mTLS, serialização
│       ├── config.py              # Endpoints produção/teste, get_endpoint()
│       ├── de.py                  # TransmissaoDE: enviar_de(), enviar_lote()
│       ├── consulta.py            # ConsultaSIFEN: consultar_de(), consultar_lote(), consultar_ruc()
│       └── evento.py              # TransmissaoEvento: enviar_evento()
├── tests/
│   ├── test_cert.pfx              # Certificado de teste (senha: test1234)
│   ├── test_de.py                 # Testes de leitura/escrita DE
│   ├── test_generate_de.py        # Testes de geração programática, round-trip, validação XSD
│   ├── test_assinatura.py         # Testes de assinatura digital com signxml
│   ├── test_transmissao.py        # Testes de transmissão SOAP (mocked)
│   ├── test_eventos.py            # Testes de eventos
│   ├── test_ws.py                 # Testes de schemas WS
│   └── test_schema_versions.py    # Detecta novas versões de schemas
└── .github/workflows/tests.yml    # CI: pytest + ruff
```

## Comandos Frequentes

```bash
# Instalar em modo dev (com assinatura e testes)
pip install -e ".[sign,test]"

# Gerar/regenerar bindings (após alterar XSD ou .xsdata.xml)
./script.sh

# Rodar testes
pytest tests/ -v

# Lint
ruff check pysifen/ tests/
```

## Convenções

### Código
- **Bindings são gerados automaticamente** — NUNCA editar arquivos em `pysifen/de/bindings/` manualmente
- **FieldName originalCase** — campos mantêm nomes do XSD (ex: `iTipEmi`, `dDesTipEmi`, `gOpeDE`)
- **CommonMixin** é injetado em todas as classes via `.xsdata.xml` Extension
- **Um arquivo .py por arquivo .xsd** (Structure: filenames)
- **Assinatura centralizada** — `pysifen/assinatura.py` é o ponto único de assinatura, usado tanto por `CommonMixin.sign_xml()` quanto por `TransmissaoBase._sign_xml()`

### Schemas XSD
- Fonte oficial: `https://ekuatia.set.gov.py/sifen/xsd/`
- Namespace: `http://ekuatia.set.gov.py/sifen/xsd`
- Todos os `schemaLocation` devem usar paths relativos locais (`./DE_Types_v150.xsd`)
- Versão na pasta usa 3 dígitos: `v150` = versão 1.50 do Manual Técnico

### Versionamento de Schemas
- v150 = Manual Técnico versão 1.50
- Schemas de versões mistas coexistem na mesma pasta (DE_Types_v150, SIFEN_Types_v141, Paises_v100)
- Nova versão major (2.00) ganha pasta `v200/`

### Testes
- Framework: pytest
- Cada tipo de DE deve ter teste de leitura (parsing) e escrita (serialização)
- Testes de round-trip: XML → objeto → XML → comparar
- Samples XML em `pysifen/de/samples/v150/`
- Testes de transmissão usam mock (não fazem chamadas reais)
- Testes de assinatura usam `tests/test_cert.pfx` (senha: `test1234`)

### Estilo
- Ruff para lint (rules: E, F, I, W)
- Target: Python 3.10
- Max line length: 79 (para bindings gerados)

## Tipos de Documento Electrónico (DE)

| Tipo | Código | Descrição |
|------|--------|-----------|
| Factura Electrónica | 1 | Fatura eletrônica padrão |
| FE Exportación | 2 | Fatura de exportação |
| FE Importación | 3 | Fatura de importação |
| Autofactura | 4 | Autofatura |
| Nota de Crédito | 5 | Nota de crédito eletrônica |
| Nota de Débito | 6 | Nota de débito eletrônica |
| Nota de Remisión | 7 | Nota de remissão eletrônica |
| Comprobante de Retención | 8 | Comprovante de retenção |

## API

### Bindings (leitura/escrita)

```python
from pysifen.de.bindings.v150.fe_v141 import RDe

# Ler XML
rde = RDe.from_path("factura.xml")
rde = RDe.from_xml(xml_string)

# Navegar
rde.DE.gDatGralOpe.gEmis.dRucEm
rde.DE.gDatGralOpe.gEmis.dNomEmi

# Serializar
xml = rde.to_xml()

# Validar contra XSD
errors = rde.validate_xml()
```

### Assinatura digital (RSA-SHA256)

```python
# Via CommonMixin (em qualquer binding)
signed = rde.sign_xml(xml, pkcs12_data, password, doc_id)

# Via função direta
from pysifen.assinatura import sign_xml
signed = sign_xml(xml, pkcs12_data, password, doc_id)
```

### Transmissão SOAP

```python
from pysifen.transmissao import (
    TransmissaoDE, ConsultaSIFEN, TransmissaoEvento,
    PRODUCCION, TEST,
)

# Enviar DE
t = TransmissaoDE(ambiente=TEST, pkcs12_data=cert, pkcs12_password=pwd)
resultado = t.enviar_de(rde)

# Enviar lote (máx 50 DEs)
resultado = t.enviar_lote([rde1, rde2, rde3])

# Consultar DE por CDC
c = ConsultaSIFEN(ambiente=TEST, pkcs12_data=cert, pkcs12_password=pwd)
resultado = c.consultar_de(cdc_44_digitos)

# Consultar RUC
resultado = c.consultar_ruc("80069563")

# Enviar evento
e = TransmissaoEvento(ambiente=TEST, pkcs12_data=cert, pkcs12_password=pwd)
resultado = e.enviar_evento(evento)
```

## Dependências Opcionais

- `sign`: `signxml` + `cryptography` + `lxml` — assinatura digital XML (RSA-SHA256)
- `transmissao`: `xsdata[soap]` + `signxml` + `cryptography` + `requests` + `lxml` — transmissão SOAP com mTLS
- `soap`: `xsdata[soap]` — cliente SOAP para WS da SET
- `test`: `pytest`, `pytest-cov`, `xmldiff`, `lxml`

## Referências

- XSD oficiais: https://ekuatia.set.gov.py/sifen/xsd/
- Manual Técnico v150: https://www.dnit.gov.py/documents/20123/420592/Manual+T%C3%A9cnico+Versi%C3%B3n+150.pdf
- nfelib (referência): https://github.com/akretion/nfelib
- xsdata docs: https://xsdata.readthedocs.io/
- jsifenlib (Java): https://github.com/roshkadev/rshk-jsifenlib

## Plano de Sprints

O plano detalhado está em `plano-sifenlib.md`. Resumo:

0. Setup inicial (git, pyproject.toml, .xsdata.xml) ✓
1. Download e organização dos XSD (ajustar schemaLocation para paths relativos) ✓
2. Geração dos bindings com xsdata ✓
3. XMLs de exemplo para cada tipo de DE ✓
4. Testes de leitura (parsing) ✓
5. Testes de escrita (serialização + round-trip) ✓
6. Detecção automática de atualizações de schema ✓
7. Documentação, README, CI/CD, publicação PyPI ✓
8. Assinatura digital com signxml (RSA-SHA256) ✓
9. Transmissão SOAP (envio DE, lote, consultas, eventos) ✓
10. Funcionalidades avançadas (CDC, QR Code, KuDE, integração Odoo)
