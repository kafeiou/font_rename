# Design

## Context

目前專案已具備 `openspec/` 預設目錄結構與 `.agents/skills/` 技能定義，但 `openspec/config.yaml` 僅包含預設註解，且尚未建立 `.agents/AGENTS.md`。動機與背景請見 `proposal.md`。

## Goals / Non-Goals

**Goals:**
- 於 `.agents/AGENTS.md` 建立結構化的專案七大鐵律。
- 於 `openspec/config.yaml` 寫入明確的 `context` 與 `rules` 設定，確保後續 OpenSpec 指令自動套用專案背景與繁體中文規範。

**Non-Goals:**
- 不修改現有的 Python 字型處理腳本（`auto_generate_mapping.py`、`rename_font.py`、`view_font_info.py`）。

## Decisions

- **集中式代理規範路徑（`.agents/AGENTS.md`）**：專案已存在 `.agents/skills/`，將 `AGENTS.md` 放置於 `.agents/` 目錄下可與現有技能目錄保持一致，並防止工具誤建單數 `.agent/` 目錄。
- **OpenSpec 雙層語言約束（`context` + `rules`）**：同時在 `openspec/config.yaml` 的全域 `context` 與各別 `rules`（`proposal`、`tasks`、`specs`）宣告繁體中文（`zh-TW`）要求，確保不論代理讀取全域背景或單一產出物規則皆能強制套用繁體中文。

## Risks / Trade-offs

- [既有註解覆蓋] → `openspec/config.yaml` 原先僅有預設範例註解，直接覆寫為正式設定可提升可讀性且不影響既有功能。
