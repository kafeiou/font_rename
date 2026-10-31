# -*- coding: utf-8 -*-
import os
from fontTools.ttLib import TTFont, TTCollection

# ==============================================================================
# ⚙️ 目錄設定
# ==============================================================================
SOURCE_DIR = "font_source"     # 統一從來源字型目錄讀取

def is_chinese(text):
    """檢查字串是否包含中文字"""
    return any('\u4e00' <= char <= '\u9fff' for char in text)

def get_font_names_clean(font_obj):
    """提取並精簡字型名稱，合併重複項目並分類中英文"""
    zh_names = set()
    en_names = set()
    name_table = font_obj['name']
    
    for record in name_table.names:
        # 只抓取字型家族(1)與完整名稱(4)
        if record.nameID == 1 or record.nameID == 4:
            try:
                name_str = record.toUnicode().strip()
                if not name_str:
                    continue
                # 依照是否包含中文進行歸類
                if is_chinese(name_str):
                    zh_names.add(name_str)
                else:
                    en_names.add(name_str)
            except Exception:
                pass
                
    return sorted(list(zh_names)), sorted(list(en_names))

def check_all_fonts_in_dir():
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ 錯誤：找不到來源資料夾: [{SOURCE_DIR}]")
        return

    print(f"🔍 開始掃描資料夾 [{SOURCE_DIR}] 中的字型檔案...\n" + "="*70)
    
    font_files = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith(('.ttf', '.ttc'))]
    
    if not font_files:
        print(f"❌ 資料夾 [{SOURCE_DIR}] 內找不到任何 .ttf 或 .ttc 檔案！")
        return

    for file_name in font_files:
        print(f"\n📦 檔案名稱: {file_name}")
        file_path = os.path.join(SOURCE_DIR, file_name)
        _, ext = os.path.splitext(file_name)
        ext = ext.lower()
        
        try:
            if ext == ".ttc":
                collection = TTCollection(file_path)
                print(f"   📊 檔案類型: TTC (字型集合檔)，內含 {len(collection.fonts)} 個子字型：")
                
                for idx, font in enumerate(collection.fonts):
                    print(f"   --------------------------------------------------")
                    print(f"   👉 子字型大編號 [{idx}] 的名稱資訊：")
                    zh, en = get_font_names_clean(font)
                    print(f"      [中文識別] {', '.join(zh) if zh else '(無)'}")
                    print(f"      [英文識別] {', '.join(en) if en else '(無)'}")
            else:
                font = TTFont(file_path)
                print(f"   📊 檔案類型: TTF (標準字型檔)")
                print(f"   --------------------------------------------------")
                zh, en = get_font_names_clean(font)
                print(f"   [中文識別] {', '.join(zh) if zh else '(無)'}")
                print(f"   [英文識別] {', '.join(en) if en else '(無)'}")
                    
        except Exception as e:
            print(f"   ❌ 讀取此檔案時發生錯誤: {str(e)}")
            
        print("=" * 70)

if __name__ == "__main__":
    check_all_fonts_in_dir()
