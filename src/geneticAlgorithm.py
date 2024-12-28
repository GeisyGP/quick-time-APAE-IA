import numpy as np

class geneticAlgorithm:
    def __init__(self, dadosOriginais, periodos):
        self.dadosOriginais = dadosOriginais
        self.periodos = periodos
        self.populationSize = 40
        self.mutationRate = 40 #Taxa de mutação (40% dos filhos terao a mutacao aplicada)
        self.generations = 400
        self.population = []

        #Variaveis para armazenar a melhor solucao
        self.best = []
        self.bestFitness = 10000

    def main(self):
        self.generatesInitialPopulation()
        print("População inicial: " )
        self.imprimePopulacao()

        for g in range(self.generations):
            F = [] #Armazenar a nova geração

            # Seleção
            for i in range(self.populationSize//2):
                t1 = self.torneio()
                t2 = self.torneio()
                while t1 == t2:
                    t2 = self.torneio()

                a, b = self.crossover(self.population[t1], self.population[t2])
        #         # a = mutation(a)
        #         # b = mutation(b)
                F.append(a)
                F.append(b)

            self.population = F
            print("População da geração: ", g+1)
            self.imprimePopulacao()

        print("Melhor solucao: ", self.best, self.bestFitness)
    
    def generatesInitialPopulation(self):
        for i in range(self.populationSize):
            individuo = []
            for a in range (len(self.dadosOriginais)):
                ch = self.dadosOriginais[a][3] #carga horaria
                isConjugated = self.dadosOriginais[a][4]
                alocacao = self.distribuirCH((len(self.periodos)), ch, isConjugated)
                individuo.append(alocacao.tolist())
            self.population.append(individuo)
         
    def distribuirCH(self, tamanho_array, quantidade_1s, isConjugated):
        array = np.zeros(tamanho_array, dtype=int)
        
        if isConjugated:
            ponto_inicio = np.random.choice(tamanho_array - quantidade_1s + 1)
            array[ponto_inicio:ponto_inicio + quantidade_1s] = 1
        else:
            indices_aleatorios = np.random.choice(tamanho_array, quantidade_1s, replace=False)
            array[indices_aleatorios] = 1
        
        return array

    def imprimePopulacao(self):
        for i in range(self.populationSize):
            f = self.fitness(i)
            print(i, self.population[i], f)

            #Armazenando a melhor solução encontrada
            if f < self.bestFitness:
                self.bestFitness = f
                self.best = self.population[i]

    def torneio(self):
        random1 = np.random.randint(0, self.populationSize-1)
        random2 = np.random.randint(0, self.populationSize-1)
        while random1 == random2:
            random2 = np.random.randint(0, self.populationSize-1)

        f1 = self.fitness(random1)
        f2 = self.fitness(random2)
        if f1 < f2:
            return random1
        elif f2 < f1:
            return random2
        else:
            return np.random.choice([random1, random2])
        
    def fitness(self, individuoIndex):
        conflitos = 0

        atividadesPorTurma = self.agruparAtividades(1)
        for turma, atividades in atividadesPorTurma.items():
            periodos_ocupados = {}

            if (len(atividades) > 0):
                for originalIndex, atividade in atividades:
                    for periodo_index, periodo in enumerate(self.population[individuoIndex][originalIndex]):
                        if periodo == 1:
                            if periodo_index in periodos_ocupados:
                                conflitos += 1
                            else:
                                periodos_ocupados[periodo_index] = originalIndex

        atividadesPorProfessor = self.agruparAtividades(2)
        for professor, atividades in atividadesPorProfessor.items():
            periodos_ocupados = {}

            if (len(atividades) > 0):
                for originalIndex, atividade in atividades:
                    for periodo_index, periodo in enumerate(self.population[individuoIndex][originalIndex]):
                        if periodo == 1:
                            if periodo_index in periodos_ocupados:
                                conflitos += 1
                            else:
                                periodos_ocupados[periodo_index] = originalIndex

        atividadesPorRecurso = self.agruparAtividades(5)
        for recurso, atividades in atividadesPorRecurso.items():
            periodos_ocupados = {}

            if (len(atividades) > 0):
                for originalIndex, atividade in atividades:
                    for periodo_index, periodo in enumerate(self.population[individuoIndex][originalIndex]):
                        if periodo == 1:
                            if periodo_index in periodos_ocupados:
                                conflitos += 1
                            else:
                                periodos_ocupados[periodo_index] = originalIndex
                        
        #Validar restrições 
        return conflitos

    def agruparAtividades(self, indexEntidade):
        atividades = {}

        for i, atividade in enumerate(self.dadosOriginais):
            entidades = atividade[indexEntidade]
            
            for e in entidades:
                if e not in atividades:
                    atividades[e] = []
                atividades[e].append((i, atividade))

        return atividades

    #crossover
    def crossover(self, x, y):
        ponto_corte = np.random.randint(1, len(x))
        filhoA = []
        filhoB = []
        for i in range(len(x)):
            if i < ponto_corte:
                filhoA.append(x[i])
                filhoB.append(y[i])
            else:
                filhoA.append(y[i])
                filhoB.append(x[i])

        return filhoA, filhoB

    #mutation


#Dados para testar
# 0ATIVIDADE, 1TURMA, 2PROFESSOR, 3CH, 4GEMINAR?, 5RECURSO
dados = [
    [1, [1], [1], 16, False, [1]],
    [2, [1], [1], 2, True, []],
    [3, [1], [1], 2, True, []],
    [4, [2], [2], 14, False, []],
    [5, [2], [3], 1, False, [1]],
    [7, [2], [4], 1, False, []],
    [8, [2], [2], 1, False, []],
    [9, [2, 3], [5], 1, False, []],
    [10, [2, 3], [4, 3], 2, True, []],
    [11, [3], [6], 14, False, []],
    [12, [3], [3], 1, False, []],
    [13, [3], [4], 1, False, []],
    [14, [3], [6], 1, False, []],
    [15, [4], [7], 15, False, []],
    [16, [4], [3], 1, False, []],
    [18, [4], [4], 2, False, []],
    [19, [4], [5], 1, False, []],
    [20, [4], [7], 1, False, []],
    [21, [5], [8], 19, False, []],
    [22, [5], [8], 1, False, []],
    [23, [6], [9], 16, False, []],
    [24, [6], [9], 1, False, []],
    [25, [6], [3], 1, False, []],
    [26, [6], [4], 1, False, []],
    [27, [6], [9], 1, False, []],
]

periodos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
teste = geneticAlgorithm(dados, periodos)
teste.main()