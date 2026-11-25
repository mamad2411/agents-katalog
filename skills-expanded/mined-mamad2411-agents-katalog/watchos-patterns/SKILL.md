---
name: watchos-patterns
description: "When to activate: watchOS app development, WatchConnectivity, complications, Health data, always-on display, SwiftUI on watchOS"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: swift
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# watchOS Patterns

## watchOS App Entry Point

```swift
import SwiftUI
import WatchKit

@main
struct MyWatchApp: App {
    @WKExtensionDelegateAdaptor(ExtensionDelegate.self) var delegate

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

class ExtensionDelegate: NSObject, WKExtensionDelegate {
    func applicationDidBecomeActive() { }
    func applicationWillResignActive() { }
    func handle(_ backgroundTasks: Set<WKRefreshBackgroundTask>) {
        for task in backgroundTasks {
            switch task {
            case let snapshotTask as WKSnapshotRefreshBackgroundTask:
                snapshotTask.setTaskCompleted(restoredDefaultState: true, estimatedSnapshotExpiration: .distantFuture, userInfo: nil)
            default:
                task.setTaskCompletedWithSnapshot(false)
            }
        }
    }
}
```

## WatchConnectivity — Phone ↔ Watch Communication

```swift
import WatchConnectivity

// Shared SessionManager (use on both iOS and watchOS targets)
final class WatchSessionManager: NSObject, ObservableObject, WCSessionDelegate {
    static let shared = WatchSessionManager()
    private let session = WCSession.default

    @Published var receivedMessage: [String: Any] = [:]

    override init() {
        super.init()
        if WCSession.isSupported() {
            session.delegate = self
            session.activate()
        }
    }

    // Send message to counterpart
    func send(_ message: [String: Any]) {
        guard session.isReachable else { return }
        session.sendMessage(message, replyHandler: nil) { error in
            print("Send error: \(error)")
        }
    }

    // Transfer user info (queued, delivered when reachable)
    func transferUserInfo(_ info: [String: Any]) {
        session.transferUserInfo(info)
    }

    func session(_ session: WCSession, didReceiveMessage message: [String: Any]) {
        DispatchQueue.main.async { self.receivedMessage = message }
    }

    func session(_ session: WCSession, activationDidCompleteWith activationState: WCSessionActivationState, error: Error?) { }

    // iOS-only delegate methods
    #if os(iOS)
    func sessionDidBecomeInactive(_ session: WCSession) { }
    func sessionDidDeactivate(_ session: WCSession) { session.activate() }
    #endif
}
```

## Complications (ClockKit)

```swift
import ClockKit

class ComplicationDataSource: NSObject, CLKComplicationDataSource {
    func getCurrentTimelineEntry(
        for complication: CLKComplication,
        withHandler handler: @escaping (CLKComplicationTimelineEntry?) -> Void
    ) {
        switch complication.family {
        case .circularSmall:
            let template = CLKComplicationTemplateCircularSmallSimpleText(textProvider: CLKSimpleTextProvider(text: "42"))
            handler(CLKComplicationTimelineEntry(date: .now, complicationTemplate: template))
        case .modularSmall:
            let template = CLKComplicationTemplateModularSmallSimpleText(textProvider: CLKSimpleTextProvider(text: "42"))
            handler(CLKComplicationTimelineEntry(date: .now, complicationTemplate: template))
        default:
            handler(nil)
        }
    }

    func getComplicationDescriptors(handler: @escaping ([CLKComplicationDescriptor]) -> Void) {
        handler([CLKComplicationDescriptor(identifier: "main", displayName: "My Complication", supportedFamilies: CLKComplicationFamily.allCases)])
    }
}
```

## HealthKit Integration

```swift
import HealthKit

class HealthManager: ObservableObject {
    private let store = HKHealthStore()

    func requestAuthorization() async throws {
        guard HKHealthStore.isHealthDataAvailable() else { return }
        let typesToRead: Set<HKObjectType> = [
            HKObjectType.quantityType(forIdentifier: .heartRate)!,
            HKObjectType.quantityType(forIdentifier: .stepCount)!,
        ]
        try await store.requestAuthorization(toShare: [], read: typesToRead)
    }

    func fetchTodaySteps() async throws -> Double {
        let stepType = HKObjectType.quantityType(forIdentifier: .stepCount)!
        let startOfDay = Calendar.current.startOfDay(for: .now)
        let predicate = HKQuery.predicateForSamples(withStart: startOfDay, end: .now)

        return try await withCheckedThrowingContinuation { continuation in
            let query = HKStatisticsQuery(
                quantityType: stepType,
                quantitySamplePredicate: predicate,
                options: .cumulativeSum
            ) { _, result, error in
                if let error { continuation.resume(throwing: error); return }
                let steps = result?.sumQuantity()?.doubleValue(for: .count()) ?? 0
                continuation.resume(returning: steps)
            }
            store.execute(query)
        }
    }
}
```

## Always-On Display

```swift
struct WorkoutView: View {
    @Environment(\.isLuminanceReduced) var isLuminanceReduced

    var body: some View {
        ZStack {
            if isLuminanceReduced {
                // Always-on: minimal, low-power rendering
                Text(elapsedTime, format: .time(pattern: .minuteSecond))
                    .font(.system(size: 32, weight: .bold, design: .rounded))
                    .foregroundStyle(.white)
            } else {
                // Active: full interface
                ActiveWorkoutView()
            }
        }
    }
}
```

## Common Anti-Patterns

- **Heavy computation on watch** — offload to iPhone via WatchConnectivity
- **Not handling `isReachable == false`** — queue with `transferUserInfo` for reliability
- **Blocking the main thread** — watchOS CPU budget is tight; use async/await
- **Oversized complications** — keep complication data minimal; update sparingly
- **Not requesting HealthKit on each launch** — authorization can be revoked; always re-request
