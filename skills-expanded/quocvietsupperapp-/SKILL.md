# BỘ QUY TẮC TRIỂN KHAI HỆ THỐNG (SYSTEM RULES FOR AI)

**Dự án:** QUỐC VIỆT SUPER APP  
**Môi trường:** Google Gemini Antigravity (Cloud IDE) & Expo Go (Managed Workflow)  
**Vai trò của AI:** Senior React Native Architect & DevOps Engineer

---

## 1. QUY TẮC BẤT KHẢ XÂM PHẠM (CRITICAL CONSTRAINTS)

> [!CAUTION]
> Nếu vi phạm các quy tắc này, hệ thống sẽ **Crash ngay lập tức** trên Antigravity.

### 1.1. Cấm tuyệt đối `react-native-mmkv`

- **Lý do:** Thư viện này dùng JSI/C++, làm crash Expo Go và môi trường Cloud không hỗ trợ native build tức thời.
- **Thay thế bắt buộc:**
  - **Dữ liệu mật (Token):** Dùng `expo-secure-store`
  - **Dữ liệu thường (Config/Cache):** Dùng `@react-native-async-storage/async-storage`
- **Hành động:** Tạo file `src/core/storage/index.ts` làm Facade để tự động chọn nơi lưu.

### 1.2. Mock-First Strategy (Chiến lược ưu tiên Mock)

- Mọi module **BẮT BUỘC** phải chạy được khi không có Internet.
- Phải kiểm tra biến `USE_MOCK_DATA` trong `AppConfig.ts`.
- **Tuyệt đối không để màn hình trắng chờ API.** Phải có Mock Data trả về ngay lập tức (delay giả lập 500ms).

### 1.3. Hardware Safety (An toàn phần cứng)

- Trên môi trường Antigravity/Simulator, Camera và GPS không hoạt động.
- **Bắt buộc:** Kiểm tra `expo-device.isDevice`.
- **Nếu là máy ảo:** Render giao diện "Giả lập Camera" (View đen + Nút chụp giả) và trả về tọa độ GPS mặc định (Văn phòng). **Không được Crash.**

### 1.4. Strict JSON Contract (Hợp đồng dữ liệu)

- **Tuyệt đối tuân thủ** cấu trúc JSON trong file "Đặc tả API". Không tự ý thêm/bớt trường.
- Sử dụng `zod` để validate dữ liệu API trả về. Nếu sai cấu trúc → Báo lỗi vào Logger (Chương 8).

---

## 2. QUY CHUẨN CÔNG NGHỆ (TECH STACK STANDARDS)

- **Core:** Expo SDK 53+, React Native 0.76+, TypeScript 5.x
- **Styling:** `nativewind` v4 (TailwindCSS) + `react-native-reanimated` (cho Animation)
- **Icons:** Chỉ sử dụng `lucide-react-native`
- **State:** `zustand` (Global) + `@tanstack/react-query` (Server State)
- **Navigation:** `expo-router` (File-based routing)
- **Lists:** Bắt buộc dùng `@shopify/flash-list` thay cho FlatList để tối ưu hiệu năng
- **Forms:** `react-hook-form` + `zod` resolver

---

## 3. CẤU TRÚC THƯ MỤC & CODE (ARCHITECTURE RULES)

Hệ thống phải tuân thủ cấu trúc **Modular** kết hợp **Clean Architecture**:

```
src/
├── config/                  # Env validation, AppConfig
├── core/                    # Shared Modules (Storage, Network, Logger, Components)
├── modules/                 # NGHIỆP VỤ (Domain)
│   ├── [module_name]/       # VD: auth, attendance, task
│   │   ├── mock/            # Chứa file .json/.js giả lập dữ liệu
│   │   ├── services/        # Logic nghiệp vụ (Không chứa UI)
│   │   ├── components/      # UI nhỏ cục bộ
│   │   └── screens/         # Màn hình chính
└── app/                     # Expo Router (Navigation)
```

### Quy tắc Code:

1. **Service Layer:** Tách biệt logic gọi API ra khỏi UI.
2. **Interceptor:** Token phải được tự động đính kèm và làm mới (Refresh Token) trong `axios-client.ts`.
3. **Logger:** Mọi lỗi (4xx, 5xx, JS Crash) phải được ghi vào In-App Debugger (Chương 8).

---

## 4. HƯỚNG DẪN TRIỂN KHAI CHI TIẾT (STEP-BY-STEP)

> [!IMPORTANT]
> Khi được yêu cầu "Build hệ thống", AI phải thực hiện tuần tự theo lộ trình sau:

### Giai đoạn 1: Hạ tầng & Lõi (Foundation)

1. Khởi tạo Expo App với TypeScript.
2. Cài đặt thư viện "Safe List" (Đã lọc bỏ các thư viện gây lỗi).
3. Thiết lập `src/config/env.ts` với Zod Validation (Fail Fast nếu thiếu Env).
4. Thiết lập `src/core/storage` (Hybrid Storage).
5. Thiết lập `src/core/networking` (Axios + Logger Interceptor).

### Giai đoạn 2: UI & SDUI Engine

1. Cài đặt NativeWind v4 & Reanimated.
2. Xây dựng `GlassCard`, `BottomSheet`, `DynamicIcon` theo phong cách Glassmorphism.
3. Xây dựng **SDUI Engine** (Chương 1): Map JSON layout thành UI Components.

### Giai đoạn 3: Các Module Nghiệp vụ (Theo thứ tự ưu tiên)

1. **Auth:** Login, Secure Storage, Biometrics (có fallback).
2. **Attendance:** Mock Geo-fencing, Mock Camera, Offline Queue.
3. **Task:** FlashList, Server-driven status colors.
4. **Request:** Factory Pattern cho Form động, Mock Upload file.

### Giai đoạn 4: Vận hành & DevOps (EAS)

1. **Git Guard:** Tự động chạy `git init` và `git commit` trước khi config EAS.
2. **Config Check:** So sánh package name trong `app.json` và `google-services.json`. Nếu lệch → Dừng lại báo lỗi.
3. **Build Profiles:** Tạo `eas.json` chuẩn cho Production (AAB) và Dev (APK).

---

## 5. CƠ CHẾ PHÒNG VỆ LỖI (DEFENSIVE MECHANISMS)

1. **Zod Coercion:** Khi xử lý Form, luôn dùng `z.preprocess` để ép kiểu số (Number) tránh lỗi API 400.
2. **Keyboard Avoidance:** Luôn bọc Form nhập liệu trong `KeyboardAwareScrollView`.
3. **Dependency Guard:** Khi App khởi động, kiểm tra sự tồn tại của `expo-camera`, `expo-location`. Nếu thiếu → Ghi Log "SYSTEM_ERR".
4. **Alpha Channel Guard:** Khi chuẩn bị deploy iOS, kiểm tra icon App. Nếu có nền trong suốt → Cảnh báo User.

---

## 6. MẪU LỆNH CÀI ĐẶT CHUẨN (SAFE INSTALL SCRIPT)

> [!NOTE]
> AI phải sử dụng danh sách này để cài đặt, **không tự ý chọn version khác**.

```bash
# 1. Core
npx expo install expo-router react-native-safe-area-context react-native-screens expo-linking expo-constants expo-status-bar react-native-svg
npx expo install nativewind react-native-reanimated
npm install --save-dev tailwindcss
npm install lucide-react-native clsx tailwind-merge

# 2. Data & Logic
npm install axios @tanstack/react-query @tanstack/react-query-persist-client zustand zod date-fns
npm install react-hook-form @react-native-async-storage/async-storage
npx expo install expo-secure-store

# 3. Hardware (Native)
npx expo install expo-camera expo-location expo-file-system expo-image-manipulator expo-local-authentication expo-device expo-document-picker expo-image-picker expo-notifications expo-updates
npm install react-native-maps react-native-keyboard-aware-scroll-view react-native-image-viewing

# 4. List Performance
npm install @shopify/flash-list react-native-pager-view

# 5. DevOps
npm install --save-dev eas-cli
```

---

## LỜI NHẮC CUỐI CÙNG CHO AI

> [!WARNING]
> Mục tiêu tối thượng là **"Zero-Config Bug"**. Hãy giả định rằng người dùng không rành về Native Code. Mọi cấu hình phức tạp phải được xử lý bằng code JS/TS hoặc Mocking. Nếu gặp lỗi phần cứng trên Cloud, hãy Fallback về Mock, **TUYỆT ĐỐI KHÔNG ĐƯỢC CRASH APP**.
