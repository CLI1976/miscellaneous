# Story Illustrator Skill

為故事文章自動生成連貫、高品質插圖的 Claude Code skill。

## 功能特色

- 🎬 **智能場景分析** - 自動識別關鍵場景，判斷最佳插圖位置
- 👥 **角色一致性** - 生成角色設定圖 + 特色附屬品，確保跨場景外觀統一
- 🎨 **風格控制** - 支援多種藝術風格（水彩、繪本、漫畫等）
- 🌐 **多語言標籤** - 圖片文字支援繁體中文 (TW) 或英文 (EN)
- 📊 **分階段工作流** - 先規劃確認，再生成圖片
- 🔧 **高度可自訂** - 支援手動調整和擴展
- 🎥 **分鏡腳本生成** - 專業鏡頭、構圖、角色位置規劃 ⭐ 新增
- 💭 **情緒追蹤系統** - 追蹤角色情緒變化曲線 ⭐ 新增
- 🔀 **轉場建議** - 場景間的視覺連接與敘事節奏 ⭐ 新增

## 快速開始

### 安裝

```bash
# 複製 skill 到 Claude Code 目錄
cp -r story-illustrator ~/.claude/skills/

# Windows
Copy-Item -Recurse story-illustrator "$env:USERPROFILE\.claude\skills\"
```

### 基本使用

```bash
# 從文件生成插圖
/story-illustrator path/to/your-story.md

# 指定風格
/story-illustrator story.md --style storybook

# 指定圖片文字語言
/story-illustrator story.md --lang TW

# 僅分析不生圖
/story-illustrator story.md --plan-only
```

## 工作流程

### 階段 1: 分析與規劃

```bash
/story-illustrator my-story.md --plan-only
```

輸出：
```
📋 場景規劃報告

總場景數: 6

🎭 角色清單（按戲份分級）:

【主要角色】(≥3 場景，需生成設定圖)
1. 政彬 - 東亞男孩、凌亂黑髮、1號運動服、🎯 特色附屬品: 紅色護腕 [6/6 場景]
2. 名揚 - 東亞男孩、整齊黑髮、4號運動服、🎯 特色附屬品: 眼鏡 [5/6 場景]

【次要角色】(1-2 場景)
3. 子強 - 東亞男孩、開朗表情 [2/6 場景]
4. 老師 - 中年男性、運動外套 [2/6 場景]

📸 場景清單:
1. 起跑線前的壓力 - 緊張
2. 訓練時的委屈 - 不滿
...

是否繼續生成插圖? (yes/no/modify)
```

### 階段 2: 生成角色設定圖

確認規劃後，系統會先生成角色設定圖：

```
🎨 正在生成主角設定圖...
✅ character-sheet-main.png 已生成

請確認角色外觀是否符合預期？
```

### 階段 3: 生成場景插圖

確認角色設定圖後：
1. 使用設定圖作為參考，逐一生成場景插圖
2. 輸出 `characters.json` 和 `generation-summary.md`

## 參數說明

### 風格選項 (--style)

| 風格 | 說明 | 適用場景 |
|------|------|----------|
| `watercolor` | 溫暖柔和的水彩風格（預設）| 散文、文學 |
| `storybook` | 傳統繪本風格 | 兒童故事 |
| `ink-brush` | 東方水墨意境 | 古典文學 |
| `manga` | 日式漫畫風格 | 青少年故事 |
| `realistic` | 寫實細膩風格 | 歷史故事 |
| `minimalist` | 現代極簡風格 | 現代題材 |

### 語言選項 (--lang) ⭐ 新增

控制圖片中文字標籤的語言：

| 參數 | 說明 | 範例 |
|------|------|------|
| `EN` | 英文標籤（預設）| "Scene 1", "Zhengbin" |
| `TW` | 繁體中文標籤 | 「場景一」、「政彬」|

```bash
# 繁體中文標籤
/story-illustrator story.md --lang TW

# 英文標籤
/story-illustrator story.md --lang EN
```

### 目標讀者 (--audience)

| 參數 | 說明 |
|------|------|
| `children` | 兒童友善，色彩鮮豔（預設）|
| `teens` | 青少年向，現代感 |
| `adults` | 成人向，成熟細膩 |

### 其他選項

```bash
--plan-only              # 僅規劃不生圖
--skip-character-sheet   # 跳過角色設定圖（使用現有的）
--scenes 10              # 手動指定場景數量
--output ./images        # 指定輸出目錄
```

### 導演模式選項 ⭐ 新增

```bash
--storyboard             # 生成分鏡腳本（鏡頭、構圖、位置圖）
--emotion-tracking       # 生成情緒追蹤表和情緒曲線
--director-mode          # 完整導演模式（分鏡+情緒+轉場）
```

## 輸出文件

```
output/
├── character-sheet-main.png     # ⭐ 主角設定圖
├── character-sheet-support.png  # 配角設定圖（如需要）
├── characters.json              # 角色設定檔
├── scenes-plan.md               # 場景規劃文件
├── storyboard.md                # 📽️ 分鏡腳本（--storyboard）
├── emotion-tracking.md          # 💭 情緒追蹤（--emotion-tracking）
├── transitions.md               # 🔀 轉場建議（--director-mode）
├── scene-01.png                 # 場景插圖
├── scene-02.png
├── ...
└── generation-summary.md        # 生成摘要
```

## 角色一致性機制 ⭐ 核心功能

### 角色設定圖 (Character Sheet)

在生成場景圖之前，先生成角色設定圖作為視覺參考：

```
┌─────────────────────────────────────────┐
│  CHARACTER REFERENCE SHEET              │
│                                         │
│  ┌─────────┐      ┌─────────┐          │
│  │ 政彬    │      │ 名揚    │          │
│  │ (front) │      │ (front) │          │
│  └─────────┘      └─────────┘          │
│  ┌─────────┐      ┌─────────┐          │
│  │ (side)  │      │ (side)  │          │
│  └─────────┘      └─────────┘          │
│                                         │
│  Style: Storybook illustration          │
└─────────────────────────────────────────┘
```

### 特色附屬品 (Unique Accessory) ⭐ 新增

為每個主要角色設計一個容易辨識的附屬品，大幅提升跨場景一致性：

| 類型 | 範例 | 適合角色 |
|------|------|----------|
| 眼鏡 | rectangular glasses | 學生、知識分子 |
| 髮飾 | red hair ribbon, headband | 女孩、活潑角色 |
| 首飾 | pearl necklace, pendant | 優雅角色 |
| 手錶 | digital sports watch | 運動員 |
| 徽章 | class monitor badge | 學生幹部 |

**選擇原則**：
1. 優先從故事內容推斷（如：班長戴眼鏡）
2. 選擇視覺顯眼、AI 不易遺漏的物品
3. 符合角色個性和身份

### characters.json 範例

```json
{
  "settings": {
    "lang": "TW",
    "style": "storybook"
  },
  "main_characters": {
    "ZhengBin": {
      "name_zh": "政彬",
      "ethnicity": "East Asian",
      "age": "12-year-old boy",
      "hair": "short messy jet-black hair",
      "eyes": "dark brown eyes",
      "clothing": "blue and white athletic uniform with number 1",
      "unique_accessory": "red wristband on left wrist",
      "personality_visual": "determined, athletic",
      "scenes": [1, 2, 4, 5, 6]
    },
    "MingYang": {
      "name_zh": "名揚",
      "ethnicity": "East Asian",
      "age": "12-year-old boy",
      "hair": "short neat jet-black hair",
      "eyes": "dark brown eyes with rectangular glasses",
      "clothing": "blue and white athletic uniform with number 4",
      "unique_accessory": "rectangular glasses",
      "personality_visual": "confident, friendly class leader",
      "scenes": [2, 3, 4, 5, 6]
    }
  }
}
```

## 使用範例

### 範例 1: 兒童故事（繁體中文標籤）

```bash
/story-illustrator fairy-tale.md --style storybook --audience children --lang TW
```

### 範例 2: 青少年小說（英文標籤）

```bash
/story-illustrator teen-novel.md --style manga --audience teens --lang EN
```

### 範例 3: 文學作品

```bash
/story-illustrator classic-story.md --style watercolor --audience adults
```

### 範例 4: 完整導演模式 ⭐ 新增

```bash
/story-illustrator story.md --style storybook --director-mode --lang TW
```

輸出專業分鏡腳本、情緒追蹤表和轉場建議。

---

## 導演模式 ⭐ 新增

### 分鏡腳本 (--storyboard)

為每個場景生成專業分鏡設定：

```
場景 1: 起跑線前的壓力
├── 鏡頭類型: Medium Close-Up (中近景)
├── 鏡頭角度: Slightly Low Angle (輕微仰視)
├── 構圖: 三分法，主角置於左側
└── 角色位置圖:
    ┌─────────────────────┐
    │ [政彬]    跑道延伸→ │
    │  緊握接力棒         │
    └─────────────────────┘
```

### 情緒追蹤 (--emotion-tracking)

追蹤角色在每個場景的情緒變化：

```
角色: 政彬
場景 1: 緊張 (4/5) → 場景 2: 不滿 (5/5) → 場景 4: 慚愧 (4/5)
     → 場景 5: 堅定 (5/5) → 場景 6: 興奮 (5/5)

情緒曲線:
5 │    ●                 ●────●
4 │  ●   ╲             ╱
3 │       ╲    ●    ╱
1 │         ╲──────╱
  └──────────────────────────
    場景 1  2  3  4  5  6
```

### 轉場建議 (--director-mode)

分析場景之間的視覺連接：

```
場景 1 → 場景 2
├── 轉場類型: 時間回溯（回憶）
├── 視覺連接: 政彬的手 → 同場景的手
└── 色調變化: 明亮 → 褪色（回憶感）

場景 5 → 場景 6
├── 轉場類型: 動態連續
├── 視覺連接: 衝刺動態 → 擁抱靜態
└── 情緒對比: 緊張 → 釋放
```

---

## 進階使用

### 自訂角色描述

編輯生成的 `characters.json`，可調整：
- 角色外觀細節
- 特色附屬品
- 出場場景

### 跳過角色設定圖

如果已有滿意的角色設定圖：

```bash
/story-illustrator story.md --skip-character-sheet
```

### 擴展 Skill

創建 `story-illustrator/EXTEND.md`:

```markdown
# 自訂風格
- anime: 日式動畫風格，大眼睛、鮮豔色彩

# 預設附屬品
- 學生角色: 眼鏡或髮帶
- 運動員: 護腕或頭帶
```

## 故障排除

### 問題: 角色外觀不一致

**解決方法**:
1. 確保使用角色設定圖作為參考
2. 為每個主角設計明顯的**特色附屬品**
3. 在提示詞中強調附屬品：`WEARING GLASSES (identifying feature)`
4. 選擇 AI 不易遺漏的附屬品（眼鏡 > 小徽章）

### 問題: 圖片中文字是英文

**解決方法**:
```bash
/story-illustrator story.md --lang TW
```

### 問題: 場景選擇不合適

**解決方法**:
1. 使用 `--plan-only` 先查看規劃
2. 手動調整場景數量 `--scenes N`
3. 編輯 `scenes-plan.md` 替換場景

### 問題: 圖片生成失敗

**解決方法**:
1. 檢查是否有可用的圖片生成工具
2. 查看 `generation-summary.md` 中的 prompt
3. 可以手動使用 prompt 在其他工具生成

## 技術架構

```
story-illustrator/
├── SKILL.md              # 主 skill 定義和工作流程
├── character-guide.md    # 角色一致性詳細指南
├── scene-analyzer.md     # 場景分析算法和規則
├── storyboard-guide.md   # ⭐ 分鏡腳本指南（新增）
├── example-characters.json  # 角色檔案範例
├── example-scenes-plan.md   # 場景規劃範例
├── INSTALL.md            # 安裝指南
└── README.md             # 本文件
```

### 核心組件

1. **場景分析器** (`scene-analyzer.md`)
   - 識別場景切換信號
   - 評分和排序場景
   - 生成場景規劃

2. **角色管理器** (`character-guide.md`)
   - 提取角色特徵
   - 設計特色附屬品
   - 建立一致性模板

3. **分鏡導演** (`storyboard-guide.md`) ⭐ 新增
   - 鏡頭類型與角度設定
   - 角色情緒追蹤
   - 場景轉場建議

4. **圖片生成器** (`SKILL.md`)
   - 生成角色設定圖
   - 調用生圖工具
   - 輸出摘要報告

## 限制

- 依賴外部圖片生成工具（Gemini / DALL-E / Stable Diffusion）
- AI 生成圖片可能存在不一致性（使用角色設定圖可大幅改善）
- 複雜場景可能需要多次調整
- 建議生成後人工檢查品質

## 常見問題

**Q: 為什麼需要角色設定圖？**

A: 角色設定圖作為視覺參考，讓 AI 在生成場景圖時有明確的角色外觀依據，大幅提升一致性。

**Q: 什麼是特色附屬品？**

A: 為角色添加一個容易辨識的物品（如眼鏡、髮帶），讓 AI 更容易在不同場景中維持角色的辨識度。

**Q: --lang TW 和 --lang EN 有什麼差別？**

A: 控制圖片中的文字標籤語言。TW 會顯示繁體中文（如「政彬」），EN 會顯示英文（如 "Zhengbin"）。

**Q: 可以用在商業用途嗎？**

A: 取決於你使用的圖片生成工具的授權條款。

**Q: 能處理多長的文章？**

A: 建議 200-3000 字。太短場景不足，太長建議分段處理。

**Q: 圖片品質如何保證？**

A: 這個 skill 專注於「規劃」和「一致性」，最終品質取決於使用的圖片生成工具。建議：
- 使用高品質的生圖工具
- 善用角色設定圖和特色附屬品
- 人工檢查和調整
- 必要時重新生成個別場景

## 更新日誌

### v1.2.0 (2026-01)
- ⭐ 新增「分鏡腳本」功能 (`--storyboard`)
  - 鏡頭類型：遠景、中景、近景、特寫等
  - 鏡頭角度：平視、俯視、仰視等
  - 構圖建議：三分法、中心構圖等
  - 角色位置圖
- ⭐ 新增「情緒追蹤」功能 (`--emotion-tracking`)
  - 角色情緒變化表
  - 情緒曲線視覺化
  - 情緒轉折點標記
- ⭐ 新增「轉場建議」功能 (`--director-mode`)
  - 場景間視覺連接
  - 轉場類型建議
  - 色調變化建議
- 新增 `storyboard-guide.md` 完整指南

### v1.1.0 (2026-01)
- ⭐ 新增 `--lang TW/EN` 語言參數，控制圖片文字語言
- ⭐ 新增「特色附屬品」(Unique Accessory) 機制，提升角色辨識度
- 更新 characters.json 格式，新增 `settings` 和 `unique_accessory` 欄位
- 改進角色設定圖生成流程

### v1.0.0
- 初始版本
- 場景分析與規劃
- 角色一致性管理
- 多風格支援

## 授權

MIT License
