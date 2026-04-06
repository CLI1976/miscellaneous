# Character Consistency Guide - 角色一致性指南

確保多張插圖中角色外觀保持一致的指導原則。

## 核心原則

**關鍵理念**：每次生成圖片時，必須使用**完全相同**的角色描述。

## 角色特徵清單

### 必須定義的屬性

每個角色必須明確以下特徵：

#### 1. 頭髮 (Hair)
- **顏色**: red, black, blonde, brown, grey, white
- **長度**: long, short, shoulder-length, waist-length
- **樣式**: braided, ponytail, bun, loose, curly, straight
- **範例**: "red hair in two long braids"

#### 2. 臉部 (Face)
- **眼睛顏色**: green, blue, brown, hazel
- **臉型**: round, oval, angular
- **特徵**: freckles, dimples, distinctive features
- **範例**: "bright green eyes, round face with freckles"

#### 3. 身材 (Build)
- **年齡**: child (5-12), teen (13-17), young adult, middle-aged, elderly
- **體型**: slim, sturdy, petite, tall
- **範例**: "slim young girl, about 11 years old"

#### 4. 衣著 (Clothing)
- **風格**: Victorian dress, modern casual, traditional
- **顏色**: 主要顏色
- **特徵**: 標誌性配件
- **範例**: "simple grey Victorian dress with white collar"

#### 5. 個性特質 (在表情中體現)
- **常見表情**: cheerful, serious, gentle, energetic
- **姿態**: confident, shy, animated
- **範例**: "energetic and expressive demeanor"

#### 6. 特色附屬品 (Unique Accessory) ⭐ 新增
- **目的**: 大幅提升角色辨識度，確保跨場景一致性
- **類型**: 眼鏡、髮飾、首飾、手錶、帽子、徽章、運動配件
- **選擇原則**:
  - 優先從故事內容推斷（如：班長戴眼鏡）
  - 選擇視覺顯眼、不易遺漏的物品
  - 符合角色個性和身份
- **範例**:
  - "rectangular glasses" (眼鏡)
  - "red ribbon hair ties" (紅色髮帶)
  - "digital sports watch on left wrist" (運動手錶)
  - "pearl pendant necklace" (珍珠項鍊)
  - "class monitor badge on chest" (班長徽章)

## 角色檔案格式

### JSON 格式

```json
{
  "角色名稱": {
    "description_template": "完整英文描述模板",
    "hair": "髮型描述",
    "eyes": "眼睛描述",
    "face": "臉部特徵",
    "build": "身材描述",
    "clothing": "衣著描述",
    "unique_accessory": "特色附屬品（增加辨識度）",
    "personality": "個性表現",
    "age_group": "年齡群組",
    "distinctive_features": "獨特特徵"
  }
}
```

### 完整範例

```json
{
  "安妮": {
    "description_template": "Anne: A slim young girl (11 years old) with distinctive red hair styled in two long braids tied with GREEN RIBBONS (identifying feature), bright green eyes, round freckled face, wearing a simple grey Victorian dress with white collar, energetic and expressive demeanor",
    "hair": "distinctive red hair in two long braids",
    "eyes": "bright green eyes",
    "face": "round face with freckles",
    "build": "slim young girl, about 11 years old",
    "clothing": "simple grey Victorian dress with white collar",
    "unique_accessory": "green ribbon hair ties on braids",
    "personality": "energetic and expressive",
    "age_group": "child",
    "distinctive_features": "red braided hair, freckles, green ribbons"
  },
  "戴安娜": {
    "description_template": "Diana: A young girl (11 years old) with neat black hair styled in a refined way, dark eyes, elegant features, wearing PEARL PENDANT NECKLACE (identifying feature), well-made Victorian clothing in dark colors, composed and graceful posture",
    "hair": "neat black hair in a refined style",
    "eyes": "dark brown eyes",
    "face": "elegant features, smooth complexion",
    "build": "young girl, about 11 years old, graceful posture",
    "clothing": "well-made Victorian dress in dark blue or burgundy colors",
    "unique_accessory": "pearl pendant necklace",
    "personality": "composed and elegant",
    "age_group": "child",
    "distinctive_features": "refined appearance, dark hair, pearl necklace"
  },
  "瑪麗亞": {
    "description_template": "Marilla: A middle-aged woman (50s) with grey hair pulled back in a strict bun, stern but kind grey-blue eyes, angular face with defined features, wearing SMALL CAMEO BROOCH at collar (identifying feature), practical Victorian dress in dark grey or black, upright and proper posture",
    "hair": "grey hair in a strict bun",
    "eyes": "stern but kind grey-blue eyes",
    "face": "angular face with defined features",
    "build": "middle-aged woman, upright posture",
    "clothing": "practical Victorian dress in dark grey or black with high collar",
    "unique_accessory": "small cameo brooch at collar",
    "personality": "stern but caring",
    "age_group": "middle-aged",
    "distinctive_features": "grey hair bun, stern expression, cameo brooch"
  }
}
```

## 提示詞組裝規則

### 基本結構

```
A [style] illustration showing [scene action].

Characters visible in this scene:
- [Character 1 name]: [COMPLETE description_template from JSON]
- [Character 2 name]: [COMPLETE description_template from JSON]

Setting: [環境描述]
Mood: [情緒基調]
Lighting: [光線]
Composition: [構圖]
Art style: [風格], suitable for [目標讀者]
```

### ⚠️ 重要規則

1. **完整複製角色描述**
   - 每次都使用完整的 `description_template`
   - 不要省略任何細節
   - 不要改寫或簡化

2. **只描述出現的角色**
   - 如果場景中沒有某角色，不要提及
   - 但其他場景中該角色必須用同樣描述

3. **保持描述順序一致**
   - 始終按照相同順序排列特徵
   - 例如：髮型 → 眼睛 → 臉型 → 衣著

## 實際應用範例

### 場景 1: 兩人下午茶

```
A warm watercolor illustration of two girls having afternoon tea in a Victorian cottage.

Characters visible in this scene:
- Anne: A slim young girl (11 years old) with distinctive red hair styled in two long braids, bright green eyes, round freckled face, wearing a simple grey Victorian dress with white collar, energetic and expressive demeanor
- Diana: A young girl (11 years old) with neat black hair styled in a refined way, dark eyes, elegant features, wearing well-made Victorian clothing in dark blue, composed and graceful posture

Setting: Cozy Victorian cottage interior, wooden table with tea set and cakes, autumn maple leaves visible through window
Mood: Warm, cheerful, friendly atmosphere
Lighting: Soft afternoon sunlight streaming through windows
Composition: Both girls seated at table, facing each other
Art style: Watercolor children's book illustration with soft colors and gentle details
```

### 場景 5: 安妮獨自道歉

```
A watercolor illustration of a girl apologizing at a doorway in winter.

Characters visible in this scene:
- Anne: A slim young girl (11 years old) with distinctive red hair styled in two long braids, bright green eyes, round freckled face, wearing a simple grey Victorian dress with white collar and winter coat, tearful and remorseful expression

Setting: Victorian house doorway, snow falling outside, warm interior light from inside
Mood: Melancholic, emotional, sincere
Lighting: Cold blue winter light outside, warm golden light from door
Composition: Anne standing at threshold, looking up earnestly
Art style: Watercolor children's book illustration with emotional depth
```

## 角色演變處理

如果故事中角色外觀有變化（換衣服、長大、受傷）：

### 方案 1: 創建變體
```json
"安妮-冬裝": {
  "base": "安妮",
  "clothing": "winter coat over grey dress, wool scarf"
}
```

### 方案 2: 添加狀態說明
```
Anne: [原有描述], currently wearing a winter coat and looking tired after the emergency
```

## 常見錯誤

### ❌ 錯誤做法

1. **描述不完整**
```
Anne: red-haired girl
Diana: black-haired girl
```

2. **每次描述不同**
```
場景1: Anne with red braids
場景2: Anne, a redhead
場景3: red-haired Anne
```

3. **省略關鍵特徵**
```
Anne: young girl in Victorian dress
(遺漏了紅髮、辮子、綠眼睛、雀斑)
```

### ✅ 正確做法

**每次都用完整的標準描述**：
```
Anne: A slim young girl (11 years old) with distinctive red hair styled in two long braids, bright green eyes, round freckled face, wearing a simple grey Victorian dress with white collar, energetic and expressive demeanor
```

## 品質檢查清單

生成插圖前確認：

- [ ] 所有角色都有完整的 description_template
- [ ] 每個特徵都具體且可視覺化
- [ ] 角色之間有明確區別
- [ ] 衣著符合故事時代/背景
- [ ] 年齡描述準確
- [ ] 個性特質可通過表情/姿態體現
- [ ] **主要角色都有設計特色附屬品 (unique_accessory)** ⭐
- [ ] **附屬品在 description_template 中有標註 (identifying feature)** ⭐

## 調試技巧

如果角色不一致：

1. **檢查 description_template**
   - 是否每次完整複製？
   - 是否有意外修改？

2. **強化特色附屬品** ⭐
   - 確保每個主角都有明顯的附屬品
   - 在提示詞中使用大寫或括號強調：`WEARING RECTANGULAR GLASSES (identifying feature)`
   - 選擇 AI 不容易遺漏的物品（眼鏡、頭飾比小徽章更可靠）

3. **增加獨特特徵**
   - 添加更明顯的視覺標記
   - 例如：特殊配件、髮飾、標誌性姿勢

4. **簡化描述**
   - 如果 AI 理解困難，簡化複雜特徵
   - 但保持核心特徵和附屬品不變

5. **使用參考圖**
   - 第一張圖最關鍵
   - 可以在提示詞中加入 "consistent with previous illustrations"
   - 確保參考圖中的附屬品清晰可見

## 特色附屬品選擇指南 ⭐ 新增

### 按可靠度排序（AI 生圖時的穩定性）

| 可靠度 | 附屬品類型 | 範例 |
|--------|-----------|------|
| ⭐⭐⭐ 高 | 眼鏡 | rectangular glasses, round glasses |
| ⭐⭐⭐ 高 | 頭飾 | headband, hair ribbon, hat |
| ⭐⭐ 中 | 明顯首飾 | large pendant necklace, earrings |
| ⭐⭐ 中 | 手錶 | sports watch, wristwatch |
| ⭐ 低 | 小型配件 | small badge, pin, bracelet |

### 推薦組合

- **學生角色**: 眼鏡 + 髮型特徵
- **運動員**: 護腕/頭帶 + 號碼
- **優雅角色**: 項鍊 + 髮飾
- **領導角色**: 眼鏡 + 徽章
