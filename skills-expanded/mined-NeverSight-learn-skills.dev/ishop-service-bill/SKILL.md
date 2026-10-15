---
name: ishop-service-bill
description: Generate service-type billing components (sales, purchase, transfer bills) following the existing codebase architecture. Create standardized models, presenters, pages, and cells for logistics business documents. Use when creating sales bills, purchase bills, transfer bills, or any service-related billing functionality.
---

# 业务类单据生成Skill

基于现有代码架构，生成标准化的业务类单据组件（销售、进货、调拨等物流类单据）。

## 适用范围

### 业务类单据包括
- **销售类**：
  - 销售订单(`sales_order`) - 预定性质
  - 销售单(`sales_bill`) - 交易凭证
  - 销售退货单(`sales_return_bill`) - 退货凭证
- **进货类**：
  - 采购订单(`purchase_order`) - 预定性质
  - 采购单(`purchase_bill`) - 交易凭证
  - 采购退货单(`purchase_return_bill`) - 退货凭证
- **配货类**：
  - 配货单(`invoice_bill`)
  - 配货出库单(`invoice_out_bill`)
  - 配货入库单(`invoice_in_bill`)
- **调拨类**：
  - 调拨单(`trans_bill`)
  - 调拨出库单(`trans_out_bill`)
  - 调拨入库单(`trans_in_bill`)
- **零售类**：
  - 零售单(`retail_bill`)
  - 零售退货单(`retail_return_bill`)

## 核心概念区分

### Bill vs Order 的区别

| 类型 | 英文 | 中文 | 特点 | 状态流转 |
|------|------|------|------|----------|
| **Bill** | Bill | 单据 | 交易凭证，已发生 | 草稿→已过账→已红冲 |
| **Order** | Order | 订单 | 预定性质，可转单 | 草稿→已审核 |

### 命名规范说明

#### 1. 单据实体类命名
- **交易类单据**：`{Type}Bill`（如 `SalesBill`, `PurchaseBill`）
- **订单类单据**：`{Type}Order`（如 `SalesOrder`, `PurchaseOrder`）

#### 2. 页面类命名规范

**订单类页面命名**：
- 列表页面：`{Type}OrdersPage`（复数形式，如 `SalesOrdersPage`）
- 编辑页面：`{Type}OrderPage`（单数形式，如 `SalesOrderPage`）
- 详情页面：`{Type}OrderDetailPage`（单数+Detail，如 `SalesOrderDetailPage`）

**其他单据类页面命名**：
- 列表页面：`{Type}BillsPage`（复数形式，如 `SalesBillsPage`）
- 编辑页面：`{Type}BillPage`（单数形式，如 `SalesBillPage`）
- 详情页面：`{Type}BillDetailPage`（单数+Detail，如 `SalesBillDetailPage`）

#### 3. 其他组件命名
- 列表Model：`{type}_bills_model.dart` 或 `{type}s_model.dart`（订单类用复数）
- 编辑Model：`{type}_bill_model.dart` 或 `{type}_model.dart`（订单类用单数）
- 列表Presenter：`{type}_bills_presenter.dart` 或 `{type}s_presenter.dart`
- 编辑Presenter：`{type}_bill_presenter.dart` 或 `{type}_presenter.dart`
- 列表Cell：`{type}_bills_cell.dart` 或 `{type}s_cell.dart`

### 示例对照表
| 单据类型 | 单据实体 | 列表Page | 编辑Page | 详情Page | 列表Model | 编辑Model |
|---------|---------|----------|----------|----------|-----------|-----------|
| 销售单 | `SalesBill` | `SalesBillsPage` | `SalesBillPage` | `SalesBillDetailPage` | `SalesBillsModel` | `SalesBillModel` |
| 销售订单 | `SalesOrder` | `SalesOrdersPage` | `SalesOrderPage` | `SalesOrderDetailPage` | `SalesOrdersModel` | `SalesOrderModel` |
| 采购单 | `PurchaseBill` | `PurchaseBillsPage` | `PurchaseBillPage` | `PurchaseBillDetailPage` | `PurchaseBillsModel` | `PurchaseBillModel` |
| 采购订单 | `PurchaseOrder` | `PurchaseOrdersPage` | `PurchaseOrderPage` | `PurchaseOrderDetailPage` | `PurchaseOrdersModel` | `PurchaseOrderModel` |

### 2. Model层架构

#### 列表Model模板
```dart
// packages/ancestry/lib/src/models/bills/lists/{bill_type}_bills_model.dart
import 'package:ancestry/ancestry.dart';

/// {单据名称}列表Model
final class {BillType}BillsModel extends BillsModel<{BillType}> {
  {BillType}BillsModel(super.filterArguments);

  @override
  BillType get billType => BillType.{billType};

  @override
  List<Sortable<EnumStorage>> get sorts => {billType}SortFields;

  @override
  List<BillFilterField> get filters {
    return BillFilterField.append([
      // 销售类使用customer，进货类使用supplier
      BillFilterField.{customer|supplier},
      BillFilterField.businessStore,
      BillFilterField.clerk,
      BillFilterField.storehouse,
    ]);
  }

  @override
  List<MarkableNamedValue> sectionTotalsItemsOf(BillGroup group) {
    final list = List.of(objects);
    return [
      ('日{单据金额名称}', Fn.amount.format(group.sub(list).map((e) => e.amount).sum, symbols: true), false),
    ];
  }

  @override
  List<MarkableNamedValue>? get summaryTotalsItems {
    return [
      (billType.totalName, Fn.amount.format(parseDouble(summaryTotals['total']), symbols: true), true),
    ];
  }

  @override
  List<{BillType}>? fromJson(List<Map<String, dynamic>> src) {
    return src.map({BillType}.fromJson).toList();
  }
}
```

#### 编辑Model模板
```dart
// packages/ancestry/lib/src/models/bills/edits/{bill_type}_bill_model.dart
import 'package:ancestry/ancestry.dart';

/// {单据名称}编辑Model
final class {BillType}BillModel extends Edit{Service|Purchases}BillModel<{BillType}Detail>
    with EditFlexibleBillModelMixin<{BillType}Detail> {
  {BillType}BillModel({
    int? billId,
    BillingMode mode = BillingMode.normal,
  }) : super(
         billId: billId,
         mode: mode,
       );

  @override
  BillType get billType => BillType.{billType};

  @override
  bool get isMergeSameGoods => billConfigs.isMergeSameGoods;

  // 销售类和进货类的区别
  // 销售类继承 EditSalesBillModel，有customer、积分等
  // 进货类继承 EditPurchasesBillModel，有supplier

  @override
  Future<void> onSetup() async {
    await super.onSetup();
    // 初始化逻辑
  }

  @override
  Map<String, dynamic>? get postingParams => <String, dynamic>{
    ...?super.postingParams,
    // 业务特定参数
  };
}
```

### 3. Presenter层架构

#### 列表Presenter模板
```dart
// packages/ancestry/lib/src/presenters/bills/lists/{bill_type}_bills_presenter.dart
import 'package:ancestry/ancestry.dart';

/// {单据名称}列表Presenter
final class {BillType}BillsPresenter extends BillsPresenter<{BillType}BillsPage, {BillType}BillsModel> {
  @override
  late final model = {BillType}BillsModel(filters);

  // 可选：自定义导出逻辑
  @override
  Future<String?> onExportList(String fileName, CancelToken? cancelToken) {
    return model.exportExcel(cancelToken);
  }

  // 可选：自定义分析功能
  Future<void> onAnalysis() async {
    await R.billAnalysis.push(
      context,
      arguments: <String, dynamic>{
        'billType': model.billType.value,
      },
    );
  }
}
```

#### 编辑Presenter模板
```dart
// packages/ancestry/lib/src/presenters/bills/edits/{bill_type}_bill_presenter.dart
import 'package:ancestry/ancestry.dart';

/// {单据名称}编辑Presenter
final class {BillType}BillPresenter extends EditBillPresenter<{BillType}BillPage, {BillType}BillModel>
    with WillPostPresenterMixin, PostedBillPresenterMixin, ScanQrcodeBillPresenterMixin {
  @override
  late final model = {BillType}BillModel(
    billId: billId,
    mode: mode,
  );

  @override
  PostingCompletion toCompletion(PostingResult result) {
    return PostingCompletion.single(
      name: '{金额名称}',
      value: Fn.amount.format(model.{amountField}, symbols: true),
    );
  }

  @override
  void computation() {
    // 计算逻辑
  }
}
```

### 4. Page层架构

#### 列表Page模板
```dart
// packages/ancestry/lib/src/pages/bills/lists/{bill_type}_bills_page.dart
import 'package:ancestry/ancestry.dart';
import 'package:flutter/material.dart';

/// {单据名称}列表页面
class {BillType}BillsPage extends StatefulWidget with HostProvider {
  const {BillType}BillsPage({super.key});

  @override
  _{BillType}BillsPageState createState() => _{BillType}BillsPageState();

  @override
  {BillType}BillsPresenter createPresenter() => {BillType}BillsPresenter();
}

class _{BillType}BillsPageState extends HostState<{BillType}BillsPage, {BillType}BillsPresenter> {
  @override
  Widget build(BuildContext context) {
    return BillsMainstay<{BillType}BillsModel>(
      model: presenter.model,
      title: const Text('{单据名称}'),
      placeholder: (() {
        final joined = [
          '单据编号',
          '{客户|供应商}名称',
          '商品',
          Settings.extendInfo1Name,
          Settings.extendInfo2Name,
          Settings.extendInfo3Name,
        ].join('、');
        return '请输入$joined';
      })(),
      onPrinting: presenter.onPrinting,
      onPosting: presenter.onPosting,
      onDownload: presenter.onDownload,
      onBatching: presenter.onBatching,
      actions: (model) {
        return [
          if (model.mode case EditingMode.normal)
            AppBarAction(
              onPressed: presenter.onAnalysis,
              child: const Text('分析'),
            ),
          BillsEllipsis(
            mode: model.mode,
            onMode: (value) => model.mode = value,
            onReviewProcess: presenter.onReviewProcess,
            configuratorsOptions: model.configuratorsOptions,
            onSaveConfigurators: model.saveConfigurators,
            onResetConfigurators: model.resetConfigurators,
          ),
        ];
      },
      itemBuilder: (context, model, index) {
        return {BillType}BillsCell(
          model: model,
          index: index,
        );
      },
      separatorBuilder: (context, index) {
        return const SizedBox(height: 9);
      },
    );
  }
}
```

#### Cell组件模板
```dart
// packages/ancestry/lib/src/pages/widgets/bills/lists/{bill_type}_bills_cell.dart
import 'package:ancestry/ancestry.dart';
import 'package:flutter/material.dart';

/// {单据名称}列表单元格
class {BillType}BillsCell extends StatelessWidget {
  const {BillType}BillsCell({
    super.key,
    required this.model,
    required this.index,
  });

  final {BillType}BillsModel model;
  final int index;

  @override
  Widget build(BuildContext context) {
    return BillsCell<{BillType}BillsModel, {BillType}>(
      model: model,
      bill: model[index],
      date: model.lastDateOf(index, model.sortValue),
    );
  }
}
```

### 5. 关键差异点

#### 销售类 vs 进货类

| 特性 | 销售类 | 进货类 |
|------|--------|--------|
| 基类 | `EditSalesBillModel` | `EditPurchasesBillModel` |
| 往来单位 | `customer` (客户) | `supplier` (供应商) |
| 金额方向 | 应收 | 应付 |
| 特有功能 | 积分、物流信息 | - |
| Mixin | `EditSalesBillModelMixin` | `EditPurchasesBillModelMixin` |

#### 订单 vs 单据 vs 退货

| 类型 | 特点 | 状态流转 |
|------|------|----------|
| 订单 | 预定性质，可转单 | 草稿→已审核 |
| 单据 | 交易凭证 | 草稿→已过账→已红冲 |
| 退货 | 反向单据 | 草稿→已过账 |

### 6. 代码生成步骤

#### Step 1: 创建Entry类
```dart
// packages/ancestry/lib/src/entries/{bill_type}.dart
import 'package:ancestry/ancestry.dart';

part '{bill_type}.g.dart';

@JsonSerializable()
final class {BillType} implements Bill {
  const {BillType}({
    required this.billId,
    required this.billNumber,
    required this.serviceDate,
    // ... 其他字段
  });

  factory {BillType}.fromJson(Map<String, dynamic> json) => _${BillType}FromJson(json);

  Map<String, dynamic> toJson() => _${BillType}ToJson(this);

  @JsonKey(name: 'billid')
  @override
  final int billId;

  @JsonKey(name: 'billno')
  @override
  final String billNumber;

  @JsonKey(name: 'billdate', fromJson: parseDate)
  @override
  final DateTime? serviceDate;

  // 销售类特有字段
  @JsonKey(name: 'customerid')
  final int? customerId;

  @JsonKey(name: 'customername')
  final String? customerName;

  // 进货类特有字段
  @JsonKey(name: 'supplierid')
  final int? supplierId;

  @JsonKey(name: 'suppliername')
  final String? supplierName;

  // 通用字段
  @JsonKey(name: 'totalamount', fromJson: parseDouble)
  final double? totalAmount;

  @JsonKey(name: 'remarks')
  final String? remarks;
}
```

#### Step 2: 创建Model
```
1. 列表Model: packages/ancestry/lib/src/models/bills/lists/{bill_type}_bills_model.dart
2. 编辑Model: packages/ancestry/lib/src/models/bills/edits/{bill_type}_bill_model.dart
3. 详情Model: packages/ancestry/lib/src/models/bills/details/{bill_type}_bill_detail_model.dart
```

#### Step 3: 创建Presenter
```
1. 列表Presenter: packages/ancestry/lib/src/presenters/bills/lists/{bill_type}_bills_presenter.dart
2. 编辑Presenter: packages/ancestry/lib/src/presenters/bills/edits/{bill_type}_bill_presenter.dart
3. 详情Presenter: packages/ancestry/lib/src/presenters/bills/details/{bill_type}_bill_detail_presenter.dart
```

#### Step 4: 创建Page
```
1. 列表Page: packages/ancestry/lib/src/pages/bills/lists/{bill_type}_bills_page.dart
2. 编辑Page: packages/ancestry/lib/src/pages/bills/edits/{bill_type}_bill_page.dart
3. 详情Page: packages/ancestry/lib/src/pages/bills/details/{bill_type}_bill_detail_page.dart
4. Cell组件: packages/ancestry/lib/src/pages/widgets/bills/lists/{bill_type}_bills_cell.dart
```

#### Step 5: 注册路由
```dart
// 在 R 枚举中添加
enum R with Routable {
  // ... 其他路由
  
  /// {单据名称}列表
  {billType}Bills({BillType}BillsPage()),
  
  /// 新增/编辑{单据名称}
  {billType}Bill({BillType}BillPage()),
  
  /// {单据名称}详情
  {billType}BillDetail({BillType}BillDetailPage()),
}
```

### 7. 标准化检查清单

#### 命名规范
- [ ] 文件名使用snake_case: `sales_bills_page.dart`
- [ ] 类名使用PascalCase: `SalesBillsPage`
- [ ] Model后缀: `SalesBillsModel`
- [ ] Presenter后缀: `SalesBillsPresenter`

#### 代码规范
- [ ] 使用`super.key`构造函数参数
- [ ] 多参数构造函数使用末尾逗号
- [ ] 行宽不超过120字符
- [ ] 枚举使用点简写语法: `.normal`
- [ ] 使用`const`修饰不可变Widget

#### 架构规范
- [ ] Model继承正确的基类
- [ ] Presenter正确混入Mixin
- [ ] Page实现HostProvider
- [ ] 正确使用ChangeNotifierProvider

#### 功能完整性
- [ ] 列表：筛选、排序、导出、打印、批量操作
- [ ] 编辑：新增、修改、复制、选择商品
- [ ] 详情：查看、操作记录、打印、分享

### 8. 常见变体处理

#### 带源单选择的单据
```dart
/// 从订单生成单据
class OrdersSelectorPresenter extends Presenter<OrdersSelectorPage> {
  Future<void> onConfirm() async {
    final selectedOrders = model.selectedElements;
    // 转换为单据
    await navigator.push(
      R.{billType}Bill.push(
        context,
        arguments: {
          'fromOrders': selectedOrders,
          'mode': BillingMode.fromOrder,
        },
      ),
    );
  }
}
```

#### 支持AI开单的单据
```dart
/// 编辑Model混入AI能力
final class SalesBillModel extends EditSalesBillModel<SalesBillDetail>
    with EditFlexibleBillModelMixin<SalesBillDetail> {
  
  @override
  Future<void> onFlexibleResult(Map<String, dynamic> value) async {
    // 处理AI返回的数据
    final headerInfo = value['headerInfo'] as Map<String, dynamic>?;
    if (headerInfo?['billDate'] case final int billDate when billDate > 0) {
      serviceDate = parseDate(billDate ~/ 1000);
    }
    // ... 其他字段处理
  }
}
```

## 使用示例

### 创建新的销售订单功能
```dart
// 1. 定义Entry (如果不存在)
// packages/ancestry/lib/src/entries/sales_order.dart

// 2. 创建Model
// packages/ancestry/lib/src/models/bills/lists/sales_orders_model.dart
final class SalesOrdersModel extends BillsModel<SalesOrder> {
  SalesOrdersModel(super.filterArguments);
  
  @override
  BillType get billType => BillType.salesOrder;
  
  @override
  List<Sortable<EnumStorage>> get sorts => salesOrderSortFields;
}

// 3. 创建Presenter
// packages/ancestry/lib/src/presenters/bills/lists/sales_orders_presenter.dart
final class SalesOrdersPresenter extends BillsPresenter<SalesOrdersPage, SalesOrdersModel> {
  @override
  late final model = SalesOrdersModel(filters);
}

// 4. 创建Page
// packages/ancestry/lib/src/pages/bills/lists/sales_orders_page.dart
class SalesOrdersPage extends StatefulWidget with HostProvider {
  const SalesOrdersPage({super.key});
  
  @override
  SalesOrdersPresenter createPresenter() => SalesOrdersPresenter();
}
```

### 创建采购订单功能
```dart
// 1. 定义Entry
// packages/ancestry/lib/src/entries/purchase_order.dart

// 2. 创建Model
// packages/ancestry/lib/src/models/bills/lists/purchase_orders_model.dart
final class PurchaseOrdersModel extends BillsModel<PurchaseOrder> {
  PurchaseOrdersModel(super.filterArguments);
  
  @override
  BillType get billType => BillType.purchaseOrder;
  
  @override
  List<Sortable<EnumStorage>> get sorts => purchaseOrderSortFields;
}

// 3. 创建Presenter
// packages/ancestry/lib/src/presenters/bills/lists/purchase_orders_presenter.dart
final class PurchaseOrdersPresenter extends BillsPresenter<PurchaseOrdersPage, PurchaseOrdersModel> {
  @override
  late final model = PurchaseOrdersModel(filters);
}

// 4. 创建Page
// packages/ancestry/lib/src/pages/bills/lists/purchase_orders_page.dart
class PurchaseOrdersPage extends StatefulWidget with HostProvider {
  const PurchaseOrdersPage({super.key});
  
  @override
  PurchaseOrdersPresenter createPresenter() => PurchaseOrdersPresenter();
}
```

这个skill提供了完整的业务类单据开发框架，确保新功能与现有代码保持一致的架构和风格。
