# Gemini 放射科報告修改工具

在 Notepad++ 中按下 F2，自動將報告送入 Gemini 自訂 Gem 進行優化，完成後瀏覽器保持開啟供後續對話。

---

## 檔案說明

| 檔案 | 說明 |
|------|------|
| `gem_web.py` | 主程式：CDP 連接 Gemini Chrome，貼上報告並送出 |
| `gem_setup.py` | 一次性設定：從已登入的 Chrome 擷取 session |
| `Gem_report.ahk` | AHK 熱鍵腳本（F2 觸發） |
| `gem.py` | 舊版 API 模式（保留備用） |

---

## 系統需求

- Python 3.x（PortablePython 可用）
- Playwright：`pip install playwright && playwright install chromium`
- AutoHotkey v2
- Google Chrome（已安裝於 `C:\Program Files\Google\Chrome\`）

---

## 初次設定（只需做一次）

### Step 1：建立 Gemini 專用 Chrome Profile

開一個新的 PowerShell，執行：

```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --remote-allow-origins=* --user-data-dir="C:\Temp\chrome-debug"
```

在這個 Chrome 裡登入 Google，確認 `gemini.google.com` 可以正常使用後關閉此 Chrome。

### Step 2：執行設定腳本

```powershell
python gem_setup.py
```

依照提示登入後按 Enter，儲存 session 狀態。

---

## 日常使用

1. 在 Notepad++ 開啟「報告暫存.txt」，貼入要修改的報告原文
2. 執行 `Gem_report.ahk`（若尚未執行）
3. 按 **F2**

### 流程
```
F2 → Tooltip「⏳ 報告處理中...」
   → 自動啟動 Gemini Chrome（若未開啟）
   → 報告貼入 Gem 並送出
   → Tooltip「✓ 報告修改完成」
   → Chrome 保持開啟 → 可直接繼續對話
```

---

## Cookie 失效處理

若出現「❌ 執行錯誤」或 Gemini 未登入，重新執行：

```powershell
# 開啟 Gemini Chrome
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --remote-allow-origins=* --user-data-dir="C:\Temp\chrome-debug"

# 確認 Gemini 正常後執行
python gem_setup.py
```

---

## 技術架構

```
Notepad++ → F2
  → AHK 讀取報告文字，寫入 %TEMP%\gem_in.txt
  → 執行 gem_web.py
     → Playwright 透過 CDP (port 9222) 連接 Gemini Chrome
     → 開新分頁，導航至 Custom Gem URL
     → PowerShell Set-Clipboard + Ctrl+V 貼上報告
     → 點擊「傳送訊息」
     → 等待送出按鈕重新啟用（回應完成）
     → 寫入 %TEMP%\gem_done.txt
  → AHK 偵測到 gem_done.txt → 顯示完成 Tooltip
  → Chrome 分頁保持開啟供後續對話
```

### 為何使用 CDP 而非直接啟動瀏覽器

Playwright 啟動的 Chrome 會加入 `--enable-automation` 等 flag，Google 會偵測並強制讓 session 在數小時內失效。改用 CDP 連接使用者自己啟動的 Chrome，Google 視為正常瀏覽器，session 長期穩定。
