# ACL na rede da UASC

A rede da UASC que vocês implantaram e tornaram redundante está em operação ([parte 1](../vlan-uasc/parte1.md) e [parte 2](../vlan-uasc/parte2.md)). Ela funciona, mas tudo o que a VLAN e o roteamento permitem passa. Nesta atividade, cada equipe encontra um problema real nessa rede que uma **ACL** resolve, implanta a solução no GNS3 e a apresenta num seminário.

> - **Escopo:** identificar um problema na rede da UASC, resolvê-lo com ACL (camada 2, 3 ou 4), provar a solução em bancada e apresentá-la
> - **Entregáveis e prazo:** ver [Entrega](#entrega)

A equipe escolhe o problema.

**Não há lista pronta**: encontrem um problema. Comecem pelo [levantamento do STI](../vlan-uasc/parte1.md#levantamento-do-sti), pelo que a rede de vocês permite hoje e não deveria, e pela seção de ACL da aula 12.

| Roteiro                                                                                  |
| ---------------------------------------------------------------------------------------- |
| [Proposta](#etapa-1-proposta): escolhe o problema e o submete ao professor                |
| [Implantação](#etapa-2-implantação-em-bancada): escreve e aplica a ACL no GNS3        |
| [Testes](#etapa-3-testes): prova que a ACL resolve o problema e não quebra o resto       |
| [Seminário](#etapa-4-seminário): apresenta o problema e a solução, com demonstração |

## Etapa 1: proposta

A equipe envia/discute em sala de aula (sexta-feira) com o professor um parágrafo com:

1. **O problema:** o que a rede permite hoje e não deveria (ou o que precisa medir), e quem é afetado.
2. **Onde ele acontece:** os switches, as portas e as VLANs envolvidas.
3. **Por que ACL?**
4. **A fonte que leram:** documentação do fabricante

Regras da proposta:

- O problema precisa existir **na rede de vocês**, como ela está no estado final da parte 2.
- A ACL pode ser de camada **2** (MAC, VLAN, EtherType), **3** (endereço IP, protocolo) ou **4** (porta TCP/UDP).
- **Não há problemas repetidos.** Se duas equipes propuserem o mesmo, fica com a primeira proposta aprovada; a outra escolhe outro.
  - Talvez permita duas propostas similares

## Etapa 2: implantação em bancada

Escrevam a ACL e apliquem-na na rede de vocês. Decidam e registrem:

- **Onde aplicar:** em quais portas ou VLANs, e em qual switch. Lembrem que o tráfego entre dois PCs da mesma VLAN, no mesmo switch, nunca passa pelo switch que roteia.
- **Em que sentido:** entrada (*ingress*) funciona em qualquer modelo; saída (*egress*) só em alguns. Usem entrada.
- **A ordem das regras** e o que acontece com o quadro que não casa com nenhuma: no EXOS, a ação padrão é **permitir**.
- **Pelo menos uma regra com `count`**, para mostrar na demonstração quantos quadros ou pacotes ela pegou.

## Etapa 3: testes

1. **Antes e depois.** Mostrem o tráfego do problema passando sem a ACL e barrado (ou contado) com ela. Guardem as saídas ou capturas.
2. **Contador.** `show access-list counter` (ou o equivalente da ACL dinâmica) antes e depois do teste: ele precisa subir.
3. **Efeito colateral.** Os seis [testes de aceite da parte 1](../vlan-uasc/parte1.md#etapa-3-testes-de-aceite), com as trocas do estado final, precisam continuar passando com a ACL aplicada. Se algum falhar, ajustem a ACL e registrem o que mudou.
4. **Limite.** Encontrem pelo menos uma situação que a ACL de vocês **não** resolve, e expliquem por quê.

## Etapa 4: seminário

Cada equipe tem **10 minutos** para a apresentação com a demonstração e perguntas.

Os slides precisam ter:

1. **O problema**, explicado sobre a **topologia**: o recorte da rede da UASC envolvido, com os switches, as portas e as VLANs, e onde a ACL fica.
2. **Os comandos:** a ACL completa (regras na ordem, critérios e ações) e o comando que a aplica.
3. **A ação padrão** e por que a ordem das regras é a que vocês escolheram.
4. **Os resultados dos testes:** antes e depois, o contador e os testes de aceite.
5. **O limite** encontrado na etapa 3.
6. **A fonte** que leram.

**Demonstração ao vivo no GNS3.** Com a ACL aplicada, mostrem o tráfego do problema sendo barrado (ou contado), o contador subindo e um tráfego legítimo que continua funcionando. Deixem o projeto aberto e testado antes da apresentação.

## Avaliação

A avaliação é feita no seminário

## Entrega

Um único arquivo `entrega-acl-<equipe>.zip`, enviado pelo SIGAA até [data], com a rede no estado final desta atividade:

```
entrega-acl-<equipe>.zip
├── uasc.gns3project      projeto GNS3 exportado, com a ACL aplicada
├── slides.pdf            os slides do seminário
├── acl/                  os arquivos de política (.pol), se usarem
└── config/               configuração de cada switch
    ├── sw-lsd.txt
    ├── sw-lacina.txt
    ├── sw-lsi.txt
    └── sw-liad.txt
```

Uso de IA: declarem e incluam o link ou o histórico do uso. A sintaxe de ACL inventada por IA é um erro comum: confiram cada comando na documentação e na bancada.

**Documentação da Extreme** (páginas das versões 31 a 33; confiram cada comando na EXOS-VM 32.6 da bancada):

- [ACL Rule Syntax](<https://documentation.extremenetworks.com/ExtremeXOS%20v33.1.1%20User%20Guide/GUID-F5115642-1799-43B1-A3D7-A85C95BC1EE7.shtml>): os critérios (*match conditions*) de camada 2, 3 e 4 e as ações
- [Example ACL Rule Entries](https://documentation.extremenetworks.com/exos_22.3/GUID-DA6C8B4B-DDED-4CAB-8D55-508C40F31A91.shtml): exemplos de regras, inclusive o cuidado com o ARP numa regra que nega tudo
- [create access-list](https://documentation.extremenetworks.com/exos_commands_31.7/GUID-FCEC8547-5175-444B-8005-4AB19F6DE162.shtml) e [configure access-list add](<https://documentation.extremenetworks.com/ExtremeXOS%20v33.1.1%20Command%20References/GUID-0C921515-10C7-4433-9E57-AD2918C94FE7.shtml>): a ACL dinâmica
