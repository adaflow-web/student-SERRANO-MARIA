# file = ["A X", "B Y", "C Z", "A Y", "B Z", "C X","A Z", "B X", "C Y"]
file = open('input.txt', 'r')
points = 0
points_2 = 0

win = ["A Y", "B Z", "C X"]
loss = ["A Z", "B X", "C Y"]
draw = ["A X", "B Y", "C Z"]

for element in file:
    if element[2] == "X":
        points += 1
    elif element[2] == "Y":
         points += 2
    else:
         points += 3

file.close()
file = open('input.txt', 'r')


for element in file:
    if element.replace("\n", "") in win:
        points_2 += 6
    elif element.replace("\n", "") in loss:
        points_2 += 0
    else:
        points_2 += 3

result = points + points_2
   
print(result)

file.close()