with open("entradaProj225TAG.txt", 'r') as file:
    arquivo = file.readlines()

#print(arquivo)

lista1 = []
lista2 = []

codigoProjeto = []
numeroVagas = []
requisitos = []

for x in arquivo:

    if x[0] == '(' and x[1] == 'P':
        x = x.replace('\n', '')
        x = x.replace('(', '')
        x = x.replace(')', '')
        lista1.append(x)

#(A1):(P1, P30, P50) (5)

    elif x[0] == '(' and x[1] == 'A':
        x = x.replace('\n', '')
        x = x.replace('(', '')
        x = x.replace(')', '')
        x = x.replace(':', ',')
        x = x.replace(' ', '')
        #temp = x[-1].replace(x[-1], ',' + x[-1])
        temp = x[-1]
        x= x.replace(x[-1], '')
        x = x + ','
        x = x+ temp
        #print(temp)
        #x = x.replace(x[-1], temp)
        #print(x)
        lista2.append(x)

#print(lista1)
print("-----")
print(lista2)


for y in lista1:
    partes = y.split(',')
    codigoProjeto.append(partes[0])
    numeroVagas.append(int(partes[1]))
    requisitos.append(int(partes[2]))

print("-----")
#print(codigoProjeto)
#print(numeroVagas)  
#print(requisitos)
print("-----")
print("-----")
print("-----")
print("-----")
print("-----")
print("-----")


codigoAluno = []
projetosPreferenciais = []
nota = []

for y in lista2:
    partes = y.split(',')
    codigoAluno.append(partes[0])
    projetosPreferenciais.append(partes[1:-1])
    nota.append(int(partes[-1]))
    #print(y)

print(codigoAluno)
print(projetosPreferenciais)
print(nota)