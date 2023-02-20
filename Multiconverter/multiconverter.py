start = input("Do you want to convert a value? yes/no ")

def exchange(third):
    euros = int(third)
    result = int(euros) *0.98
    if third == 1:
        msge = " euro is "
    else:
        msge=" euros are "
    return str(third) + msge + str(result) + " CHF"


def temp_conv(third):
    celsius = int(third)
    result = int(celsius) * 9/5 + 32
    if third == 1:
        msgc= " degree Celsius is "
    else :
        msgc= " degrees Celsius are "

    return str(third) + msgc + str(result) + " degrees Farenheit"

def inchTocm(third):
    inches = int(third)
    result = int((inches)) * 2.54
    if third == 1:
        msgi = " inche is "
    else:
        msgi = " inches are "
    return str(third) + msgi + str(result) + " cm"



if start == "yes":
    second = input("Which conversion? (euros/celsius/inches) ")
    third = int(input("Which value do you want to convert? "))
    if second == "euros":
        print(exchange(third))
    
    elif second == "celsius":
        print(temp_conv(third))
    
        
    elif second == "inches":
        print(inchTocm(third))
    
    else:
        print("I can't do this conversion")
else:
    quit()




