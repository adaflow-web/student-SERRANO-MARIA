file = open('input.txt', 'r')
array = []
suma = 0
max = 0

for element in file:
    if element != '\n':
        suma += int(element)
    else:
        array.append(suma)   
        suma = 0 

for element in array:
    if element > max:
        max = element

print(max)
file.close()
