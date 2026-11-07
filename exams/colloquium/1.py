a = 5
b = a
print(id(b) == id(a))
a = 7
print(id(b) == id(a))

list_a = [1, 2, 3]
list_b = list_a

print(id(list_a) == id(list_b))

list_b.append(2)
print(*list_a)
print(*list_b)

print(id(list_a) == id(list_b))

a, *b, c = [1, 2, 4, 5, 6, 3]
print(a, b, c)





