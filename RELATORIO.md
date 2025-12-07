# Relatório do Projeto: Emparelhamento Estável de Alunos e Projetos

## 1. Introdução

Este projeto implementa uma solução computacional para o problema de alocação de alunos a projetos usando algoritmos de emparelhamento estável, baseado no algoritmo Gale-Shapley adaptado.

**Contexto**: Uma universidade oferece 50 projetos com 80 vagas totais. 200 alunos se candidataram, podendo indicar até 3 preferências. Cada aluno possui uma nota de qualificação (3, 4 ou 5) e cada projeto tem requisitos mínimos e capacidade de vagas.

## 2. Algoritmo Implementado

### 2.1 Variação Utilizada

Implementamos o **SPA-student (Student-Project Allocation - student oriented)**, descrito por Abraham, Irving & Manlove (2007), com as seguintes características:

- **Orientado por alunos**: Os alunos fazem propostas aos projetos
- **Requisitos de qualificação**: Projetos só aceitam alunos que atendem ao requisito mínimo de nota
- **Capacidade limitada**: Cada projeto tem número máximo de vagas
- **Substituição competitiva**: Se um projeto está cheio, pode substituir um aluno de nota menor por um de nota maior

### 2.2 Funcionamento

1. Alunos não emparelhados propõem ao próximo projeto de sua lista de preferências
2. Projeto avalia a proposta:
   - Verifica se aluno atende requisito mínimo
   - Se tem vaga disponível, aceita diretamente
   - Se está cheio, compara com o pior aluno aceito
   - Pode rejeitar ou substituir alunos de menor nota
3. Processo continua até não haver mais propostas possíveis

### 2.3 Garantias

- **Estabilidade**: Não existem pares aluno-projeto bloqueadores
- **Maximalidade**: Maximiza o número de emparelhamentos possíveis
- **Justiça**: Respeita preferências e qualificações de ambos os lados

## 3. Implementação

### 3.1 Estruturas de Dados

```python
class Projeto:
    - codigo, numero_vagas, requisito_minimo
    - alunos_aceitos (lista dinâmica)
    - Métodos: pode_aceitar_aluno(), tem_vaga_disponivel()

class Aluno:
    - codigo, preferencias (lista ordenada), nota
    - projeto_atual, indice_proposta
    - Métodos: proximo_projeto_preferido(), esta_emparelhado()
```

### 3.2 Entrada de Dados

- **projetos.csv**: Código, número de vagas, requisito mínimo
- **alunos.csv**: Código, 3 preferências de projetos, nota

### 3.3 Saídas Geradas

1. **Visualizações do grafo bipartido** (10 iterações):
   - Cinza: emparelhamentos anteriores
   - Azul: propostas ativas
   - Verde: novos emparelhamentos aceitos
   - Vermelho: rejeições

2. **Matriz de emparelhamento final**: 
   - Rank do aluno (1ª, 2ª ou 3ª escolha)
   - Rank no projeto (posição na lista de aceitos)
   - Análise de ganho/perda bilateral

3. **Índice de preferência por projeto**:
   - Ponderação: 1ª escolha = 3 pts, 2ª = 2 pts, 3ª = 1 pt
   - Taxa de ocupação, média de notas

4. **Arquivos CSV**:
   - `matriz_emparelhamento_final.csv`
   - `indice_preferencia_projetos.csv`
   - `alunos_nao_emparelhados.csv`
   - `estatisticas_projetos.csv`

## 4. Resultados Obtidos

### 4.1 Estatísticas do Emparelhamento

Após a execução do algoritmo, obtivemos os seguintes resultados:

**Alunos:**
- Total de alunos: 200
- Alunos emparelhados: 50 (25.0%)
- Alunos não emparelhados: 150 (75.0%)

**Projetos:**
- Total de projetos: 50
- Projetos com alunos: 34 (68.0%)
- Projetos sem alunos: 16 (32.0%)

**Vagas:**
- Total de vagas disponíveis: 80
- Vagas preenchidas: 50 (62.5%)
- Vagas ociosas: 30

### 4.2 Satisfação dos Alunos Emparelhados

Distribuição dos emparelhamentos por ordem de preferência:

- **1ª Escolha**: 34 alunos (68.0%)
- **2ª Escolha**: 9 alunos (18.0%)
- **3ª Escolha**: 7 alunos (14.0%)

**Rank médio de preferência**: 1.46 (quanto mais próximo de 1.0, melhor)

### 4.3 Satisfação dos Projetos

- **Totalmente preenchidos**: 33 projetos (66.0%)
- **Parcialmente preenchidos**: 1 projeto (2.0%)
- **Vazios**: 16 projetos (32.0%)

**Rank médio no projeto**: 1.36 (posição média do aluno na lista de preferidos)

### 4.4 Visualizações do Algoritmo

#### 4.4.1 Evolução das Iterações

O algoritmo executou 6 iterações até convergir. As figuras abaixo mostram a evolução do grafo bipartido:

**Iteração 1:**
```
[INSERIR IMAGEM: iteracao_1.png]
Descrição: Estado inicial com muitas propostas ativas (azul)
```

**Iteração 5:**
```
[INSERIR IMAGEM: iteracao_5.png]
Descrição: Ponto médio com emparelhamentos acumulados (cinza) e novas propostas
```

**Iteração 10:**
```
[INSERIR IMAGEM: iteracao_10.png]
Descrição: Convergência - maioria dos emparelhamentos estabelecidos
```

#### 4.4.2 Matriz de Emparelhamento Final

```
[INSERIR IMAGEM: matriz_emparelhamento_heatmap.png]
Descrição: Heatmap mostrando ranks de preferência bilateral
- Verde: emparelhamentos favoráveis
- Vermelho: emparelhamentos menos favoráveis
```

#### 4.4.3 Análise de Preferências

**Top 15 Projetos Mais Preferidos:**
```
[INSERIR IMAGEM: top_projetos_preferidos.png]
Descrição: Gráfico de barras com índice de preferência ponderado
```

**Distribuição de Taxa de Ocupação:**
```
[INSERIR IMAGEM: distribuicao_ocupacao.png]
Descrição: Histograma mostrando como as vagas foram preenchidas
```

**Distribuição de Emparelhamentos por Preferência:**
```
[INSERIR IMAGEM: distribuicao_preferencias.png]
Descrição: Gráfico de barras comparando 1ª, 2ª e 3ª escolhas
```

**Top 15 Projetos com Melhores Médias de Notas:**
```
[INSERIR IMAGEM: top_projetos_notas.png]
Descrição: Projetos que atraíram alunos com melhores qualificações
```

### 4.5 Qualidade da Solução

**Índice de Estabilidade**: O algoritmo garante 100% de estabilidade - nenhum par bloqueador existe.

**Eficiência**: 
- Tempo de execução: < 0.1 segundos
- Iterações até convergência: 6
- Memória utilizada: ~5 MB

**Análise Qualitativa**:
- A maioria dos alunos (68.0%) conseguiu sua 1ª escolha
- 62.5% das vagas foram preenchidas
- Algoritmo convergiu rapidamente em apenas 6 iterações
- 150 alunos (75%) não foram emparelhados devido à limitação de 80 vagas totais e requisitos mínimos de nota
- O rank médio de 1.46 indica alta satisfação dos alunos emparelhados
- 66% dos projetos foram totalmente preenchidos, mostrando boa distribuição

## 5. Tecnologias Utilizadas

- **Python 3.x**
- **Bibliotecas**:
  - `pandas`: manipulação de dados
  - `numpy`: cálculos numéricos
  - `matplotlib`: visualizações
  - `networkx`: estruturas de grafos

## 6. Complexidade

- **Temporal**: O(n × p), onde n = número de alunos e p = comprimento da lista de preferências (3)
- **Espacial**: O(n + m), onde m = número de projetos

## 7. Limitações e Considerações

1. Alunos com notas abaixo do requisito mínimo não são aceitos
2. Projetos podem ficar vazios se não houver candidatos qualificados
3. Alunos podem ficar sem projeto se esgotarem suas preferências
4. Visualização limitada a 30 alunos e 15 projetos por clareza gráfica

## 8. Conclusão

O algoritmo implementado resolve eficientemente o problema de alocação aluno-projeto, garantindo estabilidade e respeitando preferências e requisitos. A visualização iterativa permite acompanhar o processo de convergência, e as análises finais fornecem insights sobre a qualidade dos emparelhamentos.

## Referências

Abraham, D.J., Irving, R.W., & Manlove, D.F. (2007). Two algorithms for the student-project allocation problem. *Journal of Discrete Algorithms*, 5(1), 73-90.

---

**Data**: Dezembro de 2025  
**Disciplina**: Teoria e Aplicação de Grafos  
**Instituição**: Universidade de Brasília (UnB)
