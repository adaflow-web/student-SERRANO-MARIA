#def exchange(euros):
#    msg_1 = " euros are "
#    msg_2 = " CHF"
#    result = euros * 0.98
#    return str(euros) + msg_1 + str(result) + msg_2

#print(exchange(100))


def exchange(euros):
    msg_1 = " euros are "
    msg_2 = " CHF"
    result = float(euros) * 0.98
    return str(euros) + msg_1 + str(result) + msg_2

euros = float(input("Enter the amount in €: "))
print(exchange(euros))

if euros >10000:
        print("That's a lot of money!")




