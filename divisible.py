number = int(input("Enter number: "))
def divisible(number):
    for n in range(1,number+1):
        if number % n == 0:
            print(n)
            
divisible(number)