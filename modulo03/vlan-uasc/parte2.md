<!-- PROFESSOR: os comandos de STP/RSTP são os da aula 11A e têm as mesmas pendências de bancada
(sintaxe na EXOS-VM 32.6, estado de fábrica do STP, se o Suspend do GNS3 derruba a porta dos dois
lados). Roteiro dos experimentos em sala, perguntas e respostas: gabarito/gabarito-parte2.md. -->

# Atividade a rede da UASC, parte 2: redundância com STP e RSTP

A rede que vocês entregaram na [parte 1](parte1.md) está em operação. Esta parte começa dela, **no estado final**, depois dos três pedidos de mudança, e tem entrega própria.

> **Ordem de serviço 0714**
>
> - **Solicitante:** STI/UFCG, a pedido da coordenação da UASC
> - **Cliente:** Unidade Acadêmica de Sistemas e Computação (UASC)
> - **Responsável:** a equipe de vocês
> - **Escopo:** religar o cabo da obra, tornar a rede redundante, com recuperação automática, e medir quanto tempo ela leva para se recuperar
> - **Entregáveis:** ver [Entrega](#entrega)

## Pedido 4: a obra acabou

> A obra do pedido 2 terminou, e o duto entre os dois laboratórios foi liberado. O cabo rompido foi consertado e volta a ser usado. A coordenação da UASC não quer passar outra vez pelo que aconteceu na obra: com o cabo de volta, a rede deve **continuar funcionando sozinha** se qualquer enlace entre os switches cair.

No pedido 2, vocês religaram o switch que ficou isolado por outro caminho. Por isso, quando o cabo da obra volta, a rede passa a ter um **ciclo**: dois caminhos entre os switches do ciclo. É o anel da aula 11A, agora na rede de vocês, com as VLANs de vocês.

## Antes de começar

- **Ponto de partida.** Abram o projeto GNS3 da parte 1, salvem uma cópia (*File → Save project as*) e tirem um snapshot (*Edit → Manage snapshots*). Tirem outro antes de cada etapa.
- **Comandos.** Os de STP e RSTP são os da aula 11A: [guia da aula 11A](../guia_de_aulas/11A/ROTEIRO.md), partes 2 a 4, e o [resumo dos comandos](#resumo-dos-comandos) no fim deste enunciado.
- **Recursos.** São quatro EXOS-VM, cerca de 1 GB de RAM cada. Fechem outros projetos do GNS3.

> ⚠️ **Receita de parada.** Se a CPU disparar e os consoles não responderem, suspendam o cabo da obra no GNS3 (botão direito no cabo → *Suspend*). O ciclo abre e a rede volta ao normal em alguns segundos.

> ⚠️ **Trocar o modo do STP com o ciclo fechado cria laço.** Enquanto o STP de um switch está desligado, as portas dele encaminham tudo. Antes de qualquer `disable stpd s0`, suspendam o cabo da obra; retomem só depois do `enable stpd s0` nos quatro switches.

## Etapa 1: o cabo volta, sem proteção

**Objetivo:** ver o laço acontecer na rede de vocês.

1. Com o cabo da obra ainda suspenso, desliguem o STP **nos quatro switches**, seja qual for o estado de fábrica:
   ```
   disable stpd s0
   ```
2. Nas duas pontas do cabo da obra, configurem as VLANs que vocês acham que ele deve levar. Registrem quais e por quê.
3. Retomem o cabo (*Resume*).
4. Gerem um broadcast numa VLAN que esteja em **todos** os enlaces do ciclo. Por exemplo, a ADM pingando um endereço da gerência que não existe: ela repete o pedido ARP, que é broadcast.
5. Num switch do ciclo, rodem duas vezes, com alguns segundos de intervalo, e guardem as saídas:
   ```
   show ports <portas do ciclo> statistics
   show fdb
   ```
6. Suspendam o cabo da obra e confiram que os contadores param de subir.

**O que guardar:** as saídas do passo 5 (ou capturas de tela), mostrando os contadores de broadcast disparando e o MAC da ADM aparecendo em portas diferentes.

## Etapa 2: STP (802.1D)

**Objetivo:** proteger o ciclo com o STP clássico e medir quanto tempo a rede leva para se recuperar.

Antes de configurar, decidam e registrem: **qual switch é a raiz**, qual é a **raiz reserva**, e por quê.

1. Com o cabo da obra suspenso, nos quatro switches:

   ```
   disable stpd s0
   configure stpd s0 mode dot1d
   configure stpd s0 add vlan <VLAN> ports all
   enable stpd s0
   ```

   A linha do `add vlan` se repete para cada VLAN que existe naquele switch.
2. Na raiz e na raiz reserva:

   ```
   configure stpd s0 priority 4096     (raiz)
   configure stpd s0 priority 8192     (raiz reserva)
   ```
3. Retomem o cabo da obra e esperem uns 30 s.
4. Nos switches do ciclo, `show stpd s0 ports`. **Qual porta ficou bloqueada?** Expliquem pela eleição da aula 11A (raiz, porta raiz, porta designada).

**Medição.**

1. Escolham um PC ligado a um switch do ciclo que **não** roteia, e descubram por qual enlace do ciclo passa o caminho dele até o gateway.
2. No PC: `ping <gateway> -t`.
3. Suspendam esse enlace e contem os pings perdidos até a resposta voltar: é o tempo de **queda**.
4. Retomem o enlace e contem de novo: é o tempo de **volta**.

## Etapa 3: RSTP

**Objetivo:** repetir a medição com o RSTP.

1. Suspendam o cabo da obra.
2. Nos quatro switches:

   ```
   disable stpd s0
   configure stpd s0 mode dot1w
   configure stpd s0 ports link-type point-to-point <portas entre switches>
   configure stpd s0 ports link-type edge <portas dos PCs>
   enable stpd s0
   ```

   As VLANs continuam no `s0` e as prioridades se mantêm.
3. Retomem o cabo. `show stpd s0 ports`: a mesma porta bloqueou? Que papel ela tem agora?
4. Repitam a medição da etapa 2: o **mesmo PC** e o **mesmo enlace**.

## Etapa 4: experimentos em sala

Em sala, o professor vai conduzir alguns experimentos com a rede de vocês, já em RSTP e com o ciclo fechado. Antes de cada um, tirem um snapshot. No fim de cada um, desfaçam o que ele pediu.

**Anotem o que observarem em cada experimento**: a documentação pergunta sobre isso. Não procurem a explicação antes: o objetivo é ver acontecer.

Disponivel em  : [experimento-sala.md](experimento-sala.md)

## Etapa 5: os testes de aceite com o ciclo

Os seis testes de aceite da [parte 1](parte1.md#etapa-3-testes-de-aceite), com as trocas do estado final, precisam passar em **todas** estas situações:

- com o ciclo completo;
- com **cada enlace do ciclo suspenso, um de cada vez**.

Se algum teste falhar com algum enlace suspenso, descubram a causa, corrijam e registrem a correção no histórico.

## Etapa 6: documentação

A documentação da parte 2 descreve a rede **no estado final desta parte** (RSTP, ciclo fechado) e precisa ter:

1. **Topologia com o ciclo.** Um desenho com os enlaces entre os switches, a raiz, a raiz reserva e a porta bloqueada (com o papel que ela tem no RSTP).
2. **VLANs em cada enlace do ciclo**, e quais VLANs estão no `s0` em cada switch. Se isso mudou depois dos experimentos ou da etapa 5, digam o que mudou e por quê.
3. **Evidência do laço** da etapa 1.
4. **Tabela de tempos**: pings perdidos na queda e na volta, com STP e com RSTP, informando o PC usado e o enlace suspenso.
5. **Registro dos experimentos** A, B e C: o que vocês observaram em cada um.

## Avaliação

A avaliação é feita em sala, com uma verificação ao vivo da rede no estado final desta parte.

- O professor suspende um enlace do ciclo, à escolha dele, e o grupo mostra a rede se recuperando e os testes de aceite passando.
- Um integrante sorteado na hora explica a raiz, a porta bloqueada ou as VLANs de um enlace do ciclo. Todos precisam conhecer a rede inteira.

## Entrega

Um único arquivo `entrega2-<equipe>.zip`, enviado pelo SIGAA, com a rede no **estado final da parte 2**:

```
entrega2-<equipe>.zip
├── uasc.gns3project      projeto GNS3 exportado (RSTP, ciclo fechado)
├── documentacao.pdf      documentação da parte 2
└── config/               configuração de cada switch
    ├── sw-lsd.txt
    ├── sw-lacina.txt
    ├── sw-lsi.txt
    └── sw-liad.txt
```

As regras de exportação e da pasta `config/` são as da [entrega da parte 1](parte1.md#entrega). Os três itens precisam estar coerentes entre si.

Uso de IA: lembrem de declarar e incluir o link ou o histórico do uso.
