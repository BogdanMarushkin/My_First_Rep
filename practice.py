def comps_sandwich(y_comps, add_comps,):
    '''Топпинги для сендвича'''
    print("Выберите топпинги для своего сэндвича")
    print("Если хотите закончить заказ 'q'")
    print("Доступные топпинги:", ', '.join(y_comps))
    while True:
        comp = input()
        if comp == 'q':
            break
        
        if comp in y_comps:
            add_comps.append(comp)
            print(f'Топпинг {comp} добавлен')
        else:
            print("Такого топинга нет")
        
    return add_comps
a = ["cheese", "pepperoni", "mushrooms"]
b = []
comps_sandwich(a,b)
if b == []:
    print("В ваш заказ ничего не добавлено")
else:
    print(f"В ваш заказ добавлены {', '.join(b)}!")