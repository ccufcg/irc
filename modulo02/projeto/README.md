# Projeto de Cabeamento Estruturado

Este projeto pede o desenho completo do cabeamento estruturado do Bloco CP, nos seus três pavimentos. 
A entrega cobre desde o levantamento de pontos até o orçamento de material.

O trabalho é feito em equipe. Cada equipe projeta o prédio inteiro (os três pavimentos), com o nível de detalhe descrito em cada item abaixo.

**Sumário**

- [Material fornecido](#material-fornecido)
- [Entregas](#entregas)
  - [Entrega 1: Levantamento (miniavaliação)](#entrega-1-levantamento-miniavaliação)
  - [Entrega 2: Projeto e documentação (entrega final do módulo)](#entrega-2-projeto-e-documentação-entrega-final-do-módulo)
    - [a) Planta](#a-planta)
    - [b) Tabela de distância por tomada](#b-tabela-de-distância-por-tomada)
    - [c) Backbone entre pavimentos (nível conceitual)](#c-backbone-entre-pavimentos-nível-conceitual)
    - [d) Lista de materiais](#d-lista-de-materiais)
    - [e) Orçamento de material](#e-orçamento-de-material)
    - [f) Plano de endereçamento IP](#f-plano-de-endereçamento-ip)
  - [Regras e técnicas](#regras-e-técnicas)
  - [Formato de entrega](#formato-de-entrega)
  - [Critérios de avaliação](#critérios-de-avaliação)
- [Uso de IA](#uso-de-ia)

## Material fornecido

Para esta atividade vocês podem utilizar
- `plantas/PLANTA_BAIXA_CP.drawio`: arquivo **editável**, base para as equipes desenharem o traçado de eletrocalha/eletroduto.
- `plantas/pdf/: planta de cada pavimento em PDF.
- `planilhas-projeto-cabeamento.xlsx`: Um modelo para sumarizar alguns elementos de um projeto;
<!-- - `relatorio-modelo.md`: modelo de relatório para a Entrega 2 (itens c e f) —
  pode e deve ser alterado pela equipe, ver [Formato de entrega](#formato-de-entrega). -->

As plantas trazem só a arquitetura (paredes, mobiliário, cotas, nome dos ambientes), sem nenhuma solução de cabeamento desenhada. As cotas já presentes na planta servem de referência de escala:
qualquer medição feita sobre a planta deve ser conferida contra uma dessas cotas antes de entrar nas tabelas.

## Entregas

Para este projeto teremos duas entregas:

### Entrega 1: Levantamento (miniavaliação)

- Contagem de pontos por ambiente nos três pavimentos (dados, voz, Wi-Fi/AP),
  preenchida na aba **1. Contagem de Pontos** da planilha.
- A equipe visita o prédio e confere, em pelo menos três
  ambientes por pavimento, se a planta fornecida bate com a realidade (portas,
  divisórias, ambientes remembrados). Divergências encontradas entram como
  observação na própria planilha.

> Para esta entrega basta anexar a tabela no formulario indicado

### Entrega 2: Projeto e documentação (entrega final do módulo)

#### **a) Planta**

Sobre a planta fornecida (`plantas/PLANTA_BAIXA_CP.drawio`), desenhar o traçado de
eletrocalha e/ou eletroduto para os três pavimentos, com cada trecho identificado
por um código.

> A definição do codigo deve vir descrita na planta ou em um documeto

Essa indexação vale para o prédio inteiro: todo trecho de rota horizontal/vertical desenhado
recebe um código, e todo código usado na planta precisa aparecer na coluna **Rota**
da tabela de distância por tomada (item b) e na lista de materiais (item d), com a
metragem correspondente.

#### **b) Tabela de distância por tomada**

Uma linha por tomada de telecomunicações (TO), na aba **2. Distância por Tomada**
da planilha, cobrindo todas as tomadas dos três pavimentos, com:

- a rota até a sala de telecom do pavimento, escrita como sequência de códigos;
- a distância horizontal medida sobre a planta calibrada;
- a folga vertical e a margem de manobra (a planilha já traz a premissa padrão de
  3,00 m + 0,30 m; ajustar linha a linha se a equipe tiver um valor melhor,
  registrando a mudança);
- o total estimado, calculado automaticamente, e o resultado da checagem contra o
  limite de 90 m de cabo permanente.

Medir a distância pela rota real (pelo trajeto de eletrocalha/eletroduto), nunca em
linha reta na planta.

#### **c) Backbone entre pavimentos (nível conceitual)**

Diagrama de topologia do backbone óptico ligando as salas de telecom dos três
pavimentos: tipo de fibra, número de fibras por enlace e justificativa de
dimensionamento (fibras ativas mais reserva). Não é pedido orçamento de perda óptica
(budget de potência) neste projeto.

#### **d) Lista de materiais**

Quantitativo de material na aba **3. Lista de Materiais** da planilha: cabo por
categoria e metragem total (somada a partir da tabela de distâncias, com folga para
curvas e emendas, percentual a critério da equipe e justificado), conectores,
patch panels, racks, eletrocalha e eletroduto por tipo/bitola, tomadas. Sem mão de
obra.

#### **e) Orçamento de material**

Aba **4. Orçamento** da planilha, preço pesquisado pela própria equipe para cada
item da lista de materiais. Cada linha precisa de fonte (link ou nome do
fornecedor) e data da cotação. Todas as equipes pesquisam os mesmos itens (os da
Lista de Materiais), o que muda é o fornecedor e o preço encontrado.

#### **f) Plano de endereçamento IP**

Plano de VLSM usando obrigatoriamente o bloco `10.0.0.0/8` como rede-base. A
equipe decide o critério de divisão em sub-redes (por pavimento, por ambiente, por
tipo de uso), desde que justificado e dimensionado pelo número real de pontos
levantado na Entrega 1 (contando folga de crescimento, se a equipe optar por isso,
também justificada). Entregar a tabela de sub-redes (endereço de rede, máscara,
faixa de hosts utilizável, broadcast) e uma frase de justificativa por critério de
divisão escolhido.

> Utilizar um documento separado.

### Regras e técnicas

- Toda distância medida pela rota real, nunca em linha reta.
- Toda rota desenhada na planta precisa de código e esse código
  precisa aparecer na planilha.
- VLSM a partir de `10.0.0.0/8`, sem exceção.


### Formato de entrega

Todos os arquivos de devem ser compactados em um arquivo compactado `entrega-<equipe>.zip` e depositado no SIGAA ou formulario indicado com os sequintes elementos:

- `planta-<equipe>.drawio` **e** `planta-<equipe>.pdf`  
- `relatorio-<equipe>.pdf`: texto consolidado com os itens (c) e (f) mais a planta (pode ser a exportação da planta editada, ou fotos/prints legíveis dela).
  Usar como base o modelo `relatorio-modelo.md` — ele **pode e deve ser alterado**
  pela equipe, é só um ponto de partida com a estrutura mínima esperada.
- `planilhas-<equipe>.xlsx`: a planilha modelo preenchida (abas 1 a 4).
- `README.txt` : Vocês podem incluir outros arquivos e devem descrever o conteudo nesse arquivo


### Critérios de avaliação

- Conformidade com os conceitos vistos em sala de aula.
- Coerência entre a planta, a tabela de distâncias e a lista de materiais (todo código usado num lugar aparece nos outros dois, com a mesma metragem).
- Consistência do orçamento
- Justificativa técnica das escolhas 
- Clareza da documentação
<!-- - Correção do plano de VLSM (dimensionamento pelo número real de pontos, ausência de sobreposição de faixas, máscara coerente com o critério escolhido). -->

## Uso de IA

Segue a política já definida para a disciplina: uso livre para dúvidas conceituais,
revisão e rascunho; uso declarado (com a equipe capaz de explicar e defender o que
foi gerado); uso não permitido para substituir o entendimento da equipe sobre o próprio projeto durante a apresentação/arguição. **Caso utilize LLM colocar um arquivo com o link para os prompts utilizados e resumir o uso**.