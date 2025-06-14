# A* Pathfinding Visualizer

Este projeto é uma implementação visual e interativa do algoritmo A* (A-star) em Python, permitindo explorar, aprender e experimentar o funcionamento do algoritmo de busca de caminho em grids 2D.

## Funcionalidades

- Visualização animada do algoritmo A* em tempo real.
- Interface gráfica interativa com PyQt5 (recomendada).
- Permite posicionar barreiras, ponto de início e objetivo manualmente.
- Mensagem clara quando não há caminho possível.
- Visualização passo a passo do algoritmo (células exploradas e fronteira).
- Legenda de ícones coloridos, centralizada e legível.
- Interface centralizada e moderna.
- Reinício rápido da configuração sem fechar o programa.
- Código limpo, modular e fácil de entender.

## Como usar

1. **Instale as dependências:**

```bash
pip install numpy PyQt5
```

2. **Execute o visualizador PyQt5:**

```bash
python src/pyqt_visualizer.py
```

3. **Controles da interface:**

- Clique no grid para adicionar/remover barreiras (modo padrão).
- Tecle `S` para selecionar o modo início e clique para posicionar o ponto de partida.
- Tecle `G` para selecionar o modo objetivo e clique para posicionar o destino.
- Tecle `B` para voltar ao modo barreira.
- Tecle `Enter` ou clique em "Rodar A*" para iniciar a busca do caminho.
- Se não houver caminho possível, será exibida uma mensagem no grid.
- Após a execução, tecle `R` ou clique em "Resetar" para reiniciar a configuração e experimentar novamente.

## Estrutura do Projeto

```
a_star_project/
├── src/
│   ├── a_star.py           # Implementação do algoritmo A*
│   ├── pyqt_visualizer.py  # Visualizador principal (PyQt5)
│   ├── utils.py            # Funções auxiliares (custo, vizinhos)
│   └── visualize.py        # Visualização do grid e animação (Matplotlib, legado)
├── tests/
│   └── test_a_star.py      # Testes unitários
├── requirements.txt        # Dependências do projeto
└── README.md               # Este arquivo
```

## Sobre o Algoritmo A*

O A* é um algoritmo de busca heurística eficiente para encontrar o menor caminho entre dois pontos em um grafo ou grid, amplamente utilizado em jogos, robótica e IA. Ele combina o custo real do caminho e uma estimativa heurística (neste projeto, a distância de Manhattan).

## Heurísticas no A*

O algoritmo A* utiliza uma função heurística para estimar o custo restante até o objetivo. A escolha da heurística é fundamental para garantir eficiência e correção:

- **Heurística admissível:** nunca superestima o custo real até o objetivo, garantindo que o A* encontre o menor caminho.
- **Heurística consistente (ou monótona):** para todo nó n e vizinho n', o custo estimado de n até o objetivo é menor ou igual ao custo de ir até n' mais a estimativa de n' até o objetivo.

### Por que Manhattan?

Neste projeto, foi utilizada a distância de Manhattan como heurística, pois:

- É ideal para grids onde só é possível mover-se em quatro direções (cima, baixo, esquerda, direita), como neste visualizador.
- É simples, rápida de calcular e sempre admissível e consistente nesse contexto.
- Garante que o A* encontre o menor caminho sem explorar caminhos desnecessários.

Se o grid permitisse movimentos diagonais, outras heurísticas como a distância Euclidiana poderiam ser mais apropriadas.

## Créditos

Desenvolvido por Henrique Alonso.