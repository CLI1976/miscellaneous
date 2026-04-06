# 簡體中文轉繁體中文轉換 Skill

## 描述
將簡體中文文件轉換為繁體中文（台灣用語）。支援多種檔案格式。

## 觸發條件
當用戶要求進行以下操作時使用此 skill：
- 簡轉繁、簡體轉繁體
- 將簡體中文檔案轉換為繁體
- s2t、s2tw、s2twp 轉換

## 支援的檔案格式
- `.md` - Markdown 文件
- `.txt` - 純文字檔
- `.html` / `.htm` - HTML 網頁
- `.docx` - Word 文件 (Office 2007+)
- `.xml` / `.json` / `.csv` - 其他文字格式

**注意**: 不支援舊版 `.doc` 格式，請先轉換為 `.docx`

## 使用方式

### 基本用法
```bash
python "C:\Users\xray\.claude\skills\s2t-converter\convert.py" "<檔案路徑>"
```

### 指定輸出檔案
```bash
python "C:\Users\xray\.claude\skills\s2t-converter\convert.py" "<輸入檔案>" -o "<輸出檔案>"
```

### 轉換模式選項
使用 `-c` 參數指定轉換模式：
- `s2t` - 簡體到繁體（基本字元轉換）
- `s2tw` - 簡體到台灣繁體
- `s2twp` - 簡體到台灣繁體 + 慣用詞轉換（預設，推薦）
  - 例如：「軟件」→「軟體」、「內存」→「記憶體」
- `s2hk` - 簡體到香港繁體

```bash
python "C:\Users\xray\.claude\skills\s2t-converter\convert.py" "<檔案>" -c s2hk
```

## 輸出規則
- 預設輸出檔名：`原檔名_tc.副檔名`
- 例如：`readme.md` → `readme_tc.md`
- 輸出編碼統一為 UTF-8

## 執行流程
1. 確認輸入檔案存在
2. 執行轉換命令
3. 回報轉換結果和輸出檔案路徑

## 範例

### 轉換單一 Markdown 檔案
```bash
python "C:\Users\xray\.claude\skills\s2t-converter\convert.py" "C:\docs\readme.md"
# 輸出: C:\docs\readme_tc.md
```

### 轉換 Word 文件並指定輸出
```bash
python "C:\Users\xray\.claude\skills\s2t-converter\convert.py" "report.docx" -o "report_traditional.docx"
```

### 使用香港繁體轉換
```bash
python "C:\Users\xray\.claude\skills\s2t-converter\convert.py" "article.txt" -c s2hk
```

## 錯誤處理
- 如果檔案不存在，會顯示錯誤訊息
- 如果是不支援的 `.doc` 格式，提示用戶先轉換為 `.docx`
- 如果編碼無法識別，會嘗試多種常見編碼（UTF-8、GBK、GB2312、Big5）

## 依賴套件
如果執行時出現套件錯誤，請安裝：
```bash
pip install opencc-python-reimplemented python-docx
```
