# Estoque Virtual - Documentação do Projeto

## 📋 Visão Geral
Sistema web moderno para processamento de Notas Fiscais Eletrônicas (NF-e) com criação de estoque virtual, integração planejada com Olist e Mercado Livre.

## 🏗️ Arquitetura

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: SQLite com SQLAlchemy ORM
- **Parser NF-e**: nfelib (XML) + pytesseract (OCR para PDF)
- **API**: RESTful com CORS habilitado

**Estrutura**:
```
backend/
├── app/
│   ├── main.py          # FastAPI app + endpoints
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   └── utils/
│       └── nfe_parser.py # Parsing de NF-e
├── database.py          # Config SQLAlchemy
└── requirements.txt
```

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: CSS puro + layout grid/flexbox
- **HTTP Client**: Axios

**Estrutura**:
```
frontend/
├── src/
│   ├── App.tsx                 # Root component
│   ├── components/
│   │   ├── UploadNFe.tsx      # Upload form
│   │   └── NotaFiscalList.tsx # List component
│   ├── services/
│   │   └── api.ts             # API client
│   └── main.tsx
└── index.html
```

## 🔄 Fases do Projeto

### ✅ Fase 1: Upload e Leitura de NF-e (Atual)
- [x] Upload de XML ou PDF
- [x] Parsing automático de dados
- [x] Criação de estoque virtual em BD
- [ ] Interface de confirmação/edição
- [ ] Alertas de divergências

### Fase 2: Quarentena e Conferência
- Aguardar conferência física
- Validação manual de quantidades

### Fase 3: Vinculação a Anúncios
- Auto-vinculação com produtos conhecidos
- Vinculação manual com aprovação

### Fase 4: Integração Olist
- API Olist (token: configurar em .env)
- Lançamento automático em marketplaces

## 🚀 Quick Start

### Backend
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
# API em: http://localhost:8000/api
# Docs: http://localhost:8000/docs
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# Frontend em: http://localhost:5173
```

## 📦 Modelos de Dados

### NotaFiscal
- `id`: Primary key
- `numero_nf`: Número único da NF
- `serie`: Série da NF
- `fornecedor`: Nome do fornecedor
- `data_emissao`: Quando foi emitida
- `data_upload`: Quando foi enviada ao sistema
- `arquivo_original`: Nome do arquivo
- `tipo_documento`: NFE ou PDF
- `status`: processando/processado/bloqueado
- `itens`: Relação com ItemEstoque

### ItemEstoque
- `id`: Primary key
- `nf_id`: Foreign key para NotaFiscal
- `codigo_produto`: SKU
- `descricao`: Nome do produto
- `quantidade_nf`: Quantidade da nota fiscal
- `quantidade_confirmada`: Qtd após conferência (null = não confirmado)
- `status`: quarentena/confirmado/bloqueado
- `divergencia`: Campo para alertas
- `data_criacao`: Timestamp

## 🔌 Endpoints Principais

### POST `/api/upload-nfe`
Upload de arquivo XML ou PDF
```json
Response: {
  "id": 1,
  "numero_nf": "123456",
  "status": "processado",
  "itens_encontrados": 5
}
```

### GET `/api/notas-fiscais`
Listar todas as NFs com paginação
```json
Response: {
  "total": 10,
  "skip": 0,
  "limit": 10,
  "items": [...]
}
```

### GET `/api/notas-fiscais/{id}`
Detalhe de uma NF com todos os itens

## 🔑 Variáveis de Ambiente

```env
DATABASE_URL=sqlite:///./estoque_virtual.db
UPLOAD_DIR=./uploads
ALLOWED_EXTENSIONS=xml,pdf
MAX_FILE_SIZE=10485760
OLIST_API_KEY=your_key_here
MERCADO_LIVRE_API_KEY=your_key_here
DEBUG=True
```

## 📝 Padrões de Código

### Backend
- Type hints em todas as funções
- Pydantic para validação
- SQLAlchemy para DB queries
- Erros retornam HTTP exceptions

### Frontend
- Componentes funcionais com hooks
- TypeScript strict mode
- Sem estado global por enquanto (useEffect + useState)
- Componentes isolados reutilizáveis

## 🔐 Segurança
- CORS configurado apenas para localhost
- Validação de extensão de arquivo
- Limite de tamanho de upload
- Input sanitization via Pydantic

## 📊 Próximos Passos
1. Testar upload de NF-e real (XML do Sintegra/SEFAZ)
2. Criar componente de edição de itens
3. Implementar lógica de divergência
4. Adicionar autenticação de usuário
5. Integração com Olist (Fase 4)

## 💡 Notas
- SQLite é para MVP. Em produção: PostgreSQL
- OCR é opcional, prioridade é XML
- Custodia as chaves de API em .env (não commitar!)
