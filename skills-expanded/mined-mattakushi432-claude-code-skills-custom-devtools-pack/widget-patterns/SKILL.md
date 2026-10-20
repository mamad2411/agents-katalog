---
name: widget-patterns
description: "When to activate: WidgetKit, widget timelines, AppIntents, interactive widgets, widget configuration, SwiftUI widget views"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: swift
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# WidgetKit Patterns

## Widget Structure

```swift
import WidgetKit
import SwiftUI

// 1. Timeline Entry — the data snapshot for a moment in time
struct StockEntry: TimelineEntry {
    let date: Date
    let symbol: String
    let price: Decimal
    let change: Decimal
}

// 2. Provider — creates the timeline of entries
struct StockProvider: TimelineProvider {
    func placeholder(in context: Context) -> StockEntry {
        StockEntry(date: .now, symbol: "AAPL", price: 182.00, change: 0.5)
    }

    func getSnapshot(in context: Context, completion: @escaping (StockEntry) -> Void) {
        Task {
            let entry = await fetchLatest()
            completion(entry)
        }
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<StockEntry>) -> Void) {
        Task {
            let entry = await fetchLatest()
            // Refresh every 30 minutes
            let nextUpdate = Calendar.current.date(byAdding: .minute, value: 30, to: .now)!
            completion(Timeline(entries: [entry], policy: .after(nextUpdate)))
        }
    }

    private func fetchLatest() async -> StockEntry {
        // Fetch from shared app group or network
        StockEntry(date: .now, symbol: "AAPL", price: 182.50, change: 1.2)
    }
}

// 3. View — renders the entry
struct StockWidgetView: View {
    var entry: StockEntry

    var body: some View {
        VStack(alignment: .leading) {
            Text(entry.symbol).font(.headline)
            Text(entry.price, format: .currency(code: "USD")).font(.title2.bold())
            Text(entry.change >= 0 ? "+\(entry.change)%" : "\(entry.change)%")
                .foregroundStyle(entry.change >= 0 ? .green : .red)
        }
        .containerBackground(.background, for: .widget)
    }
}

// 4. Widget definition
struct StockWidget: Widget {
    let kind = "StockWidget"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: StockProvider()) { entry in
            StockWidgetView(entry: entry)
        }
        .configurationDisplayName("Stock Price")
        .description("Track your favorite stocks.")
        .supportedFamilies([.systemSmall, .systemMedium])
    }
}
```

## Configurable Widgets (AppIntents)

```swift
struct StockSelectionIntent: WidgetConfigurationIntent {
    static var title: LocalizedStringResource = "Select Stock"
    static var description = IntentDescription("Choose a stock to track.")

    @Parameter(title: "Stock Symbol", default: "AAPL")
    var symbol: String
}

struct ConfigurableStockProvider: AppIntentTimelineProvider {
    typealias Entry = StockEntry
    typealias Intent = StockSelectionIntent

    func timeline(for configuration: StockSelectionIntent, in context: Context) async -> Timeline<StockEntry> {
        let entry = await fetchStock(symbol: configuration.symbol)
        let next = Calendar.current.date(byAdding: .minute, value: 30, to: .now)!
        return Timeline(entries: [entry], policy: .after(next))
    }
    // placeholder and snapshot implementations...
}
```

## Interactive Widgets (iOS 17+)

```swift
struct TimerWidgetView: View {
    var entry: TimerEntry

    var body: some View {
        VStack {
            Text(entry.endDate, style: .timer).font(.title)
            // Button triggers AppIntent without opening the app
            Button(intent: PauseTimerIntent()) {
                Label("Pause", systemImage: "pause.fill")
            }
            .buttonStyle(.plain)
        }
        .containerBackground(.background, for: .widget)
    }
}

struct PauseTimerIntent: AppIntent {
    static var title: LocalizedStringResource = "Pause Timer"

    func perform() async throws -> some IntentResult {
        TimerManager.shared.pause()
        return .result()
    }
}
```

## Data Sharing (App Group)

```swift
// Store data in shared UserDefaults
let defaults = UserDefaults(suiteName: "group.com.example.myapp")!
defaults.set(price, forKey: "lastPrice")

// Read in widget provider
let price = UserDefaults(suiteName: "group.com.example.myapp")?.double(forKey: "lastPrice") ?? 0

// Reload widget after app updates data
WidgetCenter.shared.reloadAllTimelines()
// or reloadTimelines(ofKind: "StockWidget")
```

## Common Anti-Patterns

- **Network calls in `getSnapshot`** — return a placeholder; snapshot must be fast
- **No `containerBackground`** — required for iOS 17+ widgets
- **Long-running work in timeline provider** — complete within ~30 seconds
- **Not using App Groups for data sharing** — widgets run in a separate process
- **Refreshing too frequently** — WidgetKit rate-limits; respect refresh budgets
