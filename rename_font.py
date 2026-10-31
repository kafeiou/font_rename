# -*- coding: utf-8 -*-
import os
import sys
from fontTools.ttLib import TTFont, TTCollection

# ==============================================================================
# ⚙️ 目錄設定
# ==============================================================================
SOURCE_DIR = "font_source"     # 來源字型目錄
CONVERT_DIR = "font_convert"   # 轉換後的輸出目錄
CONFIG_FILE = "font_mapping_config.py" # 自動生成的設定檔名

def process_all_fonts():
    # 1. 動態讀取設定檔
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ 錯誤：找不到設定檔案 [{CONFIG_FILE}]！")
        return

    try:
        sys.path.append(os.getcwd())
        if 'font_mapping_config' in sys.modules:
            del sys.modules['font_mapping_config'] # 強制刷新快取
        from font_mapping_config import FONT_MAPPING
    except Exception as e:
        print(f"❌ 讀取設定檔 [{CONFIG_FILE}] 失敗: {str(e)}")
        return

    if not os.path.exists(CONVERT_DIR):
        os.makedirs(CONVERT_DIR)

    # 2. 將設定檔依照「實體檔案」進行分組，並記錄對應的子字型索引(Index)
    grouped_mapping = {}
    for key, config in FONT_MAPPING.items():
        if "#" in key:
            file_name, sub_idx = key.split("#")
            sub_idx = int(sub_idx)
        else:
            file_name = key
            sub_idx = None # 代表是普通 TTF
        
        if file_name not in grouped_mapping:
            grouped_mapping[file_name] = []
        grouped_mapping[file_name].append((sub_idx, config))

    success_count = 0
    missing_files = []

    print(f"🚀 開始批次轉換字型 (採用絕對索引模式)...")
    print("-" * 60)

    # 3. 依照檔案逐一處理
    for file_name, configs in grouped_mapping.items():
        source_path = os.path.join(SOURCE_DIR, file_name)
        output_path = os.path.join(CONVERT_DIR, file_name)

        if not os.path.exists(source_path):
            missing_files.append(file_name)
            continue

        _, ext = os.path.splitext(file_name)
        ext = ext.lower()

        try:
            if ext == ".ttc":
                collection = TTCollection(source_path)
                modified_in_file = 0
                
                # 直接使用索引(Index)去修改對應位置的子字型
                for sub_idx, config in configs:
                    if sub_idx is not None and sub_idx < len(collection.fonts):
                        font = collection.fonts[sub_idx]
                        name_table = font['name']
                        
                        # 取得新名稱
                        new_name = config.get("to_name") if isinstance(config, dict) else config
                        
                        # 強制洗掉該子字型的所有 Name ID 1 & 4 (包含所有語言與平台)
                        for record in name_table.names:
                            if record.nameID == 1 or record.nameID == 4:
                                record.string = new_name.encode('utf-16-be' if record.isUnicode() else 'utf-8')
                        modified_in_file += 1

                collection.save(output_path)
                print(f"✅ 成功! [{file_name}] 已依序號精準修改 {modified_in_file} 個子字型，已存至 {output_path}")
                success_count += 1

            else:
                # 處理標準 TTF 字型
                font = TTFont(source_path)
                name_table = font['name']
                
                _, config = configs[0]
                new_name = config.get("to_name") if isinstance(config, dict) else config

                for record in name_table.names:
                    if record.nameID == 1 or record.nameID == 4:
                        record.string = new_name.encode('utf-16-be' if record.isUnicode() else 'utf-8')
                
                font.save(output_path)
                print(f"✅ 成功! [{file_name}] 已成功修改名稱為「{new_name}」，已存至 {output_path}")
                success_count += 1

        except Exception as e:
            print(f"❌ 處理 [{file_name}] 時發生錯誤: {str(e)}")

    print("-" * 60)
    print(f"🎉 全部處理完畢！成功轉換 {success_count} 個字型實體檔案。")

if __name__ == "__main__":
    process_all_fonts()
