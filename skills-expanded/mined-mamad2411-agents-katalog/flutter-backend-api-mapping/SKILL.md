---
name: flutter-backend-api-mapping
description: Map backend API response types to Flutter Dart model correctly. Use when API returns string IDs or mismatched field names causing runtime errors.
---

# Flutter-Backend API Mapping

## Problem

Backend Python (SQLite) trả String cho ID fields (`"1"`), frontend Dart model dùng `int`. Cast sai → app crash.

## Common mismatch patterns

| Backend | Flutter Model | Fix |
|---------|-------------|-----|
| `"empId": "1"` (String) | `int id` | `int.tryParse(data['empId']) ?? 0` |
| `"empId": 1` (Integer) | `int id` | `data['empId'] as int` |
| `"empName"` field | `name` field | Map field names explicitly |
| `initial` null missing | `initial` required | Fallback `"?"` hoặc `"M"` |

## Safe Session.fromJson

```dart
factory Session.fromJson(Map<String, dynamic> json) {
  // ID: SQLite trả String sometimes
  final rawId = json['empId'] ?? json['id'] ?? 0;
  final id = rawId is int 
    ? rawId 
    : int.tryParse(rawId.toString()) ?? 0;

  // Name: có fallback khi rỗng
  final name = (json['empName'] ?? json['name'] ?? '') as String;

  // Nested employee object
  final emp = json['employee'] as Map<String, dynamic>?;

  return Session(
    id: id,
    name: name.isEmpty ? 'Mới' : name,
    initial: emp?['initial'] as String? ?? json['initial'] as String?,
    colorIdx: emp?['color_idx'] as int? ?? json['color_idx'] as int?,
    role: json['role'] as String? ?? 'employee',
  );
}
```

## Checklist

- [ ] Backend trả `int` hay `String` cho ID?  
- [ ] Field names khớp (`empId` vs `id`, `empName` vs `name`)  
- [ ] Null safety cho mọi field  
- [ ] Fallback khi data missing  
- [ ] Test login → tab Tài khoản hiện tên chính xác