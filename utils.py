from datetime import datetime

def exception_handling(prompt,type_func, positive_only=False,is_date=False, language=None):
    while True:
        user_input = input(prompt)
        try:
            if is_date:
                return datetime.strptime(user_input,"%d-%m-%Y").date()

            value = type_func(user_input)

            if isinstance(value, (int,float)) and  positive_only and value<=0:
                print(language['isinstance_number'])
                continue

            if isinstance(value, str):
                value = value.strip()
                if not value:
                    print(language['isinstance_str'])
                    continue

            return value

        except ValueError:
            error_messages= {
                int:language['isistance_valueerror_int'],
                float:language['isistance_valueerror_float'],
                str:language['isistance_valueerror_str'],
                'date': language['isinstance_valueerror_date']
            }.get('date' if is_date else type_func, str(type_func))
            print(error_messages.get("date" if is_date else type_func, language['invalid_input']))

