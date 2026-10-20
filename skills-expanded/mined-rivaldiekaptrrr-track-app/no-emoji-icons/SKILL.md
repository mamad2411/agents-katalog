---
name: no-emoji-icons
description: "Enforce a strict rule of NO emoji/unicode characters used as icons or visual labels in Kotlin Compose UI code. Always use proper Material Icons from the androidx.compose.material.icons package instead. Apply this skill when reviewing or editing any screen, ViewModel, or component file."
---

# No Emoji Icons — Compose UI Rule

## The Problem

Using emoji characters as UI icons or visual labels is considered AI slop and poor engineering practice:
- Not scalable: Emoji rendering varies across OS versions and device manufacturers.
- Not accessible: Screen readers cannot reliably describe emoji as semantic icons.
- Not themeable: Emoji ignore your app color scheme (light/dark mode, brand colors).
- Not crisp: Emoji are not vector-based and can look blurry at non-standard sizes.
- Looks amateurish: Real production apps use proper icon systems.

## The Rule

NEVER use emoji as icons or visual indicators in Compose UI.
ALWAYS use androidx.compose.material.icons or equivalent vector icon packages.

---

## How to Fix

### Pattern A: Standalone emoji as visual icon
```kotlin
// BAD
Text("emoji", style = MaterialTheme.typography.displayMedium)

// GOOD
Icon(
    imageVector = Icons.Default.AccountBalanceWallet,
    contentDescription = "Anggaran",
    modifier = Modifier.size(48.dp),
    tint = MaterialTheme.colorScheme.primary
)
```

### Pattern B: Emoji prepended to a label string in a map/list
```kotlin
// BAD
"EXPENSE" to "emoji Expense Tracker"

// GOOD
data class ModeOption(val key: String, val label: String, val icon: ImageVector)
listOf(
    ModeOption("EXPENSE", "Expense Tracker", Icons.Default.AccountBalanceWallet),
    ModeOption("WEDDING", "Wedding Planner", Icons.Default.Favorite),
)
```

### Pattern C: Emoji in FilterChip labels
```kotlin
// BAD
FilterChip(label = { Text("emoji Expense Tracker") })

// GOOD
FilterChip(
    leadingIcon = { Icon(Icons.Default.AccountBalanceWallet, contentDescription = null, modifier = Modifier.size(16.dp)) },
    label = { Text("Expense Tracker") }
)
```

### Pattern D: Emoji in status label maps (ViewModel)
```kotlin
// BAD
val STATUS_LABELS = mapOf("SELESAI" to "emoji Selesai", "PENDING" to "emoji Pending")

// GOOD
val STATUS_LABELS = mapOf("SELESAI" to "Selesai", "PENDING" to "Menunggu")
fun statusIcon(status: String): ImageVector = when (status) {
    "SELESAI" -> Icons.Default.CheckCircle
    "PENDING" -> Icons.Default.Schedule
    else -> Icons.Default.Circle
}
```

---

## Common Emoji to Material Icon Mapping

- Money/Expense      -> Icons.Default.AccountBalanceWallet
- Wedding/Heart      -> Icons.Default.Favorite
- Goal/Target        -> Icons.Default.TrackChanges
- Statistics/Chart   -> Icons.Default.BarChart
- Calendar/Date      -> Icons.Default.CalendarToday
- Done/Success/Check -> Icons.Default.CheckCircle
- Error/Cancel       -> Icons.Default.Cancel
- Notification/Bell  -> Icons.Default.Notifications
- Security/Lock      -> Icons.Default.Lock
- Achievement        -> Icons.Default.EmojiEvents
- Search             -> Icons.Default.Search
- List/Notes         -> Icons.Default.Assignment
- Cash/Payments      -> Icons.Default.Payments
- Card               -> Icons.Default.CreditCard
- Deal/Contract      -> Icons.Default.Handshake
- Progress/Up        -> Icons.Default.TrendingUp
- Phone              -> Icons.Default.Phone
- Camera/Photo       -> Icons.Default.PhotoCamera
- Music              -> Icons.Default.MusicNote
- Venue/Building     -> Icons.Default.Business
- Catering/Food      -> Icons.Default.Restaurant
- Gift/Souvenir      -> Icons.Default.CardGiftcard
- MUA/Face           -> Icons.Default.Face
- Dress/Clothes      -> Icons.Default.Checkroom
- Pending/Loading    -> Icons.Default.Schedule
- Notes              -> Icons.Default.Notes

---

## Enforcement Checklist

- [ ] No emoji characters in Text() composables used as icons
- [ ] No emoji prepended to label strings in Map or List
- [ ] No emoji in Toast messages used as status icons
- [ ] All status indicators use Icon() composable with a vector icon
- [ ] All chip/button labels use leadingIcon parameter instead of emoji prefix
