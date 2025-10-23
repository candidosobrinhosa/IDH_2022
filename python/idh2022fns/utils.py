def age_order_list():
    return ["0","1-4"] + [f"{i}-{i+4}" for i in range(5,80,5)] + ["80+"]
