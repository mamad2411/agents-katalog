---
name: tdd-practice
description: TDD の Red→Green→Refactor 手順、テスト設計の原則、Kotlin テストパターン。developer エージェントが使用する。
---

# TDD Practice ガイド

## Red → Green → Refactor サイクル

### Red: 失敗するテストを書く

1. 受け入れ条件またはタスク仕様から、最初のテストケースを1つ選ぶ
2. テストを書く（この時点ではプロダクションコードは存在しない）
3. テストを実行し、失敗することを確認する（コンパイルエラーも Red）

```kotlin
@Test
fun `注文金額が1000円以上のとき送料無料になる`() {
    val order = Order(items = listOf(Item(price = 1000)))
    val result = order.calculateShippingFee()
    assertThat(result).isEqualTo(ShippingFee.FREE)
}
```

### Green: テストを通す最小限のコードを書く

1. テストをパスする最小限のプロダクションコードを書く
2. 「正しい」コードではなく「動く」コードでよい
3. ハードコードでも構わない（次の Red で一般化を強制される）

### Refactor: テストが通ったままリファクタリングする

1. 重複を除去する
2. 命名を改善する
3. 設計を改善する（メソッド抽出、クラス分割等）
4. テストが Red になったらリファクタリングを戻す

## テスト設計の原則

### テストケースの導出

1. **正常系**: ハッピーパス。仕様通りの入力で期待通りの出力
2. **異常系**: 不正な入力、存在しないリソース、権限エラー
3. **境界値**: 最小値、最大値、ちょうど境界の値、境界の前後

### テストの構造（AAA パターン）

```kotlin
@Test
fun `テスト名は日本語で振る舞いを記述する`() {
    // Arrange: 前提条件のセットアップ
    val order = Order(...)

    // Act: テスト対象の操作を実行
    val result = order.calculateTotal()

    // Assert: 結果を検証
    assertThat(result).isEqualTo(expected)
}
```

### テストの品質基準

- **独立性**: テスト間に順序依存がない
- **反復可能**: 何度実行しても同じ結果
- **自己検証**: 人間の目視確認が不要
- **即座に実行**: 1テスト数秒以内

## Kotlin テストパターン

### Result 型のテスト

```kotlin
@Test
fun `注文が見つからない場合 NotFound エラーを返す`() {
    val result = orderService.findOrder(OrderId("nonexistent"))

    assertThat(result.isFailure).isTrue()
    assertThat(result.exceptionOrNull())
        .isInstanceOf(OrderError.NotFound::class.java)
}
```

### パラメタライズドテスト

```kotlin
@ParameterizedTest
@CsvSource(
    "999, 500",   // 1000円未満 → 送料500円
    "1000, 0",    // 1000円ちょうど → 送料無料
    "1001, 0"     // 1000円超 → 送料無料
)
fun `注文金額に応じた送料計算`(orderAmount: Int, expectedFee: Int) {
    val fee = calculateShippingFee(orderAmount)
    assertThat(fee).isEqualTo(expectedFee)
}
```
