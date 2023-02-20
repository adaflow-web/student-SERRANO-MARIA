import random
number = random.randint(1, 100)
result = number
numb = input("Type a number from 1 to 100: ")
counter = 0
   
if numb.isnumeric():
    while int(numb) != result:
        if int(numb) < result:
                print("The secret number is bigger. Try again!")
                counter +=1
                numb = input("Type a number from 1 to 100: ")
                if numb.isnumeric() == False:
                    print("That's not a number. Try again!")
                    quit()
        elif int(numb) > result:
                print("The secret number is smaller. Try again!")
                counter +=1
                numb = input("Type a number from 1 to 100: ")
                if numb.isnumeric() == False:
                    print("That's not a number. Try again!")
                    quit()
    if int(numb)==result: 
        counter += 1
        if counter == 1:
            print("You guessed the secret number in 1 attempt")
        else:
            print("You guessed the secret number in " + str(counter) + " attempts")
if numb.isnumeric() == False:
    print("That's not a number. Try again!")
    quit()
   


# When starting the game, a secret number between 1 and 100 is generated.
# The game asks the user to enter a number.
# The game will tell the user if the secret number is bigger or smaller than the guess.
# As long as the user doesn't find the secret number, the game continues.
# As soon as the user finds the secret number, the game stops and tells the user how many attempts it took to win. Make sure to use the right wording (attempt or attempts)
# In case the user enters anything else than a number, the game should tell that to the user and quit gracefully.
