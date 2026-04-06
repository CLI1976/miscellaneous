# Story Illustrator - 安裝指南

## 快速安裝

### Windows

```powershell
# 1. 複製整個 story-illustrator 文件夾到 Claude 目錄
Copy-Item -Recurse story-illustrator "$env:USERPROFILE\.claude\skills\"

# 2. 驗證安裝
Test-Path "$env:USERPROFILE\.claude\skills\story-illustrator\SKILL.md"
# 應該輸出 True
```

### macOS / Linux

```bash
# 1. 複製整個 story-illustrator 文件夾到 Claude 目錄
cp -r story-illustrator ~/.claude/skills/

# 2. 驗證安裝
ls ~/.claude/skills/story-illustrator/SKILL.md
# 應該顯示文件路徑
```

---

## 驗證安裝

在 Claude Code 中執行：

```bash
/skills
```

你應該會看到 `story-illustrator` 出現在列表中。

---

## 測試運行

創建一個測試故事文件：

```bash
echo "小明去公園玩。他看到一隻小狗。他們成為了好朋友。" > test-story.md
```

執行測試：

```bash
/story-illustrator test-story.md --plan-only
```

應該會看到場景規劃報告。

---

## 文件結構說明

安裝後的目錄結構：

```
~/.claude/skills/story-illustrator/
├── SKILL.md                      # 主 skill 定義 ⭐ 必需
├── character-guide.md            # 角色一致性指南
├── scene-analyzer.md             # 場景分析規則
├── storyboard-guide.md           # 分鏡/情緒/轉場指南 ⭐ 新增
├── README.md                     # 使用說明
├── SUMMARY.md                    # 快速總結
├── example-characters.json       # 範例角色檔案
└── example-scenes-plan.md        # 範例場景規劃
```

**只有 SKILL.md 是必需的**，其他文件是參考資料。

---

## 依賴需求

### 圖片生成工具（可選）

此 skill 需要圖片生成能力，支援以下選項：

#### 選項 1: Claude.ai 內建（推薦）
- 在 claude.ai 對話中自動可用
- 無需額外設定

#### 選項 2: Gemini Web API
- 需要安裝 baoyu-gemini-web skill
- 參考 baoyu-skills 安裝說明

#### 選項 3: 其他 MCP 插件
- DALL-E
- Stable Diffusion
- Midjourney

#### 選項 4: 僅生成提示詞
- 即使沒有圖片生成工具
- Skill 仍可輸出完整的提示詞文件
- 你可以手動使用這些提示詞生成圖片

---

## 配置選項

### 自訂風格（可選）

創建 `story-illustrator/EXTEND.md`:

```markdown
# 自訂風格定義

## 新風格: anime
- 日式動畫風格
- 大眼睛、鮮豔色彩
- 提示詞加入: "anime style, vibrant colors, expressive eyes"

## 新風格: sketch
- 鉛筆素描風格
- 黑白或淺色
- 提示詞加入: "pencil sketch, hand-drawn, monochrome or light shading"
```

### 調整場景判斷規則（進階）

編輯 `scene-analyzer.md` 中的評分權重：

```markdown
### 評分權重
- 視覺性: 30% → 40% (增加視覺優先級)
- 重要性: 40% → 30%
- 情感強度: 20% → 20%
- 代表性: 10% → 10%
```

---

## 疑難排解

### 問題 1: Skill 未顯示

**檢查**:
```bash
# 確認文件位置
ls ~/.claude/skills/story-illustrator/SKILL.md
```

**解決**:
- 確保文件夾名稱正確（小寫，連字符）
- 重啟 Claude Code

### 問題 2: 無法生成圖片

**可能原因**:
1. 沒有可用的圖片生成工具
2. API 密鑰未設定
3. 網路問題

**解決**:
1. 使用 `--plan-only` 先查看規劃
2. 檢查 MCP 插件狀態
3. 手動使用輸出的提示詞生成圖片

### 問題 3: 角色不一致

**檢查**:
- 查看生成的 `characters.json`
- 確認 description_template 是否完整

**解決**:
- 手動編輯 `characters.json` 增加細節
- 重新生成相關場景

---

## 更新

### 更新到新版本

```bash
# 備份現有配置（如有自訂）
cp ~/.claude/skills/story-illustrator/EXTEND.md ~/story-illustrator-extend-backup.md

# 刪除舊版本
rm -rf ~/.claude/skills/story-illustrator

# 安裝新版本
cp -r story-illustrator ~/.claude/skills/

# 恢復自訂配置
cp ~/story-illustrator-extend-backup.md ~/.claude/skills/story-illustrator/EXTEND.md
```

---

## 卸載

```bash
# 刪除 skill
rm -rf ~/.claude/skills/story-illustrator

# 驗證刪除
ls ~/.claude/skills/story-illustrator
# 應該顯示: No such file or directory
```

---

## 獲取幫助

如果遇到問題：

1. **查看文檔**:
   - README.md - 使用說明
   - SKILL.md - 完整工作流程
   - character-guide.md - 角色一致性指南
   - scene-analyzer.md - 場景分析規則

2. **查看範例**:
   - example-characters.json - 角色檔案範例
   - example-scenes-plan.md - 完整規劃範例

3. **測試運行**:
   ```bash
   /story-illustrator test-story.md --debug
   ```

---

## 下一步

安裝完成後，建議：

1. **閱讀 README.md** - 了解基本使用
2. **查看範例文件** - 理解輸出格式
3. **測試簡單故事** - 熟悉工作流程
4. **調整配置** - 根據需求自訂

祝使用愉快！🎨
