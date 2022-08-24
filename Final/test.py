while True:
    option_num = input()
    try:
        option_num = int(option_num)
        # find top winner
        if option_num == 1:
            print(1)
        # find all winners
        elif option_num == 2:
            print(2)
        elif option_num == 3:
            break
        else:
            print("Please enter the correct number!")
    except:
        print("Please enter the correct number!")
