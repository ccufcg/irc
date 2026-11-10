"""Gera o cenario da aula 11B (11B-anel.gns3project) a partir do molde 9-vlan.

Uso (nesta pasta):
    python3 gerar_11B_anel.py [molde.gns3project] [saida.gns3project]
Padrao: molde = 9-vlan.gns3project, saida = 11B-anel.gns3project.

O que sai (o anel da 11A, mais o que a 11B usa):
  - SW-CP, SW-CN, SW-CO: copia da definicao do EXOS do molde (imagem, RAM, 13 portas),
    com node_id e MAC novos e sem disco proprio (o GNS3 cria um disco de fabrica ao ligar);
  - PC1..PC4 em VPCS, com o IP da tabela no startup.vpc;
  - anel CP:11-CN:11, CN:12-CO:12, CO:11-CP:12 e hosts nas portas 1 e 2;
  - segundo cabo CP:10-CN:10 (o segundo membro do LAG);
  - HUB-SALA (o "switch domestico" ligado em duas tomadas) nas portas 3 e 4 do SW-CN.
  Vem suspenso todo cabo que fecharia um laco no boot (portas de fabrica na Default):
  CO-CP, CP:10-CN:10 e HUB-SALA-CN:4.
Cada execucao gera IDs e MACs novos: depois de publicar, nao regenere sem necessidade.
Testado so na estrutura (GNS3 2.2.61); abrir no GNS3 antes de publicar.
"""
import json, uuid, zipfile, copy, sys, os

aqui = os.path.dirname(os.path.abspath(__file__))
molde_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(aqui, "9-vlan.gns3project")
out_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(aqui, "11B-anel.gns3project")
with zipfile.ZipFile(molde_path) as zm:
    molde = json.loads(zm.read([n for n in zm.namelist() if n.endswith('.gns3')][0]))
exos_molde = copy.deepcopy([n for n in molde['topology']['nodes'] if n['name'] == 'SW-01'][0])

LABEL_STYLE = "font-family: TypeWriter;font-size: 10.0;font-weight: bold;fill: #000000;fill-opacity: 1.0;"
VPCS_TEMPLATE = "19021f99-e36f-394d-b4a1-8aaa902ab9cc"   # template interno do VPCS no GNS3 2.2

macs = set()
def novo_id_com_mac():
    while True:
        nid = str(uuid.uuid4())
        h = nid.replace('-', '')
        mac = f"0c:{h[2:4]}:{h[4:6]}:{h[6:8]}:00:00"   # mesmo padrão do GNS3 (ver SW-01 do molde)
        if mac not in macs:
            macs.add(mac); return nid, mac

nodes, ids = [], {}
console = 5000
for nome, x, y in [("SW-CP", -25, -250), ("SW-CN", -300, 0), ("SW-CO", 250, 0)]:
    n = copy.deepcopy(exos_molde)
    nid, mac = novo_id_com_mac()
    n.update(name=nome, node_id=nid, console=console, x=x, y=y, z=1)
    n['label'] = dict(rotation=0, style=LABEL_STYLE, text=nome, x=0, y=-25)
    n['properties']['mac_address'] = mac
    nodes.append(n); ids[nome] = nid; console += 2

vpcs_cfg = {}
for nome, ip, gw, x, y in [("PC1", "10.0.10.21", "10.0.10.1", -450, 220),
                           ("PC2", "10.0.20.22", "10.0.20.1", -200, 220),
                           ("PC3", "10.0.10.31", "10.0.10.1", 150, 220),
                           ("PC4", "10.0.20.32", "10.0.20.1", 400, 220)]:
    nid = str(uuid.uuid4())
    nodes.append({
        "compute_id": "vm", "console": console, "console_auto_start": False,
        "console_type": "telnet", "custom_adapters": [], "first_port_name": None,
        "height": 59, "label": dict(rotation=0, style=LABEL_STYLE, text=nome, x=18, y=-25),
        "locked": False, "name": nome, "node_id": nid, "node_type": "vpcs",
        "port_name_format": "Ethernet{0}", "port_segment_size": 0, "properties": {},
        "symbol": ":/symbols/vpcs_guest.svg", "template_id": VPCS_TEMPLATE,
        "width": 65, "x": x, "y": y, "z": 1})
    ids[nome] = nid; console += 2
    vpcs_cfg[nid] = f"set pcname {nome}\nip {ip} {gw} 24\n"

# HUB-SALA: hub do GNS3 (mesmo template interno do hub da aula 8A)
hub_id = str(uuid.uuid4())
nodes.append({
    "compute_id": "vm", "console": None, "console_auto_start": False, "console_type": None,
    "custom_adapters": [], "first_port_name": None, "height": 32,
    "label": dict(rotation=0, style=LABEL_STYLE, text="HUB-SALA", x=0, y=-25),
    "locked": False, "name": "HUB-SALA", "node_id": hub_id, "node_type": "ethernet_hub",
    "port_name_format": "Ethernet{0}", "port_segment_size": 0,
    "properties": {"ports_mapping": [{"name": f"Ethernet{i}", "port_number": i} for i in range(8)]},
    "symbol": ":/symbols/hub.svg", "template_id": "b4503ea9-d6b6-3695-9fe4-1db3b39290b0",
    "width": 72, "x": -330, "y": 330, "z": 1})
ids["HUB-SALA"] = hub_id

def ponta(nome, porta):
    if nome.startswith("SW-"):     # EXOS: adaptador N = PortN
        return {"adapter_number": porta, "node_id": ids[nome], "port_number": 0,
                "label": dict(rotation=0, style=LABEL_STYLE, text=f"Port{porta}", x=10, y=10)}
    if nome == "HUB-SALA":         # hub: adaptador 0, porta N
        return {"adapter_number": 0, "node_id": ids[nome], "port_number": porta,
                "label": dict(rotation=0, style=LABEL_STYLE, text=f"e{porta}", x=10, y=10)}
    return {"adapter_number": 0, "node_id": ids[nome], "port_number": 0,     # VPCS
            "label": dict(rotation=0, style=LABEL_STYLE, text="Ethernet0", x=10, y=10)}

cabos = [  # anel: CP:11-CN:11, CN:12-CO:12, CO:11-CP:12 ; hosts nas portas 1 e 2
    (("SW-CP", 11), ("SW-CN", 11)),
    (("SW-CN", 12), ("SW-CO", 12)),
    (("SW-CO", 11), ("SW-CP", 12)),
    (("SW-CN", 1), ("PC1", 0)), (("SW-CN", 2), ("PC2", 0)),
    (("SW-CO", 1), ("PC3", 0)), (("SW-CO", 2), ("PC4", 0)),
    (("SW-CP", 10), ("SW-CN", 10)),                      # segundo membro do LAG
    (("SW-CN", 3), ("HUB-SALA", 0)), (("SW-CN", 4), ("HUB-SALA", 1)),   # tomada -> hub -> tomada
]
SUSPENSOS = {(("SW-CO", 11), ("SW-CP", 12)), (("SW-CP", 10), ("SW-CN", 10)),
             (("SW-CN", 4), ("HUB-SALA", 1))}
links = [{"filters": {}, "link_id": str(uuid.uuid4()),
          "link_style": {"color": "#000000", "type": 1, "width": 2},
          "nodes": [ponta(*a), ponta(*b)], "suspend": (a, b) in SUSPENSOS} for a, b in cabos]

proj = {k: molde[k] for k in molde if k != 'topology'}
proj.update(name="11B-anel", project_id=str(uuid.uuid4()), show_interface_labels=True)
proj['topology'] = {"computes": [], "drawings": [], "links": links, "nodes": nodes}

with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr("project.gns3", json.dumps(proj, indent=4, ensure_ascii=False))
    z.writestr("README.txt", "Project: '11B-anel'\nAuthor: Thiago Nobrega\n\n"
               "Roteiro da aula 11B: anel SW-CP / SW-CN / SW-CO (LACP, protecoes de borda, EAPS)\n")
    for d in ("project-files/images/", "project-files/captures/", "project-files/vpcs/"):
        z.writestr(d, "")
    for nid, cfg in vpcs_cfg.items():
        z.writestr(f"project-files/vpcs/{nid}/startup.vpc", cfg)
print("gerado:", out_path)
