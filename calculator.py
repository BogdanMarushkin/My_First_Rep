while True:
    print("Введите число, потом знак операции,", end=' ')
    print("которую хотите совершить (+,-,/,*)", end=' ')
    print("и затем второе число")
    print("Чтобы выключить программу введите 'q'")
    
    num1 = input()
    if num1 == 'q':
        break
    
    calculate = input()
    if calculate == 'q':
        break
    
    num2 = input()
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
        else:
            print("Неподдерживаемая операция!")
            continue
            
        print(answer)
        
    except ValueError:
        print("Вы ввели не число!")
    except ZeroDivisionError:
        print("На ноль делить нельзя!")