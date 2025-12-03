with open("entradaProj225TAG.txt", 'r') as file:
    arquivo = file.readlines()

#print(arquivo)

lista1 = []
lista2 = []

for x in arquivo:
    #print(x)
    if x[0] == '(' and x[1] == 'P':
        lista1.append(x)
    elif x[0] == '(' and x[1] == 'A':
        lista2.append(x)

print(lista1)
print(lista2)