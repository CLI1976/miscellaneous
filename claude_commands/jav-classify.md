# JAV 影片分類工具

## 功能說明

自動掃描目錄下的 JAV 影片，解析檔名並從 javdb.com/jable.tv 获取女演員資料、封面和截圖，最後將影片分類到正確的資料夾結構中。

## 使用時機

當用戶要求對 JAV 影片進行分類時使用此技能。

## 重要規則

1. **只使用繁體中文的資料**：優先從 javdb.com （繁體中文）獲取女演員資料和影片資訊
2. **演員名稱必須從 javdb.com 提取**：javdb.com 詳情頁的 `♀` 符號連結是最可靠的來源（見 3.3 節），**不要使用 jable.tv 的 URL slug 作為演員名**（很多是 MD5 hash）
3. **產生 nfo metadata 檔**：每個影片目錄需產生 `.nfo` 檔案（Kodi/XBMC 相容格式）
4. **檢查截圖大小**：下載截圖後檢查檔案大小，過小（< 5KB）或錯誤的圖檔不要儲存
5. **cover 加上前綴**：cover.jpg 檔名需加上影片番號前綴，如 `SONE-123-cover.jpg`
6. **只下載 cover，不下載 fanart**：優先從 jable.tv 取得 cover，若失敗再從 javdb.com 取得作為 fallback
7. **演員名稱驗證**：提取到的名稱必須通過驗證才能使用（見 3.4 節）

## 輸入

- 用戶指定要掃描的目錄路徑（預設為目前目錄）

## Windows 環境重要注意事項（必讀）

### 1. grep 不可使用 `-P` 旗標
Windows Git Bash 的 grep 不支援 `-P`（Perl regex），會報錯 `grep: -P supports only unibyte and UTF-8 locales`。
**一律使用 `grep -oE`（Extended regex）替代。**

```bash
# ❌ 錯誤
grep -oP '(?<=content=")[^"]+'

# ✅ 正確
grep -oE 'content="[^"]+"' | sed 's/content="//;s/"$//'
```

### 2. curl `-o` 無法處理日文/中文路徑
在 Windows 環境下，curl 的 `-o` 參數無法正確處理含有日文、中文等 CJK 字符的檔案路徑，會報 `Failure writing output to destination`。
**必須先下載到 `/tmp`，再用 `cp` 複製到目標路徑。**

```bash
# ❌ 錯誤：curl 直接寫入含日文的路徑
curl -s "$url" -o "S:/path/ひなたまりん/cover.jpg"

# ✅ 正確：先下載到 /tmp，再 cp 過去
curl -s "$url" -o /tmp/cover.jpg
cp /tmp/cover.jpg "S:/path/ひなたまりん/cover.jpg"
```

### 3. jable.tv CDN 需要 Referer 標頭
從 `assets-cdn.jable.tv` 下載圖片時，必須帶上 Referer 標頭，否則會得到 0 bytes 的空檔案。

```bash
# ❌ 錯誤：沒有 Referer，下載 0 bytes
curl -s "$cover_url" -o /tmp/cover.jpg

# ✅ 正確：加上 -e (Referer)
curl -s -A "$UA" -e "https://jable.tv/" "$cover_url" -o /tmp/cover.jpg
```

### 4. 所有 curl 請求統一使用 User-Agent
所有對外部網站的 curl 請求都必須帶上瀏覽器 User-Agent，避免被網站封鎖。

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
curl -s -A "$UA" "https://..."
```

### 5. 封面圖下載的標準流程（綜合以上所有規則）

**只下載 cover.jpg，不下載 fanart.jpg。** 優先從 jable.tv 取得，失敗時才從 javdb.com 取得作為 fallback。

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
TMP="/tmp/jav_dl"
mkdir -p "$TMP"

cover_ok=false

# 第一優先：jable.tv 封面（需要 Referer）
curl -s -A "$UA" -e "https://jable.tv/" "$jable_cover_url" -o "$TMP/cover.jpg"
fsize=$(stat -c%s "$TMP/cover.jpg" 2>/dev/null || echo "0")
if [ "$fsize" -ge 5120 ]; then
    cp "$TMP/cover.jpg" "$TARGET_DIR/${folder}-cover.jpg"
    cover_ok=true
fi

# Fallback：若 jable.tv 失敗，改從 javdb.com 取得（不需要 Referer）
if [ "$cover_ok" = false ]; then
    curl -s -A "$UA" "$javdb_cover_url" -o "$TMP/cover.jpg"
    fsize=$(stat -c%s "$TMP/cover.jpg" 2>/dev/null || echo "0")
    if [ "$fsize" -ge 5120 ]; then
        cp "$TMP/cover.jpg" "$TARGET_DIR/${folder}-cover.jpg"
        cover_ok=true
    fi
fi
```

## 處理流程

### 1. 掃描影片檔案

使用 glob 工具搜尋以下格式的檔案：
- `*.mp4`
- `*.mkv`
- `*.avi`
- `*.wmv`

### 2. 檔名清理與解析

#### 2.1 移除前綴雜訊

以下列模式移除檔名前的雜訊：
- `thzu@SONE-123` → `SONE-123`
- 方括號前綴（如 `[SONE-123]`）
- 其他非標準前綴（如 `【モザイク破壊】`、`[馬賽克破壞]`）

⚠️ **注意：不可盲目移除數字前綴**。部分番號本身帶有數字前綴（如 `390SNB-001`、`259LUXU-467`），這些數字是番號的一部分，不能移除。

```bash
# 安全的雜訊移除：只移除明確的非番號前綴
filename=$(echo "$filename" | sed 's/^thzu@//; s/^\[馬賽克破壞\]//; s/^【モザイク破壊】//')
# 移除開頭的 [ ] 包裹文字
filename=$(echo "$filename" | sed 's/^\[[^]]*\]\s*//')
```

#### 2.2 提取番號資訊

解析規則：
| 輸入 | 番號 | 類型 |
|------|------|------|
| SONE-123 | SONE-123 | 原始 |
| SONE-123-C | SONE-123 | 中文字幕 |
| SONE-123-U | SONE-123 | 破解版 |
| SONE-123-UC | SONE-123 | 破解+字幕 |

**標準番號格式**：`<英文前綴>-<數字>`
- 前綴：2-5 個英文字母（如 MAAN、SONE、MK、IPZZ）
- 數字：2-4 位數字（如 123、1151）
- 正則：`[A-Z]{2,5}-[0-9]{2,4}`

**特殊番號格式**（需額外支援）：

| 格式 | 範例 | 正則 | 說明 |
|------|------|------|------|
| 數字前綴番號 | `390SNB-001`、`259LUXU-467` | `[0-9]+[A-Z]+-[0-9]+` | 數字是番號的一部分，不可移除 |
| FC2 | `FC2-PPV-3080922` | `FC2-PPV-[0-9]+` | FC2 素人系列，數字可達 7 位 |
| 帶檔名中文描述 | `蚊香社259LUXU全崩盤！...259LUXU-467~` | — | 需從中文描述中提取番號 |

**提取番號的完整正則**：
```bash
# 優先匹配 FC2 格式
code=$(echo "$filename" | grep -oiE 'FC2-PPV-[0-9]+' | head -1 | tr 'a-z' 'A-Z')

# 其次匹配數字前綴番號（如 390SNB-001、259LUXU-467）
if [ -z "$code" ]; then
    code=$(echo "$filename" | grep -oE '[0-9]+[A-Z]{2,5}-[0-9]+' | head -1)
fi

# 最後匹配標準番號
if [ -z "$code" ]; then
    code=$(echo "$filename" | grep -oE '[A-Z]{2,5}-[0-9]{2,4}' | head -1)
fi
```

#### 2.3 從檔名提取演員名稱（備用）

當 javdb.com 無法取得演員資訊時，可嘗試從檔名中提取演員名稱作為 fallback。常見的檔名格式：

```bash
# 括號中的演員名：(及川海)、（宮藤さくら）
actress_from_filename=$(echo "$filename" | grep -oE '[（(][^）)]+[）)]' | head -1 | sed 's/[（()）]//g')

# 驗證提取到的名稱（排除番號、數字等）
if echo "$actress_from_filename" | grep -qE '^[0-9A-Z-]+$'; then
    actress_from_filename=""  # 不是演員名，清空
fi
```

**注意**：從檔名提取的演員名稱可靠性較低，僅在 javdb.com 完全無結果時使用。

#### 2.4 重複偵測

處理每個影片前，應先檢查目標目錄是否已存在相同番號：

```bash
# 檢查是否已有相同番號的目錄
existing=$(find "$BASE" -maxdepth 3 -type d -name "$folder" 2>/dev/null | head -1)
if [ -n "$existing" ]; then
    echo "DUPLICATE: $folder already exists at $existing, skipping"
    continue
fi
```

若已存在：
- **完全相同版本**（如都是 SONE-123-U）：跳過，不覆蓋
- **不同版本**（如已有 -U，新增原版）：建立新目錄（如 `SONE-123/`），移入同一演員目錄下

### 3. JAVDB / JABLE / 91MD 查詢

#### 3.1 選擇數據源

**重要：首先識別影片類型，選擇正確的數據源**

| 番號前綴範例 | 影片類型 | 數據源 |
|-------------|----------|--------|
| MDSR、MGL、MD、TM、JD、MT、91、LS、SWIC | 中國/台灣成人影片 | **91md.me** |
| SONE、HND、MAAN、MK、FC2、ABP | 日本 JAV | **javdb.com / jable.tv** |

**識別邏輯**：
```bash
# 提取番號前綴（前3-4個字母）
prefix=$(echo "$code" | grep -oE '^[A-Za-z]{3,4}')

# 判斷影片類型
if echo "$prefix" | grep -iqE '^(mdsr|mgl|md|tm|jd|mt|91|ls|swic)$'; then
    # 中國成人影片 → 使用 91md.me
    datasource="91md.me"
else
    # 日本 JAV → 使用 javdb.com / jable.tv
    datasource="javdb"
fi
```

#### 3.2 javdb.com 查詢（演員名稱首選來源）

javdb.com 是**提取演員名稱的首選來源**，因為它在 HTML 中用 `♀` 符號明確標示女演員。

**第一步：搜尋影片，取得視頻 ID**
```bash
curl -s -A "$UA" "https://javdb.com/search?q=HND-765" | grep -oE '/v/[A-Za-z0-9]+' | head -1
# 結果範例: /v/YnPpJ6
```

**第二步：提取女演員名稱（正確方法）**

⚠️ **關鍵：必須匹配 `<strong class="symbol female">♀</strong>` 來識別女演員連結**

```bash
# ✅ 正確：匹配帶有 ♀ 符號的演員連結（精確提取女演員）
curl -s -A "$UA" "https://javdb.com/v/<視頻ID>" | \
  grep -oE 'href="/actors/[A-Za-z0-9]+\">[^<]+</a><strong class="symbol female"' | \
  head -1 | sed 's/.*">//;s/<\/a>.*//'
# 結果範例: 川越にこ
```

```bash
# ❌ 錯誤方法1：僅匹配 /actors/ 連結但不過濾
# 會匹配到導航列的分類連結：/actors/censored（有碼）、/actors/uncensored（無碼）、/actors/western（歐美）
grep -oE 'href="/actors/[^"]+' | head -1
# 錯誤結果: /actors/censored → 提取出「有碼」

# ❌ 錯誤方法2：用 grep -vE 過濾分類名（不夠可靠）
grep -oE 'href="/actors/[^"]+"[^>]*>[^<]+<' | grep -vE '有碼|無碼|歐美'
# 可能漏過其他非演員連結
```

**第三步：提取封面圖 URL**
```bash
curl -s -A "$UA" "https://javdb.com/v/<視頻ID>" | \
  grep -oE 'https://c0.jdbstatic.com/covers/[^"]+\.jpg' | head -1
```

**第四步：提取截圖列表**
```bash
# 大圖：XXXXX_l_N.jpg / 小圖：XXXXX_s_N.jpg
curl -s -A "$UA" "https://javdb.com/v/<視頻ID>" | \
  grep -oE 'https://c0.jdbstatic.com/samples/[^"]+\.jpg'
```

**注意**：若 javdb.com 無法獲取截圖，請參考 3.5 節使用 javdatabase.com 作為備用來源。

#### 3.3 jable.tv 查詢（封面圖首選，不用於演員名稱）

jable.tv 主要用於**取得封面圖**（og:image 品質較好），**不應用於提取演員名稱**。

⚠️ **jable.tv 演員名稱不可靠**：jable.tv 的 `/models/` URL slug 有大量是 MD5 hash（如 `d1ebb3d61ee367652e6b1f35b469f2b6`），而非可讀的演員名稱。即使是可讀名稱也是英文羅馬字（如 `airi kijima`），而非日文名。

```bash
# 搜索影片（番號中的 - 改為空格或 %20）
curl -s -A "$UA" "https://jable.tv/search/HND%20765/" | grep -oE '/videos/[^/]+/' | head -1

# 提取封面圖（og:image）
curl -s -A "$UA" "https://jable.tv/videos/HND-765/" | \
  grep -oE 'https://[^"]+jable.tv[^"]+\.jpg' | head -1
```

#### 3.4 演員名稱驗證規則

提取到的演員名稱**必須通過以下驗證**才能使用，否則視為提取失敗：

```bash
validate_actress_name() {
    local name="$1"

    # 驗證1：不可為空
    [ -z "$name" ] && return 1

    # 驗證2：不可為 MD5 hash（32位十六進制字串）
    echo "$name" | grep -qE '^[0-9a-f]{32}$' && return 1

    # 驗證3：不可為 javdb 導航列分類名
    echo "$name" | grep -qE '^(有碼|無碼|歐美)$' && return 1

    # 驗證4：不可為純數字
    echo "$name" | grep -qE '^[0-9]+$' && return 1

    return 0
}
```

**若驗證失敗**，依序嘗試以下 fallback：
1. 重新從 javdb.com 用 `♀` 符號模式提取
2. 將影片移至 `unknown/` 目錄

#### 3.5 演員名稱提取的完整流程

```bash
get_actress_name() {
    local base_code="$1"
    UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

    # 第一優先：javdb.com（♀ 符號精確匹配）
    local search_html=$(curl -s -A "$UA" "https://javdb.com/search?q=$base_code")
    local vid=$(echo "$search_html" | grep -oE '/v/[A-Za-z0-9]+' | head -1)

    if [ -n "$vid" ]; then
        sleep 1
        local detail_html=$(curl -s -A "$UA" "https://javdb.com${vid}")
        local actress=$(echo "$detail_html" | \
            grep -oE 'href="/actors/[A-Za-z0-9]+\">[^<]+</a><strong class="symbol female"' | \
            head -1 | sed 's/.*">//;s/<\/a>.*//')

        # 驗證名稱
        if validate_actress_name "$actress"; then
            echo "$actress"
            return 0
        fi
    fi

    # 全部失敗
    echo ""
    return 1
}
```

#### 3.6 91md.me（中國成人影片）

當影片為中國/台灣成人影片（如 MDSR、MGL、91製片廠、天美傳媒等），使用 91md.me API：

```bash
# 搜索影片（番號直接傳入）
curl -s "https://91md.me/api.php/provide/vod/?wd=MDSR-0006"

# 從搜索結果獲取 vod_id後，獲取詳細資訊
curl -s "https://91md.me/api.php/provide/vod/?ac=detail&ids=<vod_id>"
```

**API 回應字段**：
| 字段 | 說明 | 範例 |
|------|------|------|
| `vod_name` | 影片名稱（繁體中文） | 麻豆傳媒映画.MDSR-0006-2.艾熙.小鳳新婚下... |
| `vod_actor` | 女演員 | 艾熙 |
| `vod_pic` | 封面圖 URL | https://tutu1.space/images/... |
| `vod_time` | 發布時間 | 2024-06-28 08:57:23 |
| `vod_score` | 評分 | 10.0 |
| `type_name` | 影片類型 | 麻豆視頻 |

**提取數據的 curl 命令**：
```bash
# 提取 vod_id
vod_id=$(curl -s "https://91md.me/api.php/provide/vod/?wd=<番號>" | grep -oE '"vod_id":[0-9]+' | head -1 | grep -oE '[0-9]+')

# 提取女演員
curl -s "https://91md.me/api.php/provide/vod/?ac=detail&ids=<vod_id>" | grep -oE '"vod_actor":"[^"]*"'

# 提取封面圖
curl -s "https://91md.me/api.php/provide/vod/?ac=detail&ids=<vod_id>" | grep -oE '"vod_pic":"[^"]*"'
```

**注意**：91md.me 為備用數據源，主要用於中國/台灣成人影片。請優先使用 javdb.com 或 jable.tv 處理日本 JAV。

### 4. 建立資料夾結構

```
<原始目錄>/
├── <女演員名>/
│   ├── <番號>/
│   │   ├── <番號>.mp4             # 原始影片
│   │   ├── <番號>-C.mp4           # 中文字幕版
│   │   ├── <番號>-U.mp4           # 破解版
│   │   ├── <番號>-UC.mp4          # 破解+字幕版
│   │   ├── <番號>.nfo             # metadata
│   │   ├── <番號>-cover.jpg       # 封面（加上番號前綴）
│   │   └── screenshots/
│   │       ├── 1.jpg
│   │       ├── 2.jpg
│   │       └── ...
│   ├── <番號>-C/                   # 中文字幕版
│   │   ├── <番號>-C.mp4
│   │   ├── <番號>-C.nfo
│   │   ├── <番號>-C-cover.jpg
│   │   └── screenshots/
│   ├── <番號>-U/                   # 破解版
│   │   ├── <番號>-U.mp4
│   │   ├── <番號>-U.nfo
│   │   ├── <番號>-U-cover.jpg
│   │   └── screenshots/
│   └── <番號>-UC/                  # 破解+字幕版
│       ├── <番號>-UC.mp4
│       ├── <番號>-UC.nfo
│       ├── <番號>-UC-cover.jpg
│       └── screenshots/
├── unknown/                       # 無法取得演員資訊的影片
│   └── <番號>/
│       ├── <番號>.mp4
│       ├── <番號>.nfo
│       └── <番號>-cover.jpg
└── failed/                        # 完全無法辨識的影片
    └── <番號>/
        ├── <番號>.mp4
        └── <番號>-preview.jpg    # 保留預覽圖
```

### 5. 失敗處理

**查詢成功但無演員資料**（javdb 上沒有列出演員）：
1. 將影片移至 `unknown/<番號>/`（使用 **mv** 而非 cp）
2. 仍下載封面圖和產生 NFO

**完全查詢失敗**（javdb/jable/91md 都找不到資料）：
1. 將原始影片移至 `failed/<番號>/`（使用 **mv** 而非 cp）
2. 保留預覽圖（如果存在）
3. 記錄失敗的番號

### 6. NFO Metadata 檔案

每個影片目錄需產生 `.nfo` 檔案（Kodi/XBMC 相容格式）：

**日本 JAV**：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<movie>
  <title>番號</title>
  <originaltitle>番號</originaltitle>
  <sorttitle>番號</sorttitle>
  <actor>
    <name>女演員名（繁體中文）</name>
    <type>Actor</type>
  </actor>
  <studio>Unknown</studio>
  <year>發布年份</year>
  <releasedate>發布日期</releasedate>
  <plot>影片描述</plot>
  <outline>影片概要</outline>
  <tagline></tagline>
  <genre>成人</genre>
  <rating>評分</rating>
  <uniqueid type="javdb" default="true">番號</uniqueid>
  <thumb aspect="poster">./番號-cover.jpg</thumb>
</movie>
```

**中國成人影片（使用 91md.me 數據）**：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<movie>
  <title>影片名稱（從 vod_name 提取）</title>
  <originaltitle>番號</originaltitle>
  <sorttitle>番號</sorttitle>
  <actor>
    <name>女演員名（從 vod_actor 提取，多個用逗號分隔）</name>
    <type>Actor</type>
  </actor>
  <studio>91md.me</studio>
  <year>發布年份（從 vod_time 提取）</year>
  <releasedate>發布日期（從 vod_time 提取）</releasedate>
  <plot></plot>
  <outline></outline>
  <tagline></tagline>
  <genre>成人</genre>
  <genre>從 type_name 提取（如：麻豆視頻）</genre>
  <rating>評分（從 vod_score 提取）</rating>
  <uniqueid type="91md" default="true">番號</uniqueid>
  <thumb aspect="poster">./番號-cover.jpg</thumb>
</movie>
```

### 7. 下載圖片

使用 curl 命令下載（**不要使用 webfetch**）。
**重要：在 Windows 環境下，必須先下載到 `/tmp`，再 `cp` 到含日文路徑的目標資料夾。jable.tv 圖片需加 Referer。**

**只下載 cover.jpg，不下載 fanart.jpg。** cover 優先從 jable.tv 取得，失敗才從 javdb.com fallback。

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
TMP="/tmp/jav_dl"
mkdir -p "$TMP"

# 封面圖：優先 jable.tv（需要 Referer）
curl -s -A "$UA" -e "https://jable.tv/" "<jable封面URL>" -o "$TMP/cover.jpg"
fsize=$(stat -c%s "$TMP/cover.jpg" 2>/dev/null || echo "0")
if [ "$fsize" -ge 5120 ]; then
    cp "$TMP/cover.jpg" "<目標路徑>/<番號>-cover.jpg"
else
    # Fallback：javdb.com（不需要 Referer）
    curl -s -A "$UA" "<javdb封面URL>" -o "$TMP/cover.jpg"
    fsize=$(stat -c%s "$TMP/cover.jpg" 2>/dev/null || echo "0")
    if [ "$fsize" -ge 5120 ]; then
        cp "$TMP/cover.jpg" "<目標路徑>/<番號>-cover.jpg"
    fi
fi

# 截圖（從 javdb.com）
curl -s -A "$UA" "<截圖URL>" -o "$TMP/ss_1.jpg"
cp "$TMP/ss_1.jpg" "<目標路徑>/screenshots/1.jpg"
```

### 8. 截圖大小檢查

**重要**：下載截圖後必須檢查檔案大小，過小或錯誤的圖檔不要儲存。
**注意**：在 Windows 下必須先下載到 `/tmp`，檢查大小後再 `cp` 到目標路徑。

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
TMP="/tmp/jav_dl"

# 下載到 /tmp
curl -s -A "$UA" "<截圖URL>" -o "$TMP/ss_1.jpg"

# 獲取檔案大小（單位：位元組）
fsize=$(stat -c%s "$TMP/ss_1.jpg" 2>/dev/null || echo "0")

# 如果 >= 5KB 才複製到目標路徑
if [ "$fsize" -ge 5120 ]; then
    cp "$TMP/ss_1.jpg" "<目標路徑>/screenshots/1.jpg"
else
    echo "刪除過小的截圖: ss_1.jpg ($fsize bytes)"
fi
```

檢查規則：
- 截圖檔案大小必須 >= 5KB
- 若圖檔損壞或過小，則跳過該截圖（不複製到目標路徑）

## 執行步驟

1. **確認掃描目錄**
   - 詢問用戶要掃描的目錄路徑
   - 預設為目前目錄

2. **掃描影片**
   - 使用 glob 搜尋所有影片檔案
   - 過濾無效檔案

3. **處理每個影片**
   - 清理檔名
   - 提取番號和類型
   - **演員名稱：從 javdb.com 提取**（用 ♀ 符號精確匹配，見 3.2 節）
   - **封面圖：優先 jable.tv，fallback javdb.com**（見 3.3 節）
   - **截圖：從 javdb.com 提取**
   - **驗證演員名稱**（見 3.4 節）
   - 建立資料夾結構（根據類型建立不同目錄）
     - 原始影片 → `<番號>/`
     - 中文字幕版 → `<番號>-C/`
     - 破解版 → `<番號>-U/`
     - 破解+字幕版 → `<番號>-UC/`
   - **使用 mv 移動影片**（不是 cp）
   - **下載圖片並檢查大小**
     - cover → `<番號>-cover.jpg`（加上番號前綴，優先 jable.tv，fallback javdb.com）
     - 截圖：下載後檢查大小，< 5KB 的不儲存
   - **產生 NFO metadata 檔**

4. **報告結果**
   - 顯示成功分類的數量
   - 顯示失敗的數量
   - 列出失敗的番號

## 錯誤處理

- **網路錯誤**：重試 3 次，每次間隔 5 秒
- **解析錯誤**：跳過該影片，移至 failed 目錄
- **檔案已存在**：詢問用戶是否覆蓋

## 限制事項

- 不從影片中截圖
- 僅支援 mp4/mkv/avi/wmv 格式

## 常見問題

### Q: webfetch 工具訪問 javdb.com 返回 403 錯誤怎麼辦？
A: javdb.com 會識別並阻止 webfetch/mcp 工具的請求。請使用 curl 命令代替。

### Q: 如何確保 curl 可以訪問但 webfetch 不行？
A: javdb.com 使用 User-Agent 識別機器人請求。**所有 curl 請求必須帶上瀏覽器 User-Agent**：
   ```bash
   UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
   curl -s -A "$UA" "https://javdb.com/..."
   ```

### Q: Windows 環境下 grep -P 報錯怎麼辦？
A: Windows Git Bash 不支援 `grep -P`。**一律使用 `grep -oE` 替代**：
   ```bash
   # ❌ grep -oP '(?<=content=")[^"]+'
   # ✅ grep -oE 'content="[^"]+"' | sed 's/content="//;s/"$//'
   ```

### Q: Windows 下 curl 下載到含日文路徑失敗怎麼辦？
A: curl 的 `-o` 在 Windows 下無法處理 CJK 字符路徑。**先下載到 /tmp 再 cp**：
   ```bash
   curl -s -A "$UA" "$url" -o /tmp/img.jpg
   cp /tmp/img.jpg "含日文的目標路徑/img.jpg"
   ```

### Q: jable.tv 的圖片下載後 0 bytes？
A: jable.tv CDN (`assets-cdn.jable.tv`) 需要 Referer 標頭。**必須加 `-e "https://jable.tv/"`**：
   ```bash
   curl -s -A "$UA" -e "https://jable.tv/" "$jable_img_url" -o /tmp/cover.jpg
   ```

### Q: 訪問被封鎖返回 "管理員禁止了你的訪問" 怎麼辦？
A: javdb.com 會臨時封鎖頻繁訪問的 IP。請：
   1. 等待 5-10 分鐘後重試
   2. 使用不同的 User-Agent
   3. 在請求之間添加延遲（每秒不超過 1 個請求）
   4. 使用備用數據源 javdatabase.com 或 jable.tv

### Q: jable.tv 的演員名稱是 MD5 hash 怎麼辦？
A: jable.tv 的 `/models/` URL slug 對很多演員使用 MD5 hash（如 `d1ebb3d61ee367652e6b1f35b469f2b6`），而非可讀名稱。**不要使用 jable.tv 的 URL slug 作為演員名稱**。正確做法：
   - 演員名稱**必須從 javdb.com 提取**，用 `♀` 符號精確匹配
   - jable.tv 只用於取得封面圖（og:image）

### Q: javdb.com 提取到「有碼」或「無碼」作為演員名？
A: javdb.com 的導航列有 `/actors/censored`（有碼）、`/actors/uncensored`（無碼）、`/actors/western`（歐美）等分類連結，如果 grep 模式不夠精確會匹配到這些。**必須用 `♀` 符號模式**：
   ```bash
   # ✅ 正確：只匹配帶 ♀ 符號的女演員連結
   grep -oE 'href="/actors/[A-Za-z0-9]+\">[^<]+</a><strong class="symbol female"' | \
     head -1 | sed 's/.*">//;s/<\/a>.*//'

   # ❌ 錯誤：會匹配到導航列分類
   grep -oE 'href="/actors/[^"]+' | head -1
   ```

### Q: jable.tv 數據源使用方法？
A: jable.tv **僅用於取得封面圖**，不用於提取演員名稱。使用方法：
   ```bash
   # 搜索影片（番號中的 - 改為空格）
   curl -s -A "$UA" "https://jable.tv/search/HND%20765/" | grep -oE '/videos/[^/]+/' | head -1

   # 獲取封面圖（og:image）
   curl -s -A "$UA" "https://jable.tv/videos/<視頻ID>/" | \
     grep -oE 'https://[^"]+jable.tv[^"]+\.jpg' | head -1
   ```

### Q: javdb.com 無法獲取截圖怎麼辦？
A: 當 javdb.com 的截圖提取失敗時，可以嘗試從 javdatabase.com 获取：
   ```bash
   # 搜索影片
   curl -s "https://www.javdatabase.com/search?q=SONE-123"

   # 從電影頁面獲取截圖
   curl -s "https://www.javdatabase.com/movies/SONE-123" | grep -oE 'https://[^"]+\.jpg'
   ```

### Q: missav.ws 可以使用嗎？
A: missav.ws 有 Cloudflare 保護，curl 無法繞過驗證，不建議使用。

### Q: 如何處理中國成人影片（如 MDSR、MGL）？
A: 中國/台灣成人影片不在 javdb.com/jable.tv 收錄範圍內，請使用 91md.me API：
   ```bash
   # 搜索影片
   curl -s "https://91md.me/api.php/provide/vod/?wd=MDSR-0006"

   # 獲取詳細資訊（需先從搜索結果獲取 vod_id）
   curl -s "https://91md.me/api.php/provide/vod/?ac=detail&ids=<vod_id>"
   ```

### Q: 91md.me API 無法獲取資料怎麼辦？
A: 91md.me 為備用數據源，可能不穩定。若無法獲取：
   1. 稍後重試
   2. 將影片移至 failed 目錄
   3. 手動建立資料夾並輸入元數據
