# import os
# import sys
# import json
# import msvcrt
import shutil
# import locale
# import datetime
# import platform
from My_library import *

try:
    import winreg  # Windows only
except ImportError:
    winreg = None


######################################################################################################
# 訊息表, 有中英雙語言, 自動判斷系統語言, 輸出對應語言訊息. // 執行檔參數: 0=英文, >0=中文 // 函式參數: 訊息代號
class MsgOutput:

    def __init__(self, force_lang=None):

        self.messages = {                     # 目前索引 正數:44
            0: ("!! 指定的訊息字串異常 !!",
                "!! Specified message string error !!"),

            1: ("==== MHServerEMU 成就語言工具 %s ====",
                "==== MHServerEMU Achievement locale Tool %s ===="),
            40: ("\t1. 選擇成就檔",
                 "\t1. Select achievement file"),
            3: ("\t2. 匯出語言檔",
                "\t2. Export locale file"),
            4: ("\t3. 匯入語言檔",
                "\t3. Import locale file"),
            5: ("\t4. 刪除語言",
                "\t4. Delete locale"),
            2: ("\t5. 舊格式檔轉語言檔",
                "\t5. Convert old format file to locale file"),
            6: ("\t6. 離開",
                "\t6. Exit"),
            7: ("\n\t請選擇功能(1~6): ",
                "\n\tPlease select a function (1~6): "),

            13: ("確定繼續執行嗎? (Y/N/B/Q): ",
                 "Confirm to proceed? (Y/N/B/Q): "),
            14: ("\n--- 請按 [Enter] 鍵以繼續 ---",
                 "\n--- Please press [Enter] to continue ---"),
            15: (" (!!檔案不存在!!)",
                 " (!!File does not exist!!)"),
            16: ("> !!! %s 檔案更名失敗 !!!",
                 "> !!! File rename error: %s !!!"),
            18: ("> !!! 發現異常, 作業失敗 !!!",
                 "> !!! Exception occurred. Task failed !!!"),
            23: ("> 作業順利完成.",
                 "> Task finished successfully."),
            24: ("> !!! 所選語言不存在 !!!",
                 "> !!! Selected locale does not exist !!!"),
            21: ("> 現有語言:",
                 "> Existing locales:"),
            41: ("> 目前成就檔案:",
                 "> Selected achievement file:"),

            42: ("---- 功能一： 選擇成就檔 AchievementStringMap*.json ----",
                 "---- Feature 1: Select AchiFile - AchievementStringMap*.json ----"),
            43: ("\n1. 預選要進行作業的成就檔 (1~%d): ",
                 "\n1. Pre-select an achievement file to work on (1-%d): "),
            44: ("> 預選檔案: ",
                 "> Pre-selected file: "),

            19: ("---- 功能二： %s 匯出語言檔 ----",
                 "---- Feature 2: Exporting locale File from %s ----"),
            34: ("\n1. 選擇現有語言: 1.en_us 2.fr_fr 3.de_de 4.pt_br 5.ru_ru 6.es_mx 7.zh_tw 8.ja_jp 9.ko_kr (1~9): ",
                 "\n1. Select existing locale:\n   1.en_us 2.fr_fr 3.de_de 4.pt_br 5.ru_ru 6.es_mx 7.zh_tw 8.ja_jp 9.ko_kr (1~9): "),
            20: ("> 來源檔案: ",
                 "> Source file: "),
            22: ("\n2. 選擇匯出語言: 1.en_us 2.fr_fr 3.de_de 4.pt_br 5.ru_ru 6.es_mx 7.zh_tw 8.ja_jp 9.ko_kr (1~9): ",
                 "\n2. Select export locale:\n   1.en_us 2.fr_fr 3.de_de 4.pt_br 5.ru_ru 6.es_mx 7.zh_tw 8.ja_jp 9.ko_kr (1~9): "),
            35: ("> 範本語言: ",
                 "> Template locale: "),
            12: ("> 匯出語言: ",
                 "> Export locale: "),
            36: ("> 匯出語言檔: ",
                 "> Export locale file: "),
            37: ("ID: %s 與 en_en 語言不符, 缺少此筆資料",
                 "ID: %s mismatch (en_en): Missing data entry."),
            38: ("ID: %s 與 en_en 語言不符, 多出此筆資料",
                 "ID: %s mismatch (en_en): Redundant data entry."),
            39: ("ID: %s 的語言欄位不是 %s",
                 "ID: %s - Locale field is not %s"),

            25: ("---- 功能三： %s 匯入語言檔 ----",
                 "---- Feature 3: Importing locale Files into %s ----"),
            26: ("\n1. 選擇匯入語言: 1.en_us 2.fr_fr 3.de_de 4.pt_br 5.ru_ru 6.es_mx 7.zh_tw 8.ja_jp 9.ko_kr (1~9): ",
                 "\n1. Select import locale:\n   1.en_us 2.fr_fr 3.de_de 4.pt_br 5.ru_ru 6.es_mx 7.zh_tw 8.ja_jp 9.ko_kr (1~9): "),
            27: ("> 匯入語言檔: ",
                 "> Import locale file: "),
            28: ("> 成就檔案: ",
                 "> Achievement file: "),
            29: ("> 匯入語言: ",
                 "> Import locale: "),

            30: ("---- 功能四：%s 刪除語言 ----",
                 "---- Feature 4: Removing locale from %s ----"),
            31: ("\n1. 選擇刪除語言: 2.fr_fr 3.de_de 4.pt_br 5.ru_ru 6.es_mx 7.zh_tw 8.ja_jp 9.ko_kr (2~9): ",
                 "\n1. Select locale to delete:\n   2.fr_fr 3.de_de 4.pt_br 5.ru_ru 6.es_mx 7.zh_tw 8.ja_jp 9.ko_kr (2~9): "),
            32: ("> 刪除語言: ",
                 "> Delete locale: "),
            33: ("> (細節請查看記錄檔: achs_Import_error.log)",
                 "> (See log file for details: achs_Import_error.log)"),

            8: ("---- 功能五：轉換舊格式檔 ???.achs_String_Texts.json ----",
                "---- Feature 5: Convert legacy format ???.achs_String_Texts.json ----"),
            9: ("1. 選取舊格式檔名: 1.eng 2.fra 3.deu 4.por 5.rus 6.spa 7.chi 8.jpn 9.kor (1~9): ",
                "1. Select legacy file format:\n   1.eng 2.fra 3.deu 4.por 5.rus 6.spa 7.chi 8.jpn 9.kor (1~9):"),
            10: ("> 舊格式檔: ",
                 "> Legacy file: "),
            11: (">        & ",
                 ">            & "),
            17: ("> 轉換完成, 資料筆數:",
                 "> Conversion complete. Records: "),
        }

        self.lang_mode = self._detect_language(force_lang)

    @staticmethod
    def _detect_language(force_lang):

        if len(sys.argv) > 1:
            try:
                arg = int(sys.argv[1])
                if arg == 0:
                    return "en"
                elif arg > 0:
                    return "zh"
            except ValueError:
                pass

        if force_lang is not None:
            if force_lang == 0:
                return "en"
            else:
                return "zh"

        if platform.system() == "Windows" and winreg:
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\International")
                locale_name, _ = winreg.QueryValueEx(key, "LocaleName")
                winreg.CloseKey(key)

                if "zh-TW" in locale_name or "zh_Hant" in locale_name:
                    return "zh"

            except OSError:
                return "en"

        return "en"

    def output(self, msg_id):

        lang_index = 0 if self.lang_mode == "zh" else 1
        xmsg = self.messages.get(msg_id)

        if not xmsg:
            error_msg = self.messages[0]
            return f"{error_msg[lang_index]} ({msg_id})"

        return xmsg[lang_index]


##########################################################################################
# 切換選擇不同的 AchievementStringMap 檔案 // 參數: 選擇索引  // 無回傳 // 直接取用兩變數
class AchievementFileSelector:
    BASE_NAME = "AchievementStringMap"
    EXT = ".json"

    FILE_SUFFIX = (
        "",                  # 0  AchievementStringMap.json
        "_00_MainPatch",     # 1
        "_02_Party",         # 2
        "_03_Restore",       # 3
        "_04_Seasonal",      # 4
        "_05_Collection",    # 5
    )

    main_name = BASE_NAME
    full_name = BASE_NAME + EXT

    @classmethod
    def select(cls, index: int):
        if index < 0 or index >= len(cls.FILE_SUFFIX):
            raise ValueError("Invalid index: %d" % index)

        cls.main_name = cls.BASE_NAME + cls.FILE_SUFFIX[index]
        cls.full_name = cls.main_name + cls.EXT

    @classmethod
    def get_all_files(cls):                                       # 回傳所有檔名 (含 .json)
        return [
            cls.BASE_NAME + suffix + cls.EXT
            for suffix in cls.FILE_SUFFIX
        ]


##########################################################################################
# 記錄匯入語言時發生的異常 // 記錄 "[時間] [語言] 問題訊息: ID"  // 儲存至 achs_Import_error.log
class AchsErrorLog:

    LOG_FILE = "achs_Import_error.log"

    @staticmethod
    def write(target_locale, message):

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_line = f"[{now}] [{target_locale}] {message}\n"

        try:
            with open(AchsErrorLog.LOG_FILE, "r", encoding="utf-8") as f:
                old_content = f.read()
        except FileNotFoundError:
            old_content = ""

        with open(AchsErrorLog.LOG_FILE, "w", encoding="utf-8") as f:                # 新訊息寫在最前面
            f.write(log_line + old_content)


##########################################################################################
# 將成就舊格式檔轉換為新格式 // 記錄 "[時間] [語言] 問題訊息: ID"  // 儲存至 achs_Import_error.log
class AchsOldFormat:

    @staticmethod
    def convert(source_locale, output_locale, folder_path="."):
        try:
            terms_filename = os.path.join(folder_path, f"{source_locale}.achs_String_terms.json")
            texts_filename = os.path.join(folder_path, f"{source_locale}.achs_String_texts.json")

            with open(terms_filename, "r", encoding="utf-8") as f:       # 讀取 terms
                terms_json = json.load(f)

            term_ids = [
                term["term_id"]
                for term in terms_json["terms"]["terms"]
            ]

            with open(texts_filename, "r", encoding="utf-8") as f:       # 讀取 texts
                texts_json = json.load(f)

            texts = [
                item["Text"]
                for item in texts_json["texts"]
            ]

            if len(term_ids) != len(texts):
                return None                                   # 錯誤, None 代表無資料, 空.

            db = {
                str(term_id): {output_locale: text}
                for term_id, text in zip(term_ids, texts)
            }

            sorted_db = dict(                                 # 數值排序
                sorted(db.items(), key=lambda x: int(x[0]))
            )

            output_filename = os.path.join(
                folder_path,
                f"AchievementStringMap.{output_locale}.json"
            )

            with open(output_filename, "w", encoding="utf-8") as f:
                json.dump(sorted_db, f, ensure_ascii=False, indent=2)

            return len(sorted_db)              # 成功, 回傳轉換筆數.

        except (KeyError, IndexError):
            return None                        # 失敗, None 代表無資料, 空.


##########################################################################################
# 成就檔語言處理
class AchsNewFormat:

    SUPPORTED_LOCALES = [
        "en_us", "fr_fr", "de_de", "pt_br", "ru_ru", "es_mx", "zh_tw", "ja_jp", "ko_kr"
    ]

    def __init__(self):
        self.db = {}            # 主資料結構

    def load(self, filename2=None):        # [函式]：載入來源檔案 ------------------

        if filename2 is None:
            filename2 = AchievementFileSelector.full_name

        with open(filename2, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        self.db.clear()

        for term_id, locale_dict in raw_data.items():       # 直接讀入（不再建立 _seq）
            self.db[term_id] = dict(locale_dict)

        self._sort_db()                                     # 依 term_id 數值排序

        existing_locales = set()                            # 回傳目前存在的語系
        for value in self.db.values():
            for key in value.keys():
                existing_locales.add(key)

        return [loc for loc in self.SUPPORTED_LOCALES if loc in existing_locales]

    def _sort_db(self):                                    # [函式]：term_id 數值排序 --------------
        self.db = dict(
            sorted(
                self.db.items(),
                key=lambda x: int(x[0])                    # 數值排序
            )
        )

    def delete_locale(self, locale_param):  # [函式]：刪除語系 ---------------------

        deleted = False

        for term_id in self.db:
            if locale_param in self.db[term_id]:
                del self.db[term_id][locale_param]
                deleted = True

        if not deleted:
            return False  # 沒找到語系

        self._sort_db()

        try:
            with open(AchievementFileSelector.full_name, "w", encoding="utf-8") as f:
                json.dump(self.db, f, ensure_ascii=False, indent=2)
        except OSError:
            return False  # 寫檔失敗

        return True  # 成功

    def export_locale(self, source_locale, target_locale):  # [函式]：匯出單語系

        try:
            self._sort_db()
            output_data = {}

            for term_id, value in self.db.items():
                if source_locale in value:
                    output_data[term_id] = {
                        target_locale: value[source_locale]
                    }

            filename2 = f"{AchievementFileSelector.main_name}.{target_locale}.json"

            with open(filename2, "w", encoding="utf-8") as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)

            return True

        except OSError:
            return False

    def import_locale(self, locale_param):            # [函式]：匯入語系 ------------------------

        max_errors = 5
        error_count = 0

        filename2 = f"{AchievementFileSelector.main_name}.{locale_param}.json"

        with open(filename2, "r", encoding="utf-8") as f:
            import_data = json.load(f)

        en_term_ids = set(self.db.keys())
        import_term_ids = set(import_data.keys())

        missing_ids = en_term_ids - import_term_ids             # 檢查 Term_ID 是否和 en_en 一致

        for term_id in missing_ids:
            AchsErrorLog.write(
                locale_param,
                msg.output(37) % term_id                        # msg 37, "ID: %s 與 en_en 語言不符, 缺少此筆資料"
            )
            error_count += 1

            if error_count >= max_errors:
                return False

        extra_ids = import_term_ids - en_term_ids               # 檢查多餘 ID

        for term_id in extra_ids:
            AchsErrorLog.write(
                locale_param,
                msg.output(38) % term_id                        # msg 38, "ID: %s 與 en_en 語言不符, 缺少此筆資料"
            )
            error_count += 1

            if error_count >= max_errors:
                return False

        for term_id in en_term_ids:                             # 檢查 locale 欄位, 是否所有資料都含有該 locale

            locale_dict = import_data.get(term_id)

            if locale_dict is None:
                continue

            if locale_param not in locale_dict:

                AchsErrorLog.write(
                    locale_param,
                    msg.output(39) % (term_id, locale_param)     # msg 39, "ID: %s 的語言欄位不是 %s"
                )

                error_count += 1

                if error_count >= max_errors:
                    return False

        if error_count > 0:                                      # 若有錯誤就停止
            return False

        for term_id in en_term_ids:                              # 匯入資料, 匯入筆數全部正確才進行
            self.db[term_id][locale_param] = import_data[term_id][locale_param]

        self._sort_db()

        with open(AchievementFileSelector.full_name, "w", encoding="utf-8") as f:
            json.dump(self.db, f, ensure_ascii=False, indent=2)

        return True


# ^^^^^^^^^^^^ 以上是物件 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#################################################################################################
# 語言代碼轉換語言名稱  // 參數: int index   // 回傳: "eng" , "en_us"
def get_language_pair(index: int):
    languages = {
        1: ("eng", "en_us"),
        2: ("fra", "fr_fr"),
        3: ("deu", "de_de"),
        4: ("por", "pt_br"),
        5: ("rus", "ru_ru"),
        6: ("spa", "es_mx"),
        7: ("chi", "zh_tw"),
        8: ("jpn", "ja_jp"),
        9: ("kor", "ko_kr"),
    }
    return languages.get(index)


#################################################################################################
# 檢查檔案存在與備份處理 // 參數: 檔名字串, 前訊息, 錯誤訊息, 備份:預設 True (=執行備份, False =不備份), 顯示:預設 False(=正常訊息, True=檔案存在就不顯示, 不影響備份失敗訊息)
#                        回傳: 檔案存在=True, 不存在=False
def check_and_optionally_backup(xname="", prefix_msg="", suffix_msg="", backup_flag=True, skip_if_exists=False) -> bool:

    if xname == "":                                     # 未輸入檔名參數, 即抓預設值
        xname = AchievementFileSelector.full_name

    exists = os.path.isfile(xname)
    if exists:                                          # 如果檔案存在
        if not skip_if_exists:                          # -當 skip_if_exists == False 就顯示
            print(prefix_msg + xname)                # -   顯示: 提示訊息 + 檔名

        if backup_flag:                                 # -當 backup_flag == True 就備份
            try:
                base, ext = os.path.splitext(xname)                     # 組成備份檔名, 不考慮"路徑"
                backup_name = f"{base}.{DateTimeString.now(7)}{ext}"
                shutil.copyfile(xname, backup_name)
            except (FileNotFoundError, PermissionError, OSError):
                print(msg.output(16) % xname)        # "> !!! %s 檔案備份失敗 !!!"

        return True                                     # 回傳: 檔案存在
    else:
        print(prefix_msg + xname + suffix_msg)       # 檔案不存在, 顯示: 提示訊息 + 檔名 + 檔案不存在訊息
        return False                                    # 回傳: 檔案不存在


#################################################################################################
# 檢查 AchievementStringMap*.json 存在/合格/載入 處理 // 參數: db 物件, 選用.檔名 //  回傳: 正常=True, 不正常=False
def check_load_achifile(db, xname=None):

    if xname is None:                                          # 如果沒有傳入檔名，使用 class AchievementFileSelector 現用檔案
        xname = AchievementFileSelector.full_name

    if not os.path.isfile(xname):
        print(msg.output(28) + xname + msg.output(15))         # msg 28, "> 成就檔案: " // msg 15, "(!!檔案不存在!!)"
        input(msg.output(14))                                  # msg 14, "\n--- 請按 [Enter] 鍵繼續 ---"
        return False, ""

    ok, err_msg = check_json_file(xname)
    if not ok:
        print("> !!!", err_msg)
        input(msg.output(14))                                  # msg 14, "\n--- 請按 [Enter] 鍵繼續 ---"
        return False, ""

    locales = db.load(xname)                                   # 讀取主檔, 回傳值: 現有語系
    print(msg.output(21), ", ".join(locales))                  # msg 21, "> 現有語言:"

    return True, locales


#################################################################################################
# 功能五: 轉換舊格式檔
def convert_old_format_file():

    while True:
        clear_screen()
        print(msg.output(8))                                                              # msg 8, "---- 功能一：轉匯舊格式檔 ???.achs_String_Texts.json ----"
        old_language_id = input_one_letter(msg.output(9), "123456789")      # msg 9, "1. 選取舊格式檔檔名: 1.eng 2.era 3.deu 4.por 5.rus 6.spa 7.chi 8.jpn 9.kor (1~9): "

        old_name, new_name = get_language_pair(int(old_language_id))                      # 取得"語言"檔名
        text_result = check_and_optionally_backup(f"{old_name}.achs_String_Texts.json", msg.output(10), msg.output(15), False)    # msg 10, "> 舊語言檔: " // msg 15, "(!!檔案不存在!!)"
        term_result = check_and_optionally_backup(f"{old_name}.achs_String_Terms.json", msg.output(11), msg.output(15), False)    # msg 11, ">        $" // msg 15, "(!!檔案不存在!!)"

        result1 = result2 = True
        if text_result and term_result:                                                     # 如果兩個檔案都存在, 才檢查是否為合格 json 檔
            result1, err_msg1 = check_json_file(f"{old_name}.achs_String_Texts.json")       # 檢查是否合格的 .Json 檔
            if not result1:
                print("> !!!", err_msg1)

            result2, err_msg2 = check_json_file(f"{old_name}.achs_String_Terms.json")       # 檢查是否合格的 .Json 檔
            if not result2:
                print("> !!!", err_msg2)

        if not (text_result and term_result and result1 and result2):                       # 4 個回傳值只要有 False, 就結束功能退回.
            input(msg.output(14))                                                           # msg 14, "\n--- 請按 [Enter] 鍵繼續 ---"
            break

        choice5 = input_one_letter("\n2. "+msg.output(13), "YyNnQqBb")                                          # msg 13, "確定進行轉匯嗎 (Y/N/B/Q): "
        if choice5 in ("Y", "y"):
            check_and_optionally_backup(f"AchievementStringMap.{new_name}.json", msg.output(12), "")    # msg 12, "> 匯出語言檔: "

            old_db = AchsOldFormat()                        # [建立 舊格式轉換 物件]
            result = old_db.convert(old_name, new_name)       # 轉換新格式語言檔 // 回傳:
            if result is None:                                # 如果回傳值為空, 代表有誤
                print(msg.output(18))                         # msg 18, "> !!! 發生措誤, 轉換失敗 !!!"
            else:
                print(msg.output(17), result)                 # msg 17, "> 轉換完成, 資料筆數:"

            input(msg.output(14))                             # msg 14, "\n--- 請按 [Enter] 鍵繼續 ---"
            break
        elif choice5 in ("N", "n"):
            continue
        elif choice5 in ("Q", "q"):
            return "Q"                                        # 回傳 Q, 結束程式
        elif choice5 in ("B", "b"):
            break                                             # 脫離無窮迴圈, 結束函式, 回主選單


#################################################################################################
# 功能二: 由 AchievementStringMap*.json 匯出語言檔
def export_locale_file():

    db = AchsNewFormat()                                                   # [建立 新格式處理 物件]

    while True:
        clear_screen()
        print(msg.output(19) % AchievementFileSelector.full_name)            # msg 19, "---- 功能二： %s 匯出語言檔 ----"

        ok, locales = check_load_achifile(db)                                # 檢查 AchievementStringMap*.json 是否 存在/合格 , 然後載入至 db.
        if not ok:                                                           # 成就檔異常就結束
            break

        source_locale_id = input_one_letter(msg.output(34), "123456789")     # msg 34, "\n1. 選擇現有語言: 1.en_us 2.fr_fr 3.de_de 4.pt_br 5.ru_ru 6.es_mx 7.zh_tw 8.ja_jp 9.ko_kr (1~9): "
        _, source_locale = get_language_pair(int(source_locale_id))          # 取得"來源語言"名稱

        print(f"{msg.output(35)}{source_locale}")                            # msg 35, "> 範本語言: "
        if source_locale not in locales:                                     # [選擇的語言不存在]
            print(msg.output(24))                                            # msg 24, "> !!! 所選語言不存在 !!!)
            input(msg.output(14))                                            # msg 14, "\n--- 請按 [Enter] 鍵繼續 ---"
            break                                                            # 來源語言不存在就結束

        target_locale_id = input_one_letter(msg.output(22), "123456789")     # msg 22, "\n2. 選擇匯出語言: 1.en_us 2.fr_fr 3.de_de 4.pt_br 5.ru_ru 6.es_mx 7.zh_tw 8.ja_jp 9.ko_kr (1~9): "
        _, target_locale = get_language_pair(int(target_locale_id))          # 取得"匯出語言"名稱
        print(msg.output(12) + target_locale)                                # msg 12, "> 匯出語言: "

        choice2 = input_one_letter(f"\n3. {msg.output(13)}", "YyNnQqBb")       # msg 13, "確定繼續執行嗎 (Y/N/B/Q): "
        if choice2 in ("Y", "y"):
            check_and_optionally_backup(f"{AchievementFileSelector.main_name}.{target_locale}.json", msg.output(36), "", backup_flag=True, skip_if_exists=False)     # 備份目的檔案 + //msg 36, "> 匯出語言檔: "

            result = db.export_locale(source_locale, target_locale)          # [匯出語言檔], 回傳: 成功=True, 異常=False
            if result:
                print(msg.output(23))                                        # msg 23, "> 作業成功完成."
            else:
                print(msg.output(18))                                        # msg 18, "> !!! 發生錯誤, 作業失敗 !!!"

            input(msg.output(14))                                            # msg 14, "\n--- 請按 [Enter] 鍵繼續 ---"
            break

        elif choice2 in ("N", "n"):
            continue
        elif choice2 in ("Q", "q"):
            return "Q"                                                       # 回傳 0, 結束程式
        elif choice2 in ("B", "b"):
            break                                                            # 脫離無窮迴圈, 結束函式, 回主選單


#################################################################################################
# 功能三: 匯入語言檔至 AchievementStringMap.json
def import_locale_file():

    db = AchsNewFormat()                          # [建立 新格式處理 物件]

    while True:
        clear_screen()
        print(msg.output(25) % AchievementFileSelector.full_name)                       # msg 25, "---- 功能三： %s 匯入語言 ----"

        ok, locales = check_load_achifile(db)       # 檢查 AchievementStringMap*.json 是否 存在/合格 , 然後載入至 db.
        if not ok:                                  # 成就檔異常就結束
            break

        locale_id = input_one_letter(msg.output(26), "123456789")    # msg 26, "\n1. 選擇匯入語言: 1.en_us 2.fr_fr 3.de_de 4.pt_br 5.ru_ru 6.es_mx 7.zh_tw 8.ja_jp 9.ko_kr (1~9): "
        _, locale = get_language_pair(int(locale_id))                              # 取得"語言"檔名
        import_file = f"{AchievementFileSelector.main_name}.{locale}.json"
        exist = check_and_optionally_backup(import_file, msg.output(27), msg.output(15), False)   # msg 27, "> 匯入語言檔: " // msg 15, "(!!檔案不存在!!)"

        is_json = True
        if exist:
            is_json, err_msg = check_json_file(import_file)         # 檢查匯入 json 檔是否合格
            if not is_json:
                print("> !!!", err_msg)                             # 顯示 json 檔發現的錯誤資訊

        if not (exist and is_json):
            input(msg.output(14))                                   # msg 14, "\n--- 請按 [Enter] 鍵繼續 ---"
            break                                                   # 當目標語言不存在, 強制離開, 回主選單
        else:
            choice3 = input_one_letter("\n2. " + msg.output(13), "YyNnQqBb")   # msg 13, "確定繼續執行嗎 (Y/N/B/Q): "

        if choice3 in ("Y", "y"):
            check_and_optionally_backup(AchievementFileSelector.full_name, msg.output(28), "", backup_flag=True, skip_if_exists=False)     # msg 28, "> 成就檔案: " // 純備份
            print(f"{msg.output(29)}{locale}")        # msg 29, "> 匯入語言: "

            result = db.import_locale(locale)         # [匯入語言檔], 回傳: 成功=True, 異常=False

            if result:
                print(msg.output(23))                 # msg 23, ">  作業順利完成."
            else:
                print(msg.output(18))                 # msg 18, "> !!! 發現異常, 作業失敗 !!!"
                print(msg.output(33))                 # msg 33, "> (細節請查看記錄檔: achs_Import_error.log)"

            input(msg.output(14))                     # msg 14, "\n--- 請按 [Enter] 鍵繼續 ---"
            break

        elif choice3 in ("N", "n"):
            continue
        elif choice3 in ("Q", "q"):
            return "Q"                                # 回傳 Q, 結束程式
        elif choice3 in ("B", "b"):
            break                                     # 脫離無窮迴圈, 結束函式, 回主選單


#################################################################################################
# 功能四: 由 AchievementStringMap*.json 刪除指定語言
def erase_locale():

    db = AchsNewFormat()                                                    # [建立 新格式處理 物件]

    while True:
        clear_screen()
        print(msg.output(30) % AchievementFileSelector.full_name)           # msg 30, "---- 功能四：AchievementStringMap*.json 刪除語言 ----"

        ok, locales = check_load_achifile(db)                               # 檢查 AchievementStringMap*.json 是否 存在/合格 , 然後載入至 db, 回傳擁有語系
        if not ok:                                                          # 成就檔異常就結束
            break

        source_locale_id = input_one_letter(msg.output(31), "23456789")     # msg 31, "\n1. 選擇刪除語言: 2.fr_fr 3.de_de 4.pt_br 5.ru_ru 6.es_mx 7.zh_tw 8.ja_jp 9.ko_kr (2~9): "
        _, target_locale = get_language_pair(int(source_locale_id))        # 取得"語言"檔名
        print(msg.output(32)+target_locale)                                # msg 32, "> 刪除語言: "

        if target_locale not in locales:                                    # 當要刪除的語言不存在 ---
            print(msg.output(24), target_locale)                            # msg 24, "> !!! 所選語言不存在 !!!)
            input(msg.output(14))                                           # msg 14, "\n--- 請按 [Enter] 鍵繼續 ---"
            choice4 = "B"                                                   # 指定結束功能, 回主選單
        else:
            choice4 = input_one_letter("\n2. "+msg.output(13), "YyNnQqBb")   # msg 13, "確定繼續執行嗎 (Y/N/B/Q): "

        if choice4 in ("Y", "y"):
            check_and_optionally_backup(AchievementFileSelector.full_name, msg.output(28), "", backup_flag=True, skip_if_exists=False)     # msg 28, "> 成就檔案: " // 純備份

            result = db.delete_locale(target_locale)                        # [刪除語言], 回傳: 成功=True, 異常=False

            if result:
                print(msg.output(23))                                       # msg 23, ">  作業順利完成."
            else:
                print(msg.output(18))                                       # msg 18, "> !!! 發現異常, 作業失敗 !!!"

            input(msg.output(14))                                           # msg 14, "\n--- 請按 [Enter] 鍵繼續 ---"
            break
        elif choice4 in ("N", "n"):
            continue
        elif choice4 in ("Q", "q"):
            return "Q"                                                      # 回傳 0, 當結束程式旗標
        elif choice4 in ("B", "b"):
            break                                                           # 脫離無窮迴圈, 結束函式, 回主選單


#################################################################################################
# 功能一: 選擇作業用 AchievementStringMap*.json 檔案
def select_achi_file():

    db = AchsNewFormat()                                                   # [建立 新格式處理 物件]
    all_achi_files = AchievementFileSelector.get_all_files()               # 取得所有 achi 檔案名稱
    total = len(all_achi_files)
    allowed_keys = "".join(str(i) for i in range(1, total + 1))            # 取得允許輸入 Key 字串, 例: "123456"

    while True:
        clear_screen()
        print(msg.output(42))                                              # msg 42, "---- 功能一： 選擇成就檔 AchievementStringMap*.json ----"
        print(f"{msg.output(41)} {AchievementFileSelector.full_name}\n")   # msg 41, "目前2成就檔案:"

        for i, achi_filename in enumerate(all_achi_files, start=1):
            print(f"  {i}. {achi_filename}")

        choice1 = input_one_letter(msg.output(43) % total, allowed_keys)   # msg 43, "\n1. 試選要進行作業的成就檔 (1~%d): "
        index = int(choice1) - 1
        ok = check_and_optionally_backup(all_achi_files[index], msg.output(44), msg.output(15), False, False)   # msg 44, "> 試選檔案: " // msg 15, "(!!檔案不存在!!)"

        good = True
        if ok:                                                       # 檔案存在, 就檢查是否合格 json 檔
            good, err_msg = check_json_file(all_achi_files[index])   # all_achi_files[index] 為暫選檔案名稱
            if not good:
                print("> !!!", err_msg)

        if not (good and ok):                                        # 檔案不存在 或 非合格 json 就離開
            input(msg.output(14))                                    # msg 14, "\n--- 請按 [Enter] 鍵繼續 ---"
            break

        locales = db.load(all_achi_files[index])                     # 讀取主檔, 回傳值: 現有語系
        print(msg.output(21), ", ".join(locales))                    # msg 21, "> 現有語言:"

        choicek = input_one_letter("\n2. " + msg.output(13), "YyNnQqBb")  # msg 13, "確定繼續執行嗎 (Y/N/B/Q): "
        if choicek in ("Y", "y"):
            AchievementFileSelector.select(index)                                       # 真實改變暫選的成就檔
            print(msg.output(41) + AchievementFileSelector.full_name)                   # msg 41, "> 目前成就檔案:"
            print(msg.output(23))                                                       # msg 23, "> 作業順利完成."
            input(msg.output(14))                                                       # msg 14, "\n--- 請按 [Enter] 鍵繼續 ---"
            break
        elif choicek in ("N", "n"):
            continue
        elif choicek in ("Q", "q"):
            return "Q"                                                # 回傳 "Q", 當結束程式旗標
        elif choicek in ("B", "b"):
            break


#################################################################################################
# 主選單
def main_menu():

    clear_screen()                                                 # 清除螢幕
    print(msg.output(1) % DateTimeString.now(1))                   # msg 1, "==== MHServerEMU 成就語言工具 %s ===="
    print(msg.output(40))                                          # msg 2, "\t1. 選擇成就檔"
    print(msg.output(3))                                           # msg 3, "\t2. 匯出指定語言檔"
    print(msg.output(4))                                           # msg 4, "\t3. 匯入指定語言檔"
    print(msg.output(5))                                           # msg 5, "\t4. 刪除指定語言"
    print(msg.output(2))                                           # msg 2, "\t5. 舊格式檔轉單語言檔"
    print(msg.output(6))                                           # msg 6, "\t6. 結束離開"

    choice0 = input_one_letter(msg.output(7), "123456")     # msg 7, "\n\t請選擇功能(1~6): "
    return choice0


# 主程式
if __name__ == "__main__":                                               # 指定本程式是主程式段

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        test_path = ""                                                   # - 生成為執行檔後,會執行這行
    else:
        test_path = ""                                                   # - IDE 環境開發時, 程式以腳本形式運行, 跑這行

    msg = MsgOutput()                               # [建立 訊息表 物件]

    err_code = None
    while True:

        choice = main_menu()                        # 主功能選單
        if choice in ("1",):                        # 1. 功能一: 選擇成就檔
            err_code = select_achi_file()
        elif choice in ("2",):                      # 2. 功能二: 匯出語言檔
            err_code = export_locale_file()
        elif choice in ("3",):                      # 3. 功能三: 匯入語言檔
            err_code = import_locale_file()
        elif choice in ("4",):                      # 4. 功能四: 刪除語言
            err_code = erase_locale()
        elif choice in ("5",):                      # 5. 功能五: 舊格式檔轉成新語言檔
            err_code = convert_old_format_file()
        elif choice in ("6",):                      # 5. 收工啦~
            break

        if err_code == "Q":                         # err_code = Q, 代表功能中按下 Q, 離開程式
            break
