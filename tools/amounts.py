async def amounts(item):
    if item == 'cookie':
        return 100
    elif item == 'chocolate':
        return 500
    elif item == 'coin':
        return 1000
    elif item == 'rare coin':
        return 5000
    elif item == 'medal':
        return 10000
    elif item == 'rare medal':
        return 50000
    elif item == 'trophy':
        return 100000
    elif item == 'rare trophy':
        return 500000
    elif item == 'ultra collectable thingy':
        return 1000000
    else:
        return False