# Proposal

## Why

目前 `font_rename (ONLYOFFICE 字型名稱批次中文化工具)` 專案尚未建立明確的 AI 代理操作鐵律與 OpenSpec 專案層級規範。為確保所有代理協作遵循統一目錄結構、執行前確認、版本控制及繁體中文文件規範，需建立基礎規範設定。

## What Changes

- 新增 `.agents/AGENTS.md`：定義專案七大鐵律（目錄規範、執行前確認、嚴格的版本控制、非同步任務同步、防呆與錯誤處理、流程圖文件化、自動同步主文件）。
- 更新 `openspec/config.yaml`：設定專案背景資訊（專案名稱 `font_rename (ONLYOFFICE 字型名稱批次中文化工具)`、技術棧 `Python 3.8+`、開發慣例與繁體中文撰寫要求）以及各產出物（`proposal`、`tasks`、`specs`）的語言規範。

## Capabilities

### New Capabilities
- `project-governance`: 規範專案內 AI 代理協作行為（`.agents/AGENTS.md`）與 OpenSpec 規格驅動開發設定（`openspec/config.yaml`）。

### Modified Capabilities
<!-- 無既有規格變更 -->

## Impact

- 新增檔案：`.agents/AGENTS.md`
- 修改檔案：`openspec/config.yaml`
- 影響範圍：專案內所有 AI 代理工作流與後續產出的 OpenSpec 規劃文件（不影響既有 Python 字型轉換程式碼）。
