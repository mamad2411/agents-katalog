---
name: prestashop-admin-columns
description: Skill para la gestion y adicion de columnas personalizadas en listados de administracion de PrestaShop 8/9 usando Symfony Grid.
---

# PRESTASHOP ADMIN COLUMNS SKILL (PS 8 / PS 9)

Este skill proporciona los patrones para extender los listados de administracion (Grids) de PrestaShop usando el sistema Symfony Grid.

> ⛔ **AVISO CRITICO (corregido 2026-07-22, verificado en produccion PS 8.1.1)**
>
> La afirmacion anterior de este skill —"en PS 8+ TODOS los listados usan Symfony Grid y los hooks legacy NO aplican"— es **FALSA** y ha costado horas de depuracion.
>
> **En PrestaShop 8.1.1 el listado de PRODUCTOS usa el HelperList LEGACY.** Evidencia real: con el modulo registrado en ambos hooks, `actionProductGridDefinitionModifier` **NUNCA se ejecuta** (0 invocaciones registradas) mientras que `actionAdminProductsListingFieldsModifier` **si se ejecuta en cada carga**.
>
> **Regla:** NO asumas cual de los dos sistemas usa el listado. **Registra los DOS e instrumenta ambos con un log en la PRIMERA linea** del hook (ver §6). El que escriba en el log es el que manda en esa instalacion.
>
> | Version | Productos | Pedidos / Clientes |
> | :--- | :--- | :--- |
> | PS 9.x | Symfony Grid ✔ (verificado) | Symfony Grid |
> | PS 8.2+ | Symfony Grid (probable, sin verificar) | Symfony Grid |
> | **PS 8.1.x** | **LEGACY HelperList ✔ (verificado)** | Symfony Grid (sin verificar) |
> | PS 1.7.x | Legacy HelperList | Legacy HelperList |

## 1. HOOKS POR ENTIDAD

| Entidad | Hook Query Builder | Hook Definition |
| :--- | :--- | :--- |
| **Orders** | `actionOrderGridQueryBuilderModifier` | `actionOrderGridDefinitionModifier` |
| **Customers** | `actionCustomerGridQueryBuilderModifier` | `actionCustomerGridDefinitionModifier` |
| **Products** | `actionProductGridQueryBuilderModifier` | `actionProductGridDefinitionModifier` |
| **Carts** | `actionCartGridQueryBuilderModifier` | `actionCartGridDefinitionModifier` |

Patron general: `action{GridId}GridQueryBuilderModifier` y `action{GridId}GridDefinitionModifier`.

---

## 2. IMPLEMENTACION (SYMFONY GRID)

Requiere 2 o 3 hooks coordinados + registro en `install()`.

### 2.0 Registro de Hooks
```php
public function install()
{
    return parent::install()
        && $this->registerHook('actionOrderGridQueryBuilderModifier')
        && $this->registerHook('actionOrderGridDefinitionModifier');
}
```

### 2.1 Modificar la Query (QueryBuilder)

```php
public function hookActionOrderGridQueryBuilderModifier(array $params): void
{
    /** @var \PrestaShop\PrestaShop\Core\Grid\Query\DoctrineSearchCriteria $searchCriteria */
    $searchCriteria = $params['search_criteria'];

    /** @var \Doctrine\DBAL\Query\QueryBuilder $searchQueryBuilder */
    $searchQueryBuilder = $params['search_query_builder'];

    $searchQueryBuilder->addSelect('m.my_value');
    $searchQueryBuilder->leftJoin(
        'o', // Alias principal (o=Orders, c=Customers, p=Products)
        _DB_PREFIX_ . 'my_table',
        'm',
        'm.id_order = o.id_order'
    );

    // Tambien para el count
    $countQueryBuilder = $params['count_query_builder'];
    $countQueryBuilder->leftJoin('o', _DB_PREFIX_ . 'my_table', 'm', 'm.id_order = o.id_order');
}
```

### 2.2 Modificar la Definicion (Columns)
Se añade la columna visual al objeto GridDefinition.

```php
use PrestaShop\PrestaShop\Core\Grid\Column\Type\Common\DataColumn;

public function hookActionOrderGridDefinitionModifier(array $params): void
{
    /** @var \PrestaShop\PrestaShop\Core\Grid\Definition\GridDefinitionInterface $definition */
    $definition = $params['definition'];

    $definition->getColumns()->addAfter(
        'reference', // ID de la columna despues de la cual se inserta
        (new DataColumn('my_value'))
            ->setName($this->trans('Mi Valor', [], 'Modules.Mymodule.Admin'))
            ->setOptions([
                'field' => 'my_value',
            ])
    );
}
```

> ⛔ **FQCN de `DataColumn` — CORREGIDO (verificado en PS 8.1.1 y PS 9)**
>
> Este skill decia que el namespace "correcto" era `...\Grid\Column\Type\Common\DataColumn`. **Es FALSO para PS 8.1 y PS 9.** El real es **sin `Common\`**:
>
> ```
> PrestaShop\PrestaShop\Core\Grid\Column\Type\DataColumn      <-- CORRECTO (8.1.1 y 9 verificados)
> PrestaShop\PrestaShop\Core\Grid\Column\Type\Common\DataColumn   <-- NO existe en 8.1/9
> ```
>
> **NUNCA fijes un solo FQCN.** Prueba candidatos y usa el que exista, y **deja rastro** de cual se uso:
>
> ```php
> $candidatos = array(
>     'PrestaShop\\PrestaShop\\Core\\Grid\\Column\\Type\\DataColumn',
>     'PrestaShop\\PrestaShop\\Core\\Grid\\Column\\Type\\Common\\DataColumn',
>     'PrestaShopBundle\\Core\\Grid\\Column\\Type\\DataColumn',
> );
> $fqcn = '';
> foreach ($candidatos as $c) {
>     if (class_exists($c)) { $fqcn = $c; break; }
> }
> if ($fqcn === '') {
>     // LOGUEARLO. Un class_exists que falla en silencio = columnas que no salen sin motivo aparente.
>     return;
> }
> ```

### 2.3 Filtros y Ordenacion

```php
// Dentro de hookActionOrderGridQueryBuilderModifier
foreach ($searchCriteria->getFilters() as $filterName => $filterValue) {
    if ($filterName === 'my_value') {
        $searchQueryBuilder->andHaving('m.my_value LIKE :my_value');
        $searchQueryBuilder->setParameter('my_value', '%' . pSQL($filterValue) . '%');
    }
}

if ($searchCriteria->getOrderBy() === 'my_value') {
    $searchQueryBuilder->orderBy('m.my_value', $searchCriteria->getOrderWay());
}
```

### 2.4 Columnas con HTML personalizado
Para mostrar HTML, usar `HtmlColumn` o una plantilla Twig:

```php
use PrestaShop\PrestaShop\Core\Grid\Column\Type\Common\HtmlColumn;

$definition->getColumns()->addAfter(
    'reference',
    (new HtmlColumn('my_html_field'))
        ->setName($this->trans('Mi Campo', [], 'Modules.Mymodule.Admin'))
        ->setOptions([
            'field' => 'my_html_field',
        ])
);
```

Para mayor control con plantilla Twig:
```php
use PrestaShop\PrestaShop\Core\Grid\Column\Type\Common\DataColumn;

// Crear columna con template Twig personalizado
(new DataColumn('my_custom_field'))
    ->setOptions([
        'field' => 'my_custom_field',
    ])
```

---

## 3. ENTIDADES ESPECIFICAS (CHEAT SHEET)

### PRODUCTOS (AdminProducts)
```php
// Query Builder
$searchQueryBuilder->leftJoin(
    'p',
    _DB_PREFIX_ . 'product_lang',
    'pl',
    'pl.id_product = p.id_product AND pl.id_lang = ' . (int) \Context::getContext()->language->id
);

// Definition
use PrestaShop\PrestaShop\Core\Grid\Column\Type\Common\DataColumn;

$definition->getColumns()->addAfter(
    'name',
    (new DataColumn('my_field'))
        ->setName($this->trans('Label', [], 'Modules.Mymodule.Admin'))
        ->setOptions(['field' => 'my_field'])
);
```

---

## 4. REGLAS Y BUENAS PRACTICAS

1. **Strict Types**: Siempre usar `declare(strict_types=1);` al principio del archivo.
2. **Namespace Global**: El archivo principal `.php` del modulo **NO** debe tener namespace.
3. **`ClassName::class`**: Usar libremente (valido desde PHP 5.5). Solo evitar `$obj::class` si se necesita compatibilidad con PHP < 8.0 (PS 8.0).
4. **Proteccion SQL**: Usar siempre `pSQL()` para strings y cast `(int)` para IDs.
5. **Multitienda**: Siempre añadir `Shop::addSqlRestriction()` o filtrar por `id_shop`.
6. **Escapado HTML**: En columnas con contenido del usuario, usar `HtmlColumn` con datos previamente escapados o `DataColumn` (escapa automaticamente).
7. **Traducciones**: Usar `$this->trans('text', [], 'Modules.Mymodule.Admin')`, NUNCA `$this->l()`.

---

## 4-BIS. VIA LEGACY (HelperList) — OBLIGATORIA PARA PS 8.1.x Y 1.7.x

Cuando el listado es legacy, el Symfony Grid NO se dispara. Hooks:

| Entidad | Hook campos + query | Hook resultados |
| :--- | :--- | :--- |
| Products | `actionAdminProductsListingFieldsModifier` | `actionAdminProductsListingResultsModifier` |
| Orders | `actionAdminOrdersListingFieldsModifier` | `actionAdminOrdersListingResultsModifier` |
| Customers | `actionAdminCustomersListingFieldsModifier` | `actionAdminCustomersListingResultsModifier` |

Patron: `action{ControllerName}ListingFieldsModifier`, lanzado desde `AdminController::getList()`.

⛔ **ATENCION — PRODUCTOS es la EXCEPCION (verificado PS 8.1.1)**

`AdminProductsController` **NO usa `AdminController::getList()`**: tiene su propia implementacion y lanza el hook con claves **`sql_*` (SQL crudo), SIN `fields`**. Log real de produccion:

```
[LEGACY] PS=8.1.1 | claves=[_ps_version,sql_select,sql_table,sql_where,
                            sql_group_by,sql_order,sql_limit,cookie,cart,altern]
         | n_fields=-1 | columna_anadida=NO
```

Consecuencia: **con `actionAdminProductsListingFieldsModifier` NO se pueden anadir columnas** en el listado de productos; solo modificar la consulta (`sql_select`, `sql_table` para el JOIN). Para las COLUMNAS hay que usar **`actionAdminProductsListingResultsModifier`**, que si recibe `fields_display` (= `$this->fields_list`) y `list` (las filas).

```php
public function hookActionAdminProductsListingResultsModifier($params)
{
    // 'fields_display' = columnas ; 'list' = filas (ambos por referencia)
    $params['fields_display']['my_value'] = array('title' => 'Mi columna', 'search' => false, 'orderby' => false);
    foreach ($params['list'] as $k => $row) {
        $params['list'][$k]['my_value'] = /* valor calculado */;
    }
}
```

> **Consejo**: rellenar los valores en el Results hook (una consulta propia por los `id_product` visibles) en vez de tocar `sql_select`/`sql_table`. Si te equivocas con el alias del SQL **revientas la pagina de productos entera**; rellenando valores, lo peor que pasa es que salgan a 0.

Para el resto de entidades (Orders, Customers…), que si usan `AdminController::getList()`, `$params` llega con estas claves, **y sus valores son REFERENCIAS** al controlador (por eso `$params` se declara por VALOR y aun asi las modificaciones surten efecto):

```php
'select' => &$this->_select,   'join'     => &$this->_join,
'where'  => &$this->_where,    'group_by' => &$this->_group,
'having' => &$this->_having,   'fields'   => &$this->fields_list,
'order_by' => &$this->_orderBy, 'order_way' => &$this->_orderWay,
```

```php
public function hookActionAdminProductsListingFieldsModifier($params)
{
    // Alias de la tabla principal en HelperList clasico = 'a' (NO 'p', que es del Symfony Grid).
    $params['select'] .= ', COALESCE(m.my_value, 0) AS my_value';
    $params['join']   .= ' LEFT JOIN `' . _DB_PREFIX_ . 'my_table` m ON (m.id_product = a.id_product)';
    $params['fields']['my_value'] = array(
        'title'   => $this->l('Mi columna'),
        'align'   => 'text-center',
        'search'  => false,     // true exige indice + havingFilter
        'orderby' => false,
    );
}
```

⚠ **Trampa mortal**: si envuelves cada modificacion en `if (isset($params['x']))` y las claves no llegan, **no hace nada y no te enteras**. Registra SIEMPRE `array_keys($params)` y si tu columna quedo puesta (ver §6).

---

## 6. VERIFICACION OBLIGATORIA — "registrado" NO es "ejecutado"

El fallo mas caro de este skill: dar por bueno que el hook funciona porque `isRegisteredInHook()` devuelve true. **Registrado ≠ invocado.**

**Antes de dar por hecho que un hook de listado funciona, instrumentalo:**

1. **Log en la PRIMERA linea del hook**, antes de cualquier `return`/guard:
   ```php
   MiLog::write('grid.log', date('c') . ' [DEF] hook disparado. PS=' . _PS_VERSION_);
   ```
2. **Log del RESULTADO real**, nunca un "aplicado" incondicional:
   ```php
   MiLog::write('grid.log', ' claves=[' . implode(',', array_keys($params)) . ']'
       . ' | columna_anadida=' . (isset($params['fields']['my_value']) ? 'SI' : 'NO'));
   ```
   Un log que dice "aplicado" cuando no aplico nada es peor que no tener log.
3. **Registra los DOS sistemas** (Grid + legacy) y deja que el log diga cual corre.
4. **Coherencia definicion ↔ query**: si el hook de query no puede hacer el JOIN (tabla ausente, etc.), el de definicion **tampoco debe anadir la columna**; si no, el grid intenta pintar un campo que no viene en el SELECT.
5. **`try/catch` que no traga**: si envuelves el hook en try/catch, el catch DEBE escribir a log. Un catch mudo convierte un fatal en "no salen las columnas y no se sabe por que".

---

## 5. TIPS DE RENDIMIENTO

- **GROUP BY**: Evitar duplicados en listados al usar JOINs 1:N.
- **Indexacion**: Asegurarse de que las columnas usadas en el JOIN de tablas personalizadas tengan indices.
- **Cache**: Si la obtencion del dato es costosa, considerar guardarlo en una tabla de soporte o usar `Configuration` si es global.
