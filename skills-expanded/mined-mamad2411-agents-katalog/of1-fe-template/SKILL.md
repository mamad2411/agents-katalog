---
name: of1-fe-template
description: Template chuẩn để implement WebUI Frontend Layer (Complex Component, Editor, HTTP Call) dùng React và custom framework @of1-webui/lib của dự án OF1.
---

# Template Frontend OF1 (WebUI Components)

Hệ thống Frontend OF1 sử dụng stack React (**Class components là chủ đạo**), thư viện UIKit nội bộ `@of1-webui/lib` (`bs`, `input`, `entity`, `app`, `server`, `util`) và tương tác Data bằng pattern rpc-like (`createHttpBackendCall`) mapping qua String Service Name bên Java.

Sử dụng skill này khi cần tạo màn hình / form Nhập liệu mới (Editor, Viewer, List).

## 1. Các Quy Chuẩn Status & Tag Color (Quan Trọng)

Tham chiếu từ `CustomerLead` và `InquiryRequest`, hệ thống OF1 render các thẻ Status (Pill UI) kết hợp biểu tượng (FeatherIcon) và màu Bootstrap-Subtle (nhạt nền, đậm chữ).

**Mẫu Data Structure cấu hình Status:**
```typescript
import * as FeatherIcon from 'react-feather';

export const MyEntityStatus = {
  NEW: { label: 'New', value: 'NEW', color: 'info', icon: FeatherIcon.Star },
  PROCESSING: { label: 'Processing', value: 'PROCESSING', color: 'primary', icon: FeatherIcon.RefreshCw },
  APPROVED: { label: 'Approved', value: 'APPROVED', color: 'success', icon: FeatherIcon.CheckCircle },
  REJECTED: { label: 'Rejected', value: 'REJECTED', color: 'danger', icon: FeatherIcon.XCircle },
  ON_HOLD: { label: 'On Hold', value: 'ON_HOLD', color: 'warning', icon: FeatherIcon.PauseCircle },
  CLOSED: { label: 'Closed', value: 'CLOSED', color: 'secondary', icon: FeatherIcon.Lock },
} as const;
```

**Mẫu Render Grid Status Column (Dùng trong `DbEntityList` / `bs.Popover` / Thẻ HTML Tag tĩnh):**
```tsx
const renderStatusBadge = (recordStatus: string) => {
  let currentStatus = MyEntityStatus[recordStatus] || MyEntityStatus.NEW;
  let StatusIcon = currentStatus.icon;
  let label = currentStatus.label;
  let color = currentStatus.color;

  // Pattern chuẩn của OF1: class d-flex flex-center px-2 py-2 rounded-2 bg-[color]-subtle text-[color]
  return (
    <div className={`flex-hbox flex-center px-2 py-1 rounded-2 bg-${color}-subtle text-${color} w-100`}>
      <StatusIcon size={14} className="me-1" />
      <span className="fw-bold" style={{ fontSize: '0.85rem' }}>{label}</span>
    </div>
  );
}
```

## 2. Mẫu Component Form (Extend `AppDbComplexEntityEditor`)

Tạo ra màn hình thêm/sửa đối tượng với khả năng auto read/write data mapping, auto commit Form.

```tsx
import React from 'react'
import * as FeatherIcon from "react-feather";
import { bs, input, entity, app, util } from '@of1-webui/lib';
import { module } from '@of1-webui/platform';

const T = (str: string) => str;

export interface UIYourEntityProps extends entity.AppComplexEntityEditorProps {
  isNew?: boolean;
}

export class UIYourNewEntityEditor extends entity.AppDbComplexEntityEditor<UIYourEntityProps> {
  state = {
    isSending: false
  };

  constructor(props: UIYourEntityProps) {
    super(props);
  }

  onPreCommit = (observer: entity.ComplexBeanObserver) => {
    let bean = observer.getMutableBean();

    if (!bean.code || !bean.code.trim()) {
      bs.dialogShow('Lỗi Dữ Liệu', 'Mã đối tượng không được để trống!', { size: 'sm', backdrop: 'static' });
      throw new Error("Validation Failed");
    }

    this.setState({ isSending: true });
  }

  onPostCommit = (savedEntity: any) => {
    let { onPostCommit, appContext } = this.props;
    this.nextViewId();
    this.setState({ isSending: false });

    appContext.addOSNotification('success', "Cập nhật thành công!");

    if (onPostCommit) {
      onPostCommit(savedEntity, this);
    } else {
      this.forceUpdate();
    }
  }

  onChangeCheckExists = (_wInput: input.WInput, _bean: any, _field: string, _oldVal: any, newVal: any) => {
    if (!newVal || newVal.trim() === '') return;

    let { appContext } = this.props;

    // 🔴 PATTERN GOI API QUAN TRỌNG NHẤT Ở OF1 🔴
    appContext.createHttpBackendCall('YourEntityService', 'findByCode', { code: newVal })
      .withSuccessData((resArray: any[]) => {
        if (resArray && resArray.length > 0) {
          let message = (
            <div className="ms-1 text-warning py-3 border-bottom">
              Mã code "{newVal}" đã tồn tại trên hệ thống. Tránh trùng lặp.
            </div>
          );
          bs.dialogShow('Cảnh Báo', message, { backdrop: 'static', size: 'sm' });
        }
      })
      .call();
  }

  onUpdateSimilarFields = (bean: any, field: string, _oldVal: any, newVal: any) => {
    bean[field] = newVal;
    if (field === 'name') {
      if (!bean['label'] || bean['label'].length == 0) bean['label'] = newVal;
      if (!bean['localizedLabel'] || bean['localizedLabel'].length == 0) bean['localizedLabel'] = newVal;
    }
    this.forceUpdate();
  }

  render() {
    let { appContext, pageContext, observer, readOnly } = this.props;
    let bean = observer.getMutableBean();
    let writeCap = pageContext.hasUserWriteCapability() && !readOnly;

    return (
      <div className="flex-vbox">
        <bs.Scrollable style={{ height: 600 }}>
          <div className='flex-vbox shadow-sm rounded h-100 bg-white p-1'>

            <bs.Row>
              <bs.Col span={3}>
                <input.BBStringField
                  bean={bean} field='code' label={T("Item Code")}
                  disable={!writeCap || !observer.isNewBean()} required
                  onBgInputChange={this.onChangeCheckExists} />
              </bs.Col>

              <bs.Col span={3}>
                <input.BBStringField
                  bean={bean} field='name' label={T("Name (Brief)")}
                  disable={!writeCap} required
                  onInputChange={this.onUpdateSimilarFields} />
              </bs.Col>

              <bs.Col span={3}>
                <input.BBSelectField
                  bean={bean} field='category' label={T("Category")} disable={!writeCap}
                  options={['CATE_A', 'CATE_B', 'CATE_C']} />
              </bs.Col>

              <bs.Col span={3}>
                <module.settings.BBRefCountry key={util.IDTracker.next()}
                  appContext={appContext} pageContext={pageContext}
                  placement="bottom-start" offset={[0, 5]} minWidth={350}
                  disable={!writeCap} label={T('Country')} placeholder="Enter Country"
                  bean={bean} beanIdField={'countryId'} beanLabelField={'countryLabel'}
                  refCountryBy='id' hideMoreInfo
                  onPostUpdate={(_inputUI: React.Component, bean: any, selectOpt: any, userInput: string) => {
                    bean['countryId'] = selectOpt['id'];
                    bean['countryLabel'] = selectOpt['label'];
                    bean['continent'] = selectOpt['continent'];
                    this.forceUpdate();
                  }} />
              </bs.Col>
            </bs.Row>

            <bs.Row>
              <bs.Col span={12}>
                <input.BBTextField
                  bean={bean} label={T('Description / Note')} field="note" disable={!writeCap}
                  style={{ height: '5em', fontSize: '1rem' }} />
              </bs.Col>
            </bs.Row>

          </div>
        </bs.Scrollable>

        <bs.Toolbar className='border'>
           <entity.ButtonEntityCommit
              btnLabel={this.state.isSending ? 'Saving Data...' : 'Save Record'}
              appContext={appContext} pageContext={pageContext}
              observer={observer} hide={!writeCap} disable={this.state.isSending}
              commit={{
                entityLabel: T('Item Title'), context: 'your_module',
                service: "YourEntityService", commitMethod: "saveEntity"
              }}
              onPreCommit={this.onPreCommit} onPostCommit={this.onPostCommit} />
        </bs.Toolbar>
      </div>
    );
  }
}
```

## 3. Các Convention Lớp Component & UI Khác Cần Ghi Nhớ
1. **Dùng `{T("Text")}`**: Luôn bọc chữ hiển thị cho Label trong hàm `T("text")` đa ngôn ngữ.
2. **Data Binding**: Input field (`BBStringField`) nhận config object `bean={bean}` và key `field='fieldName'`. Gán dữ liệu cực kỳ magic!
3. **Chuyên môn hóa Layout Grid**: Sử dụng `bs.Row` và `bs.Col span={số_chia_hết_cho_12}`.
4. **Icons**: Sử dụng icon set `<FeatherIcon.NameIcon size={12} className="me-1" />` cho UI.
5. **Component Update**: Khi update ngầm `bean[field] = 'New Text'`, cần gọi `this.forceUpdate()` để Component vẽ lại.
6. **Tooltip/Dialog System**: Tận dụng `bs.dialogShow(title, renderChildJSX(), options)` thay vì thiết kế modal rườm rà. Dùng `bs.CssTooltip` để làm hint form.
7. **Lifecycle Mặc Định**: OF1 base UI bằng Class Component nên quản lý flow cực kỳ dễ qua Overriding method `onInit`, `onPreCommit`, `onPostCommit`. Đừng cố gắng nạp React Hooks nếu không cần thiết.
