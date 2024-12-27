import numpy as np

class geneticAlgorithm:
    def __init__(self, dadosOriginais, periodos):
        self.dadosOriginais = dadosOriginais
        self.periodos = periodos
        self.populationSize = 10
        self.mutationRate = 40 #Taxa de mutação (40% dos filhos terao a mutacao aplicada)
        self.generations = 5
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
            # print("População da geração: ", g+1)
            # self.imprimePopulacao()

        print("Melhor solucao: ", self.best, self.bestFitness)
    
    def generatesInitialPopulation(self):
        for i in range(self.populationSize):
            individuo = []
            for a in range (len(self.dadosOriginais)):
                ch = self.dadosOriginais[a][3] #carga horaria
                alocacao = self.distribuirCH((len(self.periodos)), ch)
                individuo.append(alocacao.tolist())
            self.population.append(individuo)
        
    def distribuirCH(self, tamanho_array, quantidade_1s): 
        array = np.zeros(tamanho_array, dtype=int) 
        indices_aleatorios = np.random.choice(tamanho_array, quantidade_1s, replace=False) 
        array[indices_aleatorios] = 1 
        return array

    def imprimePopulacao(self):
        for i in range(self.populationSize):
            f = self.fitness(i)
            print(i, self.population[i])

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
        print("f1", f1)
        print("f2", f2)
        #Menos conflitos
        if f1 < f2:
            return random1
        elif f2 < f1:
            return random2
        else:
            return np.random.choice([random1, random2])
        
    def fitness(self, individuoIndex):
        conflitos = 0
        turmas_periodo = {}
        professores_periodo = {}
        recursos_periodo = {}
        
        #revisar essas
        # Inicializar turma, professor e recurso para cada iteração
        for atividadeIndex, atividade in enumerate(self.dadosOriginais):
            turma = None
            professor = None
            recurso = None
            
            if self.population[individuoIndex][atividadeIndex] == 1:
                turma = atividade[1][0]
                professor = atividade[2][0]
                recurso = atividade[5][0] if atividade[5] else None

            # Verificar conflitos de turma
            if turma is not None:
                turmas_periodo[turma] = atividadeIndex
                if turma in turmas_periodo:
                    conflitos += 1

            # # Verificar conflitos de professor
            if professor is not None:
                if professor in professores_periodo:
                    conflitos += 1
                professores_periodo[professor] = atividadeIndex

            # # Verificar conflitos de recurso
            if recurso is not None:
                if recurso in recursos_periodo:
                    conflitos += 1
                recursos_periodo[recurso] = atividadeIndex

            #Verificar se é pra geminar e se está geminada 
        return conflitos

    #crossover
    def crossover(self, x, y):
        a = []
        b = []
        meio = len(x)//2 #o recomendado não é o corte ser no meio e sim em posição aleatória
        for i in range(len(x)):
            if i < meio:
                a.append(x[i])
                b.append(y[i])
            else:
                a.append(y[i])
                b.append(x[i])

        return a, b

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
    [28, [5], [8], 20, False, []],
]

periodos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
teste = geneticAlgorithm(dados, periodos)
teste.main()