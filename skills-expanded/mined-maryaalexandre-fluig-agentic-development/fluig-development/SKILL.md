---
name: fluig-development
description: >
  Guia completo para desenvolvimento na plataforma TOTVS Fluig.
  Ensina a criar datasets, eventos, workflows, formulários, widgets e integrações.
  Use quando o usuário mencionar "fluig", "dataset fluig", "evento fluig",
  "workflow fluig", "formulário fluig", "widget fluig", "hAPI", "TOTVS Fluig",
  "processo BPM fluig", "WCM fluig", "WCMAPI", "Rhino", "Fluig Studio",
  "docAPI", "FormController", "DatasetFactory", "ServiceManager",
  "personalização fluig" ou qualquer tarefa de desenvolvimento na plataforma Fluig.
---

# Diretrizes de Desenvolvimento Fluig

## Visão geral da plataforma

A plataforma TOTVS Fluig é um sistema de gestão de processos (BPM), documentos (ECM) e colaboração. O desenvolvimento na plataforma envolve:

- **Datasets** — Camada universal de acesso a dados (internos, simples, avançados)
- **Eventos** — Scripts JavaScript server-side que reagem a ações na plataforma (processos, formulários, documentos, usuários, social)
- **Workflows/BPM** — Processos de negócio modelados em BPMN 2.0 com atividades, gateways e scripts condicionais
- **Formulários** — Telas HTML para entrada de dados, vinculadas a processos ou autônomas
- **Widgets/WCM** — Componentes de interface para páginas Fluig (FTL + JS + CSS)
- **Integrações** — SOAP WebServices via `ServiceManager`, REST via OAuth (`oauthUtil`), banco externo via JNDI/JDBC

---

## Regras do Motor de Personalização (Rhino)

O Fluig utiliza o motor **Mozilla Rhino** para executar JavaScript no servidor. O Rhino é compatível **APENAS com ECMA 5** (ECMAScript 5). Isso é a regra mais importante do desenvolvimento Fluig.

### Regras obrigatórias

- **SEMPRE** use `var` para declarar variáveis. **NUNCA** use `let` ou `const`.
- **NUNCA** use arrow functions (`=>`). **SEMPRE** use `function() {}`.
- **NUNCA** use template literals (`` ` ``). **SEMPRE** use concatenação com `+`.
- **NUNCA** use destructuring (`var {a, b} = obj`). **SEMPRE** acesse propriedades individualmente.
- **NUNCA** use `class`. **SEMPRE** use funções e protótipos.
- **NUNCA** use `for...of`. Use `for` tradicional ou `for...in` com `hasOwnProperty`.
- **NUNCA** use `Promise`, `async/await`, `Symbol`, `Map`, `Set`, `WeakMap`, `WeakSet`.
- **NUNCA** use default parameters (`function f(x = 1)`). Faça checagem manual.
- **NUNCA** use spread operator (`...`), rest parameters, ou computed property names.
- **NUNCA** use `Object.assign()`, `Array.from()`, `Array.of()`, `Object.keys()` (limitado), `Object.values()`, `Object.entries()`.
- **SEMPRE** use `new Array()` ou `[]` para criar arrays. Itere com `for (var i = 0; i < arr.length; i++)`.
- **SEMPRE** que precisar de um método não suportado em JS, use a classe Java equivalente.

### Interoperabilidade com Java

O Rhino permite chamar classes Java diretamente no JavaScript:

```javascript
// ArrayList (Java) — SEMPRE use para listas passadas a APIs Fluig
var lista = new java.util.ArrayList();
lista.add("item1");
lista.add("item2");

// HashMap (Java) — SEMPRE use para mapas passados a APIs Fluig
var mapa = new java.util.HashMap();
mapa.put("chave", "valor");
var resultado = mapa.get("chave");

// LinkedHashMap (Java) — Para mapas ordenados
var mapaOrdenado = new java.util.LinkedHashMap();

// Formatação de datas
var sdf = new java.text.SimpleDateFormat("dd/MM/yyyy");
var dataFormatada = sdf.format(new java.util.Date());

// Calendar
var cal = java.util.Calendar.getInstance();
cal.setTime(new java.util.Date());
cal.add(java.util.Calendar.DAY_OF_MONTH, 5);
var dataFutura = cal.getTime();

// Integer (Java) — Necessário em algumas APIs
var inteiro = new java.lang.Integer(42);
```

### Conversão entre tipos Java e JavaScript

| Tipo Java | Uso em JavaScript Rhino | Observações |
|---|---|---|
| `java.util.ArrayList` | `var list = new java.util.ArrayList()` | Use para listas que serão passadas para APIs Fluig |
| `java.util.HashMap` | `var map = new java.util.HashMap()` | Use para mapas que serão passados para APIs Fluig |
| `java.lang.Integer` | `new java.lang.Integer(valor)` | Necessário em `stateList.add()` e similares |
| `java.lang.String` | Conversão automática | Strings JS são convertidas automaticamente |
| `java.util.Date` | `new java.util.Date()` | Use para datas |
| `java.text.SimpleDateFormat` | `new java.text.SimpleDateFormat("dd/MM/yyyy")` | Formatação de datas |
| `java.util.Calendar` | `java.util.Calendar.getInstance()` | Manipulação de datas |
| `javax.naming.InitialContext` | `new javax.naming.InitialContext()` | Para lookup JNDI de datasources |

### Lidando com List, Map e Object do Java no Rhino

- Para iterar uma `java.util.List`, use `.size()` e `.get(i)`, **NÃO** `.length` e `[i]`.
- Para iterar um `java.util.Map`, use `.keySet()` e `.get(key)`.
- Numéricos Java (int, long) precisam de cast explícito em algumas operações: `parseInt(valor)`.

```javascript
// Iterando uma List Java
var lista = algumMetodoQueRetornaList();
for (var i = 0; i < lista.size(); i++) {
    var item = lista.get(i);
    log.info("Item: " + item);
}

// Iterando um Map Java
var mapa = algumMetodoQueRetornaMap();
var keys = mapa.keySet().toArray();
for (var i = 0; i < keys.length; i++) {
    var chave = keys[i];
    var valor = mapa.get(chave);
    log.info("Chave: " + chave + ", Valor: " + valor);
}
```

---

## Diretrizes de Datasets

Datasets são a camada universal de acesso a dados no Fluig. Existem 3 tipos:

### Tipos de Datasets

1. **Internos** — Acessam dados da própria plataforma (usuários, grupos, processos, formulários, documentos). Exemplos: `colleague`, `colleagueGroup`, `workflowProcess`, `document`.
2. **Simples** — Integração no-code com webservices SOAP, REST ou JDBC. Criados via Painel de Controle.
3. **Avançados** — Codificados em JavaScript. Podem acessar outros datasets, serviços externos, ou conter valores fixos.

### Regras para Datasets Avançados

- SEMPRE implemente a função `createDataset(fields, constraints, sortFields)`. Essa é a assinatura obrigatória.
- SEMPRE retorne o dataset criado via `return dataset;` ao final da função.
- Use `DatasetBuilder.newDataset()` para criar um novo dataset.
- Use `dataset.addColumn("nomeCampo")` para adicionar colunas.
- Use `dataset.addRow(new Array(valor1, valor2, ...))` para adicionar linhas.
- Para datasets avançados, o tratamento de constraints deve ser feito manualmente na codificação — constraints NÃO são aplicadas automaticamente.
- Use `getValue("WKCompany")` e `getValue("WKUser")` para obter empresa e usuário correntes.

### Acessando Datasets

- Use `DatasetFactory.getDataset(nome, campos, constraints, ordenacao)` para consultar qualquer dataset.
  - `nome`: String — nome/código do dataset
  - `campos`: String[] ou null — lista de campos a retornar (null = todos)
  - `constraints`: SearchConstraint[] ou null — filtros
  - `ordenacao`: String[] ou null — campos para ordenação

- Use `DatasetFactory.createConstraint(campo, valorInicial, valorFinal, tipo)` para criar filtros.
  - `tipo`: `ConstraintType.MUST` (obrigatório), `ConstraintType.SHOULD` (opcional), `ConstraintType.MUST_NOT` (exclusão)

- Para busca parcial (LIKE), use `constraint.setLikeSearch(true)` e valores com `%`:
```javascript
var c1 = DatasetFactory.createConstraint("mail", "%@empresa%", "%@empresa%", ConstraintType.SHOULD);
c1.setLikeSearch(true);
```

### Constraints especiais

| Constraint | Descrição |
|---|---|
| `sqlLimit` | Limita o número de registros retornados |
| `metadata#active` | Filtra apenas formulários ativos (true/false) |
| `metadata#id` | Filtra pelo número do formulário |
| `metadata#version` | Filtra pela versão do formulário |
| `tablename` | Filtra campos de uma tabela filha específica |
| `userSecurityId` | Código do usuário para validação de permissão (obrigatório em eventos) |
| `onlyMainCards` | Retorna apenas registros do formulário principal (sem filhos) |
| `checkSecurity` | Aplica segurança de acesso ao formulário |
| `offset` | Paginação — deslocamento de registros |

### API de Referência — DatasetFactory

| Retorno | Método | Descrição |
|---|---|---|
| `SearchConstraint` | `createConstraint(field, initialValue, finalValue, type)` | Cria constraint para filtro |
| `List<String>` | `getAvailableDatasets()` | Lista todos os datasets disponíveis |
| `DefaultDataset` | `getDataset(name, fields, constraints, order)` | Carrega dados de um dataset |

### API de Referência — Dataset (objeto retornado)

| Retorno | Método | Descrição |
|---|---|---|
| `void` | `addColumn(colName)` | Adiciona coluna ao dataset |
| `void` | `addRow(values)` | Adiciona linha ao dataset (Array de valores) |
| `String` | `getColumnName(colNum)` | Retorna nome da coluna pelo índice |
| `String[]` | `getColumnsName()` | Array com nomes das colunas |
| `int` | `getColumnsCount()` | Quantidade de colunas |
| `int` | `getRowsCount()` | Quantidade de linhas |
| `Object` | `getValue(row, col)` | Valor na linha e coluna (índice ou nome) |
| `Object[][]` | `getValues()` | Todos os valores como array bidimensional |
| `DefaultDataset` | `getSubDataset(field, value)` | Subconjunto filtrado dos dados |
| `ArrayList<HashMap>` | `getMap()` | Valores como lista de mapas |
| `ResultSet` | `toResultSet()` | Dados como ResultSet JDBC |

### Exemplo: Dataset com valores fixos

```javascript
function createDataset(fields, constraints, sortFields) {
    var dataset = DatasetBuilder.newDataset();

    dataset.addColumn("Sigla");
    dataset.addColumn("Estado");
    dataset.addColumn("Capital");

    dataset.addRow(new Array("SP", "São Paulo", "São Paulo"));
    dataset.addRow(new Array("RJ", "Rio de Janeiro", "Rio de Janeiro"));
    dataset.addRow(new Array("MG", "Minas Gerais", "Belo Horizonte"));
    dataset.addRow(new Array("RS", "Rio Grande do Sul", "Porto Alegre"));

    return dataset;
}
```

### Exemplo: Dataset avançado com tratamento de constraint

```javascript
function createDataset(fields, constraints, sortFields) {
    var dataset = DatasetBuilder.newDataset();
    dataset.addColumn("DDD");
    dataset.addColumn("Fone");
    dataset.addColumn("Nome");

    var tempDataset = getDefaultValues();

    if (constraints != null && constraints.length) {
        for (var a = 0; a < tempDataset.length; a++) {
            if (constraints[0].initialValue == tempDataset[a][constraints[0].fieldName]) {
                dataset.addRow(new Array(
                    tempDataset[a]["DDD"],
                    tempDataset[a]["Fone"],
                    tempDataset[a]["Nome"]
                ));
            }
        }
    } else {
        for (var a = 0; a < tempDataset.length; a++) {
            dataset.addRow(new Array(
                tempDataset[a]["DDD"],
                tempDataset[a]["Fone"],
                tempDataset[a]["Nome"]
            ));
        }
    }

    return dataset;
}

function getDefaultValues() {
    return [{
        DDD: "47", Fone: "1111-1111", Nome: "Marcos"
    }, {
        DDD: "41", Fone: "3333-3333", Nome: "Maria"
    }, {
        DDD: "11", Fone: "5555-5555", Nome: "Michel"
    }];
}
```

### Exemplo: Consultando dataset com constraint

```javascript
function createDataset(fields, constraints, sortFields) {
    var c1 = DatasetFactory.createConstraint("DDD", "47", "47", ConstraintType.MUST);
    var dataset = DatasetFactory.getDataset("exemploFiltro", null, new Array(c1), null);
    return dataset;
}
```

### Exemplo: Dataset com permissionamento (validação de grupo)

```javascript
function createDataset(fields, constraints, sortFields) {
    var newDataset = DatasetBuilder.newDataset();
    try {
        var currentUser = getValue("WKUser");
        var currentCompany = getValue("WKCompany");
        var groupCode = "meuGrupo";

        var filter = [
            DatasetFactory.createConstraint("colleagueGroupPK.companyId", currentCompany, currentCompany, ConstraintType.MUST),
            DatasetFactory.createConstraint("colleagueGroupPK.colleagueId", currentUser, currentUser, ConstraintType.MUST),
            DatasetFactory.createConstraint("colleagueGroupPK.groupId", groupCode, groupCode, ConstraintType.MUST)
        ];

        var validation = DatasetFactory.getDataset("colleagueGroup", null, filter, null);

        if (validation.rowsCount == 1) {
            newDataset.addColumn("SUCCESS");
            newDataset.addRow(["ok"]);
        } else {
            newDataset.addColumn("ERROR");
            newDataset.addRow(["sem permissão"]);
        }
    } catch (e) {
        newDataset.addColumn("ERROR");
        newDataset.addRow(["chamada incorreta"]);
    }
    return newDataset;
}
```

### Exemplo: Dataset Pai-Filho (tabela filha de formulário)

```javascript
function createDataset(fields, constraints, sortFields) {
    var dataset = DatasetBuilder.newDataset();
    dataset.addColumn("NumFormulario");
    dataset.addColumn("Id");
    dataset.addColumn("Peca");
    dataset.addColumn("Quantidade");

    var cst = DatasetFactory.createConstraint("metadata#active", true, true, ConstraintType.MUST);
    var datasetPrincipal = DatasetFactory.getDataset("dsFormPaiFilho", null, new Array(cst), null);

    for (var i = 0; i < datasetPrincipal.rowsCount; i++) {
        var documentId = datasetPrincipal.getValue(i, "metadata#id");
        var documentVersion = datasetPrincipal.getValue(i, "metadata#version");

        var c1 = DatasetFactory.createConstraint("tablename", "tabelaPecas", "tabelaPecas", ConstraintType.MUST);
        var c2 = DatasetFactory.createConstraint("metadata#id", documentId, documentId, ConstraintType.MUST);
        var c3 = DatasetFactory.createConstraint("metadata#version", documentVersion, documentVersion, ConstraintType.MUST);

        var datasetFilhos = DatasetFactory.getDataset("dsFormPaiFilho", null, new Array(c1, c2, c3), null);

        for (var j = 0; j < datasetFilhos.rowsCount; j++) {
            dataset.addRow(new Array(
                documentId,
                datasetFilhos.getValue(j, "wdk_sequence_id"),
                datasetFilhos.getValue(j, "peca"),
                datasetFilhos.getValue(j, "qtde")
            ));
        }
    }

    return dataset;
}
```

### Exemplo: Dataset acessando banco de dados externo (JNDI/JDBC)

IMPORTANTE: Configure o datasource no `standalone.xml` ou `domain.xml` do servidor de aplicação. Use `AppDS` (não `FluigDS` ou `FluigDSRO`) a partir da atualização 1.6.5.

```xml
<datasource jta="false" jndi-name="java:/jdbc/MeuDataSet" pool-name="MeuDataSet" enabled="true" use-java-context="false">
    <connection-url>jdbc:mysql://localhost:3306/minhabase</connection-url>
    <driver>mysqlDriver</driver>
    <security>
        <user-name>root</user-name>
        <password>admin</password>
    </security>
</datasource>
```

```javascript
function createDataset(fields, constraints, sortFields) {
    var newDataset = DatasetBuilder.newDataset();
    var dataSource = "/jdbc/MeuDataSet";
    var ic = new javax.naming.InitialContext();
    var ds = ic.lookup(dataSource);
    var created = false;
    var myQuery = "select * from pessoas";

    try {
        var conn = ds.getConnection();
        var stmt = conn.createStatement();
        var rs = stmt.executeQuery(myQuery);
        var columnCount = rs.getMetaData().getColumnCount();

        while (rs.next()) {
            if (!created) {
                for (var i = 1; i <= columnCount; i++) {
                    newDataset.addColumn(rs.getMetaData().getColumnName(i));
                }
                created = true;
            }
            var row = new Array();
            for (var i = 1; i <= columnCount; i++) {
                var obj = rs.getObject(rs.getMetaData().getColumnName(i));
                row[i - 1] = (obj != null) ? obj.toString() : "null";
            }
            newDataset.addRow(row);
        }
    } catch (e) {
        log.error("ERRO: " + e.message);
    } finally {
        if (rs != null) rs.close();
        if (stmt != null) stmt.close();
        if (conn != null) conn.close();
    }
    return newDataset;
}
```

### Datasets Internos mais usados

| Dataset | Descrição |
|---|---|
| `colleague` | Usuários da plataforma |
| `colleagueGroup` | Relação usuário-grupo |
| `workflowColleagueRole` | Relação usuário-papel |
| `workflowProcess` | Processos/solicitações |
| `document` | Documentos do GED |
| `group` | Grupos da plataforma |
| `role` | Papéis da plataforma |

### Acessando Datasets via HTML (formulários)

```html
<select name="estado" dataset="dsEstados" datasetkey="sigla" datasetvalue="nome"></select>
```

### Acessando Datasets via Client-Side JavaScript (widgets)

Inclua o script `vcXMLRPC.js` e utilize `DatasetFactory.getDataset()`:
```html
<script src="/webdesk/vcXMLRPC.js"></script>
<script>
var dataset = DatasetFactory.getDataset("colleague", null, null, null);
for (var i = 0; i < dataset.rowsCount; i++) {
    var nome = dataset.getValue(i, "colleagueName");
}
</script>
```

### Zoom com Dataset

```html
<input type="zoom" name="campo_zoom"
    data-zoom="{
        'displayKey': 'colleagueName',
        'datasetId': 'colleague',
        'fields': [{
            'field': 'colleagueName',
            'label': 'Nome',
            'standard': 'true'
        }]
    }" />
```

---

## Diretrizes de Eventos de Processo (Workflow)

Eventos de processo são scripts JavaScript executados automaticamente durante o ciclo de vida de uma solicitação workflow. São criados via Fluig Studio vinculados a um diagrama de processo.

### Regras gerais de eventos

- Eventos `before*` podem **bloquear** a ação usando `throw "mensagem de erro"`.
- Eventos `after*` são executados após a ação e **NÃO podem** bloquear com `throw`.
- Use `getValue("parametro")` para acessar variáveis de contexto do processo.
- Use `hAPI` para manipular formulário, atividades e anexos do workflow.
- Use `log.info()`, `log.warn()`, `log.error()`, `log.debug()` para logging.
- Use `globalVars` (Map) para passar dados entre eventos na mesma movimentação.

### Tabela completa de eventos de processo

| Evento | Descrição | Parâmetros |
|---|---|---|
| `afterCancelProcess` | Após cancelamento da solicitação | `colleagueId` (String), `processId` (Integer) |
| `afterProcessCreate` | Após criação de novo processo | `processId` (Integer) |
| `afterProcessFinish` | Após finalização da solicitação | `processId` (Integer) |
| `afterReleaseVersion` | Após liberação de versão do processo | `xml` (String) |
| `afterStateEntry` | Após entrada em uma atividade | `sequenceId` (Integer) |
| `afterStateLeave` | Após saída de uma atividade | `sequenceId` (Integer) |
| `afterTaskComplete` | Após completar uma tarefa | `colleagueId` (String), `nextSequenceId` (Integer), `userList` (List&lt;String&gt;) |
| `afterTaskCreate` | Após usuário receber uma tarefa | `colleagueId` (String) |
| `afterTaskSave` | Após salvar informações da tarefa | `colleagueId` (String), `nextSequenceId` (Integer), `userList` (List&lt;String&gt;) |
| `beforeCancelProcess` | Antes do cancelamento | `colleagueId` (String), `processId` (Integer) |
| `beforeStateEntry` | Antes da entrada em uma atividade | `sequenceId` (Integer) |
| `beforeStateLeave` | Antes da saída de uma atividade | `sequenceId` (Integer) |
| `beforeTaskComplete` | Antes de completar uma tarefa | `colleagueId` (String), `nextSequenceId` (Integer), `userList` (List&lt;String&gt;) |
| `beforeTaskCreate` | Antes de receber uma tarefa | `colleagueId` (String) |
| `beforeTaskSave` | Antes de salvar a tarefa | `colleagueId` (String), `nextSequenceId` (Integer), `userList` (List&lt;String&gt;) |
| `calculateAgreement` | Após cálculo de consenso | `currentState` (Integer), `agreementData` (Map) |
| `onNotify` | Antes de enviar notificações | — |
| `subProcessCreated` | Quando sub-processo é criado | `subProcessId` (Integer) |
| `validateAvailableStates` | Após montar lista de atividades disponíveis | `iCurrentState` (Integer), `stateList` (List&lt;Integer&gt;) |

### Ordem de execução dos eventos

**Ao criar/salvar solicitação (atividade inicial):**
1. `beforeStateEntry` → 2. `beforeTaskCreate` → 3. `afterTaskCreate` → 4. `afterStateEntry` → 5. `afterProcessCreate`

**Ao movimentar solicitação:**
1. `beforeTaskSave` → 2. `beforeTaskComplete` → 3. `beforeStateLeave` → 4. `afterStateLeave` → 5. `afterTaskComplete` → 6. `beforeStateEntry` (destino) → 7. `beforeTaskCreate` (destino) → 8. `afterTaskCreate` (destino) → 9. `afterStateEntry` (destino) → 10. `afterTaskSave`

**Ao finalizar solicitação:**
1. `beforeTaskSave` → 2. `beforeTaskComplete` → 3. `beforeStateLeave` → 4. `afterStateLeave` → 5. `afterTaskComplete` → 6. `afterProcessFinish` → 7. `afterTaskSave`

**Ao cancelar solicitação:**
1. `beforeCancelProcess` → 2. `afterCancelProcess`

### Parâmetros do getValue() — Variáveis de contexto

| Parâmetro | Descrição | Tipo retorno |
|---|---|---|
| `WKDef` | Código do processo | String |
| `WKVersDef` | Versão do processo | String |
| `WKNumProces` | Número da solicitação | String |
| `WKNumState` | Número da atividade atual | String |
| `WKCurrentState` | Número da atividade corrente | String |
| `WKCompany` | Número da empresa | String |
| `WKUser` | Código do usuário corrente | String |
| `WKUserComment` | Observações do usuário na atividade | String |
| `WKCompletTask` | Se a tarefa foi completada ("true"/"false") | String |
| `WKNextState` | Número da próxima atividade (destino) | String |
| `WKCardId` | Código do registro de formulário | String |
| `WKFormId` | Código do formulário do processo | String |
| `WKMobile` | Se acesso via dispositivo mobile | String |
| `WKManagerMode` | Se movimentado pela visão do gestor | String |
| `WKReplacement` | Código do usuário substituto | String |
| `WKIsTransfer` | Se está transferindo tarefa | String |
| `WKIsService` | Se cancelamento via serviço | String |
| `WKUserLocale` | Idioma do usuário | String |
| `WKActualThread` | Thread atual do processo | String |

### globalVars — Comunicação entre eventos

`globalVars` é um `Map<String, String>` disponível em todos os eventos da mesma movimentação:

```javascript
// Em um evento (ex: beforeTaskSave)
globalVars.put("aprovador", "admin");

// Em outro evento da mesma movimentação (ex: beforeStateEntry)
var aprovador = globalVars.get("aprovador");
log.info("Aprovador definido: " + aprovador);
```

### Exemplo: Bloquear movimentação por campo vazio

```javascript
function beforeTaskSave(colleagueId, nextSequenceId, userList) {
    var completTask = getValue("WKCompletTask");
    var nome = hAPI.getCardValue("nome");
    if (completTask == "true" && (!nome || !nome.trim())) {
        throw "Não é permitido movimentar com o campo 'Nome' vazio!";
    }
}
```

### Exemplo: Bloquear transferência de tarefa

```javascript
function beforeTaskCreate(colleagueId) {
    var isTransfer = getValue("WKIsTransfer");
    if (isTransfer !== null) {
        if (JSON.parse(isTransfer)) {
            throw "Não é permitido transferir esta atividade!";
        }
    }
}
```

### Exemplo: Filtrar atividades disponíveis

```javascript
function validateAvailableStates(iCurrentState, stateList) {
    if (iCurrentState == 1) {
        stateList.clear();
        var atividades = [4, 3, 2];
        for (var i = 0; i < atividades.length; i++) {
            stateList.add(new java.lang.Integer(atividades[i]));
        }
    }
    return stateList;
}
```

### Exemplo: Consenso personalizado

```javascript
function calculateAgreement(currentState, agreementData) {
    log.info("Consenso Atual: " + agreementData.get("currentPercentage"));
    log.info("Atividade Destino: " + agreementData.get("currentDestState"));
    agreementData.put("currentPercentage", 100);
    agreementData.put("currentDestState", 2);
    agreementData.put("currentDestUsers", "admin");
}
```

### Exemplo: Iniciar novo processo após finalização

```javascript
function afterProcessFinish(processId) {
    var wsProvider = ServiceManager.getServiceInstance("WorkflowEngineService");
    var wsLocator = wsProvider.instantiate("com.totvs.technology.ecm.workflow.ws.ECMWorkflowEngineServiceService");
    var wsService = wsLocator.getWorkflowEngineServicePort();
    var attachArray = wsProvider.instantiate("com.totvs.technology.ecm.workflow.ws.ProcessAttachmentDtoArray");
    var objectFactory = wsProvider.instantiate("net.java.dev.jaxb.array.ObjectFactory");
    var cardData = objectFactory.createStringArrayArray();
    wsService.simpleStartProcess("admin", "admin", 1, "meuProcesso", "Iniciado automaticamente", attachArray, cardData);
}
```

---

## Diretrizes de Eventos de Formulário

Eventos de formulário são scripts JavaScript server-side executados durante o ciclo de vida de um formulário Fluig. São criados no Fluig Studio vinculados a uma definição de formulário.

### Regras gerais

- TODOS os eventos de formulário recebem o parâmetro `form` (FormController) que permite manipular campos e visibilidade.
- O evento `displayFields` também recebe `customHTML` (StringBuilder) para injetar scripts client-side.
- Use `form.getValue("campo")` para ler valores e `form.setValue("campo", valor)` para definir valores.
- Use `form.getFormMode()` para identificar o modo: `"ADD"` (novo), `"MOD"` (edição), `"VIEW"` (visualização).
- Use `throw "mensagem"` em `validateForm` e `beforeProcessing` para bloquear o salvamento.
- Campos checkbox retornam `"on"` quando marcados ou `""` quando desmarcados.

### Tabela de eventos de formulário

| Evento | Execução | Assinatura | Descrição |
|---|---|---|---|
| `beforeProcessing` | Server-side | `beforeProcessing(form)` | Antes de qualquer processamento. Primeiro evento executado. |
| `displayFields` | Server-side | `displayFields(form, customHTML)` | Controla visibilidade e valores dos campos antes da renderização. |
| `enableFields` | Server-side | `enableFields(form)` | Controla quais campos estão habilitados/desabilitados. |
| `inputFields` | Server-side | `inputFields(form)` | Manipula valores dos campos antes de gravar no banco. |
| `validateForm` | Server-side | `validateForm(form)` | Valida os dados do formulário. Use `throw` para bloquear. |
| `afterSaveNew` | Server-side | `afterSaveNew(form)` | Após salvar um novo registro de formulário. |
| `afterProcessing` | Server-side | `afterProcessing(form)` | Último evento executado, após todo o processamento. |
| `beforeMovementOptions` | Client-side JS | `var beforeMovementOptions = function(numState) {}` | Antes de exibir opções de movimentação. |
| `beforeSendValidate` | Client-side JS | `var beforeSendValidate = function(numState, nextState) {}` | Validação client-side antes de enviar movimentação. |

### FormController (objeto `form`) — API de referência

| Método | Retorno | Descrição |
|---|---|---|
| `form.getValue("campo")` | String | Retorna valor do campo |
| `form.setValue("campo", valor)` | void | Define o valor do campo |
| `form.getFormMode()` | String | Modo do formulário: "ADD", "MOD", "VIEW" |
| `form.getDocumentId()` | int | Código do documento |
| `form.getVersion()` | int | Versão do formulário |
| `form.getCardIndex()` | int | Código do card index |
| `form.getCompanyId()` | long | Código da empresa |
| `form.setVisible("campo", bool)` | void | Oculta/exibe campo pelo name |
| `form.setVisibleById("id", bool)` | void | Oculta/exibe elemento pelo id |
| `form.setEnabled("campo", bool)` | void | Habilita/desabilita campo |
| `form.setEnabled("campo", bool, protect)` | void | Com proteção contra manipulação |
| `form.setEnhancedSecurityHiddenInputs(bool)` | void | Segurança aprimorada em campos ocultos |
| `form.setShowDisabledFields(bool)` | void | Exibe campos desabilitados |
| `form.setHideDeleteButton(bool)` | void | Oculta botão de exclusão |
| `form.setHidePrintLink(bool)` | void | Oculta botão de impressão |

### Exemplo: displayFields — Preencher campos automaticamente e injetar JS

```javascript
function displayFields(form, customHTML) {
    var atividadeAtual = getValue("WKNumState");
    var modo = form.getFormMode();
    var usuario = getValue("WKUser");

    if (modo != "VIEW") {
        if (atividadeAtual == 0 || atividadeAtual == 1) {
            form.setValue("solicitante", usuario);
            form.setValue("dataSolicitacao", retornaDataAtual());
        }
    }

    // Injetar variáveis no client-side
    customHTML.append("<script type='text/javascript'>");
    customHTML.append("var modoFormulario = '" + modo + "';");
    customHTML.append("var atividadeAtual = " + atividadeAtual + ";");
    customHTML.append("</script>");
}

function retornaDataAtual() {
    return (new java.text.SimpleDateFormat("dd/MM/yyyy")).format(new java.util.Date());
}
```

### Exemplo: displayFields — Ocultar campos condicionalmente

```javascript
function displayFields(form, customHTML) {
    var ocultarTabela = form.getValue("ocultarTabela") == "on";
    var ocultarCampoA = form.getValue("ocultarCampoA") == "on";

    if (ocultarTabela) {
        form.setVisibleById("minhaTabela", false);
    }
    if (ocultarCampoA) {
        form.setVisible("campoA", false);
    }

    form.setHideDeleteButton(true);
    form.setHidePrintLink(true);
}
```

### Exemplo: enableFields — Desabilitar campos condicionalmente

```javascript
function enableFields(form) {
    if (form.getFormMode() != "ADD") {
        form.setEnabled("codigo", false, true);  // true = protege contra manipulação
        form.setEnabled("tipo", false);
    }
}
```

IMPORTANTE: Quando `setEnabled("campo", false)` é usado, o Fluig adiciona `_` ao `name` e `id` do campo no HTML. Use `setEnabled("campo", false, true)` com o terceiro parâmetro `true` para proteger contra manipulação pelo usuário.

### Exemplo: inputFields — Formatar data antes de gravar

```javascript
function inputFields(form) {
    var regEx = /^\d{4}-\d{2}-\d{2}$/;
    if (form.getValue("dt_solicitacao").match(regEx)) {
        var split = form.getValue("dt_solicitacao").split("-");
        form.setValue("dt_solicitacao", split[2] + "-" + split[1] + "-" + split[0]);
    }
}
```

### Exemplo: validateForm — Validar campo obrigatório

```javascript
function validateForm(form) {
    if (form.getValue("nome") == null || form.getValue("nome") == "") {
        throw "O campo 'Nome' é obrigatório!\nPreencha e tente novamente.";
    }
}
```

### Exemplo: afterSaveNew — Log após salvar

```javascript
function afterSaveNew(form) {
    log.info("Novo registro criado. Solicitante: " + form.getValue("solicitante"));
}
```

### Exemplo: beforeMovementOptions — Validação client-side antes de exibir opções

```javascript
var beforeMovementOptions = function(numState) {
    if (document.form.codigo.value == "") {
        throw "Erro: O código não foi preenchido";
    }
    return true;
}
```

### Exemplo: beforeSendValidate — Validação client-side por atividade destino

```javascript
var beforeSendValidate = function(numState, nextState) {
    if (numState == 1 && nextState == 2 && document.form.codigo.value == "") {
        throw "Para movimentar para a atividade 2, o código deve ser preenchido";
    }
    return true;
}
```

### Exemplo: Buscar nome do usuário por código usando dataset

```javascript
function buscaNomeUsuario(codigoUsuario) {
    var constraint = DatasetFactory.createConstraint("colleaguePK.colleagueId", codigoUsuario, codigoUsuario, ConstraintType.MUST);
    var dataset = DatasetFactory.getDataset("colleague", null, [constraint], null);
    if (dataset.rowsCount > 0) {
        return dataset.getValue(0, "colleagueName");
    }
    return "";
}
```

### Logging em eventos de formulário

```javascript
// log.info — Informações gerais
log.info("Valor do campo: " + form.getValue("codigo"));

// log.warn — Avisos
log.warn("Campo código em branco, pode causar problemas");

// log.error — Erros
log.error("Falha ao processar campo: " + form.getValue("codigo"));

// log.debug — Debug
log.debug("Verificando conteúdo do campo código");

// log.dir — Imprimir objeto como JSON
var obj = {"codigo": form.getValue("codigo"), "nome": form.getValue("nome")};
log.dir(obj);
```

---

## Diretrizes de hAPI (Workflow Helper API)

A `hAPI` é a variável global disponível em todos os eventos de processo que permite manipular formulários, atividades, anexos e sub-processos do workflow.

### Regras importantes

- **NUNCA** tente usar `hAPI.getCardValue()` ou `hAPI.setCardValue()` na atividade inicial (primeira atividade do processo). Só funciona a partir da segunda atividade.
- **SEMPRE** verifique o `sequenceId` antes de manipular dados do formulário:
```javascript
function beforeStateEntry(sequenceId) {
    if (sequenceId != 0) { // 0 = atividade inicial
        var campo = hAPI.getCardValue("meuCampo");
    }
}
```
- Campos checkbox via `hAPI.getCardValue()` retornam `"on"` (marcado) ou `""` (desmarcado).
- Para campos pai-filho, use o padrão `nomeCampo___N` onde N é o índice sequencial.

### Tabela completa de métodos da hAPI

| Método | Descrição |
|---|---|
| `hAPI.getCardValue("campo")` | Retorna o valor de um campo do formulário |
| `hAPI.setCardValue("campo", "valor")` | Define o valor de um campo do formulário |
| `hAPI.getCardData(numProcesso)` | Retorna HashMap com todos os campos/valores do formulário. Para pai-filho: `campo___1`, `campo___2`, etc. |
| `hAPI.setAutomaticDecision(numAtiv, listaColab, "obs")` | Define o fluxo de saída de uma atividade automaticamente. `listaColab` é `java.util.ArrayList`. |
| `hAPI.getActiveStates()` | Retorna lista das atividades ativas do processo |
| `hAPI.setDueDate(numProcesso, numThread, "userId", dataConclusao, tempoSeg)` | Altera o prazo de conclusão de uma atividade |
| `hAPI.startProcess(processId, ativDest, listaColab, "obs", completarTarefa, valoresForm, modoGestor)` | Inicia nova solicitação workflow. `valoresForm` é `java.util.HashMap`. Retorna mapa com info da solicitação. |
| `hAPI.setColleagueReplacement(userId)` | Define um usuário substituto |
| `hAPI.setTaskComments("userId", numProcesso, numThread, "obs")` | Define observação para uma tarefa |
| `hAPI.getAdvancedProperty("propriedade")` | Retorna valor de propriedade avançada do processo |
| `hAPI.calculateDeadLineHours(data, segundos, prazo, periodId)` | Calcula prazo em horas baseado no expediente. Retorna Array [data, hora]. |
| `hAPI.calculateDeadLineTime(data, segundos, prazo, periodId)` | Calcula prazo em minutos baseado no expediente. Retorna Array [data, hora]. |
| `hAPI.getUserTaskLink(numAtiv)` | Retorna link para movimentação de uma atividade |
| `hAPI.createAdHocTasks(processInstanceId, sequenceId, assunto, detalhamento, listaTarefas)` | Cria atividades ad-hoc |
| `hAPI.listAttachments()` | Retorna lista de anexos do processo (DocumentDto[]) |
| `hAPI.publishWorkflowAttachment(documento)` | Publica anexo workflow no GED |
| `hAPI.attachDocument(documentId)` | Anexa documento do GED à solicitação |
| `hAPI.getAvailableStatesDetail(companyId, userId, processId, processInstanceId, threadSequence)` | Retorna detalhes das atividades disponíveis (ProcessStateDto[]) |
| `hAPI.getChildrenInstances(processInstanceId)` | Retorna lista com números das solicitações filhas |
| `hAPI.getParentInstance(processInstanceId)` | Retorna número da solicitação pai |
| `hAPI.addCardChild(tableName, cardData)` | Adiciona linha filho no formulário pai-filho. `cardData` é `java.util.HashMap`. |
| `hAPI.removeCardChild(tableName, lineIndex)` | Remove linha de tabela pai-filho (a partir da 1.8.1) |
| `hAPI.getChildrenIndexes(tableName)` | Retorna array com os índices dos filhos |

### Exemplo: Decisão automática

```javascript
function beforeStateEntry(sequenceId) {
    if (sequenceId == 4) {
        var users = new java.util.ArrayList();
        users.add("admin");
        hAPI.setAutomaticDecision(7, users, "Decisão automática pelo sistema");
    }
}
```

### Exemplo: Decisão automática com Pool:Group ou Pool:Role

```javascript
function beforeStateEntry(sequenceId) {
    if (sequenceId == 5) {
        var users = new java.util.ArrayList();
        // Para grupo: Pool:Group:codigoGrupo
        users.add("Pool:Group:aprovadores");
        // Para papel: Pool:Role:codigoPapel
        // users.add("Pool:Role:gestor");
        hAPI.setAutomaticDecision(6, users, "Encaminhado ao grupo");
    }
}
```

### Exemplo: Iniciar sub-processo com dados do formulário

```javascript
function beforeStateEntry(sequenceId) {
    if (sequenceId == 5) {
        var users = new java.util.ArrayList();
        users.add("Pool:Role:analista");
        var formData = new java.util.HashMap();
        formData.put("campo1", "Valor do Campo 1");
        formData.put("campo2", "Valor do Campo 2");
        hAPI.startProcess("meuProcesso", 4, users, "Solicitação via hAPI", true, formData, false);
    }
}
```

### Exemplo: Alterar prazo de conclusão

```javascript
function afterTaskCreate(colleagueId) {
    var atividade = getValue("WKCurrentState");
    if (atividade == 5) {
        var prazo = hAPI.getCardValue("prazoConclusao");
        if (prazo != undefined && prazo != "") {
            var partes = prazo.split("/");
            var data = new Date();
            data.setDate(parseInt(partes[0]));
            data.setMonth(parseInt(partes[1]) - 1);
            data.setFullYear(parseInt(partes[2]));
            var processo = getValue("WKNumProces");
            hAPI.setDueDate(processo, 0, colleagueId, data, (24 * 60 * 60) - 1);
        }
    }
}
```

### Exemplo: Calcular prazo com expediente

```javascript
function afterTaskCreate(colleagueId) {
    var data = new Date();
    var obj = hAPI.calculateDeadLineHours(data, 50000, 2, "Default");
    var dt = obj[0];
    var segundos = obj[1];
    var processo = getValue("WKNumProces");
    hAPI.setDueDate(processo, 0, colleagueId, dt, segundos);
}
```

### Exemplo: Validar anexos obrigatórios

```javascript
function beforeTaskSave(colleagueId, nextSequenceId, userList) {
    var attachments = hAPI.listAttachments();
    var encontrou = false;
    for (var i = 0; i < attachments.size(); i++) {
        var attachment = attachments.get(i);
        if (attachment.getDocumentDescription() == "contrato.pdf") {
            encontrou = true;
        }
    }
    if (!encontrou) {
        throw "É obrigatório anexar o arquivo 'contrato.pdf'!";
    }
}
```

### Exemplo: Publicar anexos workflow no GED

```javascript
function beforeStateEntry(sequenceId) {
    if (sequenceId == 4) {
        var calendar = java.util.Calendar.getInstance().getTime();
        var docs = hAPI.listAttachments();
        for (var i = 0; i < docs.size(); i++) {
            var doc = docs.get(i);
            if (doc.getDocumentType() != "7") {
                continue;
            }
            doc.setParentDocumentId(27);
            doc.setVersionDescription("Processo: " + getValue("WKNumProces"));
            doc.setExpires(false);
            doc.setCreateDate(calendar);
            doc.setInheritSecurity(true);
            doc.setTopicId(1);
            doc.setUserNotify(false);
            doc.setValidationStartDate(calendar);
            doc.setVersionOption("0");
            doc.setUpdateIsoProperties(true);
            hAPI.publishWorkflowAttachment(doc);
        }
    }
}
```

### Exemplo: Manipular formulário pai-filho

```javascript
// Adicionar linha filho
function beforeStateEntry(sequenceId) {
    if (sequenceId == 4) {
        var childData = new java.util.HashMap();
        childData.put("matricula", "0041");
        childData.put("nome", "João Silva");
        childData.put("cpf", "44455889987");
        hAPI.addCardChild("funcionarios", childData);
    }
}

// Remover todas as linhas filhas
function beforeStateEntry(sequenceId) {
    var indexes = hAPI.getChildrenIndexes("funcionarios");
    for (var i = indexes.length - 1; i >= 0; i--) {
        hAPI.removeCardChild("funcionarios", indexes[i]);
    }
}

// Ler dados dos filhos
function beforeStateEntry(sequenceId) {
    var indexes = hAPI.getChildrenIndexes("itens");
    for (var i = 0; i < indexes.length; i++) {
        var campo = "descricao___" + indexes[i];
        var valor = hAPI.getCardValue(campo);
        log.info("Item " + indexes[i] + ": " + valor);
    }
}
```

### Exemplo: Obter dados do processo pai

```javascript
function beforeStateEntry(sequenceId) {
    if (sequenceId == 2) {
        var numProcess = getValue("WKNumProces");
        var parentProcess = hAPI.getParentInstance(numProcess);
        var parentCardData = hAPI.getCardData(parentProcess);
        var cnpj = parentCardData.get("cnpj");
        hAPI.setCardValue("cnpj", cnpj);
    }
}
```

### Exemplo: Notificação personalizada com link da tarefa

```javascript
function afterTaskCreate(colleagueId) {
    var sequenceId = getValue("WKCurrentState");
    if (sequenceId == 2) {
        var destinatarios = new java.util.ArrayList();
        destinatarios.add(colleagueId);
        var parametros = new java.util.HashMap();
        parametros.put("WDK_CompanyId", getValue("WKCompany"));
        parametros.put("WDK_TaskLink", hAPI.getUserTaskLink(sequenceId));
        notifier.notify(getValue("WKUser"), "meuTemplate", parametros, destinatarios, "text/html");
    }
}
```

### Scripts Condicionais

Scripts condicionais são expressões JavaScript usadas em gateways do diagrama BPMN para determinar o fluxo. Variáveis e funções disponíveis:

| Objeto | Descrição |
|---|---|
| `log` | Logging (info, warn, error, debug) |
| `ServiceManager` | Acesso a serviços SOAP registrados |
| `DatasetManager` / `DatasetFactory` | Acesso a datasets |
| `DatasetBuilder` | Construção de datasets |
| `ConstraintType` | Tipos de constraint (MUST, SHOULD, MUST_NOT) |
| `notifier` | Envio de notificações |
| `WKParams` | Parâmetros do processo (WKDef, WKUser, etc.) |
| `hAPI` | API de workflow |

```javascript
// Exemplo de script condicional em gateway
var aprovado = hAPI.getCardValue("aprovado");
if (aprovado == "sim") {
    true; // Segue para atividade de aprovação
} else {
    false; // Segue para atividade de rejeição
}
```

---

## Diretrizes de Formulários HTML

Formulários Fluig são páginas HTML que servem como interface de entrada de dados para processos (workflows) ou como registros autônomos. São criados via Fluig Studio.

### Regras gerais

- SEMPRE inclua os CSS e JS do Fluig Style Guide no formulário para manter a consistência visual.
- SEMPRE use a classe `fluig-style-guide` como wrapper principal.
- SEMPRE use `name` nos campos de input — o Fluig usa o atributo `name` para gravar os valores.
- Para formulários vinculados a processos, o `name` dos campos é o que será acessado por `hAPI.getCardValue("name")`.
- NUNCA use IDs duplicados no formulário.
- Para tabelas pai-filho, use o atributo `tablename` na tag `<table>` e `addbuttonlabel` para o botão de adicionar.

### Estrutura básica de formulário

```html
<html>
<head>
    <link rel="stylesheet" href="/portal/resources/style-guide/css/fluig-style-guide.min.css" />
    <script src="/portal/resources/js/jquery/jquery.js"></script>
    <script src="/portal/resources/style-guide/js/fluig-style-guide.min.js"></script>
</head>
<body>
<div class="fluig-style-guide">
    <form name="form" role="form">
        <div class="form-group">
            <label for="nome">Nome</label>
            <input type="text" class="form-control" name="nome" id="nome" />
        </div>
        <div class="form-group">
            <label for="email">E-mail</label>
            <input type="email" class="form-control" name="email" id="email" />
        </div>
        <div class="form-group">
            <label for="observacao">Observação</label>
            <textarea class="form-control" name="observacao" id="observacao" rows="3"></textarea>
        </div>
    </form>
</div>
</body>
</html>
```

### Campos de formulário — Tipos suportados

| Tipo HTML | Uso | Observações |
|---|---|---|
| `<input type="text">` | Textos simples | Padrão para maioria dos campos |
| `<input type="hidden">` | Campos ocultos | Para dados de controle não visíveis |
| `<input type="checkbox">` | Opções on/off | Retorna `"on"` ou `""` |
| `<input type="radio">` | Seleção única | Mesmo `name` para o grupo |
| `<select>` | Lista de opções | Pode vincular a dataset |
| `<textarea>` | Textos longos | Para observações e descrições |
| `<input type="zoom">` | Zoom (lookup) | Campo especial Fluig para consulta em datasets |

### Vinculando Select a Dataset

```html
<select name="estado" dataset="dsEstados" datasetkey="sigla" datasetvalue="nome">
</select>
```

Atributos:
- `dataset` — Nome/código do dataset
- `datasetkey` — Coluna usada como `value` da option
- `datasetvalue` — Coluna usada como texto visível da option

### Zoom (Campo de Consulta)

```html
<input type="zoom" name="cliente"
    data-zoom="{
        'displayKey': 'nome',
        'datasetId': 'dsClientes',
        'limit': '10',
        'fields': [{
            'field': 'codigo',
            'label': 'Código',
            'standard': 'false'
        }, {
            'field': 'nome',
            'label': 'Nome',
            'standard': 'true'
        }]
    }" />
```

Propriedades do `data-zoom`:
- `displayKey` — Campo exibido no input após seleção
- `datasetId` — Dataset consultado
- `limit` — Número máximo de resultados (0 = sem limite)
- `fields` — Colunas exibidas na janela de zoom
- `standard` — Coluna usada para busca padrão (`"true"`)

### Formulário Pai-Filho (Tabela Dinâmica)

```html
<table class="table table-bordered" tablename="itens"
       addbuttonlabel="Adicionar Item" cellspacing="0" width="100%">
    <thead>
        <tr>
            <td>Descrição</td>
            <td>Quantidade</td>
            <td>Valor Unitário</td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><input class="form-control" name="descricao" type="text" /></td>
            <td><input class="form-control" name="quantidade" type="text" /></td>
            <td><input class="form-control" name="valorUnitario" type="text" /></td>
        </tr>
    </tbody>
</table>
```

Regras para pai-filho:
- O atributo `tablename` define o nome da tabela filha (usado em constraints: `DatasetFactory.createConstraint("tablename", "itens", "itens", ConstraintType.MUST)`)
- Cada linha gera campos com sufixo `___N` (ex: `descricao___1`, `descricao___2`)
- O campo especial `wdk_sequence_id` contém o índice da linha
- Use `hAPI.addCardChild("itens", hashMap)` para adicionar linhas via evento
- Use `hAPI.getChildrenIndexes("itens")` para obter índices existentes
- Use `addbuttonlabel` para definir o texto do botão de adicionar

### CSS no Formulário — Guia de Estilos Fluig

O Fluig utiliza um framework CSS baseado no Bootstrap. Caminhos corretos:

```html
<!-- CSS principal (Fluig Voyager 2.0.0+) -->
<link rel="stylesheet" href="/style-guide/css/fluig-style-guide-flat.min.css" />

<!-- CSS legado (antes do Voyager 2.0.0) -->
<link rel="stylesheet" href="/portal/resources/style-guide/css/fluig-style-guide.min.css" />

<!-- JS -->
<script src="/portal/resources/style-guide/js/fluig-style-guide.min.js"></script>
```

Classes CSS comuns:
- `form-group` — Wrapper de campo
- `form-control` — Estilo de inputs
- `table`, `table-bordered`, `table-striped` — Tabelas
- `btn`, `btn-primary`, `btn-default`, `btn-danger` — Botões
- `alert`, `alert-success`, `alert-warning`, `alert-danger` — Alertas
- `panel`, `panel-default`, `panel-heading`, `panel-body` — Painéis
- `row`, `col-md-*` — Grid (12 colunas)
- `fluig-style-guide` — Wrapper obrigatório

### Exemplo: Formulário completo com grid

```html
<html>
<head>
    <link rel="stylesheet" href="/portal/resources/style-guide/css/fluig-style-guide.min.css" />
    <script src="/portal/resources/js/jquery/jquery.js"></script>
    <script src="/portal/resources/style-guide/js/fluig-style-guide.min.js"></script>
</head>
<body>
<div class="fluig-style-guide">
    <form name="form" role="form">
        <h3>Solicitação de Compra</h3>
        <div class="row">
            <div class="col-md-4">
                <div class="form-group">
                    <label>Solicitante</label>
                    <input type="text" class="form-control" name="solicitante" readonly />
                </div>
            </div>
            <div class="col-md-4">
                <div class="form-group">
                    <label>Data</label>
                    <input type="text" class="form-control" name="dataSolicitacao" readonly />
                </div>
            </div>
            <div class="col-md-4">
                <div class="form-group">
                    <label>Centro de Custo</label>
                    <select name="centroCusto" class="form-control"
                            dataset="dsCentroCusto" datasetkey="codigo" datasetvalue="descricao">
                    </select>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <div class="form-group">
                    <label>Justificativa</label>
                    <textarea class="form-control" name="justificativa" rows="3"></textarea>
                </div>
            </div>
        </div>
        <h4>Itens da Compra</h4>
        <table class="table table-bordered" tablename="itensCompra"
               addbuttonlabel="Adicionar Item" width="100%">
            <thead>
                <tr>
                    <td>Material</td>
                    <td>Quantidade</td>
                    <td>Valor Estimado</td>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><input class="form-control" name="material" type="text" /></td>
                    <td><input class="form-control" name="qtde" type="text" /></td>
                    <td><input class="form-control" name="valorEstimado" type="text" /></td>
                </tr>
            </tbody>
        </table>
        <div class="form-group">
            <label>
                <input type="checkbox" name="urgente" /> Solicitação Urgente
            </label>
        </div>
    </form>
</div>
</body>
</html>
```

---

## Diretrizes de Widgets e WCM

Widgets são componentes de interface reutilizáveis para páginas Fluig. São compostas por templates Freemarker (FTL), JavaScript client-side e CSS. Diferente dos formulários, widgets são executadas no contexto de páginas WCM (Web Content Management).

### Estrutura de uma Widget

```
minha-widget/
├── application.info          # Manifesto obrigatório
├── src/main/webapp/
│   ├── resources/
│   │   ├── js/
│   │   │   └── minha-widget.js    # JavaScript client-side
│   │   └── css/
│   │       └── minha-widget.css   # Estilos
│   └── WEB-INF/
│       └── jspf/
│           ├── view.ftl           # Template de visualização
│           └── edit.ftl           # Template de configuração
```

### Arquivo application.info

```properties
application.type=widget
application.title=Minha Widget
application.description=Descrição da minha widget
application.category=Categoria
application.renderer=freemarker
application.icon=icon-widget
developer.name=Desenvolvedor
developer.url=http://empresa.com
```

### Templates FTL (Freemarker)

Os templates usam a sintaxe Freemarker (FTL) para renderizar HTML dinâmico no servidor:

```html
<!-- view.ftl -->
<div id="minhaWidget_${instanceId}">
    <h3>${i18n.getTranslation("titulo.widget")}</h3>
    <div class="widget-content">
        <table class="table table-striped" id="tabela_${instanceId}">
            <thead>
                <tr>
                    <th>Nome</th>
                    <th>Email</th>
                </tr>
            </thead>
            <tbody id="corpo_${instanceId}">
            </tbody>
        </table>
    </div>
</div>
```

Variáveis FTL disponíveis:
- `${instanceId}` — ID único da instância da widget na página (SEMPRE use para evitar conflitos com múltiplas instâncias)
- `${i18n.getTranslation("chave")}` — Internacionalização
- `${request.contextPath}` — Contexto da aplicação

### JavaScript da Widget

IMPORTANTE: O JavaScript de widgets roda no CLIENT-SIDE (navegador), então pode usar ES6+ se o navegador suportar. Porém, para máxima compatibilidade, recomenda-se ES5.

```javascript
var MinhaWidget = SuperWidget.extend({
    instanceId: null,
    
    init: function() {
        this.instanceId = this.options.instanceId;
        this.carregarDados();
    },
    
    bindings: {
        local: {
            'click #btnAtualizar': ['atualizar']
        }
    },
    
    carregarDados: function() {
        var self = this;
        FLUIGC.ajax({
            type: 'GET',
            url: '/api/public/ecm/dataset/search',
            data: {
                datasetId: 'colleague'
            },
            success: function(result) {
                self.renderizarTabela(result);
            },
            error: function(args) {
                WCMAPI.failHandler(args, true);
            }
        });
    },
    
    atualizar: function() {
        this.carregarDados();
    },
    
    renderizarTabela: function(dados) {
        var html = '';
        for (var i = 0; i < dados.length; i++) {
            html += '<tr>';
            html += '<td>' + dados[i].nome + '</td>';
            html += '<td>' + dados[i].email + '</td>';
            html += '</tr>';
        }
        $('#corpo_' + this.instanceId).html(html);
    }
});
```

### WCMAPI — API Client-Side

| Método | Descrição |
|---|---|
| `WCMAPI.version` | Versão do Fluig |
| `WCMAPI.serverURL` / `WCMAPI.getServerURL()` | Endereço do servidor |
| `WCMAPI.organizationId` / `WCMAPI.getOrganizationId()` | ID do tenant |
| `WCMAPI.tenantCode` / `WCMAPI.getTenantCode()` | Código do tenant |
| `WCMAPI.serverContextURL` / `WCMAPI.getServerContextURL()` | Retorna "/portal" |
| `WCMAPI.getProtectedContextPath()` | Retorna "/portal/p" |
| `WCMAPI.Create(options)` | Envia requisição ao servidor |
| `WCMAPI.logoff()` | Encerra a sessão do usuário |
| `WCMAPI.addListener(widget, event, callback)` | Adiciona listener de evento entre widgets |
| `WCMAPI.fireEvent(event, data)` | Dispara evento para outras widgets |
| `WCMAPI.failHandler(args, showAlert)` | Exibe alerta de erro de requisição |
| `WCMAPI.convertFtlAsync(widgetName, ftlName, data, callback)` | Renderiza template FTL no frontend |
| `WCMAPI.generateId()` | Gera ID único (wcmid4, wcmid5, ...) |
| `WCMAPI.getSourceImage(src, options, callback)` | Retorna URL ou base64 de imagem |
| `WCMAPI.setSessionAttribute(key, value)` | Salva valor na sessão (backend) |
| `WCMAPI.getSessionAttribute(key)` | Recupera valor da sessão (backend) |
| `WCMAPI.isNull(value)` | Verifica se valor é nulo |

### Exemplo: WCMAPI.Create — Requisição customizada

```javascript
WCMAPI.Create({
    url: '/api/public/ecm/dataset/search',
    contentType: 'application/json',
    dataType: 'json',
    data: JSON.stringify({datasetId: 'colleague'}),
    success: function(data) {
        // processar resultado
    }
});
```

### Exemplo: Comunicação entre Widgets

```javascript
// Widget A — Disparar evento
var dados = [{id: 1, nome: 'Item Selecionado'}];
WCMAPI.fireEvent('item-selecionado', dados);

// Widget B — Ouvir evento
WCMAPI.addListener(this, 'item-selecionado', function(eventName, data) {
    // data contém os dados do evento
    console.log("Item recebido:", data);
});
```

### Exemplo: Renderizar FTL via JavaScript

```javascript
WCMAPI.convertFtlAsync('minha-widget', 'item-template', JSON.stringify({
    nome: 'Produto',
    valor: 99.90
}), function(html) {
    $('#container_' + this.instanceId).append(html);
});
```

### FLUIGC — Componentes de UI

O Fluig oferece componentes prontos via `FLUIGC`:

```javascript
// DataTable com Dataset
var tabela = FLUIGC.datatable('#meuContainer', {
    dataRequest: {
        url: '/api/public/ecm/dataset/search',
        options: {
            contentType: 'application/json',
            dataType: 'json',
            method: 'POST',
            data: JSON.stringify({datasetId: 'colleague'}),
            crossDomain: true,
            cache: false
        },
        root: '',
        limit: 10
    },
    renderContent: ['colleagueName', 'mail'],
    multiSelect: false,
    search: { enabled: true },
    scroll: { target: '#meuContainer', enabled: true }
});

// Toast (notificação)
FLUIGC.toast({
    title: 'Sucesso',
    message: 'Operação realizada com sucesso!',
    type: 'success'  // success, warning, danger, info
});

// Modal
FLUIGC.modal('#meuModal', {
    title: 'Confirmação',
    content: '<p>Deseja continuar?</p>',
    size: 'small',
    actions: [{
        label: 'Confirmar',
        autoClose: true
    }]
});
```

### Acessando Datasets via Client-Side (Widget)

Inclua `vcXMLRPC.js` para acessar datasets no navegador:

```html
<script src="/webdesk/vcXMLRPC.js"></script>
<script>
var constraints = [];
constraints.push(DatasetFactory.createConstraint("colleaguePK.colleagueId", "admin", "admin", ConstraintType.MUST));
var dataset = DatasetFactory.getDataset("colleague", null, constraints, null);
for (var i = 0; i < dataset.values.length; i++) {
    var nome = dataset.values[i]["colleagueName"];
    console.log(nome);
}
</script>
```

### Eventos Globais — Referência rápida

Eventos globais são scripts server-side que reagem a ações globais da plataforma (login, criação de usuários, notificações, etc.). São criados no Fluig Studio na pasta `events`.

| Evento | Descrição |
|---|---|
| `beforeLogin(login)` / `afterLogin(login)` | Login do usuário |
| `onLoginError(login, errorCause)` | Erro no login |
| `onLogout(login)` | Logout |
| `beforeCreateUser(user)` / `afterCreateUser(user)` | Criação de usuário (UserEventVO) |
| `beforeUpdateUser(user)` / `afterUpdateUser(user)` | Atualização de usuário |
| `beforeDeactivateUser(login)` / `afterDeactivateUser(login)` | Desativação de usuário |
| `beforeActivateUser(login)` / `afterActivateUser(login)` | Ativação de usuário |
| `onNotify(subject, receivers, template, params)` | Customização de notificações |
| `beforeSendNotification / afterSendNotification` | Envio de notificações |
| `displayCentralTasks(links)` | Antes da exibição da central de tarefas |
| `onDisplayTasks(tasks)` | Customização da exibição de tarefas |
| `onDisplayTasksSummary(resumeTasks)` | Customização do contador de tarefas |
| `afterReleaseProcessVersion` | Após liberação de versão de processo |

```javascript
// Exemplo: Evento global - bloquear login fora do horário
function beforeLogin(login) {
    var hora = java.util.Calendar.getInstance().get(java.util.Calendar.HOUR_OF_DAY);
    if (hora < 7 || hora > 22) {
        throw "Acesso não permitido fora do horário comercial (7h às 22h)";
    }
}

// Exemplo: Evento global - log após criação de usuário
function afterCreateUser(user) {
    log.info("Novo usuário criado: " + user.getLogin());
    log.info("Email: " + user.getEmail());
    log.info("Nome: " + user.getFullName());
}
```

---

## Diretrizes de Integrações

O Fluig suporta integração com sistemas externos via SOAP WebServices, REST API (OAuth), e acesso direto a banco de dados via JNDI/JDBC.

### Integração via WebServices SOAP (ServiceManager)

O Fluig permite consumir WebServices SOAP registrados na plataforma via `ServiceManager`. Os serviços devem ser previamente cadastrados no Painel de Controle.

Padrão de consumo:
1. Obter instância do serviço: `ServiceManager.getServiceInstance("nomeServico")`
2. Instanciar o locator: `.instantiate("pacote.ClasseLocator")`
3. Obter a porta: `.getPort()` ou `.getXxxServicePort()`
4. Chamar os métodos

Regras:
- SEMPRE registre o WebService no Painel de Controle antes de usar no código.
- SEMPRE use `ServiceManager.getServiceInstance("nome")` — o nome é o cadastrado no Painel.
- Use `.instantiate("classe")` para criar instâncias de classes do stub gerado.
- Todos os métodos de WS são do tipo POST — envie todos os campos obrigatórios na atualização.

### Exemplo: Criar usuário via ColleagueService

```javascript
function afterTaskComplete(colleagueId, nextSequenceId, userList) {
    if (nextSequenceId == 2) {
        var provider = ServiceManager.getServiceInstance("Colleague");
        var locator = provider.instantiate("com.totvs.technology.ecm.foundation.ws.ECMColleagueServiceService");
        var service = locator.getColleagueServicePort();

        var dto = provider.instantiate("com.totvs.technology.ecm.foundation.ws.ColleagueDto");
        dto.setCompanyId(1);
        dto.setColleagueId("novo_usuario");
        dto.setColleagueName("Novo Usuário");
        dto.setActive(true);
        dto.setVolumeId("Default");
        dto.setLogin("novo_usuario");
        dto.setMail("[email protected]");
        dto.setPasswd("senha123");
        dto.setAdminUser(false);
        dto.setEmailHtml(true);
        dto.setDialectId("pt_BR");

        var dtoArray = provider.instantiate("com.totvs.technology.ecm.foundation.ws.ColleagueDtoArray");
        dtoArray.getItem().add(dto);

        var result = service.createColleague("admin", "admin", 1, dtoArray);
        log.info("Resultado: " + result);
    }
}
```

### Exemplo: Atualizar campo de formulário via ECMCardService

```javascript
function afterStateEntry(sequenceId) {
    if (sequenceId == 2) {
        var provider = ServiceManager.getServiceInstance("ECMCardService");
        var locator = provider.instantiate("com.totvs.technology.ecm.dm.ws.ECMCardServiceService");
        var service = locator.getCardServicePort();

        var fieldArray = provider.instantiate("com.totvs.technology.ecm.dm.ws.CardFieldDtoArray");
        var field = provider.instantiate("com.totvs.technology.ecm.dm.ws.CardFieldDto");
        field.setField("status");
        field.setValue("Aprovado via WS");

        var fields = new Array();
        fields.push(field);
        fieldArray.getItem().addAll(fields);

        service.updateCardData(1, "admin", "admin", 8, fieldArray);
    }
}
```

### Integração via REST API (OAuth)

O Fluig expõe APIs REST acessíveis via OAuth 1.0. Para consumir nos eventos server-side, use `oauthUtil`.

Pré-requisitos:
- Cadastrar aplicativo OAuth no Painel de Controle (gera Consumer Key, Consumer Secret, Access Token, Token Secret)
- Ou usar `oauthUtil.getNewAPIConsumerAsCurrentUser()` para autenticar como o usuário corrente

### Exemplo: Consumir API REST desde um evento

```javascript
function afterStateEntry(sequenceId) {
    if (sequenceId == 3) {
        // Com credenciais explícitas
        var consumer = oauthUtil.getNewAPIConsumer(
            "consumer_key",
            "consumer_secret",
            "access_token",
            "token_secret"
        );

        // GET — buscar dados
        var response = consumer.get("/api/public/2.0/users/getCurrent");
        log.info("Resposta GET: " + response.getResult());

        // POST — enviar dados
        var body = '{"field": "value"}';
        var postResponse = consumer.post("/api/public/2.0/...", body);
        log.info("Resposta POST: " + postResponse.getResult());
    }
}
```

### Exemplo: API REST como usuário corrente

```javascript
function afterStateEntry(sequenceId) {
    // Autenticação como o usuário logado (sem credenciais explícitas)
    var consumer = oauthUtil.getNewAPIConsumerAsCurrentUser();
    var response = consumer.get("/api/public/2.0/users/getCurrent");
    log.info("Usuário: " + response.getResult());
}
```

### docAPI — API de Documentos

A `docAPI` permite criar e manipular documentos e pastas do GED (Gestão Eletrônica de Documentos) a partir de eventos.

| Método | Descrição |
|---|---|
| `docAPI.newDocumentDto()` | Nova instância de DocumentDto (tipo 2 como padrão) |
| `docAPI.newAttachment()` | Nova instância de Attachment |
| `docAPI.newApproverDto()` | Nova instância de ApproverDto |
| `docAPI.newDocumentSecurityConfigDto()` | Nova instância de DocumentSecurityConfigDto |
| `docAPI.newRelatedDocumentDto()` | Nova instância de RelatedDocumentDto |
| `docAPI.createDocument(doc, attachments, security, approvers, relatedDocs)` | Cria documento no GED. Retorna DocumentDto. |
| `docAPI.createFolder(doc, security, approvers)` | Cria pasta no GED. Retorna DocumentDto. |
| `docAPI.copyDocumentToUploadArea(docId, version)` | Copia arquivo para área de upload. Retorna Array de Strings. |
| `docAPI.getDocumentVersion(docId, version)` | Retorna DocumentDto de um documento |
| `docAPI.getUserPermissions(docId, version)` | Retorna permissão do usuário no documento |
| `docAPI.isUserInGroup(group)` | Verifica se usuário logado pertence ao grupo |

### Exemplo: Criar pasta no GED

```javascript
function afterProcessFinish(processId) {
    try {
        var dto = docAPI.newDocumentDto();
        dto.setDocumentDescription("Documentos do Processo " + processId);
        dto.setDocumentType("1"); // 1 = Pasta
        dto.setParentDocumentId(20); // Pasta pai
        dto.setDocumentTypeId("");
        var folder = docAPI.createFolder(dto, null, null);
        log.info("Pasta criada com ID: " + folder.getDocumentId());
    } catch (e) {
        log.error("Erro ao criar pasta: " + e);
    }
}
```

### Exemplo: Publicar anexo workflow como documento no GED

```javascript
function beforeStateEntry(sequenceId) {
    if (sequenceId == 5) {
        var attachments = hAPI.listAttachments();
        for (var i = 0; i < attachments.size(); i++) {
            var docDto = attachments.get(i);
            if (docDto.getDocumentType() == "7") { // 7 = Anexo workflow
                docAPI.copyDocumentToUploadArea(docDto.getDocumentId(), docDto.getVersion());
                docDto.setDocumentId(0);
                docDto.setParentDocumentId(20);

                var mainAttach = docAPI.newAttachment();
                mainAttach.setFileName(docDto.getPhisicalFile());
                mainAttach.setPrincipal(true);
                mainAttach.setAttach(false);

                var attachArray = new java.util.ArrayList();
                attachArray.add(mainAttach);

                docDto.setActiveVersion(true);
                docDto.setColleagueId(getValue("WKUser"));
                docDto.setPublisherId(getValue("WKUser"));

                try {
                    var doc = docAPI.createDocument(docDto, attachArray, null, null, null);
                    log.info("Documento publicado ID: " + doc.getDocumentId());
                } catch (e) {
                    log.error("Erro na publicação: " + e);
                }
            }
        }
    }
}
```

---

## Diretrizes de Logging e Debug

### Objetos de log

| Contexto | Objeto | Disponibilidade |
|---|---|---|
| Server-side (Rhino) | `log` | Todas as versões |
| Server-side (Rhino 2.0+) | `console` | A partir da atualização 2.0 |

### Métodos disponíveis

| Método | Nível | Descrição |
|---|---|---|
| `log.info(msg)` / `console.log(msg)` | INFO | Mensagens informativas |
| `log.warn(msg)` / `console.warn(msg)` | WARN | Avisos |
| `log.error(msg)` / `console.error(msg)` | ERROR | Erros |
| `log.debug(msg)` / `console.debug(msg)` | DEBUG | Debug detalhado |
| `log.dir(obj)` / `console.dir(obj)` | INFO | Imprime objeto como JSON |

### Configuração de truncamento

Por padrão, mensagens de log são truncadas. Para alterar o limite:

No Linux (`setenv.sh`):
```bash
JAVA_OPTS="$JAVA_OPTS -Dcom.fluig.sdk.api.log.ScriptingLog.truncateLength=500"
```

No Windows (`setenv.bat`):
```bat
set "JAVA_OPTS=%JAVA_OPTS% -Dcom.fluig.sdk.api.log.ScriptingLog.truncateLength=500"
```

### Boas práticas de logging

- Use `log.info()` para registrar marcos do fluxo (entrada em atividades, dados processados)
- Use `log.warn()` para situações inesperadas mas não críticas
- Use `log.error()` dentro de blocos `catch` para registrar exceções
- Use `log.debug()` para detalhamento em desenvolvimento (desabilite em produção)
- Use `log.dir()` para inspecionar objetos complexos (mapas, arrays)
- NUNCA faça log de senhas, tokens ou dados sensíveis
- SEMPRE inclua contexto na mensagem: número do processo, usuário, atividade

```javascript
function beforeStateEntry(sequenceId) {
    var processo = getValue("WKNumProces");
    var usuario = getValue("WKUser");
    log.info("[Processo " + processo + "] Entrada na atividade " + sequenceId + " por " + usuario);

    try {
        var valor = hAPI.getCardValue("campo");
        log.debug("[Processo " + processo + "] Valor do campo: " + valor);
    } catch (e) {
        log.error("[Processo " + processo + "] Erro ao ler campo: " + e.message);
    }
}
```

---

## Estrutura de Projeto Fluig

Projetos Fluig são criados via Fluig Studio (IDE baseada no Eclipse). A estrutura de pastas segue um padrão:

```
meu-projeto-fluig/
├── events/                      # Eventos globais (.js)
│   ├── afterLogin.js
│   ├── beforeCreateUser.js
│   └── ...
├── forms/                       # Formulários HTML
│   └── meu-formulario/
│       ├── meu-formulario.html  # HTML do formulário
│       └── events/              # Eventos do formulário
│           ├── displayFields.js
│           ├── validateForm.js
│           ├── enableFields.js
│           └── ...
├── processes/                   # Processos BPM
│   └── meu-processo/
│       ├── meu-processo.process # Diagrama BPMN 2.0
│       └── events/              # Eventos do processo
│           ├── beforeStateEntry.js
│           ├── afterTaskCreate.js
│           └── ...
├── datasets/                    # Datasets avançados (.js)
│   └── ds_meu_dataset.js
├── wcm/                         # Widgets
│   └── minha-widget/
│       ├── application.info
│       └── src/main/webapp/...
├── mechanisms/                  # Mecanismos de atribuição
└── reports/                     # Relatórios BIRT
```

### Regras de estrutura

- Cada formulário fica em subpasta própria dentro de `forms/`.
- Cada processo fica em subpasta própria dentro de `processes/`.
- Eventos de formulário ficam em `forms/nome/events/`.
- Eventos de processo ficam em `processes/nome/events/`.
- Eventos globais ficam diretamente em `events/`.
- Datasets ficam em `datasets/` — o nome do arquivo é o código do dataset.
- Widgets seguem a estrutura padrão com `application.info` e templates FTL.

### Fluxo de desenvolvimento

1. **Criar projeto** no Fluig Studio (File > New > Fluig Project)
2. **Configurar servidor** no Studio (IP, porta, credenciais)
3. **Desenvolver** formulários, processos, datasets, eventos, widgets
4. **Exportar/Deploy** para o servidor Fluig (botão Export no Studio)
5. **Testar** no ambiente Fluig

### Importação e exportação

- Use o Fluig Studio para importar/exportar processos, formulários, eventos globais e relatórios.
- Exportação gera um pacote que pode ser importado em outro ambiente.
- Processos ECM 3 podem ser importados para o Fluig.

---

## Snippets e Aceleradores de Desenvolvimento

Padrões de código reutilizáveis para desenvolvimento Fluig organizados por categoria.

### BPM — Adicionar linha em tabela filha via evento

```javascript
function beforeStateEntry(sequenceId) {
    var childData = new java.util.HashMap();
    childData.put("descricao", hAPI.getCardValue("descricao_item"));
    childData.put("quantidade", hAPI.getCardValue("qtde_item"));
    childData.put("valor", hAPI.getCardValue("valor_item"));
    hAPI.addCardChild("itens", childData);
}
```

### BPM — Consultar dataset pai-filho em evento de processo

```javascript
function beforeStateEntry(sequenceId) {
    var user = getValue("WKUser");
    var cst1 = DatasetFactory.createConstraint("metadata#active", true, true, ConstraintType.MUST);
    var cst2 = DatasetFactory.createConstraint("userSecurityId", user, user, ConstraintType.MUST);
    var dataset = DatasetFactory.getDataset("dsFormulario", null, new Array(cst1, cst2), null);

    for (var i = 0; i < dataset.rowsCount; i++) {
        var docId = dataset.getValue(i, "metadata#id");
        var docVer = dataset.getValue(i, "metadata#version");

        var c1 = DatasetFactory.createConstraint("tablename", "itens", "itens", ConstraintType.MUST);
        var c2 = DatasetFactory.createConstraint("metadata#id", docId, docId, ConstraintType.MUST);
        var c3 = DatasetFactory.createConstraint("metadata#version", docVer, docVer, ConstraintType.MUST);
        var c4 = DatasetFactory.createConstraint("userSecurityId", user, user, ConstraintType.MUST);

        var filhos = DatasetFactory.getDataset("dsFormulario", null, new Array(c1, c2, c3, c4), null);
        for (var j = 0; j < filhos.rowsCount; j++) {
            log.info("Item: " + filhos.getValue(j, "descricao"));
        }
    }
}
```

### BPM — Criar pasta GED via docAPI

```javascript
function afterProcessCreate(processId) {
    try {
        var dto = docAPI.newDocumentDto();
        dto.setDocumentDescription("Processo " + processId);
        dto.setDocumentType("1");
        dto.setParentDocumentId(100);
        dto.setDocumentTypeId("");
        var pasta = docAPI.createFolder(dto, null, null);
        log.info("Pasta criada: " + pasta.getDocumentId());
    } catch (e) {
        log.error("Erro: " + e);
    }
}
```

### BPM — Enviar e-mail via evento

```javascript
function afterTaskCreate(colleagueId) {
    var destinatarios = new java.util.ArrayList();
    destinatarios.add(colleagueId);
    var parametros = new java.util.HashMap();
    parametros.put("WDK_CompanyId", getValue("WKCompany"));
    parametros.put("assunto", "Nova tarefa atribuída");
    parametros.put("corpo", "Você recebeu uma nova solicitação: " + getValue("WKNumProces"));
    notifier.notify(getValue("WKUser"), "templateEmail", parametros, destinatarios, "text/html");
}
```

### BPM — Obter grupos do usuário via FluigAPI

```javascript
function beforeStateEntry(sequenceId) {
    var user = getValue("WKUser");
    var company = getValue("WKCompany");
    var filter = [
        DatasetFactory.createConstraint("colleagueGroupPK.companyId", company, company, ConstraintType.MUST),
        DatasetFactory.createConstraint("colleagueGroupPK.colleagueId", user, user, ConstraintType.MUST)
    ];
    var dsGrupos = DatasetFactory.getDataset("colleagueGroup", null, filter, null);
    for (var i = 0; i < dsGrupos.rowsCount; i++) {
        log.info("Grupo: " + dsGrupos.getValue(i, "colleagueGroupPK.groupId"));
    }
}
```

### DATASET — Busca com LIKE

```javascript
function createDataset(fields, constraints, sortFields) {
    var c1 = DatasetFactory.createConstraint("mail", "%@empresa.com%", "%@empresa.com%", ConstraintType.SHOULD);
    c1.setLikeSearch(true);
    var dataset = DatasetFactory.getDataset("colleague", null, new Array(c1), null);
    return dataset;
}
```

### DATASET — Dados de fonte externa com serviço autorizado

```javascript
function createDataset(fields, constraints, sortFields) {
    var newDataset = DatasetBuilder.newDataset();
    newDataset.addColumn("id");
    newDataset.addColumn("nome");
    newDataset.addColumn("email");

    try {
        var consumer = oauthUtil.getNewAPIConsumer(
            "consumer_key", "consumer_secret",
            "access_token", "token_secret"
        );
        var response = consumer.get("/api/public/2.0/users/listAll");
        var dados = JSON.parse(response.getResult());

        for (var i = 0; i < dados.content.length; i++) {
            var user = dados.content[i];
            newDataset.addRow(new Array(user.userCode, user.fullName, user.email));
        }
    } catch (e) {
        log.error("Erro ao buscar dados: " + e);
    }
    return newDataset;
}
```

### WCM — Requisição REST GET (Widget)

```javascript
$.ajax({
    type: 'GET',
    url: WCMAPI.getServerURL() + '/api/public/2.0/users/getCurrent',
    contentType: 'application/json',
    success: function(data) {
        console.log("Usuário: " + data.content.fullName);
    },
    error: function(xhr) {
        WCMAPI.failHandler(xhr, true);
    }
});
```

### WCM — Requisição REST POST (Widget)

```javascript
$.ajax({
    type: 'POST',
    url: WCMAPI.getServerURL() + '/api/public/ecm/document/createDocument',
    contentType: 'application/json',
    data: JSON.stringify({
        description: 'Meu Documento',
        parentId: 100,
        attachments: []
    }),
    success: function(data) {
        FLUIGC.toast({
            title: 'Sucesso',
            message: 'Documento criado!',
            type: 'success'
        });
    }
});
```

### WCM — DataTable com Dataset

```javascript
var tabela = FLUIGC.datatable('#container', {
    dataRequest: {
        url: '/api/public/ecm/dataset/search',
        options: {
            contentType: 'application/json',
            dataType: 'json',
            method: 'POST',
            data: JSON.stringify({ datasetId: 'colleague' })
        },
        root: '',
        limit: 10
    },
    renderContent: ['colleagueName', 'mail', 'login'],
    multiSelect: false,
    search: { enabled: true },
    scroll: { target: '#container', enabled: true }
});
```

### Validação de CPF (Client-Side)

```javascript
function validarCPF(cpf) {
    cpf = cpf.replace(/[^\d]+/g, '');
    if (cpf.length != 11 || /^(\d)\1{10}$/.test(cpf)) return false;
    var soma = 0;
    for (var i = 0; i < 9; i++) soma += parseInt(cpf.charAt(i)) * (10 - i);
    var resto = 11 - (soma % 11);
    if (resto == 10 || resto == 11) resto = 0;
    if (resto != parseInt(cpf.charAt(9))) return false;
    soma = 0;
    for (var i = 0; i < 10; i++) soma += parseInt(cpf.charAt(i)) * (11 - i);
    resto = 11 - (soma % 11);
    if (resto == 10 || resto == 11) resto = 0;
    if (resto != parseInt(cpf.charAt(10))) return false;
    return true;
}
```

### Validação de CNPJ (Client-Side)

```javascript
function validarCNPJ(cnpj) {
    cnpj = cnpj.replace(/[^\d]+/g, '');
    if (cnpj.length != 14) return false;
    var tamanho = cnpj.length - 2;
    var numeros = cnpj.substring(0, tamanho);
    var digitos = cnpj.substring(tamanho);
    var soma = 0;
    var pos = tamanho - 7;
    for (var i = tamanho; i >= 1; i--) {
        soma += parseInt(numeros.charAt(tamanho - i)) * pos--;
        if (pos < 2) pos = 9;
    }
    var resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado != parseInt(digitos.charAt(0))) return false;
    tamanho = tamanho + 1;
    numeros = cnpj.substring(0, tamanho);
    soma = 0;
    pos = tamanho - 7;
    for (var i = tamanho; i >= 1; i--) {
        soma += parseInt(numeros.charAt(tamanho - i)) * pos--;
        if (pos < 2) pos = 9;
    }
    resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado != parseInt(digitos.charAt(1))) return false;
    return true;
}
```

---

## Exemplo Completo: Processo de Solicitação de Compras

Este exemplo demonstra um processo BPM completo com formulário, dataset avançado, eventos de processo e eventos de formulário — cobrindo os principais conceitos do desenvolvimento Fluig.

### Visão geral

- **Processo:** Solicitação de Compras com aprovação
- **Fluxo:** Solicitante → Aprovador → Compras → Finalizado
- **Formulário:** Nome, data, centro de custo, justificativa, itens (pai-filho), urgência
- **Dataset:** Consulta itens aprovados para relatório
- **Eventos:** Preenchimento automático, validações, decisão automática por valor

### Estrutura do projeto

```
solicitacao-compras/
├── forms/
│   └── formCompras/
│       ├── formCompras.html
│       └── events/
│           ├── displayFields.js
│           ├── validateForm.js
│           └── enableFields.js
├── processes/
│   └── solCompras/
│       ├── solCompras.process
│       └── events/
│           ├── beforeStateEntry.js
│           ├── afterTaskCreate.js
│           └── beforeTaskSave.js
├── datasets/
│   └── ds_itens_aprovados.js
└── events/
```

### 1. Formulário HTML (formCompras.html)

```html
<html>
<head>
    <link rel="stylesheet" href="/portal/resources/style-guide/css/fluig-style-guide.min.css" />
    <script src="/portal/resources/js/jquery/jquery.js"></script>
    <script src="/portal/resources/style-guide/js/fluig-style-guide.min.js"></script>
</head>
<body>
<div class="fluig-style-guide">
    <form name="form" role="form">
        <h3>Solicitação de Compras</h3>

        <div class="row">
            <div class="col-md-3">
                <div class="form-group">
                    <label>Solicitante</label>
                    <input type="text" class="form-control" name="solicitante" id="solicitante" readonly />
                </div>
            </div>
            <div class="col-md-3">
                <div class="form-group">
                    <label>Nome do Solicitante</label>
                    <input type="text" class="form-control" name="nomeSolicitante" id="nomeSolicitante" readonly />
                </div>
            </div>
            <div class="col-md-3">
                <div class="form-group">
                    <label>Data da Solicitação</label>
                    <input type="text" class="form-control" name="dataSolicitacao" id="dataSolicitacao" readonly />
                </div>
            </div>
            <div class="col-md-3">
                <div class="form-group">
                    <label>Centro de Custo</label>
                    <select name="centroCusto" class="form-control">
                        <option value="">Selecione...</option>
                        <option value="TI">TI</option>
                        <option value="RH">Recursos Humanos</option>
                        <option value="FIN">Financeiro</option>
                        <option value="COM">Comercial</option>
                    </select>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-md-12">
                <div class="form-group">
                    <label>Justificativa</label>
                    <textarea class="form-control" name="justificativa" id="justificativa" rows="3"></textarea>
                </div>
            </div>
        </div>

        <h4>Itens da Compra</h4>
        <table class="table table-bordered" tablename="itensCompra"
               addbuttonlabel="Adicionar Item" width="100%" id="tabelaItens">
            <thead>
                <tr>
                    <td>Descrição do Material</td>
                    <td>Quantidade</td>
                    <td>Valor Unitário (R$)</td>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><input class="form-control" name="material" type="text" /></td>
                    <td><input class="form-control" name="qtde" type="text" /></td>
                    <td><input class="form-control" name="valorUnit" type="text" /></td>
                </tr>
            </tbody>
        </table>

        <div class="row">
            <div class="col-md-4">
                <div class="form-group">
                    <label>Valor Total Estimado (R$)</label>
                    <input type="text" class="form-control" name="valorTotal" id="valorTotal" readonly />
                </div>
            </div>
            <div class="col-md-4">
                <div class="form-group">
                    <label>
                        <input type="checkbox" name="urgente" /> Solicitação Urgente
                    </label>
                </div>
            </div>
            <div class="col-md-4">
                <div class="form-group">
                    <label>Status</label>
                    <input type="text" class="form-control" name="status" id="status" readonly />
                </div>
            </div>
        </div>

        <!-- Campos do aprovador (ocultos na primeira atividade) -->
        <div id="areaAprovacao">
            <h4>Aprovação</h4>
            <div class="row">
                <div class="col-md-6">
                    <div class="form-group">
                        <label>Parecer</label>
                        <select name="parecer" class="form-control">
                            <option value="">Selecione...</option>
                            <option value="aprovado">Aprovado</option>
                            <option value="reprovado">Reprovado</option>
                            <option value="devolvido">Devolvido para ajuste</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-group">
                        <label>Observação do Aprovador</label>
                        <textarea class="form-control" name="obsAprovador" rows="2"></textarea>
                    </div>
                </div>
            </div>
        </div>
    </form>
</div>
</body>
</html>
```

### 2. Evento displayFields.js (Formulário)

```javascript
function displayFields(form, customHTML) {
    var atividadeAtual = getValue("WKNumState");
    var modo = form.getFormMode();
    var usuario = getValue("WKUser");

    // Atividade inicial (0) ou primeira atividade (1): preencher dados do solicitante
    if (modo != "VIEW") {
        if (atividadeAtual == 0 || atividadeAtual == 1) {
            form.setValue("solicitante", usuario);
            form.setValue("nomeSolicitante", buscaNomeUsuario(usuario));
            form.setValue("dataSolicitacao", retornaDataAtual());
            form.setValue("status", "Em Análise");
        }
    }

    // Ocultar área de aprovação na primeira atividade
    if (atividadeAtual == 0 || atividadeAtual == 1) {
        form.setVisibleById("areaAprovacao", false);
    }

    // Injetar variáveis para uso no client-side
    customHTML.append("<script type='text/javascript'>");
    customHTML.append("var modoFormulario = '" + modo + "';");
    customHTML.append("var atividadeAtual = " + atividadeAtual + ";");
    customHTML.append("</script>");
}

function retornaDataAtual() {
    return (new java.text.SimpleDateFormat("dd/MM/yyyy")).format(new java.util.Date());
}

function buscaNomeUsuario(codigo) {
    var c = DatasetFactory.createConstraint("colleaguePK.colleagueId", codigo, codigo, ConstraintType.MUST);
    var ds = DatasetFactory.getDataset("colleague", null, [c], null);
    if (ds.rowsCount > 0) {
        return ds.getValue(0, "colleagueName");
    }
    return "";
}
```

### 3. Evento validateForm.js (Formulário)

```javascript
function validateForm(form) {
    var atividadeAtual = getValue("WKNumState");

    // Validações na atividade do solicitante
    if (atividadeAtual == 0 || atividadeAtual == 1) {
        if (!form.getValue("centroCusto") || form.getValue("centroCusto") == "") {
            throw "Selecione o Centro de Custo!";
        }
        if (!form.getValue("justificativa") || form.getValue("justificativa").trim() == "") {
            throw "Informe a Justificativa da compra!";
        }
    }

    // Validações na atividade do aprovador
    if (atividadeAtual == 2) {
        if (!form.getValue("parecer") || form.getValue("parecer") == "") {
            throw "Selecione o Parecer (Aprovado/Reprovado/Devolvido)!";
        }
    }
}
```

### 4. Evento enableFields.js (Formulário)

```javascript
function enableFields(form) {
    var atividadeAtual = getValue("WKNumState");

    // Na atividade de aprovação, desabilitar campos do solicitante
    if (atividadeAtual == 2) {
        form.setEnabled("solicitante", false);
        form.setEnabled("nomeSolicitante", false);
        form.setEnabled("dataSolicitacao", false);
        form.setEnabled("centroCusto", false);
        form.setEnabled("justificativa", false);
        form.setEnabled("valorTotal", false);
    }

    // Na atividade de compras, tudo readonly exceto status
    if (atividadeAtual == 3) {
        form.setEnabled("solicitante", false);
        form.setEnabled("nomeSolicitante", false);
        form.setEnabled("dataSolicitacao", false);
        form.setEnabled("centroCusto", false);
        form.setEnabled("justificativa", false);
        form.setEnabled("parecer", false);
        form.setEnabled("obsAprovador", false);
    }
}
```

### 5. Evento beforeStateEntry.js (Processo)

```javascript
function beforeStateEntry(sequenceId) {
    var processo = getValue("WKNumProces");
    log.info("[Sol.Compras #" + processo + "] Entrando na atividade " + sequenceId);

    // Atividade 2 = Aprovação — decisão automática para valores baixos
    if (sequenceId == 2) {
        var valorTotal = parseFloat(hAPI.getCardValue("valorTotal"));
        if (!isNaN(valorTotal) && valorTotal <= 500) {
            log.info("[Sol.Compras #" + processo + "] Valor <= R$500. Aprovação automática.");
            hAPI.setCardValue("parecer", "aprovado");
            hAPI.setCardValue("obsAprovador", "Aprovação automática (valor <= R$500)");
            hAPI.setCardValue("status", "Aprovado");
            var users = new java.util.ArrayList();
            users.add("Pool:Group:compras");
            hAPI.setAutomaticDecision(3, users, "Aprovado automaticamente por valor");
        }
    }

    // Atividade 3 = Compras — atualizar status
    if (sequenceId == 3) {
        hAPI.setCardValue("status", "Em Processamento");
    }
}
```

### 6. Evento afterTaskCreate.js (Processo)

```javascript
function afterTaskCreate(colleagueId) {
    var atividade = getValue("WKCurrentState");
    var processo = getValue("WKNumProces");

    // Definir prazo de 48h para aprovação
    if (atividade == 2) {
        var data = new Date();
        var prazo = hAPI.calculateDeadLineHours(data, 0, 48, "Default");
        hAPI.setDueDate(processo, 0, colleagueId, prazo[0], prazo[1]);
        log.info("[Sol.Compras #" + processo + "] Prazo de 48h definido para " + colleagueId);
    }

    // Notificar solicitante sobre a aprovação
    if (atividade == 3) {
        var solicitante = hAPI.getCardValue("solicitante");
        if (solicitante && solicitante != "") {
            var destinatarios = new java.util.ArrayList();
            destinatarios.add(solicitante);
            var params = new java.util.HashMap();
            params.put("WDK_CompanyId", getValue("WKCompany"));
            params.put("processo", processo);
            params.put("status", "Sua solicitação foi aprovada e encaminhada para Compras.");
            notifier.notify(getValue("WKUser"), "notifCompras", params, destinatarios, "text/html");
        }
    }
}
```

### 7. Evento beforeTaskSave.js (Processo)

```javascript
function beforeTaskSave(colleagueId, nextSequenceId, userList) {
    var completTask = getValue("WKCompletTask");
    var atividade = getValue("WKNumState");

    // Validar se existe ao menos 1 item na tabela ao movimentar
    if (completTask == "true" && (atividade == 0 || atividade == 1)) {
        var indexes = hAPI.getChildrenIndexes("itensCompra");
        if (indexes == null || indexes.length == 0) {
            throw "Adicione ao menos um item à solicitação de compra!";
        }

        // Calcular valor total
        var total = 0;
        for (var i = 0; i < indexes.length; i++) {
            var qtde = parseFloat(hAPI.getCardValue("qtde___" + indexes[i])) || 0;
            var valor = parseFloat(hAPI.getCardValue("valorUnit___" + indexes[i])) || 0;
            total += qtde * valor;
        }
        hAPI.setCardValue("valorTotal", total.toFixed(2));
        log.info("Valor total calculado: R$ " + total.toFixed(2));
    }

    // Na aprovação, direcionar conforme parecer
    if (completTask == "true" && atividade == 2) {
        var parecer = hAPI.getCardValue("parecer");
        if (parecer == "aprovado") {
            hAPI.setCardValue("status", "Aprovado");
        } else if (parecer == "reprovado") {
            hAPI.setCardValue("status", "Reprovado");
        } else if (parecer == "devolvido") {
            hAPI.setCardValue("status", "Devolvido para Ajuste");
        }
    }
}
```

### 8. Dataset Avançado (ds_itens_aprovados.js)

Dataset que consolida todos os itens de solicitações aprovadas para relatório:

```javascript
function createDataset(fields, constraints, sortFields) {
    var dataset = DatasetBuilder.newDataset();
    dataset.addColumn("numProcesso");
    dataset.addColumn("solicitante");
    dataset.addColumn("centroCusto");
    dataset.addColumn("material");
    dataset.addColumn("quantidade");
    dataset.addColumn("valorUnitario");
    dataset.addColumn("valorTotal");
    dataset.addColumn("dataSolicitacao");

    // Buscar formulários ativos do processo de compras
    var c1 = DatasetFactory.createConstraint("metadata#active", true, true, ConstraintType.MUST);
    var dsForm = DatasetFactory.getDataset("dsFormCompras", null, new Array(c1), null);

    for (var i = 0; i < dsForm.rowsCount; i++) {
        var status = dsForm.getValue(i, "status");

        // Somente solicitações aprovadas
        if (status == "Aprovado" || status == "Em Processamento") {
            var docId = dsForm.getValue(i, "metadata#id");
            var docVer = dsForm.getValue(i, "metadata#version");
            var solicitante = dsForm.getValue(i, "nomeSolicitante");
            var centroCusto = dsForm.getValue(i, "centroCusto");
            var dataSol = dsForm.getValue(i, "dataSolicitacao");

            // Buscar itens filhos
            var cf1 = DatasetFactory.createConstraint("tablename", "itensCompra", "itensCompra", ConstraintType.MUST);
            var cf2 = DatasetFactory.createConstraint("metadata#id", docId, docId, ConstraintType.MUST);
            var cf3 = DatasetFactory.createConstraint("metadata#version", docVer, docVer, ConstraintType.MUST);
            var dsFilhos = DatasetFactory.getDataset("dsFormCompras", null, new Array(cf1, cf2, cf3), null);

            for (var j = 0; j < dsFilhos.rowsCount; j++) {
                var qtde = dsFilhos.getValue(j, "qtde") || "0";
                var valorUnit = dsFilhos.getValue(j, "valorUnit") || "0";
                var valorItem = (parseFloat(qtde) * parseFloat(valorUnit)).toFixed(2);

                dataset.addRow(new Array(
                    docId,
                    solicitante,
                    centroCusto,
                    dsFilhos.getValue(j, "material"),
                    qtde,
                    valorUnit,
                    valorItem,
                    dataSol
                ));
            }
        }
    }

    return dataset;
}
```

### Resumo dos conceitos demonstrados

| Conceito | Onde foi usado |
|---|---|
| Formulário HTML com Fluig Style Guide | `formCompras.html` |
| Tabela pai-filho (`tablename`) | `formCompras.html` — tabela `itensCompra` |
| Zoom/Select com dataset | `formCompras.html` — seleção de centro de custo |
| `displayFields` + `customHTML` | `displayFields.js` — preenchimento automático + JS injection |
| `validateForm` com `throw` | `validateForm.js` — validação por atividade |
| `enableFields` por atividade | `enableFields.js` — campos readonly por etapa |
| `hAPI.getCardValue/setCardValue` | `beforeStateEntry.js`, `beforeTaskSave.js` |
| `hAPI.setAutomaticDecision` | `beforeStateEntry.js` — aprovação automática |
| `hAPI.calculateDeadLineHours/setDueDate` | `afterTaskCreate.js` — prazo de 48h |
| `hAPI.getChildrenIndexes` | `beforeTaskSave.js` — iterar itens pai-filho |
| `notifier.notify` | `afterTaskCreate.js` — notificação ao solicitante |
| `DatasetBuilder/DatasetFactory` | `ds_itens_aprovados.js` — dataset avançado |
| `getValue("WKUser/WKNumProces/...")` | Todos os eventos — variáveis de contexto |
| `log.info/log.error` | Todos os eventos — logging |
| `java.text.SimpleDateFormat` | `displayFields.js` — formatação de data |
| Constraint `metadata#active/id/version` | `ds_itens_aprovados.js` — consulta formulários |
| Constraint `tablename` | `ds_itens_aprovados.js` — consulta filhos |
