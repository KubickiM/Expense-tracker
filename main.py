# Tracker wydatkow
# Funkcja dodania, wyswietlania, usuwania, edytowania, zapisania pliku, odczytania pliku,
# Dane kategoria, cena, nazwa, ilosc, data
import json
from datetime import datetime

FILENAME = "expenses.json"

def exception_handling(prompt,type_func, positive_only=False,is_date=False):
    while True:
        user_input = input(prompt)
        try:
            if is_date:
                value = datetime.strptime(user_input,"%d-%m-%Y").date()
            else:
                value = type_func(user_input)

                if isinstance(value, (int,float)):
                    if positive_only and value<=0:
                        print("Wartosci musza byc wieksze od zera")
                        continue

                if isinstance(value, str):
                    value = value.strip()
                    if not value:
                        print("Tekst nie moze byc pusty")
                        continue

            return value

        except ValueError:
            type_name= {
                int:"Podaj liczbe calkowita",
                float:"Podaj liczbe zmienno przecinkową",
                str:"Wprowadz tekst",
                'date': "Wprowadza poprawny format daty"
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

def add_expense(expenses):

    item_name = exception_handling("Wprowadz nazwe zakupionego produktu ", str)
    quantity = exception_handling("Wprowadz ilosc zakupionego produktu ", int,positive_only=True)
    value = exception_handling("Wprowadz wartość produktu ", float,positive_only=True)
    date = exception_handling("Wprowadz date zakupu ", str,is_date=True)
    date_obj = datetime.strptime(date, "%d-%m-%Y").date()
    category = exception_handling("Wprowadz kategorie produktu ", str)



    expenses.append({
        "item_name": item_name,
        "quantity": quantity,
        "value": value,
        "date": date_obj,
        "category": category
    })
    save_expenses(expenses)
    print("Expenses saved")

def del_expense(expenses):
    input_del = exception_handling("Wprowadz liczbe wydatku do usuniecia",int,positive_only=True) - 1
    del expenses[input_del]

def edit_expense(expenses):
    input_record = exception_handling("Wybierz ktory wydatek chcesz edytowac",int,positive_only=True) - 1
    while True:
        print("\n=== Wybor wpisu do edycji ===")
        print(f"1. {expenses[input_record]['item_name']}")
        print(f"2. {expenses[input_record]['quantity']}")
        print(f"3. {expenses[input_record]['value']}")
        print(f"4. {expenses[input_record]['date']}")
        print(f"5. {expenses[input_record]['category']}")
        print(f"6. Exit")

        input_edit_record = exception_handling("Wybierz ktora czesc chcesz edytowac",int,positive_only=True)

        if input_edit_record == 1:
            expenses[input_record]['item_name'] = exception_handling("Wprowadz nowa wartosc",str)
        elif input_edit_record == 2:
            expenses[input_record]['quantity'] = exception_handling("Wprowadz nowa wartosc",int,positive_only=True)
        elif input_edit_record == 3:
            expenses[input_record]['value'] = exception_handling("Wprowadz nowa wartosc", float,positive_only=True)
        elif input_edit_record == 4:
            expenses[input_record]['date'] = exception_handling("Wprowadz nowa wartosc DD-MM-YYYY",str,is_date=True)
        elif input_edit_record == 5:
            expenses[input_record]['category'] = exception_handling("Wprowadz nowa wartosc",str)
        else:
            break

def view_expenses(expenses):

    display_list = []
    for idx,expense in enumerate(expenses, start=1):
        display_list.append({
            "id": idx,
            **expense
        })
    choose_list = display_list


    prompt_view_sort = "1. Sortowanie po dacie\ndowolna inna liczba aby kontynuowac bez sortowania\n"
    input_sort = exception_handling(prompt_view_sort, int, positive_only=True, is_date=False)
    if input_sort == 1:
        display_list_sorted = sorted(display_list, key=lambda display_list: display_list['date'])
        choose_list = display_list_sorted

    for expense in choose_list:
        print(f"{expense['id']}. {expense['item_name']} - {expense['quantity']} - PLN:{expense['value']} - {expense['date'].strftime('%d-%m-%Y')} - {expense['category']}")




def show_summary(expenses):
    total = sum(expense['value'] for expense in expenses)
    print(f"\nTotal spent: PLN{total: .2f}")

def category_list(expenses):
    seen_category = set()
    list_category = []

    for idx,expense in enumerate(expenses,start=1):
       if expense['category'] not in seen_category:
           seen_category.add(expense['category'])
           list_category.append({
                "id": idx,
                "category": expense['category']
            })

    for expense in list_category:
        print(f"{expense['id']}. {expense['category']}")
    return list_category

def cateogry_summary(expenses):
    list_category = category_list(expenses)
    total_category = 0
    input_category = exception_handling("\nWybierz jedna z kategorii",int) - 1

    for expense in expenses:
        if expense['category'] == list_category[input_category]['category']:
            total_category += expense['value']
    print(f"\nTotal spent: PLN{total_category: .2f}")

def main():
    expenses = load_expenses()

    while True:
        print("\n=== Personal Expense Tracker ===")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Show Summary")
        print("4. Show Summary from category")
        print("5. Delete Expense")
        print("6. Edit Expense")
        print("7. Exit")

        choice = exception_handling("\nWybierz akcje menu\n",int, positive_only=True)

        if choice == 1:
            add_expense(expenses)
        elif choice == 2:
            view_expenses(expenses)
        elif choice == 3:
            show_summary(expenses)
        elif choice == 4:
            cateogry_summary(expenses)
        elif choice == 5:
            view_expenses(expenses)
            del_expense(expenses)
            save_expenses(expenses)
        elif choice == 6:
            view_expenses(expenses)
            edit_expense(expenses)
            save_expenses(expenses)
        elif choice == 7:
            break
        else:
            print("Invalid input")

if __name__ == "__main__":
    main()



''' 
#input_sort = input("1. Sortowanie po dacie\ndowolny przycisk aby kontynuowac bez sortowania\n")
def view_expenses(expenses):
   id_count = 0
    id_expenses_copy = []
    for expense in expenses:
        id_count = id_count+1
        id_expenses_copy.append({
            "id": id_count,
            "item_name": expense['item_name'],
            "quantity": expense['quantity'],
            "value": expense['value'],
            "date": expense['date'],
            "category": expense['category']
        })
    id_expenses_copy_sorted = sorted(id_expenses_copy,key=lambda id_expenses_copy: id_expenses_copy['date'])
    for expense in id_expenses_copy_sorted:
        print(f"{expense['id']}. {expense['item_name']} - {expense['quantity']} - PLN:{expense['value']} - {expense['date'].strftime('%d-%m-%Y')} - {expense['category']}")
'''