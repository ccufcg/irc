# Instalando o EXOS VM no GNS3

Este guia assume que o GNS3 já está instalado e funcionando na sua máquina, seja via VM do GNS3 rodando no Hyper-V, seja por qualquer outro modo de instalação. O foco aqui é só a importação do appliance EXOS VM e a verificação do primeiro boot.

## 1. O que é o EXOS VM

O EXOS VM é a imagem virtual do ExtremeXOS mantida pela própria Extreme Networks, publicada como appliance oficial no catálogo do GNS3 (categoria "multilayer switch"). Ele reproduz o comportamento de um switch L3 real da Extreme, o que mantém a aula consistente com os switches físicos que chegam mais adiante no curso.

**Onde encintrar** : 
    - https://www.gns3.com/marketplace/appliances/exos-vm

- ⚠️ utilizem o `EXOS VM 32.6.3.126`

## 2. Importando o appliance

Siga as instruções dessa pagina:

https://docs.gns3.com/docs/using-gns3/beginners/import-gns3-appliance/


Há mais de uma versão listada (por exemplo 33.6.1.14 e 32.7.2.19). Se você já souber a versão de EXOS que vai rodar nos switches físicos que chegam depois, prefira a mesma, para manter a CLI consistente entre o laboratório virtual e o equipamento real.

#### ⚠️ Para os nossos laboratorios utilizaremos a Versão
- EXOS VM 32.6.3.126


## 3. Nested virtualization no Hyper-V ou equivalente

Como o GNS3 roda dentro de uma VM no Hyper-V, a aceleração KVM que o appliance usa por padrão só funciona se a virtualização aninhada estiver habilitada para essa VM no host Hyper-V. Sem isso, o EXOS VM ainda funciona, mas por emulação de software, bem mais lento para subir.

Antes de montar uma topologia com vários EXOS ao mesmo tempo, vale testar com um único nó primeiro, para confirmar que o boot está rápido o suficiente para uso em aula.

Por exemplo no Hyper-V eu fiz assim:

```ps1
Set-VMProcessor -VMName "GNS3 VM" -ExposeVirtualizationExtensions $true
```

Verifiquem no computador de vocês


## 4. Teste

Com o EXOS VM instalado e testado, o roteiro de demonstração ([`demo.md`](../modulo01/demo.md)) parte do princípio de que os nós já estão importados e prontos para uso, cobrindo a montagem da topologia e a configuração de VLAN, IP, roteamento e teste de conectividade.
