# grupo FGA SISTEMAS - Gustavo rm570720 - Felipe Eloy rm573404 - Andrey rm569922

import json
import urllib.request
import urllib.error
from datetime import datetime

ARQUIVO = "dados_camera.json"

MODOS = {
    1: ("RETRATO", "12MP"),
    2: ("VÍDEO", "4K 24FPS"),
    3: ("FOTO", "12MP"),
    4: ("CÂMERA LENTA", "1080P 240FPS"),
    5: ("CINEMA", "4K 60FPS")
}

CIDADES = {
    1: ("São Paulo", -23.55, -46.63),
    2: ("Rio de Janeiro", -22.91, -43.17),
    3: ("Belo Horizonte", -19.92, -43.94),
    4: ("Curitiba", -25.43, -49.27)
}


def ler_numero(msg, minimo, maximo):
    while True:
        try:
            valor = int(input(msg))
            if minimo <= valor <= maximo:
                return valor
            print(f"Digite um numero entre {minimo} e {maximo}.")
        except ValueError:
            print("Digite apenas numeros, tente de novo.")


def carregar_dados():
    padrao = {
        "camera": {"modo": "FOTO", "qualidade": "12MP", "flash": False, "timer": "OFF", "zoom": "1.0x"},
        "configuracoes": {"grade": False, "modo noturno": False, "estabilizacao": True,
                          "hdr": False, "som da camera": True, "localizacao": False},
        "galeria": []
    }
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return padrao


def salvar_dados(camera, configuracoes, galeria):
    dados = {"camera": camera, "configuracoes": configuracoes, "galeria": galeria}
    try:
        with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
    except OSError:
        print("Erro: nao foi possivel salvar os dados.")


def mostrar_camera(camera):
    str_flash = "[⚡]" if camera["flash"] else "[⚡̸]"
    str_timer = f"⏱️ {camera['timer']}"

    print("\n==========================================")
    print(f" {camera['qualidade']}         {str_flash}        {str_timer}  ⚙️")
    print("------------------------------------------")
    print(" |                                       |")
    print(" |                                       |")
    print(f" |               ┌───┐            {camera['zoom']} |")
    print(" |               │   │             │     |")
    print(" |               └───┘             ●     |")
    print(" |                                       |")
    print("------------------------------------------")

    linha_modos = "  "
    for numero in MODOS:
        nome = MODOS[numero][0]
        if nome == camera["modo"]:
            linha_modos += f"[{nome}] "
        else:
            linha_modos += f"{nome} "
    print(linha_modos)
    print("------------------------------------------")
    print("  [🖼️ Galeria]      [ ⚪ CAPTURAR ]      [🔍 Zoom]")
    print("==========================================")


def menu_principal():
    print("\nComandos Rápidos:")
    print("1 - ⚪ Tirar Foto / Gravar Vídeo")
    print("2 - ↔️ Alternar Modo")
    print("3 - ⚡ Ligar/Desligar Flash")
    print("4 - ⏱️ Ajustar Timer")
    print("5 - 🔍 Alternar Zoom (1.0x / 2.0x)")
    print("6 - 🖼️ Abrir Galeria")
    print("7 - ⚙️ Configurações")
    print("8 - 🤖 Câmera Inteligente JOVI")
    print("0 - 🔴 Desligar Câmera")


def trocar_modo(camera):
    print("\nEscolha o modo:")
    for numero in MODOS:
        print(f"{numero} - {MODOS[numero][0]}")

    opcao = ler_numero("Opcao: ", 1, 5)
    camera["modo"] = MODOS[opcao][0]
    camera["qualidade"] = MODOS[opcao][1]
    print(f"Modo alterado para {camera['modo']}.")
    return camera


def alternar_flash(camera):
    camera["flash"] = not camera["flash"]
    status = "LIGADO" if camera["flash"] else "DESLIGADO"
    print(f"Flash {status}.")
    return camera


def ajustar_timer(camera):
    print("\nOpcoes de Temporizador:")
    print("1 - Desligado (OFF)")
    print("2 - 3 segundos")
    print("3 - 10 segundos")

    opcao = ler_numero("Opcao: ", 1, 3)
    if opcao == 1:
        camera["timer"] = "OFF"
    elif opcao == 2:
        camera["timer"] = "3s"
    else:
        camera["timer"] = "10s"
    print(f"Timer ajustado para: {camera['timer']}")
    return camera


def alternar_zoom(camera):
    if camera["zoom"] == "1.0x":
        camera["zoom"] = "2.0x"
    else:
        camera["zoom"] = "1.0x"
    print(f"Zoom alterado para: {camera['zoom']}")
    return camera


def capturar_midia(camera, galeria):
    if camera["timer"] != "OFF":
        print(f"Aguardando temporizador de {camera['timer']}...")

    tipo = "foto" if camera["modo"] in ["FOTO", "RETRATO"] else "video"

    nome = input("Digite um nome para a captura (ou ENTER para padrao): ")
    if nome == "":
        nome = f"{tipo}_{len(galeria) + 1}"

    item = {
        "nome": nome,
        "tipo": tipo,
        "modo": camera["modo"],
        "qualidade": camera["qualidade"],
        "data": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    galeria.append(item)
    print(f"📸 Capturado com sucesso: {nome} [{tipo.upper()}]")
    return galeria


def ver_galeria(galeria):
    print("\n----- 🖼️ GALERIA DE MÍDIAS -----")
    if len(galeria) == 0:
        print("A galeria esta vazia.")
        return galeria

    for i in range(len(galeria)):
        item = galeria[i]
        print(f"{i + 1} - {item['nome']} | {item['tipo']} | {item['modo']} | {item['data']}")

    print("\n1 - Apagar item")
    print("0 - Voltar")
    opcao = ler_numero("Opcao: ", 0, 1)
    if opcao == 1:
        numero = ler_numero("Numero do item que quer apagar: ", 1, len(galeria))
        removido = galeria.pop(numero - 1)
        print(f"Item '{removido['nome']}' removido.")
    return galeria


def tela_configuracoes(configuracoes):
    while True:
        print("\n----- ⚙️ CONFIGURAÇÕES -----")
        chaves = list(configuracoes.keys())

        for i in range(len(chaves)):
            status = "LIGADO" if configuracoes[chaves[i]] else "DESLIGADO"
            print(f"{i + 1} - {chaves[i].title()}: {status}")
        print(f"{len(chaves) + 1} - Voltar")

        opcao = ler_numero("Escolha uma opcao: ", 1, len(chaves) + 1)
        if opcao == len(chaves) + 1:
            return configuracoes
        chave = chaves[opcao - 1]
        configuracoes[chave] = not configuracoes[chave]


def buscar_clima(latitude, longitude):
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}"
           f"&current=temperature_2m,cloud_cover,is_day")
    try:
        with urllib.request.urlopen(url, timeout=8) as resposta:
            dados = json.loads(resposta.read().decode("utf-8"))
        return dados["current"]
    except (urllib.error.URLError, TimeoutError, KeyError, json.JSONDecodeError):
        return None


def aplicar_cena(camera, configuracoes, cena):
    if cena == "BAIXA LUZ":
        camera["modo"], camera["qualidade"] = "FOTO", "12MP"
        configuracoes["modo noturno"] = True
    elif cena == "MOVIMENTO":
        camera["modo"], camera["qualidade"] = "VÍDEO", "4K 24FPS"
        configuracoes["estabilizacao"] = True
    elif cena == "RETRATO":
        camera["modo"], camera["qualidade"] = "RETRATO", "12MP"
        configuracoes["hdr"] = True
    elif cena == "COMIDA":
        camera["modo"], camera["qualidade"] = "FOTO", "12MP"
        configuracoes["hdr"] = True
        configuracoes["grade"] = True
    else:
        camera["modo"], camera["qualidade"] = "FOTO", "12MP"
        configuracoes["hdr"] = True
        configuracoes["grade"] = True

    print(f"\n🤖 Cena reconhecida: {cena}")
    print(f"Modo {camera['modo']} ({camera['qualidade']}) e ajustes ligados automaticamente!")
    return camera, configuracoes


def camera_inteligente(camera, configuracoes):
    print("\n----- 🤖 CÂMERA INTELIGENTE JOVI -----")
    print("1 - Analisar o ambiente pelo clima (internet)")
    print("2 - Escolher a cena manualmente")
    print("0 - Voltar")
    opcao = ler_numero("Opcao: ", 0, 2)

    if opcao == 1:
        print("\nEm qual cidade voce esta?")
        for numero in CIDADES:
            print(f"{numero} - {CIDADES[numero][0]}")
        escolha = ler_numero("Opcao: ", 1, 4)
        nome, lat, lon = CIDADES[escolha]

        clima = buscar_clima(lat, lon)
        if clima is None:
            print("Nao foi possivel buscar o clima (sem internet?). Tente a opcao manual.")
            return camera, configuracoes

        print(f"\nClima em {nome}: {clima['temperature_2m']}°C, nuvens: {clima['cloud_cover']}%")
        if clima["is_day"] == 0:
            cena = "BAIXA LUZ"
        elif clima["cloud_cover"] >= 70:
            cena = "RETRATO"
        else:
            cena = "PAISAGEM"
        camera, configuracoes = aplicar_cena(camera, configuracoes, cena)

    elif opcao == 2:
        cenas = ["BAIXA LUZ", "MOVIMENTO", "RETRATO", "COMIDA", "PAISAGEM"]
        print("\nQual e a cena?")
        for i in range(len(cenas)):
            print(f"{i + 1} - {cenas[i]}")
        escolha = ler_numero("Opcao: ", 1, 5)
        camera, configuracoes = aplicar_cena(camera, configuracoes, cenas[escolha - 1])

    return camera, configuracoes


def main():
    dados = carregar_dados()
    camera = dados["camera"]
    configuracoes = dados["configuracoes"]
    galeria = dados["galeria"]

    print("Bem-vindo(a) a Camera JOVI!")

    rodando = True
    while rodando:
        mostrar_camera(camera)
        menu_principal()
        opcao = ler_numero("Comando: ", 0, 8)

        if opcao == 1:
            galeria = capturar_midia(camera, galeria)
        elif opcao == 2:
            camera = trocar_modo(camera)
        elif opcao == 3:
            camera = alternar_flash(camera)
        elif opcao == 4:
            camera = ajustar_timer(camera)
        elif opcao == 5:
            camera = alternar_zoom(camera)
        elif opcao == 6:
            galeria = ver_galeria(galeria)
        elif opcao == 7:
            configuracoes = tela_configuracoes(configuracoes)
        elif opcao == 8:
            camera, configuracoes = camera_inteligente(camera, configuracoes)
        else:
            print("Salvando dados e desligando camera...")
            rodando = False

        salvar_dados(camera, configuracoes, galeria)


main()