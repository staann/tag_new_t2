import pandas as pd
import numpy as np

# Carregar dados
projetos_df = pd.read_csv('projetos.csv', delimiter=';')
alunos_df = pd.read_csv('alunos.csv', delimiter=';')

# Estatísticas básicas
print('=== DADOS DE ENTRADA ===')
print(f'Total de alunos: {len(alunos_df)}')
print(f'Total de projetos: {len(projetos_df)}')
print(f'Total de vagas: {projetos_df["Numero_Vagas"].sum()}')
print()

# Simular algoritmo simples para obter estatísticas
class Projeto:
    def __init__(self, codigo, numero_vagas, requisito_minimo):
        self.codigo = codigo
        self.numero_vagas = numero_vagas
        self.requisito_minimo = requisito_minimo
        self.alunos_aceitos = []
        
    def pode_aceitar_aluno(self, aluno):
        return aluno.nota >= self.requisito_minimo
    
    def tem_vaga_disponivel(self):
        return len(self.alunos_aceitos) < self.numero_vagas
    
    def adicionar_aluno(self, aluno):
        if self.pode_aceitar_aluno(aluno):
            self.alunos_aceitos.append(aluno)
            return True
        return False
    
    def remover_pior_aluno(self):
        if self.alunos_aceitos:
            pior_aluno = min(self.alunos_aceitos, key=lambda a: a.nota)
            self.alunos_aceitos.remove(pior_aluno)
            return pior_aluno
        return None

class Aluno:
    def __init__(self, codigo, preferencias, nota):
        self.codigo = codigo
        self.preferencias = preferencias
        self.nota = nota
        self.projeto_atual = None
        self.indice_proposta = 0
        
    def proximo_projeto_preferido(self):
        if self.indice_proposta < len(self.preferencias):
            return self.preferencias[self.indice_proposta]
        return None

# Criar objetos
projetos = {}
for _, row in projetos_df.iterrows():
    codigo = row['Codigo_Projeto']
    projetos[codigo] = Projeto(codigo, row['Numero_Vagas'], row['Requisito_Minimo_Nota'])

alunos = []
for _, row in alunos_df.iterrows():
    preferencias = [
        row['Projeto_Preferencia_1'],
        row['Projeto_Preferencia_2'],
        row['Projeto_Preferencia_3']
    ]
    preferencias = [p for p in preferencias if pd.notna(p) and p != '']
    aluno = Aluno(row['Codigo_Aluno'], preferencias, row['Nota'])
    alunos.append(aluno)

# Executar algoritmo
alunos_livres = [a for a in alunos]
iteracao = 0

while alunos_livres and iteracao < 1000:
    iteracao += 1
    alunos_para_remover = []
    
    for aluno in alunos_livres:
        projeto_codigo = aluno.proximo_projeto_preferido()
        
        if projeto_codigo is None:
            alunos_para_remover.append(aluno)
            continue
        
        if projeto_codigo not in projetos:
            aluno.indice_proposta += 1
            continue
        
        projeto = projetos[projeto_codigo]
        
        if projeto.pode_aceitar_aluno(aluno):
            if projeto.tem_vaga_disponivel():
                projeto.adicionar_aluno(aluno)
                aluno.projeto_atual = projeto_codigo
                alunos_para_remover.append(aluno)
            else:
                pior_aluno_atual = min(projeto.alunos_aceitos, key=lambda a: a.nota)
                if aluno.nota > pior_aluno_atual.nota:
                    pior_aluno = projeto.remover_pior_aluno()
                    pior_aluno.projeto_atual = None
                    alunos_livres.append(pior_aluno)
                    
                    projeto.adicionar_aluno(aluno)
                    aluno.projeto_atual = projeto_codigo
                    alunos_para_remover.append(aluno)
                else:
                    aluno.indice_proposta += 1
        else:
            aluno.indice_proposta += 1
    
    for aluno in alunos_para_remover:
        if aluno in alunos_livres:
            alunos_livres.remove(aluno)

# Calcular resultados
alunos_emparelhados = [a for a in alunos if a.projeto_atual]
alunos_nao_emparelhados = [a for a in alunos if not a.projeto_atual]

projetos_com_alunos = [p for p in projetos.values() if len(p.alunos_aceitos) > 0]
projetos_sem_alunos = [p for p in projetos.values() if len(p.alunos_aceitos) == 0]

total_vagas = sum(p.numero_vagas for p in projetos.values())
vagas_preenchidas = sum(len(p.alunos_aceitos) for p in projetos.values())

# Calcular satisfação
primeira_escolha = 0
segunda_escolha = 0
terceira_escolha = 0

for aluno in alunos_emparelhados:
    if aluno.projeto_atual:
        try:
            rank = aluno.preferencias.index(aluno.projeto_atual) + 1
            if rank == 1:
                primeira_escolha += 1
            elif rank == 2:
                segunda_escolha += 1
            elif rank == 3:
                terceira_escolha += 1
        except ValueError:
            pass

total_emparelhados = len(alunos_emparelhados)
media_rank = (primeira_escolha * 1 + segunda_escolha * 2 + terceira_escolha * 3) / total_emparelhados if total_emparelhados > 0 else 0

# Projetos preenchidos
projetos_totalmente_preenchidos = len([p for p in projetos.values() if len(p.alunos_aceitos) == p.numero_vagas])
projetos_parcialmente_preenchidos = len([p for p in projetos.values() if 0 < len(p.alunos_aceitos) < p.numero_vagas])

# Calcular rank médio no projeto
ranks_projeto = []
for projeto in projetos.values():
    if len(projeto.alunos_aceitos) > 0:
        alunos_ordenados = sorted(projeto.alunos_aceitos, key=lambda a: a.nota, reverse=True)
        for i, aluno in enumerate(projeto.alunos_aceitos):
            rank = alunos_ordenados.index(aluno) + 1
            ranks_projeto.append(rank)

media_rank_projeto = np.mean(ranks_projeto) if ranks_projeto else 0

# Imprimir resultados
print('\n=== RESULTADOS DO EMPARELHAMENTO ===')
print(f'\nAlunos emparelhados: {len(alunos_emparelhados)} ({len(alunos_emparelhados)/len(alunos)*100:.1f}%)')
print(f'Alunos não emparelhados: {len(alunos_nao_emparelhados)} ({len(alunos_nao_emparelhados)/len(alunos)*100:.1f}%)')
print(f'\nProjetos com alunos: {len(projetos_com_alunos)} ({len(projetos_com_alunos)/len(projetos)*100:.1f}%)')
print(f'Projetos sem alunos: {len(projetos_sem_alunos)} ({len(projetos_sem_alunos)/len(projetos)*100:.1f}%)')
print(f'\nVagas preenchidas: {vagas_preenchidas} ({vagas_preenchidas/total_vagas*100:.1f}%)')
print(f'Vagas ociosas: {total_vagas - vagas_preenchidas}')
print(f'\nIterações até convergência: {iteracao}')
print(f'\n--- SATISFAÇÃO DOS ALUNOS ---')
print(f'1ª Escolha: {primeira_escolha} ({primeira_escolha/total_emparelhados*100:.1f}%)')
print(f'2ª Escolha: {segunda_escolha} ({segunda_escolha/total_emparelhados*100:.1f}%)')
print(f'3ª Escolha: {terceira_escolha} ({terceira_escolha/total_emparelhados*100:.1f}%)')
print(f'Rank médio de preferência: {media_rank:.2f}')
print(f'\n--- SATISFAÇÃO DOS PROJETOS ---')
print(f'Totalmente preenchidos: {projetos_totalmente_preenchidos} ({projetos_totalmente_preenchidos/len(projetos)*100:.1f}%)')
print(f'Parcialmente preenchidos: {projetos_parcialmente_preenchidos} ({projetos_parcialmente_preenchidos/len(projetos)*100:.1f}%)')
print(f'Vazios: {len(projetos_sem_alunos)} ({len(projetos_sem_alunos)/len(projetos)*100:.1f}%)')
print(f'Rank médio no projeto: {media_rank_projeto:.2f}')
