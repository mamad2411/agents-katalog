---
name: prestashop-admin-grid
description: Skill for creating and extending modern Admin Grids (Symfony-based) in PrestaShop 8 and 9.
---

# PrestaShop Admin Grid Skill

This skill explains how to implement modern back-office lists (Grids) using the PrestaShop Grid component, as well as how to hook into existing grids to add columns or filters.

## 1. Technical Guide

### Creating a New Grid
A Grid consists of three main components:
1. **Definition**: Define columns, filters, and actions.
2. **Query Builder**: Create the SQL query (using Doctrine DBAL).
3. **Data Factory**: Combine definition and query to produce the grid data.

#### Grid Definition Factory (`src/Grid/Definition/Factory/MyGridDefinitionFactory.php`)
```php
final class MyGridDefinitionFactory extends AbstractGridDefinitionFactory
{
    protected function getColumns()
    {
        return (new ColumnCollection())
            ->add((new DataColumn('id_my_entity'))->setName($this->trans('ID', [], 'Admin.Global')))
            ->add((new DataColumn('name'))->setName($this->trans('Name', [], 'Admin.Global')));
    }
}
```

#### Grid Query Builder (`src/Grid/Query/MyGridQueryBuilder.php`)
```php
final class MyGridQueryBuilder extends AbstractDoctrineQueryBuilder
{
    public function getSearchQueryBuilder(SearchCriteriaInterface $searchCriteria)
    {
        $qb = $this->connection->createQueryBuilder();
        $qb->select('m.id_my_entity, m.name')
           ->from($this->dbPrefix . 'my_entity', 'm');
        // ... grid filtering logic
        return $qb;
    }
}
```

### Extending Existing Grids
To add a column to an existing grid (e.g., Products), use the `action*GridDefinitionModifier` hook.

```php
public function hookActionProductGridDefinitionModifier(array $params)
{
    /** @var GridDefinitionInterface $definition */
    $definition = $params['definition'];

    $column = (new DataColumn('my_custom_column'))
        ->setName($this->trans('My Column', [], 'Modules.Mymodule.Admin'));

    $definition->getColumns()->addAfter('name', $column);
}
```

### Adding Row Actions
You can add buttons (edit, delete, or custom) to each row of the grid.

```php
public function hookActionOrderGridDefinitionModifier(array $params): void
{
    /** @var GridDefinitionInterface $definition */
    $definition = $params['definition'];
    
    // Find the actions column
    $actions = null;
    foreach ($definition->getColumns() as $column) {
        if ('actions' === $column->getId()) { $actions = $column; break; }
    }

    if ($actions) {
        $actions->getOptions()['actions']->add(
            (new SubmitRowAction('my_action'))
                ->setName($this->trans('Do Something', [], 'Admin.Actions'))
                ->setIcon('flag')
                ->setOptions([
                    'route' => 'my_custom_route',
                    'route_param_name' => 'id',
                    'route_param_field' => 'id_object',
                    'use_inline_display' => true, // Show icon directly, not in dropdown
                ])
        );
    }
}
```

## 2. Professional Development Guide

### Hooks for Grids
- `action[GridId]GridDefinitionModifier`: Modify columns/filters.
- `action[GridId]GridQueryBuilderModifier`: Modify the SQL query (e.g., join another table).
- `action[GridId]GridDataModifier`: Modify the results before rendering.

### Architecture Best Practices
- **Decoupling**: Keep your query logic separate from definition logic.
- **Dependency Injection**: Register your factories and query builders in `services.yml`.
- **Naming**: Grid IDs should be unique and follow the PrestaShop naming convention (e.g., `product`, `customer`).

## 3. User Guide

### How to use
- Modern grids support sorting, filtering per column, and pagination out of the box.
- Changes to grids through modules are safe and do not require overrides.

## Rules & Best Practices
- **DBAL**: Always use `Doctrine\DBAL\Query\QueryBuilder` for grid queries.
- **Prefix**: Prefix your custom column IDs with your module name to avoid conflicts.
- **Translations**: Use the modern translation system.
