# 🛠️ ONLYOFFICE 字型名稱批次中文化工具

本工具專門用於解決 **ONLYOFFICE Docs** 無法正確識別 `.ttc` (字型集合檔) 或預設優先顯示字型英文名稱（如將「新細明體」顯示為 `PMingLiU`）的問題。透過修改字型內部的元數據（Name Table ID 1 & 4），強迫 ONLYOFFICE 只能讀取到正確的中文顯示名稱。

---

## 📂 專案目錄結構

請確保你的資料夾結構長這樣（`font_source` 需手動建立）：

```text
字型專案/
├── font_source/            <-- 📥 【手動建立】放你想要修改的原始 .ttf 或 .ttc 檔案
├── font_convert/           <-- 📤 【自動生成】轉換完成、乾淨的字型檔案會輸出在這裡
├── auto_generate_mapping.py <-- 🔍 步驟 1：自動掃描來源並產生設定檔
├── rename_font.py           <-- 🚀 步驟 3：自動讀取設定並執行字型改名
├── view_font_info.py        <-- 📊 輔助工具：檢視原始字型的內部中英文家族名稱
├── requirements.txt         <-- 📦 Python 套件依賴清單
└── README.md                <-- 📄 本說明文件
```

---

## 📦 安裝與準備工作

本工具基於 Python 開發，核心依賴強大的字型處理庫 `fonttools`。

### 1. 安裝 Python
請確保你的電腦或 Docker 容器內已安裝 **Python 3.8 或以上版本**。
* **Windows**: 可至官網下載安裝，安裝時請務必勾選 "Add Python to PATH"。
* **Linux/Ubuntu**: `sudo apt update && sudo apt install python3 python3-pip -y`

### 2. 安裝必要套件
打開終端機（CMD 或 Bash），切換到本專案目錄下，執行以下指令安裝套件：
```bash
pip install -r requirements.txt
```

### 3. 放入原始字型
手動建立 `font_source` 資料夾，並把你想要調整的微軟正黑體、新細明體、標楷體或宋體（`.ttf` 或 `.ttc` 檔）全部丟進去。

---

## 🚀 三步自動化操作流程

### 步驟 1：自動掃描並產生設定檔
執行以下指令，程式會自動去 `font_source` 撈取檔案，並在根目錄自動產生 `font_mapping_config.py` 設定檔：
```bash
python auto_generate_mapping.py
```

### 步驟 2：自訂與校對字型名稱（選用）
用文字編輯器（如 Notepad++、VS Code 或記事本）打開新產生的 **`font_mapping_config.py`**：
* 程式會自動幫你抓取該字型在系統中合適的中文名稱。
* **客製化修改**：如果你想把名稱改掉（例如把「MingLiU」改為「細明體（舊字形）」），直接修改檔案中 `"to_name": "你的新名字"` 的欄位並存檔即可。
* ⚠️ *注意：同一個 TTC 檔案內部的多個子字型，請盡量給予不同的 `to_name`，避免 ONLYOFFICE 發生覆蓋衝突。*

### 步驟 3：一鍵執行字型轉換
確認設定無誤後，直接執行核心轉換程式：
```bash
python rename_font.py
```
程式會自動載入剛剛的設定檔，精準修改字型內部的名稱，並以**原檔名**輸出到 `font_convert` 資料夾中。

---

## 📊 輔助工具：如何肉眼檢視字型詳細結構？
如果你不確定某個字型內部到底包了什麼、有哪些中英文名字，你可以執行：
```bash
python view_font_info.py
```
它會直接印出 `font_source` 裡所有字型的內部 Name ID 1（字型家族）與 Name ID 4（完整名稱）的所有語言版本，方便你進行排錯或核對。

---

## 🐳 如何部署到 Docker ONLYOFFICE 容器內？

當你順利在 `font_convert` 中取得洗完檔名的字型後，請依照以下步驟讓 ONLYOFFICE 生效：

1. **清除舊快取**（在 ONLYOFFICE 容器內執行）：
   ```bash
   rm -rf /var/www/onlyoffice/documentserver/fonts/*
   ```
2. **複製新字型**：將 `font_convert` 內的所有檔案，複製到 ONLYOFFICE 容器掛載的字型目錄（通常為 `/usr/share/fonts/truetype/custom/`）。
3. **重新全域生成字型快取**（在 ONLYOFFICE 容器內執行）：
   ```bash
   /usr/bin/documentserver-generate-allfonts.sh
   ```
4. **重啟服務**（在 ONLYOFFICE 容器內執行）：
   ```bash
   supervisorctl restart all
   ```
5. **瀏覽器端**：如果是 Docs 8.1.3 或更舊版本，請務必在前端頁面按下 `Ctrl + F5` 強制清除瀏覽器快取，全新的中文選單即會正確顯示！
