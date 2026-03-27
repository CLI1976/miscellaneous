# RadioAssistant (gem.py)

放射科報告優化工具。從 Notepad++ 取得報告文字，送至 Gemini API 精煉後以 PyQt6 視窗顯示結果。

輸出採用結構化 JSON 格式，由 Python 自行生成 HTML，確保排版穩定一致。

---

## 環境需求

- Windows 10/11（64-bit）
- Python 3.12（PortablePython 或完整安裝版皆可）
- AutoHotkey v2（若使用快捷鍵觸發）
- UIA Library for AHK v2（若使用 `Gem_report.ahk`）

---

## Python 套件安裝

```bash
pip install google-genai PyQt6 PyQt6-WebEngine
```

| 套件 | 用途 |
|------|------|
| `google-genai` | Gemini API |
| `PyQt6` | GUI 框架 |
| `PyQt6-WebEngine` | Chromium 渲染引擎（顯示結果視窗，約 130MB） |

---

## 檔案說明

| 檔案 | 說明 |
|------|------|
| `gem.py` | 主程式：呼叫 Gemini API、解析 JSON、生成 HTML、顯示視窗 |
| `Gem_report.ahk` | AutoHotkey 腳本：在 Notepad++ 按 F2 觸發報告處理 |
| `api.ini` | API Key 設定檔（勿上傳 git） |

---

## 使用方式

### 直接執行（測試用）

```bash
python gem.py
```

執行內建測試問題，結果顯示於視窗。

### 搭配 AutoHotkey 使用

1. 在 Notepad++ 開啟 `報告暫存.txt`，將報告文字貼入
2. 執行 `Gem_report.ahk`
3. Notepad++ 為 active 視窗時按 **F2**
4. Tooltip 顯示「正在執行...」，視窗開啟後自動消失
5. 視窗內可直接 Select / Copy 文字，連結可點擊開啟瀏覽器

---

## 設定

`gem.py` 頂部可調整：

```python
GEM_MODEL   = "gemini-2.5-flash"                          # 切換模型
FONT_FAMILY = "Microsoft JhengHei, Segoe UI, sans-serif"  # 字型
FONT_SIZE   = 15                                           # 字體大小 (px)
```

可用模型：
- `gemini-2.5-flash`（預設，穩定）
- `gemini-3-flash-preview`（較新，備用）

CSS 樣式集中在 `gem.py` 的 `CSS` 變數，可直接修改。

---

## 架構說明

```
Notepad++ 報告文字
    ↓ AHK F2
gem.py
    ↓ Gemini API（要求輸出 JSON）
json_to_html()  ← Python 自己組 HTML，不依賴 model 的格式習慣
    ↓
QWebEngineView（Chromium 渲染）
```

---

## 注意事項

- API Key 寫在 `api.ini`，搬移時請確認 Key 仍有效，**不要將 `api.ini` 上傳至 git**
- `PyQt6-WebEngine` 約 130MB，安裝時需要網路
- AHK 腳本依賴 UIA Library，需另外安裝：[UIA for AHK v2](https://github.com/Descolada/UIA-v2)
