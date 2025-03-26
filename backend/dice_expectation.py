import ast
from collections import Counter
from itertools import product
###############################
## ПРЕВРАЩАЕТ 1d2+1 В [2, 3] ##
###############################
def dice_to_values(dice_string): 
    dice_string = str(dice_string)
    if 'd' in dice_string:              # ПРОВЕРЯЕМ ЭТО КУБИК ИЛИ ЧИСЛО
        parts = dice_string.split('d')
        dice_count = int(parts[0])
        remaining = parts[1]
        additional = 0
        if '+' in remaining:
            dice_shapes, add = remaining.split('+')
            additional = int(add)
        elif '-' in remaining:
            dice_shapes, sub = remaining.split('-')
            additional = -int(sub)
        else:   
            dice_shapes = remaining
        dice_shapes = int(dice_shapes)

        single_die = [i + additional for i in range(1, dice_shapes + 1)]    # МОМЕНТ ПРЕВРАЩЕНИЯ
        return dice_multiply(single_die, dice_count)
    else:
        return [int(dice_string)]

###################################
## ПРЕВРАЩАЕТ 2d2 В [1, 2, 3 ,4] ##
###################################

def dice_multiply(values, count):
    if count == 1:
        return values
    result = []
    for x in values:
        for y in dice_multiply(values, count - 1):
            result.append(x + y)
    return result

####################################
## ПРЕВРАЩАЕТ [2, 3] В 2: 0.5 ##
####################################

def calculate_distribution(values): 
    total = len(values)
    return {v: round(count/total, 2) for v, count in Counter(values).items()} # Counter -> [2, 2, 3] ПРЕВРАЩАЕТ В [2:2, 3:1]

def process_component(component_list): #СОЗДАЕТ РАСПРЕДЕЛЕНИЕ [2, 3] -> [2: 0.5, 3: 0.5 ] И КУБИКИ ПРЕВРАЩАЕТ В ЗНАЧЕНИЯ
    distributions = {}
    combined = []
    for dice in component_list:
        values = dice_to_values(dice)
        distributions[dice] = calculate_distribution(values)
        combined.append(values)
    
    # Calculate combined values for the component
    if not combined:
        return distributions, []
    
    result = combined[0]
    for values in combined[1:]:
        result = [x + y for x in result for y in values]
    return distributions, result

def main():
    data = input("GIVE ME DICT AS A STRING: ")
    input_dict = ast.literal_eval(data)
    
    result = {
        "vulnerability": {},
        "ordinary": {},
        "stability": {},
        "all": {}
    }
    
    # ПОЛУЧАЕМ ЗНАЧЕНИЯ КУБОВ И РАСПРЕДЕЛЕНИЯ
    vuln_dist, vuln_values = process_component(input_dict["vulnerability"])
    ord_dist, ord_values = process_component(input_dict["ordinary"])
    stab_dist, stab_values = process_component(input_dict["stability"])
    
    # МНОЖИТЕЛЬ ДЛЯ СТОЙКОСТИ И УЯЗВИМОСТИ
    vuln_values = [int(x * 2) for x in vuln_values]  
    stab_values = [x // 2 for x in stab_values]
    
    # ЗАГРУЖАЕМ РАСПРЕДЕЛЕНИЯ В СТРОКУ result
    result["vulnerability"] = {k: {vk: round(vc, 2) for vk, vc in v.items()} for k, v in vuln_dist.items()}
    result["ordinary"] = {k: {vk: round(vc, 2) for vk, vc in v.items()} for k, v in ord_dist.items()}
    result["stability"] = {k: {vk: round(vc, 2) for vk, vc in v.items()} for k, v in stab_dist.items()}
    
    # СОЗДАЕМ СПИСОК ЗНАЧЕНИЙ ВСЕХ КУБОВ
    modifier = input_dict["modifier"]
    all_combinations = product(vuln_values, ord_values, stab_values)
    total = []
    for combo in all_combinations:
        total.append(sum(combo) + modifier)
    
    # НА ОСНОВЕ ПРЕДЫДУЩЕГО ШАГА СОЗДАЕМ РАСПРЕДЕЛЕНИЕ
    counts = Counter(total)
    total_count = len(total)
    result["all"] = {k: round(v/total_count, 2) for k, v in counts.items()}
    
    print(result)

if __name__ == "__main__":
    main()