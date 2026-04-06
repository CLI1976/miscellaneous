# Yealico SiteRule 製作工具

## 功能說明

分析目標漫畫/圖片網站的 HTML 結構，自動產生 Yealico App 可匯入的 SiteRule JSON 檔案。
Yealico 是一個 iOS App，透過使用者自訂的 SiteRule（JSON 格式）來抓取網站內容並在 App 內呈現。
本質上是使用者端爬蟲 + 閱讀器。

## 使用時機

當用戶提供一個漫畫/圖片網站 URL，要求製作 Yealico 的 SiteRule 時使用此技能。

## 輸入

- `$ARGUMENTS`：目標網站的首頁 URL（例如 `https://dogemanga.com/`）
- 如果用戶未提供 URL，請主動詢問

## Windows 環境重要注意事項

### grep 不可使用 `-P` 旗標
Windows Git Bash 的 grep 不支援 `-P`（Perl regex），會報錯。
**一律使用 `grep -oE`（Extended regex）替代。**

### Python 輸出中文需設定 encoding
```python
import sys
sys.stdout.reconfigure(encoding='utf-8')
```

### 優先使用 python 而非 python3
Windows 上 `python3` 可能指向 WindowsApps stub，使用 `python` 更可靠。

---

## 執行流程

### 第一步：抓取並分析三個層級的頁面

用 curl 或 Python 抓取以下三個頁面的 HTML（帶 User-Agent header 避免 403）：

```bash
curl -s -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" "URL"
```

如果 curl 被 403 擋，嘗試 Python urllib：
```python
import urllib.request
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 ...'})
html = urllib.request.urlopen(req).read().decode('utf-8')
```

#### 1. 列表頁（首頁/熱門/最新）
- 找出漫畫卡片的重複容器元素（item）
- 從每個卡片中找出：標題（title）、封面圖（cover）、作者（author）、連結（含 idCode）、更新時間（datetime）
- 確認分頁機制：URL 參數分頁（`?page=2`）或 JS 無限滾動
- 確認搜尋 URL 格式（通常在 `<form>` 標籤中）

#### 2. 詳情頁（單部漫畫）
- 從列表頁找一個漫畫連結，記下 URL 格式（如 `/manga/{id}`）
- 找出：標題、封面大圖、作者、分類/狀態、簡介描述
- 找出章節列表的結構：每個章節的容器、標題、連結、章節 idCode
- 找出標籤（tag）列表（如有）

#### 3. 閱讀頁（漫畫圖片頁）
- 從詳情頁找一個章節連結，記下 URL 格式（如 `/chapter/{id}`）
- 找出所有漫畫圖片的容器和圖片 URL
- 注意：圖片可能用 `data-src`、`data-original`、`data-page-image-url` 等懶載入屬性而非 `src`

### 第二步：分析並確認 CSS Selector

對每個需要的欄位，確認：
1. **CSS Selector**：能精確選中目標元素
2. **Function**：`text`（純文字）、`attr`（屬性值）、`html`（HTML 內容）
3. **Param**：如果 function 是 `attr`，需要哪個屬性（`href`、`src`、`data-src` 等）
4. **Regex**：如果需要從字串中提取部分內容（如從 URL 提取 id）
5. **Replacement**：搭配 regex，用 `$1`、`$2` 等組合結果

### 第三步：產生 JSON 並存檔

輸出到用戶工作目錄下的 `{sitename}_siterule.json`。

---

## Yealico SiteRule 完整語法參考

### Selector 物件的 5 個參數

| 參數 | 說明 | 範例 |
|------|------|------|
| `selector` | CSS3 選擇器（也支援 JSONPath，前綴 `$root`） | `"div.card"`, `"a.title"` |
| `function` | 取值方式：`text`、`html`、`attr`、空值（含自身 HTML） | `"text"`, `"attr"` |
| `param` | 當 function 為 `attr` 時，指定屬性名。多個用逗號分隔 | `"href"`, `"src,data-src"` |
| `regex` | 正則表達式，含至少一個 Group `()` | `"/manga/(.*)"` |
| `replacement` | 搭配 regex，用 `$1` `$2` 佔位符組合結果。預設 `$1` | `"$1"`, `"$1/$2"` |

#### 特殊 selector 值
- `"this"`：代表當前已選取的元素（在子規則中使用）

#### 進階 function（v6.7.0+）
可用 dot notation 串接：`"attr.decodeBase64"`, `"text.replace(old,new)"`
- `decodeBase64`、`removingPercentEncoding`、`addingPercentEncoding()`
- `replace(old,new)`、`decompressFromBase64`、`reversed`、`regexReplacement`

#### replacement 特殊語法
- `"{source:}"`：保留原始字串（當 regex 無匹配時使用）
- `"$1/180.jpg|{source:}"`：有匹配用前者，無匹配用原值

### URL 佔位符

| 佔位符 | 說明 | 範例 |
|--------|------|------|
| `{page:起始:增量}` | 分頁（增量 1 可省略） | `{page:1:1}`, `{page:1}`, `{page:0}` |
| `{pageFormat:{page:...}}` | 第一頁不帶頁碼的分頁 | `{pageFormat:{page:2}}` |
| `{idCode:}` | 漫畫唯一識別碼 | 由 indexRule 的 idCode 提取 |
| `{cidCode:}` | 章節唯一識別碼 | 由 chapterRule 的 idCode 提取 |
| `{keyword:}` | 搜尋關鍵詞 | 用戶輸入的搜尋字串 |
| `{urlPath:n}` | URL 路徑片段（0=host） | `{urlPath:1}` |
| `{urlQuery:key}` | URL query 參數 | `{urlQuery:id}` |
| `{json:formatString}` | POST 請求的 JSON body（v6.11+） | |

### Flags 設定

用逗號分隔多個 flag。

| Flag | 說明 |
|------|------|
| `jsNeededIndex` | 列表頁需要 JS 渲染 |
| `jsNeededDetail` | 詳情頁需要 JS 渲染 |
| `jsNeededGallery` | 閱讀頁需要 JS 渲染 |
| `jsNeededSearch` | 搜尋頁需要 JS 渲染 |
| `jsNeededAll` | 所有頁面都需要 JS 渲染 |
| `scrollIndex` | 列表頁自動捲動載入更多（v6.14.1+） |
| `scrollDetail` | 詳情頁自動捲動 |
| `scrollGallery` | 閱讀頁自動捲動 |
| `loginRequired` | 需要登入 |
| `consentRequired` | 需要用戶同意（v6.13） |
| `repeatedThumbnail` | 重複縮圖 |
| `ignoreDetail` | 忽略詳情頁 |
| `postSearch` | 搜尋用 POST |
| `postIndex` / `postDetail` / `postAll` | 對應頁面用 POST |
| `userAgentMobile` | 模擬手機瀏覽 |
| `big5CharsetIndex` / `gbkCharsetIndex` | 字元編碼 |

### JSON 整體結構模板

```json
{
  "isEditable": true,
  "name": "網站名稱",
  "version": "1.0",
  "displayMode": "collection",
  "indexUrl": "列表頁 URL（含 {page:} 佔位符，如有分頁）",
  "detailUrl": "詳情頁 URL（含 {idCode:} 佔位符）",
  "galleryUrl": "閱讀頁 URL（含 {cidCode:} 佔位符，可能也有 {idCode:}）",
  "searchUrl": "搜尋頁 URL（含 {keyword:} 佔位符）",
  "flags": "",

  "indexRule": {
    "name": "",
    "index": -1,
    "item": { "selector": "每個漫畫卡片的容器" },
    "title": { "selector": "...", "function": "text" },
    "cover": { "selector": "...", "param": "src", "function": "attr" },
    "author": { "selector": "...", "function": "text" },
    "idCode": { "selector": "...", "param": "href", "function": "attr", "regex": "從 URL 提取 id 的正則" },
    "datetime": { "selector": "...", "function": "text" }
  },

  "detailRule": {
    "name": "",
    "index": -1,
    "title": { "selector": "...", "function": "text" },
    "cover": { "selector": "...", "param": "src", "function": "attr" },
    "author": { "selector": "...", "function": "text" },
    "category": { "selector": "...", "function": "text" },
    "desc": { "selector": "...", "function": "text" },
    "tagRule": {
      "item": { "selector": "每個標籤的容器" },
      "name": { "selector": "this", "function": "text" },
      "url": { "selector": "this", "param": "href", "function": "attr" }
    },
    "chapterRule": {
      "item": { "selector": "每個章節的容器" },
      "title": { "selector": "...", "function": "text" },
      "url": { "selector": "...", "param": "href", "function": "attr" },
      "idCode": { "selector": "...", "param": "href", "function": "attr", "regex": "從章節 URL 提取 cidCode 的正則" }
    }
  },

  "galleryRule": {
    "name": "",
    "index": -1,
    "item": { "selector": "漫畫圖片的容器或 img 元素" },
    "image": { "selector": "this", "param": "src,data-src", "function": "attr" }
  },

  "pages": [
    {
      "name": "頁面名稱",
      "displayMode": "collection",
      "listUrl": "此頁面的 URL",
      "index": 0
    }
  ]
}
```

### displayMode 選項
- `"text"`：文字列表
- `"table"`：表格
- `"collection"`：卡片集合（最常用於漫畫）
- `"waterfall"`：瀑布流
- `"tag"`：標籤雲

### 子規則中的 Selector 作用域
`indexRule`、`detailRule` 等規則中的子 selector（如 `title`、`cover`），**作用域是相對於 `item` 所選中的元素**。
例如 `item` 選中 `div.card`，則 `title` 的 `selector: "h3"` 會在 `div.card` 內部搜尋 `h3`。

### 多個 listRule 的用法
如果不同頁面需要不同的列表解析規則，可用 `listRules` 陣列搭配 pages 中的 `relListRuleIndex` 指定。

### HTTP Header 與 Cookie
- `httpHeaders`：自訂 HTTP headers（JSON 格式）
- `browserCookie`：瀏覽器 cookie（瀏覽時自動擷取）
- `customCookie`：手動設定 cookie

---

## 實戰經驗與常見陷阱

### 1. 判斷是否需要 JS 渲染
- 用 curl 抓取 HTML，如果目標內容（漫畫卡片、章節列表、圖片 URL）已在 HTML 中 → 不需 JS
- 如果 curl 只得到空的容器或 loading 畫面 → 需設 `jsNeeded*` flag
- 有些網站「部分」內容在 HTML 中（如初始幾筆），更多內容需 JS 載入 → 按需設定

### 2. 圖片懶載入處理
很多網站的 `<img>` 標籤不用 `src` 放真實圖片 URL，而是用自定義屬性：
- `data-src`、`data-original`、`data-lazy-src`、`data-page-image-url` 等
- **解法**：`param` 設為 `"data-src,src"` 可兩者兼顧（優先取前者）

### 3. idCode 提取
idCode 通常從 `<a>` 標籤的 `href` 中用 regex 提取：
- URL 如 `/manga/abc123` → regex: `"/manga/(.*)"`
- URL 如 `/m/abc123/chapter/1` → regex: `"/m/([^/]+)"` 
- 注意 regex 要準確，避免匹配到多餘的路徑片段

### 4. 無限滾動 vs 傳統分頁
- 傳統分頁：URL 有 `?page=2` 或 `/page/2` → 用 `{page:1}` 佔位符
- 無限滾動：沒有頁碼參數 → 設 `jsNeededIndex` + `scrollIndex` flag
- 有些網站兩者都支持 → 優先用 URL 分頁（更可靠）

### 5. 搜尋頁結構
- 如果搜尋結果頁的 HTML 結構和列表頁一樣 → 不需額外設 searchRule
- 如果不同 → 需在 JSON 中加 `searchRule`

### 6. 章節排序
- 有些網站章節是倒序排列（最新在前） → Yealico 會按原始順序顯示
- 確認章節的 item selector 選到所有章節，不只是前幾個

### 7. 空卡片與廣告元素
- 有些網站的列表中混雜廣告 `<div>`，和漫畫卡片用相同容器 class
- 這些空卡片可能沒有標題/封面 → Yealico 通常會自動忽略
- 如果造成問題，嘗試更精確的 item selector

### 8. 多來源圖片
閱讀頁可能有多種圖片元素：
- 第一張用 `<img src="...">` 直接顯示
- 其餘用隱藏的 `<img data-src="...">` 延遲載入
- 選 selector 時要選到**所有**圖片的元素，而非只有可見的那個

### 9. 編碼問題
- 繁體中文網站可能用 Big5 → 設 `big5CharsetIndex` flag
- 簡體中文網站可能用 GBK → 設 `gbkCharsetIndex` flag
- 大多數現代網站用 UTF-8，不需特別設定

### 10. 相對 URL vs 絕對 URL
- Yealico 的 attr 取得的 href/src 如果是相對路徑（如 `/images/cover.jpg`），通常能自動補全
- 但如果是 `//cdn.example.com/img.jpg`（protocol-relative），可能需要在 replacement 中補上 `https:`

---

## 完整範例：漫畫狗 (dogemanga.com)

以下是實際製作完成的 SiteRule，可作為參考模板：

```json
{
  "isEditable": true,
  "name": "漫畫狗",
  "version": "1.0",
  "displayMode": "collection",
  "indexUrl": "https://dogemanga.com/",
  "detailUrl": "https://dogemanga.com/m/{idCode:}",
  "galleryUrl": "https://dogemanga.com/p/{cidCode:}",
  "searchUrl": "https://dogemanga.com/?q={keyword:}",
  "flags": "",
  "indexRule": {
    "name": "",
    "index": -1,
    "item": { "selector": ".site-card" },
    "title": { "selector": "a.site-card__manga-title", "function": "text" },
    "cover": { "selector": "img.card-img-top", "param": "src", "function": "attr" },
    "author": { "selector": "h6.card-subtitle a", "function": "text" },
    "idCode": { "selector": "a.site-card__manga-title", "param": "href", "function": "attr", "regex": "/m/(.*)" },
    "datetime": { "selector": "small.text-muted", "function": "text", "regex": "最近更新：(.*)", "replacement": "$1" }
  },
  "detailRule": {
    "name": "",
    "index": -1,
    "title": { "selector": "span.site-card__manga-title", "function": "text" },
    "cover": { "selector": "img.site-manga__cover-image", "param": "src", "function": "attr" },
    "author": { "selector": "h4.text-muted a", "function": "text" },
    "desc": { "selector": "p.site-card__brief", "function": "text" },
    "category": { "selector": "small.text-muted", "function": "text", "regex": "連載狀態：([^\\n]+)", "replacement": "$1" },
    "chapterRule": {
      "item": { "selector": ".site-manga-thumbnail" },
      "title": { "selector": "span.text-center", "function": "text" },
      "url": { "selector": "a.site-manga-thumbnail__link", "param": "href", "function": "attr" },
      "idCode": { "selector": "a.site-manga-thumbnail__link", "param": "href", "function": "attr", "regex": "/p/(.*)" }
    }
  },
  "galleryRule": {
    "name": "",
    "index": -1,
    "item": { "selector": "img.site-reader__image" },
    "image": { "selector": "this", "param": "data-page-image-url", "function": "attr" }
  },
  "pages": [
    { "name": "熱門排行", "displayMode": "collection", "listUrl": "https://dogemanga.com/", "index": 0 },
    { "name": "最新連載", "displayMode": "collection", "listUrl": "https://dogemanga.com/?s=1", "index": 1 }
  ]
}
```

### 這個範例的關鍵決策：
- **無 JS flags**：三個頁面的核心內容都在伺服器端 HTML 中
- **圖片用 `data-page-image-url`**：閱讀頁的圖片 URL 存在自定義屬性中
- **無分頁**：首頁用無限滾動，沒有 URL 分頁參數
- **搜尋結構同列表頁**：不需額外 searchRule
- **兩個 pages**：熱門排行 + 最新連載

---

## 輸出要求

1. 分析完成後，清楚列出三個頁面的 URL 格式和 selector 對應表
2. 產生完整的 JSON 檔案，存到用戶工作目錄
3. 列出注意事項（JS 需求、分頁方式、特殊處理等）
4. 提醒用戶可在 Yealico App 中匯入測試
