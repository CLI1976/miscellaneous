# Story Illustrator - 故事插圖導演

為故事文章自動規劃場景、角色，並生成連貫的插圖。

## 功能特色

- 🎬 自動分析文章結構，規劃場景數量
- 👥 識別角色並建立一致性檔案
- 🎨 生成高品質插圖提示詞
- 📸 調用 AI 圖片生成工具
- 🔄 **使用角色設定圖 + 參考圖機制確保角色一致性**
- 🎥 **自動生成分鏡腳本** ⭐ 新增
- 💭 **角色情緒變化追蹤** ⭐ 新增
- 🔀 **場景轉場建議** ⭐ 新增

## 使用方式

```bash
# 從 Markdown 文件生成
/story-illustrator path/to/story.md

# 指定風格
/story-illustrator story.md --style watercolor

# 指定圖片文字語言（預設 EN）
/story-illustrator story.md --lang TW    # 繁體中文標籤/說明
/story-illustrator story.md --lang EN    # 英文標籤/說明

# 指定目標讀者
/story-illustrator story.md --audience children

# 僅分析不生圖
/story-illustrator story.md --plan-only

# 跳過角色設定圖（使用現有的）
/story-illustrator story.md --skip-character-sheet

# 生成完整分鏡腳本 ⭐ 新增
/story-illustrator story.md --storyboard

# 啟用情緒追蹤 ⭐ 新增
/story-illustrator story.md --emotion-tracking

# 完整導演模式（分鏡+情緒+轉場）⭐ 新增
/story-illustrator story.md --director-mode
```

## 工作流程

當用戶調用此 skill 時，執行以下步驟：

### 階段 1: 分析與規劃

1. **讀取文章內容**
   - 從指定路徑讀取 Markdown 文件
   - 或接收直接輸入的文字

2. **場景分析**
   - 識別故事中的關鍵場景
   - 判斷需要幾張插圖（建議 5-10 張）
   - 標記每個場景的情緒基調

3. **角色識別與分級**（重要）
   - 從文章中提取所有角色
   - **必須明確指定：種族/膚色、髮型、髮色、五官特徵**
   - **為主要角色設計「特色附屬品」(Unique Accessory)** ⭐ 新增
     - 從故事內容推斷或創意添加
     - 例如：眼鏡、髮帶、手錶、項鍊、耳環、帽子、徽章
     - 用途：大幅提升角色辨識度，確保跨場景一致性
   - **按戲份分級角色**：
     - **主要角色**：出場 ≥3 個場景 → 生成主角設定圖 + 設計特色附屬品
     - **次要角色**：出場 1-2 個場景 → 生成配角設定圖
     - **背景角色**：無台詞/無特寫 → 僅文字描述
   - 建立角色一致性檔案

4. **輸出規劃報告**
   ```
   📋 場景規劃報告

   總場景數: 8

   🎭 角色清單（按戲份分級）:

   【主要角色】(≥3 場景，需生成設定圖)
   1. 安妮 - 白人女孩、橘紅色雙辮子、綠色眼睛、雀斑、簡樸洋裝 [7/8 場景]
   2. 戴安娜 - 白人女孩、黑色直髮齊瀏海、棕色眼睛、優雅洋裝 [5/8 場景]

   【次要角色】(1-2 場景，需生成設定圖)
   3. 瑪麗亞 - 白人年長女性、灰色髮髻、嚴肅但善良 [1/8 場景]
   4. 馬修 - 白人年長男性、灰髮、農夫背心 [1/8 場景]
   5. 蜜妮 - 白人幼童、深色短髮、戴安娜的妹妹 [1/8 場景]

   📸 場景清單:
   1. [0-500字] 綠屋的下午茶 - 溫暖、歡樂
   2. [500-800字] 戴安娜不舒服 - 擔憂、緊張
   ...

   是否繼續生成插圖? (yes/no/modify)
   ```

### 階段 2: 生成角色設定圖 (Character Sheet) ⭐ 重要

**這是確保角色一致性的關鍵步驟！**

#### 2.1 多張角色設定圖策略

根據角色戲份生成不同的設定圖：

| 設定圖 | 包含角色 | 用途 |
|--------|----------|------|
| `character-sheet-main.png` | 主要角色（≥3 場景）| 大多數場景的參考圖 |
| `character-sheet-support.png` | 次要角色（1-2 場景）| 特定場景的參考圖 |

#### 2.2 生成順序

1. **先生成主角設定圖** (`character-sheet-main.png`)
   - 包含出場 ≥3 次的角色
   - 用戶確認後繼續

2. **再生成配角設定圖** (`character-sheet-support.png`)
   - 包含出場 1-2 次的角色
   - 用戶確認後繼續

#### 2.3 角色設定圖提示詞模板

```
Character design reference sheet, white background, multiple views.

[Character 1 Name]: [ethnicity] [age], [hair description], [eye color], [skin tone], [distinctive features], [clothing]. Show front view and 3/4 view.

[Character 2 Name]: [ethnicity] [age], [hair description], [eye color], [skin tone], [distinctive features], [clothing]. Show front view and 3/4 view.

Style: [art style], consistent character design, model sheet, clean lines.
```

#### 2.4 範例：主角設定圖提示詞

```
Character design reference sheet, white background, storybook style.

Anne Shirley: Caucasian girl age 11, bright orange-red hair in two long braids, large green eyes, pale skin with freckles across nose and cheeks, thin build, wearing simple brown Victorian dress with white apron. Show front view and 3/4 view.

Diana Barry: Caucasian girl age 11, straight jet-black hair with neat bangs cut above eyebrows, warm brown eyes, fair porcelain skin, slightly plump cheeks, wearing elegant navy blue Victorian dress with lace collar. Show front view and 3/4 view.

Style: children's storybook illustration, consistent character design, model sheet, clean lines, soft colors.
```

#### 2.5 範例：配角設定圖提示詞

```
Character design reference sheet, white background, storybook style.

Marilla Cuthbert: Caucasian elderly woman age 55-60, gray hair in tight bun, stern but kind eyes, thin lips, wearing plain dark Victorian dress with white collar. Show front view.

Matthew Cuthbert: Caucasian elderly man age 55-60, thinning gray hair, shy gentle expression, wearing farmer's vest and work shirt. Show front view.

Minnie May Barry: Caucasian toddler girl age 3-4, dark brown short hair, round chubby face, wearing white nightgown (sick). Show front view.

Style: children's storybook illustration, consistent character design, model sheet, clean lines, soft colors.
```

#### 2.6 確認角色設定圖

- 顯示生成的設定圖給用戶
- 詢問是否滿意，或需要重新生成（最多 3 次）
- **主角設定圖確認後，才生成配角設定圖**
- **全部確認後，才進入場景生成階段**

### 階段 3: 生成場景插圖（使用參考圖）

#### 3.1 建立角色檔案

創建 `characters.json` 儲存所有角色特徵（含分級）：

```json
{
  "settings": {
    "lang": "TW",
    "style": "storybook"
  },
  "main_characters": {
    "Anne": {
      "name_zh": "安妮",
      "ethnicity": "Caucasian",
      "age": "11-year-old girl",
      "hair": "bright orange-red hair in two long braids",
      "eyes": "large green eyes",
      "skin": "pale skin with freckles across nose and cheeks",
      "face": "thin face, expressive features",
      "body": "thin build",
      "clothing": "simple brown Victorian dress with white apron",
      "unique_accessory": "green ribbon hair ties on braids",
      "personality_visual": "energetic, animated expressions",
      "scenes": [1, 2, 3, 4, 5, 6, 7]
    },
    "Diana": {
      "name_zh": "戴安娜",
      "ethnicity": "Caucasian",
      "age": "11-year-old girl",
      "hair": "straight jet-black hair with neat bangs cut above eyebrows",
      "eyes": "warm brown eyes",
      "skin": "fair porcelain skin",
      "face": "slightly plump cheeks, gentle features",
      "body": "average build",
      "clothing": "elegant navy blue Victorian dress with lace collar",
      "unique_accessory": "pearl pendant necklace",
      "personality_visual": "calm, graceful demeanor",
      "scenes": [1, 2, 4, 5]
    }
  },
  "support_characters": {
    "Marilla": {
      "name_zh": "瑪麗亞",
      "ethnicity": "Caucasian",
      "age": "elderly woman (55-60)",
      "hair": "gray hair in tight bun",
      "eyes": "stern but kind eyes",
      "clothing": "plain dark Victorian dress",
      "unique_accessory": "small cameo brooch at collar",
      "scenes": []
    },
    "Matthew": {
      "name_zh": "馬修",
      "ethnicity": "Caucasian",
      "age": "elderly man (55-60)",
      "hair": "thinning gray hair",
      "clothing": "farmer's vest and work shirt",
      "unique_accessory": "old pocket watch chain visible",
      "scenes": [5]
    },
    "MinnieMay": {
      "name_zh": "蜜妮",
      "ethnicity": "Caucasian",
      "age": "toddler (3-4)",
      "hair": "dark brown short hair",
      "clothing": "white nightgown",
      "unique_accessory": null,
      "scenes": [6]
    }
  }
}
```

#### 3.2 選擇參考圖的邏輯

根據場景中出現的角色，選擇適當的參考圖：

| 場景角色組成 | 使用的參考圖 |
|--------------|--------------|
| 只有主要角色 | `--ref character-sheet-main.png` |
| 包含次要角色 | `--ref character-sheet-main.png --ref character-sheet-support.png`（如支援多張）|
| 只有次要角色 | `--ref character-sheet-support.png` |

**若 API 只支援單張參考圖**：優先使用主角設定圖，次要角色靠精確文字描述補充。

#### 3.3 場景生成命令格式

**只有主要角色的場景**：
```bash
npx -y bun ${GEMINI_SCRIPT} \
  --prompt "[場景提示詞]" \
  --ref character-sheet-main.png \
  --image scene-XX.png
```

**包含次要角色的場景**（API 支援多參考圖時）：
```bash
npx -y bun ${GEMINI_SCRIPT} \
  --prompt "[場景提示詞]" \
  --ref character-sheet-main.png \
  --ref character-sheet-support.png \
  --image scene-XX.png
```

**場景提示詞必須包含完整角色描述**（即使有參考圖也要寫，雙重保險）

#### 3.4 調用圖片生成

- 根據場景角色選擇適當的參考圖
- 逐個場景生成插圖
- 顯示生成進度
- 將圖片保存到指定目錄

#### 3.5 生成摘要文件

---

## 角色描述精確模板 ⭐ 重要

### 必填欄位（避免歧義）

| 欄位 | 說明 | 錯誤示範 | 正確示範 |
|------|------|----------|----------|
| **種族/膚色** | 明確指定 | `fair skin` | `Caucasian, pale skin` |
| **髮色** | 具體顏色 | `red hair` | `bright orange-red hair` |
| **髮型** | 詳細描述 | `black hair` | `straight jet-black hair with bangs` |
| **眼睛** | 顏色+形狀 | `big eyes` | `large almond-shaped green eyes` |
| **年齡** | 具體數字 | `young girl` | `11-year-old girl` |
| **臉型** | 特徵描述 | (省略) | `oval face with freckles` |
| **特色附屬品** ⭐ | 增加辨識度 | (省略) | `rectangular glasses`, `red hair ribbon` |

### 特色附屬品 (Unique Accessory) 設計指南 ⭐ 新增

**目的**：為每個主要角色添加一個視覺上容易識別的附屬品，大幅提升跨場景一致性。

**選擇原則**：
1. **故事相關**：優先從故事內容中提取（如：班長戴眼鏡、運動員戴護腕）
2. **視覺顯眼**：選擇容易在不同場景中辨識的物品
3. **角色適合**：符合角色個性和身份
4. **不易遺漏**：選擇 AI 生圖時不容易忽略的物品

**推薦附屬品類型**：

| 類型 | 範例 | 適合角色 |
|------|------|----------|
| 眼鏡類 | rectangular glasses, round glasses, sunglasses | 學生、知識分子 |
| 髮飾類 | red hair ribbon, blue headband, hairpin | 女孩、活潑角色 |
| 首飾類 | pearl necklace, simple pendant, earrings | 優雅角色 |
| 手錶類 | digital sports watch, classic wristwatch | 運動員、成熟角色 |
| 帽子類 | baseball cap, beanie, straw hat | 戶外活動者 |
| 徽章類 | class monitor badge, team pin | 學生幹部、隊員 |
| 運動類 | wristband, sweatband, knee brace | 運動員 |

**提示詞中的使用方式**：
```
MINGYANG: East Asian boy age 12, short neat jet-black hair,
WEARING RECTANGULAR GLASSES (important identifying feature),
friendly class leader appearance...
```

**注意**：在提示詞中強調附屬品，使用大寫或括號標記其重要性。

### 避免歧義的描述規則

1. **髮色 "black" 的問題**
   - ❌ `black hair` → 可能被誤解為黑人的頭髮
   - ✅ `jet-black straight hair` 或 `raven-black hair`
   - ✅ 加上種族：`East Asian girl with black hair` 或 `Caucasian girl with black hair`

2. **膚色描述**
   - ❌ `fair skin` → 模糊
   - ✅ `pale Caucasian skin` / `light East Asian skin tone` / `warm olive skin`

3. **年齡描述**
   - ❌ `young girl` → 模糊（3歲? 15歲?）
   - ✅ `11-year-old girl` / `preteen girl around 11`

### 完整角色描述範例

```
Anne Shirley: Caucasian preteen girl (age 11), bright orange-red hair styled in two long braids tied with ribbons, large expressive green eyes, pale ivory skin with a distinctive spray of freckles across her nose and cheeks, thin oval face, slender build, wearing a simple brown Victorian-era dress with white apron and black boots.

Diana Barry: Caucasian preteen girl (age 11), straight jet-black hair falling to shoulders with neat straight bangs cut just above her eyebrows, warm brown eyes with long lashes, fair porcelain skin with rosy cheeks, round gentle face, average build, wearing an elegant navy blue Victorian dress with white lace collar and cuffs.
```

---

## 場景提示詞模板（含參考圖使用）

### 標準格式

```
[Style] illustration showing [scene action].

Characters present (MUST match reference sheet exactly):
- [Character 1]: [full description from characters.json - copy exactly]
- [Character 2]: [full description from characters.json - copy exactly]

Scene: [specific scene description]
Setting: [environment details]
Mood: [emotional tone]
Lighting: [lighting description]

Style: [art style] illustration, consistent with reference sheet, suitable for [audience].
Important: The reference image is for character appearance ONLY. Show ONLY the characters described in this scene — do not reproduce extra figures or views from the reference sheet.
```

### 範例場景提示詞

```
Warm storybook illustration showing two girls having afternoon tea together.

Characters present (MUST match reference sheet exactly):
- Anne Shirley: Caucasian preteen girl (age 11), bright orange-red hair in two long braids, large green eyes, pale skin with freckles, thin build, simple brown Victorian dress with white apron, cheerful animated expression
- Diana Barry: Caucasian preteen girl (age 11), straight jet-black hair with neat bangs, warm brown eyes, fair porcelain skin, rosy cheeks, elegant navy blue Victorian dress, holding a glass of red juice with delighted expression

Scene: Anne and Diana sitting at a wooden table having afternoon tea, Diana drinking red juice
Setting: Cozy Victorian cottage interior, warm afternoon sunlight, red autumn maple leaves visible through the window, table set with pastries and a glass pitcher of red juice
Mood: Warm, cheerful, friendly, innocent joy
Lighting: Soft golden afternoon light from window

Style: Children's storybook illustration, soft watercolor textures, consistent with reference sheet.
Important: The reference image is for character appearance ONLY. Show ONLY the characters described in this scene — do not reproduce extra figures or views from the reference sheet.
```

---

## 圖片生成調用（更新）

### 使用 Gemini Web API（推薦）

**階段 2：生成角色設定圖**
```bash
npx -y bun ${SKILL_DIR}/scripts/main.ts \
  --prompt "[角色設定圖提示詞]" \
  --image "${OUTPUT_DIR}/character-sheet.png"
```

**階段 3：生成場景圖（使用參考圖）**
```bash
npx -y bun ${SKILL_DIR}/scripts/main.ts \
  --prompt "[場景提示詞]" \
  --reference "${OUTPUT_DIR}/character-sheet.png" \
  --image "${OUTPUT_DIR}/scene-01.png"
```

### 其他 API 的參考圖用法

| API | 參考圖參數 |
|-----|-----------|
| Gemini Web | `--reference image.png` |
| OpenAI DALL-E | 不支援（需用 GPT-4V 描述後生成）|
| Stable Diffusion | ControlNet / IP-Adapter |
| Midjourney | `--sref` 或圖片 URL |

### 不使用 Session

**重要：不要使用 `--sessionId`**

Session 會導致 token 累積（第 N 張圖 = N 倍 token），成本過高且大多數正式 API 不支援。

使用 `--reference` 參考圖是更好的方案：
- 成本固定（每張多一張圖片輸入）
- 效果更好（視覺參考比文字更精確）
- API 相容性高

---

## 輸出文件結構（更新）

```
output/
├── character-sheet-main.png     # ⭐ 主角設定圖
├── character-sheet-support.png  # 配角設定圖
├── characters.json              # 角色設定檔（含分級）
├── scenes-plan.md               # 場景規劃文件
├── storyboard.md                # ⭐ 分鏡腳本（--storyboard）
├── emotion-tracking.md          # ⭐ 情緒追蹤（--emotion-tracking）
├── transitions.md               # ⭐ 轉場建議（--director-mode）
├── scene-01.png                 # 場景插圖
├── scene-02.png
├── ...
└── generation-summary.md        # 生成摘要
```

---

## 風格參數

支援的風格選項：

- `watercolor` (水彩，預設) - 柔和溫暖
- `ink-brush` (水墨) - 東方意境
- `storybook` (繪本) - 兒童友善
- `realistic` (寫實) - 細節豐富
- `manga` (漫畫) - 日式風格
- `minimalist` (極簡) - 簡潔現代

## 目標讀者參數

- `children` (兒童) - 色彩鮮豔、簡化細節
- `teens` (青少年) - 現代感、動態
- `adults` (成人) - 成熟、細膩

## 語言參數 `--lang`

控制圖片中文字標籤的語言：

| 參數值 | 說明 | 範例 |
|--------|------|------|
| `EN` (預設) | 英文標籤 | "Scene 1: The Race", "Zhengbin" |
| `TW` | 繁體中文標籤 | 「場景一：接力賽」、「政彬」|

**使用時機**：
- 角色設定圖的角色名稱標籤
- 場景圖的場景標題/說明文字
- 情緒/氛圍標註

**提示詞範例（TW）**：
```
Character design reference sheet with labels in Traditional Chinese (繁體中文).
角色名稱標籤使用繁體中文顯示。

政彬 (Zhengbin): East Asian boy age 12...
名揚 (Mingyang): East Asian boy age 12...

Label each character with their Chinese name (政彬、名揚).
```

**提示詞範例（EN）**：
```
Character design reference sheet with English labels.

ZHENGBIN: East Asian boy age 12...
MINGYANG: East Asian boy age 12...

Label each character with their English name.
```

---

## 導演模式功能 ⭐ 新增

### 分鏡腳本 (--storyboard)

為每個場景生成專業分鏡設定：

```markdown
## 場景 1: 起跑線前的壓力

### 分鏡設定
- **鏡頭類型**: Medium Close-Up (MCU) / 中近景
- **鏡頭角度**: Slightly Low Angle / 輕微仰視
- **構圖**: 三分法，主角置於左側，跑道延伸至右側

### 角色位置圖
┌─────────────────────────┐
│  ☀️                     │
│ [政彬]        跑道延伸→ │
│  緊握接力棒             │
│ ════起跑線════          │
└─────────────────────────┘

### 動作描述
1. 政彬站在起跑位置，身體微微前傾
2. 雙手緊握接力棒，指節發白
3. 眼神凝視前方，眉頭微皺
```

**鏡頭類型參考**：
| 類型 | 英文 | 用途 |
|------|------|------|
| 遠景 | Wide Shot (WS) | 展示環境 |
| 全景 | Full Shot (FS) | 角色全身 |
| 中景 | Medium Shot (MS) | 腰部以上 |
| 近景 | Close-Up (CU) | 臉部特寫 |
| 雙人鏡頭 | Two Shot | 兩人互動 |

### 情緒追蹤 (--emotion-tracking)

追蹤角色在每個場景的情緒變化：

```markdown
## 角色情緒追蹤：政彬

| 場景 | 情緒 | 強度 | 表情描述 |
|------|------|------|----------|
| 1 | 緊張+壓力 | 4/5 | 皺眉、握緊拳頭 |
| 2 | 不滿+委屈 | 5/5 | 抱胸、撇嘴 |
| 4 | 慚愧+感動 | 4/5 | 低頭、眼眶泛紅 |
| 5 | 堅定+熱血 | 5/5 | 眼神銳利、嘴角上揚 |
| 6 | 興奮+釋然 | 5/5 | 大笑、張開雙臂 |

### 情緒曲線
強度
5 │    ●                 ●────●
4 │  ●   ╲             ╱
3 │       ╲           ╱
2 │        ╲    ●    ╱
1 │         ╲──────╱
  └──────────────────────────
    場景 1  2  3  4  5  6

### 關鍵轉折點
- 場景 2→4: 從「不滿」到「慚愧」（角色成長）
- 場景 5→6: 從「堅定」到「興奮」（高潮釋放）
```

**情緒在提示詞中的應用**：
```
CHARACTER: Zhengbin, East Asian boy age 12...
EMOTION: determined and focused (intensity 5/5),
eyes sharp with resolve, slight confident smile
```

### 轉場建議 (--director-mode)

分析場景之間的視覺連接：

```markdown
## 轉場分析

### 場景 1 → 場景 2
- **轉場類型**: 時間回溯（回憶）
- **時間跨度**: 幾天前
- **情緒變化**: 緊張 → 不滿
- **視覺連接**:
  - 場景1 結尾：政彬握著接力棒的手
  - 場景2 開頭：同樣的手，在訓練場景
- **色調變化**: 明亮 → 稍微褪色（回憶感）

### 場景 5 → 場景 6
- **轉場類型**: 動態連續
- **時間跨度**: 即時
- **情緒變化**: 堅定 → 興奮
- **視覺連接**:
  - 場景5：衝刺的動態
  - 場景6：擁抱的靜態（動靜對比）
```

**轉場類型參考**：
| 類型 | 說明 | 適用情境 |
|------|------|----------|
| 時間跳躍 | 直接切換時間 | 回憶、跳過 |
| 空間切換 | 地點改變 | 場景轉移 |
| 情緒對比 | 情緒反差 | 製造張力 |
| 動態連續 | 動作延續 | 連貫敘事 |

### 完整導演模式輸出

使用 `--director-mode` 會同時生成：
1. `storyboard.md` - 完整分鏡腳本
2. `emotion-tracking.md` - 角色情緒追蹤表
3. `transitions.md` - 場景轉場建議

並在場景提示詞中自動整合：
- 鏡頭類型與角度
- 構圖建議
- 情緒強度與表情描述
- 色調建議

---

## 實作指南

### 場景識別邏輯

使用以下標準判斷場景切換：
1. 時間變化 (「隔天」、「不久後」)
2. 地點變化 (「回到家」、「來到...」)
3. 情節轉折 (對話重大變化、情緒轉換)
4. 段落分析 (通常 1-3 段落 = 1 場景)

建議場景數量：
- 短文 (500-1000字): 3-5 場景
- 中篇 (1000-2000字): 5-8 場景
- 長文 (2000字以上): 8-12 場景

### 角色特徵提取（更新）

從文章中搜尋以下關鍵詞，並**推斷合理的種族/外觀設定**：

| 類別 | 提取內容 | 推斷規則 |
|------|----------|----------|
| 種族 | 文章背景、人名、地點 | 加拿大愛德華王子島 → Caucasian |
| 髮色 | 紅髮、黑髮、金髮 | 紅色 → orange-red / auburn |
| 髮型 | 辮子、長髮、短髮 | 辮子 → braids / pigtails |
| 膚色 | 白皙、黝黑、雀斑 | 雀斑 → freckled pale skin |
| 年齡 | 小孩、少女、老人 | 推算具體年齡 |
| 衣著 | 洋裝、圍裙、西裝 | 結合時代背景 |

---

## 錯誤處理

- 文章太短 (< 200字): 建議至少 3 個場景
- 無法識別角色: 詢問用戶提供角色描述
- **角色設定圖不滿意**: 重新生成（最多 3 次）
- 圖片生成失敗: 保存 prompt 並繼續下一張
- 風格參數錯誤: 使用預設 watercolor

---

## 品質檢查

### 主角設定圖檢查
- [ ] 所有主要角色（≥3 場景）都有呈現
- [ ] 種族/膚色符合設定
- [ ] 髮型髮色清晰可辨
- [ ] 風格統一

### 配角設定圖檢查
- [ ] 所有次要角色（1-2 場景）都有呈現
- [ ] 與主角設定圖風格一致
- [ ] 年齡/體型符合設定

### 場景圖檢查
- [ ] 主要角色外觀與主角設定圖一致
- [ ] 次要角色外觀與配角設定圖一致
- [ ] 場景順序符合故事邏輯
- [ ] 圖片風格統一
- [ ] 情緒基調符合文字
- [ ] 適合目標讀者年齡

---

## 使用範例

```bash
# 完整流程
/story-illustrator my-story.md --style storybook --audience children

# 輸出流程:
# 1. 分析報告（角色精確描述）
# 2. 用戶確認
# 3. 生成 character-sheet.png（角色設定圖）
# 4. 用戶確認角色設定圖
# 5. 生成場景插圖（每張都使用 --reference）
# 6. 生成摘要文件
```

---

## 自訂擴展

可以在同目錄創建 `EXTEND.md` 來：
- 添加自定義風格
- 修改場景判斷規則
- 調整提示詞模板
- 指定特定生圖工具
- **自訂角色種族/外觀預設值**

---

## 成本估算

| 項目 | 數量 | 預估成本 |
|------|------|----------|
| 主角設定圖 | 1 張 | ~$0.04 |
| 配角設定圖 | 1 張 | ~$0.04 |
| 參考圖輸入 | N 次 | ~$0.005 × N |
| 場景圖生成 | N 張 | ~$0.04 × N |
| 文字 token | +600 | ~$0.001 |

**7 張場景總成本 ≈ $0.34-0.40**（比使用 Session 省 50%+）

**成本優化提示**：
- 若次要角色只出現 1 場景，可考慮不生成配角設定圖，僅靠精確文字描述
- 根據故事複雜度彈性調整

---

## 注意事項

⚠️ **角色一致性（最重要）**：
- **一定要先生成角色設定圖**（主角 + 配角分開）
- 根據場景角色選擇適當的參考圖
- 提示詞中仍要包含完整角色描述（雙重保險）
- 種族/膚色/髮型必須明確指定
- **次要角色也需要精確描述**，避免每次出場外觀不同

⚠️ **參考圖幽靈人物問題**（常見）：
- 使用 character-sheet 作為 `--ref` 時，AI 可能把設定圖中的多視角（正面+側面）誤判為多個人物，在場景中生成多餘的半身/全身人影
- **必須**在每張場景提示詞末尾加入防護語句：
  `Important: The reference image is for character appearance ONLY. Show ONLY the characters described in this scene — do not reproduce extra figures or views from the reference sheet.`

⚠️ **圖片品質**：
- 不同風格適合不同故事類型
- 兒童故事建議使用 watercolor 或 storybook
- 複雜場景可能需要簡化

⚠️ **版權**：
- 生成的圖片請確認使用條款
- 商業用途需注意授權問題

---

## 實戰經驗與改進指南（基於 12 個 Unit 的實際生成經驗）

### 1. 文章類型自動判斷

在階段 1 分析時，根據以下規則自動判斷文章類型，決定是否需要角色設定圖和對話呈現方式：

| 文章類型 | 判斷依據 | 角色設定圖 | 對話呈現 |
|----------|----------|-----------|----------|
| 人物故事（有對話） | 有角色名、有引號對話 | ✅ 需要 | 對話框 (speech bubble) |
| 擬人化敘事 | 非人類角色說話（天氣、器官等） | ❌ 不需要 | 對話框（擬人角色台詞） |
| 知識/科學/教學文章 | 無角色、說明文體、步驟教學 | ❌ 不需要 | 文字方塊 (text box) |

**重要**：沒有人物角色的文章，不要硬加對話框。重要的說明文字應以文字方塊搭配畫風呈現。

### 2. 科學/解剖類內容的特別處理

當文章涉及科學、人體、地理等需要「事實正確」的內容時：

**問題**：AI 生圖容易產生解剖錯誤（如多出器官、位置錯誤），且修正後容易變成教科書風格。

**解決方案**：
- 使用**肯定句描述正確結構**，避免否定句（AI 容易忽略 "NOT" "don't"）
  - ❌ `ONE PAIR of lungs — NOT two pairs`
  - ✅ `One pair of lungs surrounds the heart — one left lung and one right lung`
- 同時強調畫風：`NOT a medical textbook — this is a Ghibli fantasy world`
- 用「魔幻世界」包裝科學內容：血管→魔法河流、血球→可愛角色、器官→擬人化夥伴
- 避免使用 `diagram`、`label`、`chart` 等觸發教科書風格的詞彙，改用 `illustrated`、`whimsical`、`enchanting`

### 3. 常見生圖問題預防

以下問題在實際生成中反覆出現，提示詞撰寫時應主動預防：

| 問題 | 原因 | 預防措施 |
|------|------|----------|
| **對話框重複** | 提示詞中多次提及同一句台詞 | 整篇提示詞中每句台詞只寫一次，集中在 `Speech bubble from X:` 區塊 |
| **提示詞文字洩漏到畫面** | 提示詞中的指令性文字被當成畫面元素 | 精簡 `Style:` `Important:` 等指令，避免過長的技術描述 |
| **身體部位分離** | 動態姿勢（瑜伽、運動）生成失敗 | 加入 `anatomically correct connected body` 描述 |
| **器官/物體數量錯誤** | AI 忽略數量限制 | 用空間關係描述（`surrounds`、`on each side`）取代數量否定句 |
| **畫風偏移** | 科學內容觸發教科書風格 | 強調 `Ghibli fantasy world` + 避免 diagram/chart 等詞 |
| **參考圖幽靈人物** ⭐ | character-sheet 的多視角被當成多個人物複製到場景中，出現多餘的半身/全身人影 | 場景提示詞末尾加入：`The reference image is for character appearance ONLY. Show ONLY the characters described in this scene — do not reproduce extra figures or views from the reference sheet.` |

### 4. 提示詞精簡化原則

場景提示詞應控制在合理長度內，過長的提示詞會導致 AI 混亂或文字洩漏：

**建議結構（5-7 行核心描述）**：
```
[風格] illustration showing [場景動作].

Scene: [具體場景描述，2-3 句]
Setting: [環境，1 句]
Mood: [情緒關鍵詞]
Lighting: [光線描述]

Speech bubble from [角色]: "[台詞]"
```

**避免**：
- 重複寫 `Important: Characters must match...`（有參考圖時一次就夠）
- 在不同段落重複描述同一角色的外觀
- 過多的 `MUST`、`IMPORTANT`、`CRITICAL` 等強調詞

### 5. 風格錨定策略

**有角色設定圖的文章**：用 `--ref character-sheet-main.png` 自然錨定風格，效果較好。

**無角色設定圖的教學文章**：各場景之間的風格容易飄移。建議：
- 第一張場景圖生成後，後續場景可用 `--ref scene-01.png` 作為風格參考
- 或額外生成一張「風格參考圖」（style-reference.png），僅用於錨定色調和畫風

### 6. 重試與錯誤記錄

在 `generation-summary.md` 中記錄重試資訊，方便日後優化：

```markdown
## 生成備註
- `scene-03.png`: 首次生成解剖不正確（兩組肺），調整提示詞後重新生成
- `scene-05.png`: 首次超時，重試成功
```
