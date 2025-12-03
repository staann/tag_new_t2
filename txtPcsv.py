import csv

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
#print(lista2)


for y in lista1:
    partes = y.split(',')
    codigoProjeto.append(partes[0])
    numeroVagas.append(int(partes[1]))
    requisitos.append(int(partes[2]))

print("-----")
#print(codigoProjeto)
#print(numeroVagas)  
#print(requisitos)



codigoAluno = []
projetosPreferenciais = []
nota = []

for y in lista2:
    partes = y.split(',')
    codigoAluno.append(partes[0])
    projetosPreferenciais.append(partes[1:-1])
    nota.append(int(partes[-1]))
    #print(y)

#print(codigoAluno)
#print(projetosPreferenciais)
#print(nota)

# Criar CSV de Projetos
with open('projetos.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(['Codigo_Projeto', 'Numero_Vagas', 'Requisito_Minimo_Nota'])
    for i in range(len(codigoProjeto)):
        writer.writerow([codigoProjeto[i], numeroVagas[i], requisitos[i]])

print("Arquivo 'projetos.csv' criado com sucesso!")

# Criar CSV de Alunos
with open('alunos.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(['Codigo_Aluno', 'Projeto_Preferencia_1', 'Projeto_Preferencia_2', 'Projeto_Preferencia_3', 'Nota'])
    for i in range(len(codigoAluno)):
        # Garantir que temos 3 projetos preferenciais (ou menos)
        prefs = projetosPreferenciais[i]
        pref1 = prefs[0] if len(prefs) > 0 else ''
        pref2 = prefs[1] if len(prefs) > 1 else ''
        pref3 = prefs[2] if len(prefs) > 2 else ''
        writer.writerow([codigoAluno[i], pref1, pref2, pref3, nota[i]])

print("Arquivo 'alunos.csv' criado com sucesso!")

