#file = ["vJrwpWtwJgWrhcsFMMfFFhFp", "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL", "PmmdzqPrVvPwwTWBwg", "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn", "ttgJtRGJQctTZtZT", "CrZsJsPPZsGzwwsLwLmpwMDw"]
file = open('input.txt', 'r')
gifts = {"a":1, "b":2, "c":3, "d":4, "e":5, "f":6, "g":7, "h":8, "i":9, "j":10, "k":11, "l":12, "m":13, "n":14, "o":15, "p":16, "q":17, "r":18, "s":19, "t":20, "u":21, "v":22, "w":23, "x":24, "y":25, "z":26}
points = 0

def groups(line_1, line_2, line_3):
    el_1 = set(line_1)
    el_2= set(line_2)
    el_3= set(line_3)
    common = list(el_1 & el_2 & el_3)[0]

    if common.isupper() == True:
        gifts.get(common.lower())
        result = gifts.get(common.lower())
        points = result + 26
    else:
        points = gifts.get(common)
    return points

for line in file:
    line_1 = line.replace('\n', "")
    line_2 = file.readline().replace('\n', "")
    line_3 = file.readline().replace('\n', "")
    points += groups(line_1, line_2, line_3)
print(points)

file.close()  
