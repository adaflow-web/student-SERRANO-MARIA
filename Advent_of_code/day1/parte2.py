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

array.sort(reverse=True)

print(array)

result = array[0] + array[1] + array[2]
print(result)
file.close()