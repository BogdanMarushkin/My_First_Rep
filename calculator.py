while True:
    print("Введите число, потом знак операции,", end=' ')
    print("которую хотите совершить (+,-,/,*,&,//)", end=' ')
    # '+' - сложение, '-' - вычетание, '/' - обычное деление
    # '//' - целочисленное деление, '*' - умножение, '&' - остаток

    print("и затем второе число")
    print("Чтобы выключить программу введите 'q'")
    
    num1 = input("Введите первое число: ")
    if num1 == 'q':
        break
    
    calculate = input("Введите операцию: ")
    if calculate == 'q':
        break
    
    num2 = input("Введите второе число:")
    if num2 == 'q':
        break
    
    try:
        if calculate == '+':
            answer = int(num1) + int(num2)
        elif calculate == '-':
            answer = int(num1) - int(num2)
        elif calculate == '*':
            answer = int(num1) * int(num2)
        elif calculate == '/':
            answer = int(num1) // int(num2)
        elif calculate == '&':
            answer = int(num1) & int(num2)
        elif calculate == '/':
            answer = int(num1) / int(num2)
        else:
            print("Неподдерживаемая операция!")
            continue
            
        print(f"Результат: {answer}")
        
    except ValueError:
        print("Вы ввели не число!")
    except ZeroDivisionError:
        print("На ноль делить нельзя!")