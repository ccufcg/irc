# Guia prático da Aula: a Solução do problema do hub

Vamos substituir o hub por um switch e ver a conversa ficar restrita a quem participa dela.

### Troque o equipamento

No GNS3:

1. Pare a simulação (■ vermelho).
2. Selecione o **Hub** e apague (tecla *Delete*). Os links dele somem junto.
3. No painel esquerdo, em *Switches*, arraste o **Ethernet switch** para a área de trabalho.
4. Ligue a `eth0` (Ethernet0) de cada VM a uma porta do switch.
5. Inicie a simulação.


### Refaça o teste

Repita **exatamente** o que você fez na parte 1, na mesma ordem:

1. **VM-1:** recrie o `index.html` e rode `python3 -m http.server 8000` (passo 1.1; o arquivo em `/root/lab` pode ter sobrevivido, confira com `ls /root/lab`).
2. **VM-3:** comece a escutar. No Wireshark, clique com o botão direito no link entre a **VM-3** e o **switch** e escolha *Start capture*. Ou rode `tcpdump -ni eth0 -e -A 'arp or tcp port 8000'`.
3. **VM-2:** `curl http://10.0.0.1:8000/`
4. **VM-1:** `ping -c 3 10.0.0.2` (com `tcpdump -ni eth0 -e icmp` na VM-3).

O que acontece? Qual o Resultado?

| O quê                      | Com hub       | Com switch     |
| --------------------------- | ------------- | -------------- |
| `curl` da VM-2 funciona   | sim           |             |
| VM-3 vê o ARP (broadcast)  | sim           |  |
| VM-3 vê o HTML e o`ping` | **sim** |  |


O switch **aprende** em qual porta cada MAC está (olhando o MAC de origem dos quadros) e passa a encaminhar o quadro **só** para a porta do destino. Esse é o assunto da seção 3 da aula.
