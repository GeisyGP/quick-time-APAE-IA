# quick-time-APAE-IA
Repositório com o algoritmo de inteligência artificial para gerar o quadro de horários.

## Funcionamento do algoritmo

Resultado do algoritmo é uma matriz, sendo cada linha uma atividade e cada coluna um período. Onde tem 1 indica que o período é ocupado pela atividade.

_Menor quantidade de conflitos encontrados até o momento: **1**_ Com a seguinte configuração:
- self.populationSize = 500
- self.mutationRate = 50 #Taxa de mutação (40% dos filhos terao a mutacao aplicada)
- self.generations = 400

### População inicial
A população inicial é gerada conforme a carga horária de cada atividade e respeitando a indicação se deve ser geminada.

### Fitness
Na função fitness é contado a quantidade de conflitos que há no indivíduo da população. Cada indivíduo representa uma solução para o quadro de horários. Validações feitas na fitness:
- Conflito de turma: uma mesma turma com mais de uma atividade no mesmo período
- Conflito de professor: um mesmo professor com mais de uma atividade no mesmo período
- Conflito de recurso: um mesmo recurso com mais de uma atividade no mesmo período

Ainda não implementadas:
- Conflito de restrição: turma ou professor não disponível no período (talvez implementar já na geração da população inicial)

### Crossover 
Inicialmente implementado dividindo as ativadades dos pais, da seguinte forma:
- Escolhe um ponto de corte aleatório
- As atividades do pai 1 até o corte vão para o filho A
- As atividades do pai 2 até o corte vão para o filho B
- As atividades do pai 1 apóso corte vão para o filho B
- As atividades do pai 2 apóso corte vão para o filho A

Podemos considerar, caso necessário, implementar o crossover por períodos. O que implica em organizar novamente a CH e geminação.

### Mutação
?