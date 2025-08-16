# Tracker wydatkow
# Funkcja dodania, wyswietlania, usuwania, edytowania, zapisania pliku, odczytania pliku,
# Dane kategoria, cena, nazwa, ilosc, data
import os
import json
from datetime import datetime

FILENAME = "expenses.json"

def load_language():
    try:
        entries = os.listdir()
        language_files = [entry for entry in entries if entry.endswith(".json") and  entry != "expenses.json"]
        for idx,file in enumerate(language_files, start=1):
            print(f"{idx}. {file[:-5]}")
    except FileNotFoundError:
        print("No language files found in the current directory.")

    input_language_idx = exception_handling("Choose language ", int) - 1
    input_language = language_files[input_language_idx]

    try:
        with open(f"{input_language}", "r") as file:
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

def load_expenses():
    try:
        with open(FILENAME, "r") as file:
            expenses = json.load(file)
            for expense in expenses:
                expense['date'] = datetime.strptime(expense['date'], "%d-%m-%Y").date()
            return expenses
    except FileNotFoundError:
        with open(FILENAME, "w") as file:
            json.dump([],file)
        return []

def save_expenses(expenses):
    serializable_expenses = []
    for expense in expenses:
        expense_copy = expense.copy()
        expense_copy['date'] = expense_copy['date'].strftime("%d-%m-%Y")
        serializable_expenses.append(expense_copy)

    with open(FILENAME, "w") as file:
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
        display_list_sorted = sorted(display_list, key=lambda display_list: display_list['date'])
        choose_list = display_list_sorted

    for expense in choose_list:
        print(f"{expense['id']}. {expense['item_name']} - {expense['quantity']} - PLN:{expense['value']} - {expense['date'].strftime('%d-%m-%Y')} - {expense['category']}")

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
    input_category = exception_handling(f"\n{language['input_category']}",int) - 1

    for expense in expenses:
        if expense['category'] == list_category[input_category]['category']:
            total_category += expense['value']* expense['quantity']
    print(f"\n{language['show_summary_total']}{total_category: .2f}")

def main():
    expenses = load_expenses()
    language = load_language()
    while True:
        print(f"\n{language['main_menu_title']}")
        print(f"1. {language['main_menu_1']}")
        print(f"2. {language['main_menu_2']}")
        print(f"3. {language['main_menu_3']}")
        print(f"4. {language['main_menu_4']}")
        print(f"5. {language['main_menu_5']}")
        print(f"6. {language['main_menu_6']}")
        print(f"7. {language['menu_exit']}")

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
            save_expenses(expenses)
        elif choice == 6:
            view_expenses(expenses,language)
            edit_expense(expenses,language)
            save_expenses(expenses)
        elif choice == 7:
            break
        else:
            print(language['invalid_input'])

if __name__ == "__main__":
    main()