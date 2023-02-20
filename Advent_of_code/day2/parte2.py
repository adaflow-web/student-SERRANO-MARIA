file = open('input.txt', 'r')
points = 0

for element in file:
    if element.split()[1] == "X" and element.split()[0] == "A":
        points += 3
    elif element.split()[1] == "X" and element.split()[0] == "B":
        points += 1
    elif element.split()[1] == "X" and element.split()[0] == "C":
        points += 2
    elif element.split()[1] == "Y" and element.split()[0] == "A":
        points += 4
    elif element.split()[1] == "Y" and element.split()[0] == "B":
        points += 5
    elif element.split()[1] == "Y" and element.split()[0] == "C":
        points += 6
    elif element.split()[1] == "Z" and element.split()[0] == "A":
        points += 8
    elif element.split()[1] == "Z" and element.split()[0] == "B":
        points += 9
    elif element.split()[1] == "Z" and element.split()[0] == "C":
        points += 7

print(points)

file.close()
