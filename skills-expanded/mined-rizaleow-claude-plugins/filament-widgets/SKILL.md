---
description: Build Filament v5 widgets — StatsOverviewWidget, ChartWidget, TableWidget, custom widgets — including polling, lazy loading, column span, sort order, and PanelProvider registration. Use when creating or modifying Filament v5 dashboard widgets.
---

# Filament v5 Widgets

Widgets are full-Livewire dashboard cards. They live in `app/Filament/Widgets/` (or `app/Filament/<Panel>/Widgets/` for multi-panel apps) and are auto-discovered when the panel has `->discoverWidgets(...)`.

## Preflight

- `mcp__boost__filament_list_widgets` — see what's registered per panel.
- `mcp__boost__filament_scaffold_widget --type stats|chart|table --name RevenueOverview` — generate a diff.

## Stats overview

```php
namespace App\Filament\Widgets;

use Filament\Widgets\StatsOverviewWidget;
use Filament\Widgets\StatsOverviewWidget\Stat;

class RevenueOverview extends StatsOverviewWidget
{
    protected static ?int $sort = 1;
    protected int | string | array $columnSpan = 'full';
    protected static ?string $pollingInterval = '30s';

    protected function getStats(): array
    {
        return [
            Stat::make('Revenue (MTD)', '$12,400')
                ->description('+8% vs last month')
                ->descriptionIcon('heroicon-m-arrow-trending-up')
                ->chart([3, 4, 6, 7, 9, 12])
                ->color('success'),
            Stat::make('Active customers', 142),
            Stat::make('Churn', '1.2%')->color('danger'),
        ];
    }
}
```

## Chart widget

```php
use Filament\Widgets\ChartWidget;

class SignupsChart extends ChartWidget
{
    protected ?string $heading = 'Signups (last 30d)';
    protected static ?int $sort = 2;
    protected int | string | array $columnSpan = 'full';
    protected static ?string $pollingInterval = null; // disable polling

    protected function getData(): array
    {
        return [
            'datasets' => [['label' => 'Signups', 'data' => [4, 8, 6, 12, 9]]],
            'labels'   => ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        ];
    }

    protected function getType(): string
    {
        return 'line';
    }
}
```

## Table widget

```php
use Filament\Widgets\TableWidget;
use Filament\Tables\Table;
use Filament\Tables\Columns\TextColumn;
use App\Models\Order;

class LatestOrders extends TableWidget
{
    protected static ?int $sort = 3;
    protected int | string | array $columnSpan = 'full';

    public function table(Table $table): Table
    {
        return $table
            ->query(Order::query()->latest()->limit(10))
            ->columns([
                TextColumn::make('number')->searchable(),
                TextColumn::make('customer.name'),
                TextColumn::make('total')->money('USD'),
                TextColumn::make('created_at')->since(),
            ]);
    }
}
```

## Lazy loading

Heavy widgets should defer their query:

```php
protected static bool $isLazy = true;     // skeleton until visible
```

`StatsOverviewWidget` is non-lazy by default; flip to `true` when stats hit several aggregations.

## Authorization & filtering

```php
public static function canView(): bool
{
    return auth()->user()?->can('viewRevenue') ?? false;
}
```

Use `InteractsWithPageFilters` on a Page to expose date filters, then read them in widget via `$this->filters['startDate']`.

## Registering on a panel

```php
// AdminPanelProvider::panel()
->discoverWidgets(in: app_path('Filament/Widgets'), for: 'App\\Filament\\Widgets')
->widgets([
    Widgets\AccountWidget::class, // first-party
    RevenueOverview::class,
])
```

Sort order on the dashboard is controlled by `static $sort` on the widget class (lower = earlier).

## Column span

`'full'` spans all 12 grid columns; pass an int for a fixed width; pass an array `['md' => 6, 'xl' => 4]` for responsive.

See also: filament-panels, filament-tables, filament-schemas.
