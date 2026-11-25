---
name: moodle-external-api-development
description: Crie APIs de web service externas personalizadas para Moodle LMS. Use ao implementar web services para gerenciamento de cursos, rastreamento de usuários, operações de quiz ou funcionalidade de plugin personalizado. Abrange validação de parâmetros, operações de banco de dados, tratamento de erros, registro de serviços e padrões de código do Moodle.
---

# Desenvolvimento de API Externa do Moodle

Esta habilidade o guia através da criação de APIs de web service externas personalizadas para Moodle LMS, seguindo o framework de API externa do Moodle e padrões de código.

## Quando Usar Esta Habilidade

- Criar web services personalizados para plugins Moodle
- Implementar endpoints REST/AJAX para gerenciamento de cursos
- Construir APIs para operações de quiz, rastreamento de usuários ou relatórios
- Expor funcionalidade do Moodle para aplicações externas
- Desenvolver backends de aplicativos móveis usando Moodle

## Padrão de Arquitetura Central

APIs externas do Moodle seguem um padrão rigoroso de três métodos:

1. **`execute_parameters()`** - Define a estrutura de parâmetros de entrada
2. **`execute()`** - Contém a lógica de negócios
3. **`execute_returns()`** - Define a estrutura de retorno

## Implementação Passo a Passo

### Passo 1: Criar o Arquivo da Classe API Externa

**Localização**: `/local/yourplugin/classes/external/your_api_name.php`

```php
<?php
namespace local_yourplugin\external;

defined('MOODLE_INTERNAL') || die();
require_once("$CFG->libdir/externallib.php");

use external_api;
use external_function_parameters;
use external_single_structure;
use external_value;

class your_api_name extends external_api {
    
    // Three required methods will go here
    
}
```

**Pontos-chave**:
- A classe deve estender `external_api`
- O namespace segue: `local_pluginname\external` ou `mod_modname\external`
- Inclua a verificação de segurança: `defined('MOODLE_INTERNAL') || die();`
- Exija externallib.php para as classes base

### Passo 2: Definir Parâmetros de Entrada

```php
public static function execute_parameters() {
    return new external_function_parameters([
        'userid' => new external_value(PARAM_INT, 'User ID', VALUE_REQUIRED),
        'courseid' => new external_value(PARAM_INT, 'Course ID', VALUE_REQUIRED),
        'options' => new external_single_structure([
            'includedetails' => new external_value(PARAM_BOOL, 'Include details', VALUE_DEFAULT, false),
            'limit' => new external_value(PARAM_INT, 'Result limit', VALUE_DEFAULT, 10)
        ], 'Options', VALUE_OPTIONAL)
    ]);
}
```

**Tipos de Parâmetros Comuns**:
- `PARAM_INT` - Inteiros
- `PARAM_TEXT` - Texto simples (HTML removido)
- `PARAM_RAW` - Texto bruto (sem limpeza)
- `PARAM_BOOL` - Valores booleanos
- `PARAM_FLOAT` - Números de ponto flutuante
- `PARAM_ALPHANUMEXT` - Alfanumérico com caracteres estendidos

**Estruturas**:
- `external_value` - Valor único
- `external_single_structure` - Objeto com campos nomeados
- `external_multiple_structure` - Array de itens

**Sinalizadores de Valor**:
- `VALUE_REQUIRED` - Parâmetro deve ser fornecido
- `VALUE_OPTIONAL` - Parâmetro é opcional
- `VALUE_DEFAULT, defaultvalue` - Opcional com padrão

### Passo 3: Implementar Lógica de Negócios

```php
public static function execute($userid, $courseid, $options = []) {
    global $DB, $USER;

    // 1. Validate parameters
    $params = self::validate_parameters(self::execute_parameters(), [
        'userid' => $userid,
        'courseid' => $courseid,
        'options' => $options
    ]);

    // 2. Check permissions/capabilities
    $context = \context_course::instance($params['courseid']);
    self::validate_context($context);
    require_capability('moodle/course:view', $context);

    // 3. Verify user access
    if ($params['userid'] != $USER->id) {
        require_capability('moodle/course:viewhiddenactivities', $context);
    }

    // 4. Database operations
    $sql = "SELECT id, name, timecreated
            FROM {your_table}
            WHERE userid = :userid
              AND courseid = :courseid
            LIMIT :limit";
    
    $records = $DB->get_records_sql($sql, [
        'userid' => $params['userid'],
        'courseid' => $params['courseid'],
        'limit' => $params['options']['limit']
    ]);

    // 5. Process and return data
    $results = [];
    foreach ($records as $record) {
        $results[] = [
            'id' => $record->id,
            'name' => $record->name,
            'timestamp' => $record->timecreated
        ];
    }

    return [
        'items' => $results,
        'count' => count($results)
    ];
}
```

**Etapas Críticas**:
1. **Sempre valide parâmetros** usando `validate_parameters()`
2. **Verifique o contexto** usando `validate_context()`
3. **Verifique capacidades** usando `require_capability()`
4. **Use consultas parametrizadas** para prevenir injeção SQL
5. **Retorne dados estruturados** correspondendo à definição de retorno

### Passo 4: Definir Estrutura de Retorno

```php
public static function execute_returns() {
    return new external_single_structure([
        'items' => new external_multiple_structure(
            new external_single_structure([
                'id' => new external_value(PARAM_INT, 'Item ID'),
                'name' => new external_value(PARAM_TEXT, 'Item name'),
                'timestamp' => new external_value(PARAM_INT, 'Creation time')
            ])
        ),
        'count' => new external_value(PARAM_INT, 'Total items')
    ]);
}
```

**Regras de Estrutura de Retorno**:
- Deve corresponder exatamente ao que `execute()` retorna
- Use tipos de parâmetros apropriados
- Documente cada campo com descrição
- Estruturas aninhadas são permitidas

### Passo 5: Registrar o Serviço

**Localização**: `/local/yourplugin/db/services.php`

```php
<?php
defined('MOODLE_INTERNAL') || die();

$functions = [
    'local_yourplugin_your_api_name' => [
        'classname'   => 'local_yourplugin\external\your_api_name',
        'methodname'  => 'execute',
        'classpath'   => 'local/yourplugin/classes/external/your_api_name.php',
        'description' => 'Brief description of what this API does',
        'type'        => 'read',  // or 'write'
        'ajax'        => true,
        'capabilities'=> 'moodle/course:view', // comma-separated if multiple
        'services'    => [MOODLE_OFFICIAL_MOBILE_SERVICE] // Optional
    ],
];

$services = [
    'Your Plugin Web Service' => [
        'functions' => [
            'local_yourplugin_your_api_name'
        ],
        'restrictedusers' => 0,
        'enabled' => 1
    ]
];
```

**Chaves de Registro de Serviço**:
- `classname` - Nome completo da classe com namespace
- `methodname` - Sempre 'execute'
- `type` - 'read' (SELECT) ou 'write' (INSERT/UPDATE/DELETE)
- `ajax` - Defina true para acesso AJAX/REST
- `capabilities` - Capacidades obrigatórias do Moodle
- `services` - Pacotes de serviço opcionais

### Passo 6: Implementar Tratamento de Erros e Logging

```php
private static function log_debug($message) {
    global $CFG;
    $logdir = $CFG->dataroot . '/local_yourplugin';
    if (!file_exists($logdir)) {
        mkdir($logdir, 0777, true);
    }
    $debuglog = $logdir . '/api_debug.log';
    $timestamp = date('Y-m-d H:i:s');
    file_put_contents($debuglog, "[$timestamp] $message\n", FILE_APPEND | LOCK_EX);
}

public static function execute($userid, $courseid) {
    global $DB;

    try {
        self::log_debug("API called: userid=$userid, courseid=$courseid");
        
        // Validate parameters
        $params = self::validate_parameters(self::execute_parameters(), [
            'userid' => $userid,
            'courseid' => $courseid
        ]);

        // Your logic here
        
        self::log_debug("API completed successfully");
        return $result;

    } catch (\invalid_parameter_exception $e) {
        self::log_debug("Parameter validation failed: " . $e->getMessage());
        throw $e;
    } catch (\moodle_exception $e) {
        self::log_debug("Moodle exception: " . $e->getMessage());
        throw $e;
    } catch (\Exception $e) {
        // Log detailed error info
        $lastsql = method_exists($DB, 'get_last_sql') ? $DB->get_last_sql() : '[N/A]';
        self::log_debug("Fatal error: " . $e->getMessage());
        self::log_debug("Last SQL: " . $lastsql);
        self::log_debug("Stack trace: " . $e->getTraceAsString());
        throw $e;
    }
}
```

**Melhores Práticas de Tratamento de Erros**:
- Envolva a lógica em blocos try-catch
- Registre erros com timestamps e contexto
- Capture consultas SQL em erros de banco de dados
- Preserve stack traces para depuração
- Re-lance exceções após logging

## Padrões Avançados

### Operações Complexas de Banco de Dados

```php
// Transaction example
$transaction = $DB->start_delegated_transaction();

try {
    // Insert record
    $recordid = $DB->insert_record('your_table', $dataobject);
    
    // Update related records
    $DB->set_field('another_table', 'status', 1, ['recordid' => $recordid]);
    
    // Commit transaction
    $transaction->allow_commit();
} catch (\Exception $e) {
    $transaction->rollback($e);
    throw $e;
}
```

### Trabalhando com Módulos de Curso

```php
// Create course module
$moduleid = $DB->get_field('modules', 'id', ['name' => 'quiz'], MUST_EXIST);

$cm = new \stdClass();
$cm->course = $courseid;
$cm->module = $moduleid;
$cm->instance = 0; // Will be updated after activity creation
$cm->visible = 1;
$cm->groupmode = 0;
$cmid = add_course_module($cm);

// Create activity instance (e.g., quiz)
$quiz = new \stdClass();
$quiz->course = $courseid;
$quiz->name = 'My Quiz';
$quiz->coursemodule = $cmid;
// ... other quiz fields ...

$quizid = quiz_add_instance($quiz, null);

// Update course module with instance ID
$DB->set_field('course_modules', 'instance', $quizid, ['id' => $cmid]);
course_add_cm_to_section($courseid, $cmid, 0);
```

### Restrições de Acesso (Grupos/Disponibilidade)

```php
// Restrict activity to specific user via group
$groupname = 'activity_' . $activityid . '_user_' . $userid;

// Create or get group
if (!$groupid = $DB->get_field('groups', 'id', ['courseid' => $courseid, 'name' => $groupname])) {
    $groupdata = (object)[
        'courseid' => $courseid,
        'name' => $groupname,
        'timecreated' => time(),
        'timemodified' => time()
    ];
    $groupid = $DB->insert_record('groups', $groupdata);
}

// Add user to group
if (!$DB->record_exists('groups_members', ['groupid' => $groupid, 'userid' => $userid])) {
    $DB->insert_record('groups_members', (object)[
        'groupid' => $groupid,
        'userid' => $userid,
        'timeadded' => time()
    ]);
}

// Set availability condition
$restriction = [
    'op' => '&',
    'show' => false,
    'c' => [
        [
            'type' => 'group',
            'id' => $groupid
        ]
    ],
    'showc' => [false]
];

$DB->set_field('course_modules', 'availability', json_encode($restriction), ['id' => $cmid]);
```

### Seleção Aleatória de Questões com Tags

```php
private static function get_random_questions($categoryid, $tagname, $limit) {
    global $DB;
    
    $sql = "SELECT q.id
            FROM {question} q
            INNER JOIN {question_versions} qv ON qv.questionid = q.id
            INNER JOIN {question_bank_entries} qbe ON qbe.id = qv.questionbankentryid
            INNER JOIN {question_categories} qc ON qc.id = qbe.questioncategoryid
            JOIN {tag_instance} ti ON ti.itemid = q.id
            JOIN {tag} t ON t.id = ti.tagid
            WHERE LOWER(t.name) = :tagname
              AND qc.id = :categoryid
              AND ti.itemtype = 'question'
              AND q.qtype = 'multichoice'";
    
    $qids = $DB->get_fieldset_sql($sql, [
        'categoryid' => $categoryid,
        'tagname' => strtolower($tagname)
    ]);
    
    shuffle($qids);
    return array_slice($qids, 0, $limit);
}
```

## Testando Sua API

### 1. Via Cliente de Teste de Web Services do Moodle

1. Habilite web services: **Administração do site > Recursos avançados**
2. Habilite protocolo REST: **Administração do site > Plugins > Web services > Gerenciar protocolos**
3. Crie serviço: **Administração do site > Servidor > Web services > Serviços externos**
4. Teste a função: **Administração do site > Desenvolvimento > Cliente de teste de web service**

### 2. Via curl

```bash
# Get token first
curl -X POST "https://yourmoodle.com/login/token.php" \
  -d "username=admin" \
  -d "password=yourpassword" \
  -d "service=moodle_mobile_app"

# Call your API
curl -X POST "https://yourmoodle.com/webservice/rest/server.php" \
  -d "wstoken=YOUR_TOKEN" \
  -d "wsfunction=local_yourplugin_your_api_name" \
  -d "moodlewsrestformat=json" \
  -d "userid=2" \
  -d "courseid=3"
```

### 3. Via JavaScript (AJAX)

```javascript
require(['core/ajax'], function(ajax) {
    var promises = ajax.call([{
        methodname: 'local_yourplugin_your_api_name',
        args: {
            userid: 2,
            courseid: 3
        }
    }]);

    promises[0].done(function(response) {
        console.log('Success:', response);
    }).fail(function(error) {
        console.error('Error:', error);
    });
});
```

## Armadilhas Comuns e Soluções

### 1. Erro "Função não encontrada"
**Solução**: 
- Limpe os caches: **Administração do site > Desenvolvimento > Limpar todos os caches**
- Verifique se o nome da função em services.php corresponde exatamente
- Verifique se o namespace e nome da classe estão corretos

### 2. "Valor de parâmetro inválido detectado"
**Solução**:
- Certifique-se de que os tipos de parâmetros correspondem entre definição e uso
- Verifique parâmetros obrigatórios vs opcionais
- Valide definições de estrutura aninhada

### 3. Vulnerabilidades de Injeção SQL
**Solução**:
- Sempre use parâmetros de placeholder (`:paramname`)
- Nunca concatene entrada do usuário em strings SQL
- Use métodos de banco de dados do Moodle: `get_record()`, `get_records()`, etc.

### 4. Erros de Permissão Negada
**Solução**:
- Chame `self::validate_context($context)` no início do execute()
- Verifique se capacidades obrigatórias correspondem às permissões do usuário
- Verifique se o usuário tem atribuições de papel no contexto

### 5. Deadlocks de Transação
**Solução**:
- Mantenha transações curtas
- Sempre commit ou rollback em blocos finally
- Evite transações aninhadas

## Lista de Verificação de Depuração

- [ ] Verifique o modo de debug do Moodle: **Administração do site > Desenvolvimento > Depuração**
- [ ] Revise logs de web services: **Administração do site > Relatórios > Logs**
- [ ] Verifique arquivos de log personalizados em `$CFG->dataroot/local_yourplugin/`
- [ ] Verifique consultas de banco de dados usando `$DB->set_debug(true)`
- [ ] Teste com usuário admin para descartar problemas de permissão
- [ ] Limpe o cache do navegador e caches do Moodle
- [ ] Verifique logs de erro PHP no servidor

## Lista de Verificação de Estrutura de Plugin

```
local/yourplugin/
├── version.php                 # Plugin version and metadata
├── db/
│   ├── services.php           # External service definitions
│   └── access.php             # Capability definitions (optional)
├── classes/
│   └── external/
│       ├── your_api_name.php  # External API implementation
│       └── another_api.php    # Additional APIs
├── lang/
│   └── en/
│       └── local_yourplugin.php  # Language strings
└── tests/
    └── external_test.php      # Unit tests (optional but recommended)
```

## Exemplos de Implementação Real

### API de Leitura Simples (Obter Tentativas de Quiz)

```php
<?php
namespace local_userlog\external;

defined('MOODLE_INTERNAL') || die();
require_once("$CFG->libdir/externallib.php");

use external_api;
use external_function_parameters;
use external_single_structure;
use external_value;

class get_quiz_attempts extends external_api {
    public static function execute_parameters() {
        return new external_function_parameters([
            'userid' => new external_value(PARAM_INT, 'User ID'),
            'courseid' => new external_value(PARAM_INT, 'Course ID')
        ]);
    }

    public static function execute($userid, $courseid) {
        global $DB;

        self::validate_parameters(self::execute_parameters(), [
            'userid' => $userid,
            'courseid' => $courseid
        ]);

        $sql = "SELECT COUNT(*) AS quiz_attempts
                FROM {quiz_attempts} qa
                JOIN {quiz} q ON qa.quiz = q.id
                WHERE qa.userid = :userid AND q.course = :courseid";

        $attempts = $DB->get_field_sql($sql, [
            'userid' => $userid,
            'courseid' => $courseid
        ]);

        return ['quiz_attempts' => (int)$attempts];
    }

    public static function execute_returns() {
        return new external_single_structure([
            'quiz_attempts' => new external_value(PARAM_INT, 'Total number of quiz attempts')
        ]);
    }
}
```

### API de Escrita Complexa (Criar Quiz de Categorias)

Veja o arquivo `create_quiz_from_categories.php` anexado para um exemplo abrangente incluindo:
- Múltiplas inserções de banco de dados
- Criação de módulo de curso
- Configuração de instância de quiz
- Seleção aleatória de questões com tags
- Restrições de acesso baseadas em grupos
- Logging de erros extenso
- Gerenciamento de transações

## Referência Rápida: Tabelas Comuns do Moodle

| Tabela | Propósito |
|--------|-----------|
| `{user}` | Contas de usuário |
| `{course}` | Cursos |
| `{course_modules}` | Instâncias de atividades em cursos |
| `{modules}` | Tipos de atividades disponíveis (quiz, forum, etc.) |
| `{quiz}` | Configurações de quiz |
| `{quiz_attempts}` | Registros de tentativas de quiz |
| `{question}` | Banco de questões |
| `{question_categories}` | Categorias de questões |
| `{grade_items}` | Itens do livro de notas |
| `{grade_grades}` | Notas dos alunos |
| `{groups}` | Grupos de cursos |
| `{groups_members}` | Associações de grupos |
| `{logstore_standard_log}` | Logs de atividades |

## Recursos Adicionais

- [Documentação da API Externa do Moodle](https://moodledev.io/docs/5.2/apis/subsystems/external/functions)
- [Estilo de Código do Moodle](https://moodledev.io/general/development/policies/codingstyle)
- [API de Banco de Dados do Moodle](https://moodledev.io/docs/5.2/apis/core/dml)
- [Documentação da API de Web Services](https://moodledev.io/docs/5.2/apis/subsystems/external)

## Diretrizes

- Sempre valide parâmetros de entrada usando `validate_parameters()`
- Verifique contexto do usuário e capacidades antes de operações
- Use consultas SQL parametrizadas (nunca concatenação de strings)
- Implemente tratamento de erros e logging abrangentes
- Siga convenções de nomenclatura do Moodle (minúsculas, underscores)
- Documente todos os parâmetros e valores de retorno claramente
- Teste com diferentes papéis e permissões de usuário
- Considere segurança de transação para operações de escrita
- Limpe caches após mudanças de registro de serviço
- Mantenha métodos da API focados e com um único propósito