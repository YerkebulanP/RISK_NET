# RESIDUAL LOSS
def calculate_residual_loss(loss, effect):
    if loss > 0:
        return loss
    if effect == "низкая":
        return loss * 1.0
    elif effect == "средняя":
        return loss * 0.5
    elif effect == "высокая":
        return loss * 0.3
    else:
        return 0



# CALCULATION OF TOTAL_PROB_1
def calculate_condition(AA_values, Y_values):
    total = sum(AA_values)
    weighted_sum = sum(AA * Y for AA, Y in zip(AA_values, Y_values))
    weighted_avg = weighted_sum / total

    if weighted_avg >= 100:
        return 100
    else:
        return weighted_avg
        
        
Y_values = [100,100,100,100,100,100,5,0,0,5] 
AA_values = [-15630, 0, 0, 0, 0, 4086, -80, 0, 0, -72]  

result = calculate_condition(AA_values, Y_values)
print(result)