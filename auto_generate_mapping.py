# -*- coding: utf-8 -*-
import os
from fontTools.ttLib import TTFont, TTCollection

# 設定來源目錄名稱
SOURCE_DIR = "font_source"

def is_chinese(text):
    """檢查字串是否包含中文字"""
    return any('\u4e00' <= char <= '\u9fff' for char in text)

def clean_string(text):
    """清理字串，移除不可見字元與前後空白"""
    if not text:
        return ""
    # 移除一些常見的控制字元或無效字元
    return "".join(c for c in text if c.isprintable()).strip()

def get_best_name_and_keyword(font_obj):
    """從字型中挑選出合法的微軟 Windows 平台中英文名稱，徹底過濾亂碼"""
    chinese_name = None
    english_name = None
    target_keyword = None
    name_table = font_obj['name']
    
    for record in name_table.names:
        # 核心防禦：只處理 Microsoft 平台 (Platform ID = 3) 且為 Unicode 格式的紀錄
        # 這樣可以徹底避開造成亂碼的舊版 Mac (ID 1) 或特定 Big5 非標準編碼
        if record.platformID == 3:
            if record.nameID == 1: # Family Name (字型家族名稱)
                try:
                    name_str = clean_string(record.toUnicode())
                    if not name_str:
                        continue
                        
                    if is_chinese(name_str):
                        # 優先選用沒有奇怪符號、字數合理的中文名稱
                        if not chinese_name or (len(name_str) < len(chinese_name)):
                            chinese_name = name_str
                    else:
                        if not english_name:
                            english_name = name_str
                except Exception:
                    pass
                    
    # 決定 final 顯示名稱
    final_name = chinese_name if chinese_name else (english_name if english_name else "Unknown_Font")
    
    # 決定用來做唯一比對的關鍵字（優先選英文，避免對照檔本身產生編碼衝突）
    target_keyword = english_name if english_name else final_name
    
    return final_name, target_keyword

def generate_config():
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ 找不到來源資料夾: [{SOURCE_DIR}]，請先建立它並放入原始字型。")
        return

    font_files = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith(('.ttf', '.ttc'))]
    if not font_files:
        print(f"❌ 資料夾 [{SOURCE_DIR}] 內找不到任何 .ttf 或 .ttc 檔案！")
        return

    output_lines = [
        "# -*- coding: utf-8 -*-",
        "# 這是經過精細防禦過濾後自動生成的字型設定檔",
        "FONT_MAPPING = {"
    ]

    print(f"🔍 開始進行防禦性分析，掃描 [{SOURCE_DIR}] 中的字型...")
    
    for file_name in font_files:
        file_path = os.path.join(SOURCE_DIR, file_name)
        _, ext = os.path.splitext(file_name)
        ext = ext.lower()
        
        try:
            if ext == ".ttc":
                collection = TTCollection(file_path)
                output_lines.append(f"    # --- 集合字型 {file_name} (內含 {len(collection.fonts)} 個子字型) ---")
                
                for idx, font in enumerate(collection.fonts):
                    best_name, target_keyword = get_best_name_and_keyword(font)
                    
                    output_lines.append(f'    "{file_name}#{idx}": {{')
                    output_lines.append(f'        "only_target": "{target_keyword}",')
                    output_lines.append(f'        "to_name": "{best_name}"')
                    output_lines.append(f'    }},')
            else:
                font = TTFont(file_path)
                best_name, _ = get_best_name_and_keyword(font)
                output_lines.append(f'    "{file_name}": "{best_name}",')
                
            print(f"✅ 分析完成 (已過濾潛在亂碼): {file_name}")
        except Exception as e:
            print(f"❌ 分析 {file_name} 失敗: {str(e)}")

    output_lines.append("}")
    
    with open("font_mapping_config.py", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
        
    print("=" * 60)
    print(f"🎉 乾淨的設定檔已自動生成：[font_mapping_config.py]")
    print(f"🚀 現在您可以直接執行 `python rename_font.py` 來進行無亂碼的高壓字型改名了！")

if __name__ == "__main__":
    generate_config()
