# Gemini 放射科報告修改工具

在 Notepad++ 中按下 F2，自動將報告送入 Gemini 自訂 Gem 進行優化，完成後瀏覽器保持開啟供後續對話。

---

## 檔案說明

| 檔案 | 說明 |
|------|------|
| `gem_web.py` | 主程式：CDP 連接 Gemini Chrome，貼上報告並送出 |
| `Gem_report.ahk` | AHK 熱鍵腳本（F2 觸發） |

---

## 系統需求

- Python 3.x（PortablePython 可用）
- Playwright：`pip install playwright && playwright install chromium`
- AutoHotkey v2
- Google Chrome

---

## 搬到新電腦的設定步驟

### Step 1：建立 Gemini Chrome 捷徑

在桌面建立 Google Chrome 的捷徑，目標設為：

```
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --remote-allow-origins=* --user-data-dir="C:\Users\你的帳號\AppData\Local\ChromeGemini"
```

> **重要**：`--user-data-dir` 必須是非預設路徑，否則 port 9222 不會開啟。
> 建議放在 AppData 而非 Temp，避免被系統清掉。

### Step 2：登入 Google

用這個捷徑開啟 Chrome，登入 Google 帳號，確認 `gemini.google.com` 可以正常使用。

登入後這個 Chrome 就是日常的工作瀏覽器，可以正常使用。

### Step 3：安裝 Python 套件

```powershell
pip install playwright
playwright install chromium
```

### Step 4：設定 gem_web.py

開啟 `gem_web.py`，確認以下兩行設定正確：

```python
GEM_URL = "https://gemini.google.com/gem/ecabec39c76d"  # 你的 Custom Gem URL
CDP_URL = "http://localhost:9222"                        # 通常不需更動
```

### Step 5：啟動 AHK 腳本

執行 `Gem_report.ahk`（需要 AutoHotkey v2）。

---

## 日常使用

1. 用 Gemini Chrome 捷徑開啟瀏覽器（已登入即可）
2. 在 Notepad++ 開啟「報告暫存.txt」，貼入報告原文
3. 按 **F2**

### 流程
```
F2 → Tooltip「⏳ 報告處理中...」
   → 偵測已開啟的 Gemini Chrome
   → 報告貼入 Gem 並送出（分頁在背景也可運作）
   → Tooltip「✓ 報告修改完成」
   → Chrome 保持開啟 → 可直接繼續對話
```

---

## Tooltip 錯誤訊息對照

| 訊息 | 原因 | 處理方式 |
|------|------|----------|
| `⚠ 請先開啟 Gemini Chrome（port 9222）` | Chrome 未開啟，或捷徑缺少 `--remote-debugging-port=9222` | 用正確捷徑開啟 Chrome |
| `⚠ 請在 Chrome 登入 Gemini 後再按 F2` | Chrome 開著但沒有 Gemini 分頁 | 在 Chrome 開啟 gemini.google.com |
| `❌ 執行錯誤，請查看 gem_web.log` | 其他錯誤 | 查看同目錄的 `gem_web.log` |

---

## 技術架構

```
Notepad++ → F2
  → AHK 讀取報告文字，寫入 %TEMP%\gem_in.txt
  → 執行 gem_web.py
     → Playwright 透過 CDP (port 9222) 連接已開啟的 Chrome
     → 偵測已登入的 Gemini 分頁
       - 已有 Gem URL 分頁 → 重用
       - 無 Gem 分頁 → 開新頁
     → 導航至 Custom Gem URL
     → PowerShell Set-Clipboard + Ctrl+V 貼上報告
     → 點擊「傳送訊息」
     → 等待送出按鈕 disabled → enabled（回應完成判斷）
     → 寫入 %TEMP%\gem_done.txt
  → AHK 偵測到 gem_done.txt（每 200ms 輪詢）→ 顯示完成 Tooltip
  → Chrome 分頁保持開啟供後續對話
```

### 為何使用 CDP 而非直接啟動瀏覽器

Playwright 啟動的 Chrome 會加入 `--enable-automation` flag，Google 偵測後數小時內 session 強制失效。
CDP 連接使用者自己開的 Chrome，Google 視為正常瀏覽器，session 長期穩定。

### 為何背景分頁也能運作

Playwright 透過 Chrome DevTools Protocol 直接操作 DOM，不依賴視窗焦點，分頁在背景或最小化都可正常貼上、送出。
