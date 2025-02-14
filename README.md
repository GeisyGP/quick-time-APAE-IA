# quick-time-APAE-IA
Repositório com o algoritmo de inteligência artificial para gerar o quadro de horários.

## Funcionamento do algoritmo

Resultado do algoritmo é uma matriz, sendo cada linha uma atividade e cada coluna um período. Onde tem 1 indica que o período é ocupado pela atividade.

Ao encontrar uma solução com 0 conflitos o algoritmo encerra retornando a solução. Por padrão o máximo de gerações está com 200 mil gerações.

Dessa forma, o tempo para encontrar a solução pode variar:
- Solução encontrada em 4 segundos:
![Imagem com exemplo de solução](doc_files/400generations.png)
- Solução encontrada em 262 segundos:
![Imagem com exemplo de solução](doc_files/25000generations.png)

### População inicial
A população inicial é gerada conforme:
- a carga horária de cada atividade; e
- respeitando os períodos indisponíveis.

> :exclamation: Caso não tenha períodos disponíveis suficientes para a carga horária de uma atividade, irá dar erro. Essa validação precisa ser feita antes de chamar esse algoritmo para prevenir quebra.

> :exclamation: Caso um conjuntos de atividades de um mesmo professor, turma ou recurso ultrapasse a carga horária, irá sempre dar conflito até que isso seja alterado no banco de dados.

### Fitness
Na função fitness é contado a quantidade de conflitos que há no indivíduo da população. Cada indivíduo representa uma solução para o quadro de horários. Validações feitas na fitness:
- Conflito de turma: uma mesma turma com mais de uma atividade no mesmo período
- Conflito de professor: um mesmo professor com mais de uma atividade no mesmo período
- Conflito de recurso: um mesmo recurso com mais de uma atividade no mesmo período
- Conflito de geminação: uma atividade que precisa ser geminada em aulas duplas não está geminada

### Crossover 
Inicialmente implementado dividindo as ativadades dos pais, da seguinte forma:
- Escolhe um ponto de corte aleatório
- As atividades do pai 1 até o corte vão para o filho A
- As atividades do pai 2 até o corte vão para o filho B
- As atividades do pai 1 após o corte vão para o filho B
- As atividades do pai 2 após o corte vão para o filho A

Podemos considerar, caso necessário, implementar o crossover por períodos. O que implica em organizar novamente a carga horária.

### Mutação
A mutação está ocorrendo da seguinte forma:
- É aplicada a "hardMutation". Nela é realizada uma nova distribuição aleatória da carga horária de uma atividade selecionada aleatoriamente dentre as atividades de um indivíduo.

Essa estratégia foi escolhida observando que é mais eficiente ter uma maior variedade para diminuir mais rapidamente a quantidade de conflitos.

## API

Copie o arquivo `example.env` como `.env` e substitua os valores das variáveis por valores reais.

Crie o ambiente virtual se ainda não existe:
```bash
# Windows
py -3 -m venv .venv

# Linux
python3 -m venv .venv
```

Ative o ambiente virtual:
```bash
# Windows
.venv\Scripts\activate

# Linux
. .venv/bin/activate
```

Execute a API:
```bash
pip install -r .\requirements.txt

flask --app app run
```

Após finalizar, pode desativar o ambiente virtual:
```bash
deactivate
```