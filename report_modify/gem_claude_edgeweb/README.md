# 放射科報告 AI 修改工具

在 Notepad++ 中按下熱鍵，自動將報告送入 Gemini Gem 或 Claude Project 進行優化，完成後瀏覽器保持開啟供後續對話。

---

## 檔案說明

| 檔案 | 說明 |
|------|------|
| `gem_web.py` | 主程式：CDP 連接 Edge，將報告送入 Gemini Custom Gem |
| `edge_web.py` | 主程式：CDP 連接 Edge，將報告送入 Claude Project |
| `Gem_report.ahk` | AHK 熱鍵腳本（F2 / F3 / F5 觸發） |

---

## 熱鍵

| 鍵 | 動作 |
|----|------|
| F2 | 送出至 Gemini Gem |
| F3 | 送出至 Claude Project |
| F5 | 同時送出至 Gemini & Claude |

---

## 系統需求

- Python 3.x（PortablePython 可用）
- Playwright：`pip install playwright && playwright install chromium`
- AutoHotkey v2
- Microsoft Edge

---

## 搬到新電腦的設定步驟

### Step 1：建立 Edge 捷徑

在桌面建立 Microsoft Edge 的捷徑，目標設為：

```
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"  --remote-debugging-port=9222 --user-data-dir="C:\EdgeDebugProfile" --download-default-directory="C:\Users\%USERNAME%\Downloads" --safebrowsing-disable-download-protection
```

> **注意**：64-bit Edge 路徑為 `C:\Program Files\Microsoft\Edge\Application\msedge.exe`（無 `(x86)`）。
> `C:\EdgeDebugProfile` 會保留登入狀態，不需要每次重新登入。

### Step 2：登入帳號

用上述捷徑開啟 Edge，登入 Google 帳號（Gemini）與 Anthropic 帳號（Claude）。登入一次後 profile 會永久保留 session。

### Step 3：安裝 Python 套件

```powershell
pip install playwright
playwright install chromium
```

### Step 4：設定目標 URL

**`gem_web.py`**：
```python
GEM_URL = "https://gemini.google.com/gem/ecabec39c76d"  # 你的 Custom Gem URL
```

**`edge_web.py`**：
```python
CLAUDE_URL = "https://claude.ai/project/019d4d28-2751-77c6-8a88-1ab1ebaf233e"  # 你的 Project URL
```

### Step 5：啟動 AHK 腳本

執行 `Gem_report.ahk`（需要 AutoHotkey v2）。

---

## 日常使用

1. 用上述 Edge 捷徑開啟瀏覽器（已登入即可）
2. 在 Notepad++ 開啟「報告暫存.txt」，貼入報告原文
3. 按 **F2**（Gemini）、**F3**（Claude）或 **F5**（兩邊同時）

### 流程
```
F2/F3/F5 → Tooltip「⏳ 處理中...」
   → 偵測已開啟的 Edge（port 9222）
   → 報告貼入目標分頁並送出（背景也可運作）
   → Tooltip 顯示完成或錯誤訊息
   → 分頁保持開啟 → 可直接繼續對話
```

---

## Tooltip 錯誤訊息對照

| 訊息 | 原因 | 處理方式 |
|------|------|----------|
| `⚠ 請先開啟 Edge（port 9222）` | Edge 未開啟，或捷徑缺少 `--remote-debugging-port=9222` | 用正確捷徑開啟 Edge |
| `⚠ 請在 Edge 登入 Gemini 後再按 F2` | 無已登入的 Gemini 分頁 | 在 Edge 開啟 gemini.google.com |
| `⚠ 請在 Edge 登入 Claude 後再按 F3` | 無已登入的 Claude 分頁 | 在 Edge 開啟 claude.ai |
| `❌ 執行錯誤，請查看 gem_web.log` | 其他錯誤 | 查看同目錄的 `gem_web.log` |
| `❌ 執行錯誤，請查看 edge_web.log` | 其他錯誤 | 查看同目錄的 `edge_web.log` |

---

## 技術架構

```
Notepad++ → F2 / F3 / F5
  → AHK 讀取報告文字，寫入 %TEMP%\gem_in.txt / claude_in.txt
  → 執行 gem_web.py 和/或 edge_web.py
     → Playwright 透過 CDP (port 9222) 連接已開啟的 Edge
     → 偵測已登入的目標分頁
       - 已有目標 URL 分頁 → 重用
       - 無目標分頁 → 開新頁
     → 導航至目標 URL
     → PowerShell Set-Clipboard + Ctrl+V 貼上報告
     → 點擊送出按鈕
     → 等待回應完成（Gemini：送出按鈕 disabled→enabled；Claude：Stop 按鈕出現→消失）
     → 寫入 %TEMP%\gem_done.txt / claude_done.txt
  → AHK 偵測到 done 檔（每 200ms 輪詢）→ 顯示完成 Tooltip
  → 分頁保持開啟供後續對話
```

### 為何使用 CDP 而非直接啟動瀏覽器

Playwright 啟動的瀏覽器會加入 `--enable-automation` flag，Google 偵測後數小時內 session 強制失效。
CDP 連接使用者自己開的 Edge，Google/Anthropic 視為正常瀏覽器，session 長期穩定。

### 為何背景分頁也能運作

Playwright 透過 Chrome DevTools Protocol 直接操作 DOM，不依賴視窗焦點，分頁在背景或最小化都可正常貼上、送出。

### F5 雙邊同時送出為何不衝突

- CDP 支援多個 client 同時連線同一 Edge
- 兩個腳本貼上的是同一份文字，剪貼簿即使被覆寫內容也相同
- Playwright CDP 的鍵盤事件直接送往各自 page，不經過 OS 視窗焦點
