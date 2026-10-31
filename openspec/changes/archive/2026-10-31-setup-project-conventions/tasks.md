# Tasks

## 1. 建立代理鐵律規範檔

- [x] 1.1 建立 `.agents/AGENTS.md` 並寫入七大專案鐵律（目錄規範、執行前確認、嚴格的版本控制、非同步任務同步、防呆與錯誤處理、流程圖文件化、自動同步主文件），完成後讀取檔案驗證內容完整性且確認專案根目錄下不存在單數 `.agent/` 目錄

## 2. 更新 OpenSpec 專案設定檔

- [x] 2.1 更新 `openspec/config.yaml`，填入專案名稱 `font_rename (ONLYOFFICE 字型名稱批次中文化工具)`、技術棧 `Python 3.8+`、開發慣例與繁體中文（`zh-TW`）規範及 `proposal`、`tasks`、`specs` 規則，完成後執行 `openspec status --change "setup-project-conventions"` 驗證設定檔語法有效且能正常解析
