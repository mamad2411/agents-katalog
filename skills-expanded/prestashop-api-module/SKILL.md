---
name: prestashop-api-module
description: Skill para crear y extender APIs en PrestaShop 8 (WebService legacy) y PrestaShop 9 (API Platform + WebService).
---

# PrestaShop API Module Skill

Este skill cubre los DOS sistemas de API disponibles segun la version de PrestaShop.

> **IMPORTANTE**: PS 8 y PS 9 usan sistemas de API completamente diferentes. No confundirlos.

## Matriz de Compatibilidad

| Sistema | PS 8 | PS 9 |
|---------|------|------|
| **WebService Legacy** (XML) | Unico disponible | Disponible (deprecated) |
| **API Platform** (REST/JSON) | NO existe | Nuevo sistema principal |

---

## 1. WebService Legacy (PS 8 + PS 9)

El sistema clasico basado en XML y ObjectModel. Funciona en ambas versiones.

### Hook de Registro
```php
public function install()
{
    return parent::install() && $this->registerHook('addWebserviceResources');
}
```

### Exponer un Recurso
```php
public function hookAddWebserviceResources($params)
{
    return [
        'my_module_articles' => [
            'description' => 'Access to module articles',
            'class' => 'MyArticle', // Debe extender ObjectModel
            'forbidden_method' => [], // Opcional: ['DELETE', 'PUT']
        ],
    ];
}
```

### ObjectModel Requerido
```php
class MyArticle extends ObjectModel
{
    public $title;

    public static $definition = [
        'table' => 'my_article',
        'primary' => 'id_my_article',
        'fields' => [
            'title' => [
                'type' => self::TYPE_STRING,
                'validate' => 'isGenericName',
                'size' => 255,
                'webservice' => true,
            ],
        ],
    ];
}
```

### Uso del WebService
1. Ir a **Parametros Avanzados > Webservice**.
2. Crear o editar una API Key.
3. El recurso `my_module_articles` aparecera en la lista de permisos.
4. Autenticacion via HTTP Basic Auth con la API Key como usuario.

```
GET https://mitienda.com/api/my_module_articles
Authorization: Basic BASE64(API_KEY:)
```

---

## 2. API Platform (SOLO PS 9)

PrestaShop 9 introduce un sistema nuevo basado en **API Platform** y **Symfony 6.4** con autenticacion **OAuth2**.

> **NO confundir** con el WebService legacy. Son sistemas independientes con rutas, autenticacion y formatos diferentes.

### Definir un API Resource
Crear configuracion en `src/Resources/api_platform/`:

```yaml
# src/Resources/api_platform/my_entity.yml
resources:
    MyModule\ApiPlatform\Resource\MyEntity:
        shortName: 'MyEntity'
        description: 'Operations for my custom entity'
        operations:
            ApiPlatform\Metadata\Get:
                provider: MyModule\ApiPlatform\State\MyEntityProvider
            ApiPlatform\Metadata\GetCollection:
                provider: MyModule\ApiPlatform\State\MyEntityCollectionProvider
            ApiPlatform\Metadata\Post:
                processor: MyModule\ApiPlatform\State\MyEntityProcessor
        normalizationContext:
            groups: ['my_entity:read']
        denormalizationContext:
            groups: ['my_entity:write']
```

### State Provider (lectura)
```php
declare(strict_types=1);

namespace MyModule\ApiPlatform\State;

use ApiPlatform\Metadata\Operation;
use ApiPlatform\State\ProviderInterface;

final class MyEntityProvider implements ProviderInterface
{
    public function __construct(
        private readonly \Db $db
    ) {
    }

    public function provide(Operation $operation, array $uriVariables = [], array $context = []): object|array|null
    {
        // Logica para obtener datos
        $id = (int) ($uriVariables['id'] ?? 0);
        // ...
    }
}
```

### State Processor (escritura)
```php
declare(strict_types=1);

namespace MyModule\ApiPlatform\State;

use ApiPlatform\Metadata\Operation;
use ApiPlatform\State\ProcessorInterface;

final class MyEntityProcessor implements ProcessorInterface
{
    public function process(mixed $data, Operation $operation, array $uriVariables = [], array $context = []): mixed
    {
        // Logica para guardar datos
        return $data;
    }
}
```

### Autenticacion OAuth2 (PS 9)
PS 9 usa OAuth2 con scopes. **NO** usa la pagina de WebService ni X-API-Key.

1. Configurar cliente OAuth2 en el admin de PS 9 (**Parametros Avanzados > Authorization Server**).
2. Obtener un token:
```
POST /admin-api/access_token
Content-Type: application/x-www-form-urlencoded

client_id=MY_CLIENT_ID&client_secret=MY_SECRET&grant_type=client_credentials&scope=my_scope
```
3. Usar el token:
```
GET /api/my-entities
Authorization: Bearer <access_token>
```

### Documentacion Interactiva
Disponible en `/api/docs` (Swagger UI) en instalaciones PS 9.

---

## 3. Reglas y Buenas Practicas

- **Strict Types**: Usar `declare(strict_types=1);` en todas las clases API.
- **Validadores**: Usar validadores reales de PrestaShop (`isGenericName`, `isCleanHtml`, etc.). NO existe `isString`.
- **Prefijos**: Usar nombre del modulo como prefijo en recursos para evitar colisiones.
- **Rendimiento**: El WebService XML puede ser lento con datasets grandes. En PS 9, preferir API Platform.
- **Campos multilenguaje**: En WebService, marcar con `'lang' => true` en la definicion del ObjectModel.
