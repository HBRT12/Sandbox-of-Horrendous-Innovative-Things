uppercase_count=0
lowercase_count=0
symbol_count=0
number_count=0
password = input('Please type a password for the strength checker>>> ')
for char in password:
    uppercase=False
    lowercase=False
    number=False
    symbol=False
    if char.upper() == char:
        uppercase=True
    if char.lower() == char: # Determines if the character is upper/lower case
        lowercase=True
    try:
        char=int(char) # Tries to convert string number to integer to
        number=True    # confirm that there is a number
    except:
        pass
    if number == True:
        number_count+=1
        print('number')
    elif uppercase == True and lowercase == True:
        symbol_count+=1
        print('symbol')
    else:
        if uppercase == True:
            uppercase_count+=1
            print('upper')
        elif lowercase == True:
            lowercase_count+=1
            print('lower')
