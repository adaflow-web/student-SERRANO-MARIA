# file = ["vJrwpWtwJgWrhcsFMMfFFhFp", "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL", "PmmdzqPrVvPwwTWBwg", "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn", "ttgJtRGJQctTZtZT", "CrZsJsPPZsGzwwsLwLmpwMDw"] 
file = open('input.txt', 'r')
gifts = {"a":1, "b":2, "c":3, "d":4, "e":5, "f":6, "g":7, "h":8, "i":9, "j":10, "k":11, "l":12, "m":13, "n":14, "o":15, "p":16, "q":17, "r":18, "s":19, "t":20, "u":21, "v":22, "w":23, "x":24, "y":25, "z":26}
points = 0

def com_char(points):
    for element in file:
        el_1 = set(element[:len(element)//2])
        el_2 = set(element[len(element)//2:])
        common= list(el_1 & el_2)[0]

        if common.isupper():
            gifts.get(common.lower())
            result = gifts.get(common.lower())
            points += result + 26
        else:
            points += gifts.get(common)

    return points
        
print(com_char(points))

file.close()  
