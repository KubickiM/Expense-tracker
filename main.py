import os
import json
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

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

def exception_handling(prompt,type_func, positive_only=False,is_date=False, language=None):
    while True:
        user_input = input(prompt)
        try:
            if is_date:
                value = datetime.strptime(user_input,"%d-%m-%Y").date()
            else:
                value = type_func(user_input)

                if isinstance(value, (int,float)):
                    if positive_only and value<=0:
                        print(language['isinstance_number'])
                        continue

                if isinstance(value, str):
                    value = value.strip()
                    if not value:
                        print(language['isinstance_str'])
                        continue

            return value

        except ValueError:
            type_name= {
                int:language['isistance_valueerror_int'],
                float:language['isistance_valueerror_float'],
                str:language['isistance_valueerror_str'],
                'date': language['isinstance_valueerror_date']
            }.get('date' if is_date else type_func, str(type_func))



def load_expenses(language=None):
    expenses_folder = "expenses"
    try:
        entries = os.listdir(expenses_folder)
        expenses_files = [entry for entry in entries if entry.endswith(".json")]
        for idx, file in enumerate(expenses_files, start=1):
            print(f"{idx}. {file[:-5]}")
    except FileNotFoundError:
        print(language['expense_file_error'])

    input_expenses_idx = exception_handling(language['input_expenses_idx'], int, positive_only=True) - 1
    expenses_file = expenses_files[input_expenses_idx]
    expenses_path = os.path.join(expenses_folder,expenses_file)

    try:
        with open(expenses_path, "r") as file:
            expenses = json.load(file)
            for expense in expenses:
                expense['date'] = datetime.strptime(expense['date'], "%d-%m-%Y").date()
            return expenses,expenses_path,expenses_file
    except FileNotFoundError:
        with open(expenses_path, "w") as file:
            json.dump([],file)
        return []

def save_expenses(expenses,expenses_path):
    serializable_expenses = []
    for expense in expenses:
        expense_copy = expense.copy()
        expense_copy['date'] = expense_copy['date'].strftime("%d-%m-%Y")
        serializable_expenses.append(expense_copy)

    with open(expenses_path, "w") as file:
        json.dump(serializable_expenses, file, indent=4)

def add_expense(expenses,language=None):

    item_name = exception_handling(language['item_name'], str)
    quantity = exception_handling(language['quantity'], int,positive_only=True)
    value = exception_handling(language['value'], float,positive_only=True)
    date = exception_handling(language['date'], str,is_date=True)
    category = exception_handling(language['category'], str)

    expenses.append({
        "item_name": item_name,
        "quantity": quantity,
        "value": value,
        "date": date,
        "category": category
    })
    save_expenses(expenses)
    print(language['expenses_saved'])

def del_expense(expenses,language=None):
    input_del = exception_handling(language['input_del'],int,positive_only=True) - 1
    del expenses[input_del]

def edit_expense(expenses,language=None):
    input_record = exception_handling(language['input_record'],int,positive_only=True) - 1
    while True:
        print(f"\n{language['menu_edit']}")
        print(f"1. {expenses[input_record]['item_name']}")
        print(f"2. {expenses[input_record]['quantity']}")
        print(f"3. {expenses[input_record]['value']}")
        print(f"4. {expenses[input_record]['date']}")
        print(f"5. {expenses[input_record]['category']}")
        print(f"6. {language['menu_exit']}")

        input_edit_record = exception_handling(language['input_edit_record'],int,positive_only=True)

        if input_edit_record == 1:
            expenses[input_record]['item_name'] = exception_handling(language['input_edit_record_1'],str)
        elif input_edit_record == 2:
            expenses[input_record]['quantity'] = exception_handling(language['input_edit_record_2'],int,positive_only=True)
        elif input_edit_record == 3:
            expenses[input_record]['value'] = exception_handling(language['input_edit_record_3'], float,positive_only=True)
        elif input_edit_record == 4:
            expenses[input_record]['date'] = exception_handling(language['input_edit_record_4'],str,is_date=True)
        elif input_edit_record == 5:
            expenses[input_record]['category'] = exception_handling(language['input_edit_record_5'],str)
        else:
            break
def filter_expenses(expenses, language=None):
    if not expenses:
        print(language['no_expenses'])
        return

    while True:
        print(f"\n{language['filter_menu_title']}")
        print(f"1. {language['filter_by_category']}")
        print(f"2. {language['filter_by_date']}")
        print(f"3. {language['filter_by_price']}")
        print(f"4. {language['filter_by_name']}")
        print(f"5. {language['menu_exit']}")

        choice = exception_handling(language['filter_choice'], int, positive_only=True)

        if choice == 1:
            cat_list = category_list(expenses)
            category_input = exception_handling(language['filter_input_category'], int)-1
            choosen_category = cat_list[category_input]
            filtered = [exp for exp in expenses if exp['category'].lower() == choosen_category['category']]

        elif choice == 2:
            start_date = exception_handling(language['filter_start_date'], str, is_date=True)
            end_date = exception_handling(language['filter_end_date'], str, is_date=True)
            filtered = [exp for exp in expenses if start_date <= exp['date'] <= end_date]

        elif choice == 3:
            min_price = exception_handling(language['filter_min_price'], float, positive_only=True)
            max_price = exception_handling(language['filter_max_price'], float, positive_only=True)
            filtered = [exp for exp in expenses if min_price <= exp['value'] <= max_price]

        elif choice == 4:
            name = exception_handling(language['filter_input_name'], str)
            filtered = [exp for exp in expenses if name.lower() in exp['item_name'].lower()]

        elif choice == 5:
            break
        else:
            print(language['invalid_input'])
            continue

        if filtered:
            print(f"\n{language['filter_results']}")
            for idx, expense in enumerate(filtered, start=1):
                print(f"{idx}. {expense['item_name']} - {expense['quantity']} szt. - PLN: {expense['value']} - "
                      f"{expense['date'].strftime('%d-%m-%Y')} - {expense['category']}")
        else:
            print(language['filter_no_results'])

def view_expenses(expenses,language=None):

    display_list = []
    for idx,expense in enumerate(expenses, start=1):
        display_list.append({
            "id": idx,
            **expense
        })
    choose_list = display_list

    prompt_view_sort = f"{language['prompt_view_sort']}\n"
    input_sort = exception_handling(prompt_view_sort, int, positive_only=True, is_date=False)
    if input_sort == 1:
        display_list_sorted = sorted(display_list, key=lambda display_list: display_list['item_name'])
        choose_list = display_list_sorted
    if input_sort == 2:
        display_list_sorted = sorted(display_list, key=lambda display_list: display_list['date'])
        choose_list = display_list_sorted
    if input_sort == 3:
        display_list_sorted = sorted(display_list, key=lambda display_list: display_list['value'])
        choose_list = display_list_sorted

    for expense in choose_list:
        print(f"{expense['id']}. {expense['item_name']} - {expense['quantity']} - PLN:{expense['value']} - {expense['date'].strftime('%d-%m-%Y')} - {expense['category']}")

    while True:
        print(f"\n1. {language['filter_menu_option']}")
        print(f"2. {language['menu_exit']}")

        view_expenses_menu = exception_handling(language['main_menu_choice'],int)

        if view_expenses_menu == 1:
            filter_expenses(expenses,language)
        elif view_expenses_menu== 2:
            break

    df = pd.DataFrame(choose_list)
    df['total'] = df['value'] * df['quantity']

    grouped = df.groupby('date').agg({
        'total': 'sum',
        'item_name': lambda x: ', '.join(x)
    }).reset_index()

    grouped['date_str'] = grouped['date'].apply(lambda d: d.strftime('%d-%m-%Y'))

    plt.figure(figsize=(10, 5))
    bars = plt.bar(grouped['date_str'], grouped['total'])

    for bar, label in zip(bars, grouped['item_name']):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                 label, ha='center', va='bottom', rotation=0, fontsize=8)

    plt.ylabel(language['view_expense_label_value'])
    plt.title(language['view_expense_label_date'])
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

def show_summary(expenses,language=None):
    total = sum(expense['value']*expense['quantity'] for expense in expenses)
    print(f"\n{language['show_summary_total']}{total: .2f}")

def category_list(expenses):
    seen_category = set()
    list_category = []

    for expense in expenses:
       if expense['category'] not in seen_category:
           seen_category.add(expense['category'])
           list_category.append({
                "id": len(list_category) + 1,
                "category": expense['category']
            })

    for expense in list_category:
        print(f"{expense['id']}. {expense['category']}")
    return list_category

def cateogry_summary(expenses,language=None):
    list_category = category_list(expenses)
    total_category = 0

    df = pd.DataFrame(expenses)
    df['total'] = df['quantity'] * df['value']

    grouped = df.groupby('category')['total'].sum()

    plt.figure(figsize=(7, 7))
    plt.pie(grouped, labels=grouped.index, autopct='%1.1f%%', startangle=140)
    plt.title(language['category_summary_pie_chart_title'])
    plt.tight_layout()
    plt.show()

    input_category = exception_handling(f"\n{language['input_category']}",int) - 1

    for expense in expenses:
        if expense['category'] == list_category[input_category]['category']:
            total_category += expense['value']* expense['quantity']
    print(f"\n{language['show_summary_total']}{total_category: .2f}")

def export_to_excel(expenses,expenses_file, language=None):
    export_folder = "exports"

    df = pd.DataFrame(expenses)
    df['total'] = df['quantity'] * df['value']
    df['date'] = pd.to_datetime(df['date'])

    filename = f"{expenses_file}_export_{datetime.now().strftime('%d%m%Y_%H%M%S')}.xlsx"
    filepath = os.path.join(export_folder, filename)

    df.to_excel(filepath, index=False)

    print(f"{language['excel_export_success']} {filename}")

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
        print(f"8. {language['menu_exit']}")

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
            break
        else:
            print(language['invalid_input'])

if __name__ == "__main__":
    main()