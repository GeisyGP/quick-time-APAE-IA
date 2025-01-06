import numpy as np
import time
from dotenv import load_dotenv
import os

load_dotenv()

class geneticAlgorithm:
    def __init__(self, originalData, periods):
        self.originalData = originalData
        self.periods = periods
        self.populationSize = int(os.getenv("POPULATION_SIZE"))
        self.mutationRate = int(os.getenv("MUTATION_RATE"))
        self.generations = int(os.getenv("GENERATIONS"))
        self.population = []

        self.activitiesByClass = self._groupActivities(1)
        self.activitiesByTeacher = self._groupActivities(2)
        self.activitiesByResource = self._groupActivities(5)

        self.best = []
        self.bestFitness = 10000

    def run(self):
        start_time = time.time()
        self._generatesInitialPopulation()
        self._printsPopulation()

        for g in range(self.generations):
            F = []

            # Selection
            for i in range((self.populationSize)//2):
                t1 = self._tournament()
                t2 = self._tournament()
                while t1 == t2:
                    t2 = self._tournament()
                a, b = self._crossover(self.population[t1], self.population[t2])
               
                a = self._mutation(a)
                b = self._mutation(b)   

                F.append(a)
                F.append(b)

            self.population = F

            self._printsPopulation()
            if (g+1) % 500 == 0:
                print("Generation: ", g+1, self.bestFitness)

            if self.bestFitness == 0:
                break
        
        end_time = time.time()
        execution_time = end_time - start_time

        print("Best solution: ", self.best, self.bestFitness)
        print(f"Execution time: {execution_time:.2f} seconds")
        return self.best, self.bestFitness
    
    def _groupActivities(self, entityIndex):
        activities = {}

        for i, activity in enumerate(self.originalData):
            entities = activity[entityIndex]
            
            for e in entities:
                if e not in activities:
                    activities[e] = []
                activities[e].append((i, activity))

        return activities

    def _generatesInitialPopulation(self):
        for i in range(self.populationSize):
            chromosome = []
            for a in range (len(self.originalData)):
                workload = self.originalData[a][3]
                isConjugated = self.originalData[a][4]
                unavailablePeriods = self.originalData[a][6]
                allocation = self._distributeWorkload(workload, isConjugated, unavailablePeriods)
                chromosome.append(allocation.tolist())
            self.population.append(chromosome)
         
    def _distributeWorkload(self, workload, isConjugated, unavailablePeriods):
        arraySize = len(self.periods)
        array = np.zeros((arraySize), dtype=int)
        
        if workload > (arraySize):
            print(f"Error: workload {workload} greater than number of periods {(arraySize)}")
            return array

        idToIndex = {id: idx for idx, id in enumerate(self.periods)}
        unavailableIndexes = [idToIndex[id] for id in unavailablePeriods if id in idToIndex]

        for periodo in unavailableIndexes:
            array[periodo] = -1

        if isConjugated:
            max_attempts = 100
            attempt = 0
            while attempt < max_attempts:
                startIndex = np.random.randint(0, arraySize - workload + 1)
                segment = array[startIndex:startIndex + workload]
                if -1 not in segment:
                    array[startIndex:startIndex + workload] = 1
                    break
                attempt += 1
            if attempt == max_attempts:
                print("Error: It was not possible to find a valid point for the conjugate allocation")

        else:
            availablePeriods = [i for i in range(arraySize) if array[i] == 0]
            if len(availablePeriods) >= workload:
                randomIndexes = np.random.choice(availablePeriods, workload, replace=False)
                array[randomIndexes] = 1
            else:
                print("Erro: Not enough periods available for allocation")
        
        array[array == -1] = 0
        return array

    def _printsPopulation(self):
        for i in range(self.populationSize):
            f = self._fitness(self.population[i])
            # print(i, f)

            if f < self.bestFitness:
                # print(i, f)
                self.bestFitness = f
                self.best = self.population[i]

    def _tournament(self):
        random1 = np.random.randint(0, self.populationSize-1)
        random2 = np.random.randint(0, self.populationSize-1)
        while random1 == random2:
            random2 = np.random.randint(0, self.populationSize-1)

        f1 = self._fitness(self.population[random1])
        f2 = self._fitness(self.population[random2])
        if f1 < f2:
            return random1
        elif f2 < f1:
            return random2
        else:
            return np.random.choice([random1, random2])
        
    def _fitness(self, chromosome):
        conflicts = 0

        conflicts += self._calculateConflictsByEntity(self.activitiesByClass, chromosome)
        conflicts += self._calculateConflictsByEntity(self.activitiesByTeacher, chromosome)
        conflicts += self._calculateConflictsByEntity(self.activitiesByResource, chromosome)
                        
        return conflicts

    def _calculateConflictsByEntity(self, activitiesByEntity, chromosome):
        conflicts = 0
        for entity, activities in activitiesByEntity.items():
            busyPeriods = {}

            if (len(activities) > 0):
                for originalIndex, activity in activities:
                    for periodIndex, period in enumerate(chromosome[originalIndex]):
                        if period == 1:
                            if periodIndex in busyPeriods:
                                conflicts += 1
                            else:
                                busyPeriods[periodIndex] = originalIndex
        return conflicts

    def _crossover(self, x, y):
        cutoffPoint = np.random.randint(1, len(x))

        childA = x[:cutoffPoint] + y[cutoffPoint:]
        childB = y[:cutoffPoint] + x[cutoffPoint:]

        return childA, childB

    def _mutation(self, x):
        r = np.random.randint(1, 100)
        if r <= self.mutationRate:
            randomIndex = np.random.randint(0, len(x)-1)
            
            workload = self.originalData[randomIndex][3]
            isConjugated = self.originalData[randomIndex][4]
            unavailablePeriods = self.originalData[randomIndex][6]
            newAllocation = self._distributeWorkload(workload, isConjugated, unavailablePeriods)
            x[randomIndex] = newAllocation.tolist()
            
        return x

#Dados para testar
# 0ATIVIDADE, 1TURMA, 2PROFESSOR, 3CH, 4GEMINAR?, 5RECURSO, 6ids de periodos indisponiveis
dados = [
    [1, [1], [1], 16, False, [1], [16, 20]],
    [2, [1], [1], 2, True, [], []],
    [3, [1], [1], 2, True, [], []],
    [4, [2], [2], 14, False, [], []],
    [5, [2], [3], 1, False, [1], [4, 8, 12, 16, 20]],
    [7, [2], [4], 1, False, [], []],
    [8, [2], [2], 1, False, [], []],
    [9, [2, 3], [5], 1, False, [], []],
    [10, [2, 3], [4, 3], 2, True, [], []],
    [11, [3], [6], 14, False, [], []],
    [12, [3], [3], 1, False, [], []],
    [13, [3], [4], 1, False, [], []],
    [14, [3], [6], 1, False, [], []],
    [15, [4], [7], 15, False, [], []],
    [16, [4], [3], 1, False, [], []],
    [18, [4], [4], 2, False, [], []],
    [19, [4], [5], 1, False, [], []],
    [20, [4], [7], 1, False, [], []],
    [21, [5], [8], 19, False, [], []],
    [22, [5], [8], 1, False, [], []],
    [23, [6], [9], 16, False, [], []],
    [24, [6], [9], 1, False, [], []],
    [25, [6], [3], 1, False, [], []],
    [26, [6], [4], 1, False, [], []],
    [27, [6], [9], 1, False, [], [1]],
]

periodos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
teste = geneticAlgorithm(dados, periodos)
best, conflicts = teste.run()