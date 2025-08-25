import os
import json
from reports import generate_pdf_report,export_to_excel
from utils import exception_handling
from expenses import  load_expenses,save_expenses,add_expense,view_expenses,show_summary,cateogry_summary,del_expense,edit_expense

def load_language():
    language_folder = "languages"
    try:
        entries = os.listdir(language_folder)
        language_files = [entry for entry in entries if entry.endswith(".json") and  entry != "expenses.json"]
        for idx,file in enumerate(language_files, start=1):
            print(f"{idx}. {file[:-5]}")
    except FileNotFoundError:
        print("No language files found in the current directory.")

    input_language_idx = exception_handling("Choose language ", int) - 1
    language_file = language_files[input_language_idx]
    language_path = os.path.join(language_folder, language_file)

    try:
        with open(language_path, "r",encoding='utf-8') as file:
            language = json.load(file)
            return language
    except FileNotFoundError:
        print("File with language not found")

def main():
    language = load_language()
    expenses,expenses_path,expenses_file = load_expenses(language)

    while True:
        print(f"\n{language['main_menu_title']}")
        print(f"1. {language['main_menu_1']}")
        print(f"2. {language['main_menu_2']}")
        print(f"3. {language['main_menu_3']}")
        print(f"4. {language['main_menu_4']}")
        print(f"5. {language['main_menu_5']}")
        print(f"6. {language['main_menu_6']}")
        print(f"7. {language['main_menu_7']}")
        print(f"8. {language['main_menu_8']}")
        print(f"9. {language['menu_exit']}")

        choice = exception_handling(f"\n{language['main_menu_choice']}\n",int, positive_only=True)

        if choice == 1:
            add_expense(expenses,language)
        elif choice == 2:
            view_expenses(expenses,language)
        elif choice == 3:
            show_summary(expenses,language)
        elif choice == 4:
            cateogry_summary(expenses,language)
        elif choice == 5:
            view_expenses(expenses,language)
            del_expense(expenses,language)
            save_expenses(expenses,expenses_path)
        elif choice == 6:
            view_expenses(expenses,language)
            edit_expense(expenses,language)
            save_expenses(expenses,expenses_path)
        elif choice == 7:
            export_to_excel(expenses,expenses_file,language)
        elif choice == 8:
            generate_pdf_report(expenses,"reports",language)
        elif choice == 9:
            break
        else:
            print(language['invalid_input'])

if __name__ == "__main__":
    main()