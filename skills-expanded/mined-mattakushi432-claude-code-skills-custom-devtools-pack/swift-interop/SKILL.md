---
name: swift-interop
description: "When to activate: Swift/Objective-C interop, @objc, bridging headers, C interop, Swift/C++ interop, NS prefixed types"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: swift
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Swift Interoperability Patterns

## Objective-C Interop

```swift
// Expose Swift class to Objective-C
@objc class SwiftService: NSObject {
    @objc var name: String = ""

    @objc func performAction() { }

    // Exclude from ObjC while keeping Swift visible
    func swiftOnlyMethod() { }
}

// ObjC protocol in Swift
@objc protocol DataDelegate: NSObjectProtocol {
    func didReceive(data: Data)
    @objc optional func didFail(error: Error)  // optional ObjC method
}

// Calling ObjC APIs safely
if let method = delegate?.didFail {
    method(error)
} else {
    // optional not implemented
}
```

## Bridging Header

```objc
// MyApp-Bridging-Header.h
// Import ObjC headers you want to use in Swift
#import "LegacyManager.h"
#import "ThirdPartyLib/ThirdParty.h"
```

```swift
// After bridging header, use ObjC types directly
let manager = LegacyManager()
manager.configure(withKey: "abc")
```

## Swift from Objective-C

```objc
// Import the generated header
#import "MyModule-Swift.h"

SwiftService *service = [[SwiftService alloc] init];
[service performAction];
```

## C Interop

```swift
import Darwin   // macOS/iOS C standard library
import Glibc    // Linux

// Calling C functions
let pid = getpid()
let time = clock()

// C string bridging
let swiftString = "hello"
swiftString.withCString { cString in
    // cString is valid only within this block
    let result = strlen(cString)
    print(result)
}

// C pointers
var buffer = [UInt8](repeating: 0, count: 1024)
buffer.withUnsafeMutableBufferPointer { ptr in
    _ = read(fd, ptr.baseAddress, ptr.count)
}
```

## Swift/C++ Interop (Swift 5.9+)

```cpp
// MathUtils.hpp
#pragma once
namespace math {
    int add(int a, int b);
    struct Point { double x, y; };
}
```

```swift
// Package.swift
.target(
    name: "App",
    swiftSettings: [.interoperabilityMode(.Cxx)]
)

// Swift usage
import CxxMathUtils
let result = math.add(1, 2)
var point = math.Point(x: 1.0, y: 2.0)
```

## NS Type Bridging

```swift
// Most NS types bridge transparently
let nsString: NSString = "hello" as NSString
let swiftString: String = nsString as String

let nsArray: NSArray = [1, 2, 3] as NSArray
let swiftArray: [Any] = nsArray as! [Any]

// Bridging collections
let dict: [String: Int] = ["a": 1]
let nsDict = dict as NSDictionary  // free bridge

// Explicit bridging when needed
let nsData = Data([0x01, 0x02]) as NSData
let mutableData = nsData.mutableCopy() as! NSMutableData
```

## Sending Swift Code to ObjC Runtime

```swift
// @objcMembers exposes all members automatically
@objcMembers
class Config: NSObject {
    var apiKey: String = ""
    var timeout: TimeInterval = 30
    var retryCount: Int = 3
}

// Dynamic dispatch for KVC/KVO
class Observable: NSObject {
    @objc dynamic var value: Int = 0  // enables KVO
}

let obj = Observable()
obj.addObserver(self, forKeyPath: "value", options: .new, context: nil)
```

## Common Anti-Patterns

- **`@objc` on every Swift type** — only expose what ObjC actually needs; it has overhead
- **Using `NSString`/`NSArray` in Swift code** — use native `String`/`Array` unless interop requires it
- **Bridging large Swift value types repeatedly** — cache the bridged result
- **Force-casting bridged types** — use `as?` and handle the `nil` case
- **C pointer arithmetic without bounds checking** — always use `UnsafeBufferPointer` with `.count`
