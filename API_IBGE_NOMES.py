import requests

# Dicionário fixo com os códigos de localidade dos estados brasileiros (IBGE)
estados_ibge = {
    "AC": 12,"AL": 27,"AP": 16,"AM": 13,"BA": 29,"CE": 23,"DF": 53,"ES": 32,"GO": 52,"MA": 21,"MT": 51,"MS": 50,"MG": 31,"PA": 15,"PB": 25,"PR": 41,"PE": 26,"PI": 22,"RJ": 33,"RN": 24,"RS": 43,"RO": 11,"RR": 14,"SC": 42,"SP": 35,"SE": 28,"TO": 17,
}

# 1. Entrada do nome principal
nome_usuario = input("Digite o primeiro nome apenas para consultar no IBGE: ").strip().lower()

if not nome_usuario:
  print("[-] Você precisa digitar um nome válido!")
  exit()

print(
    "\n--- Opções de Filtro Geográfico (Deixe em branco para buscar no Brasil"
    " inteiro) ---"
)

# 2. Pergunta se quer agrupar por todas as UFs ou filtrar por um estado específico
uf_grupo = input(
    "Deseja o ranking separado por todas as UFs? (Digite 'sim' ou deixe em"
    " branco caso queira visualizar um estado em específico, digite o codigo do estado): "
).strip().lower()

estado_escolhido = ""
if uf_grupo != "sim":
  # Mostra as opções disponíveis para facilitar
  print(
      "Estados disponíveis: "
      + ", ".join(estados_ibge.keys())
      + " (ou aperte Enter para ignorar)"
  )
  estado_escolhido = (
      input("Digite a sigla do estado desejado (ex: SP, RJ): ")
      .strip()
      .upper()
  )

# 3. Montagem inteligente da URL e parâmetros
url = f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome_usuario}"
parametros = {}

if uf_grupo == "sim":
  parametros["groupBy"] = "UF"
elif estado_escolhido in estados_ibge:
  # Pega o código numérico correspondente no dicionário
  codigo_uf = estados_ibge[estado_escolhido]
  parametros["localidade"] = codigo_uf
  print(f"[i] Filtrando para o estado: {estado_escolhido} (Código: {codigo_uf})")

print(f"\n[*] Consultando API do IBGE...")
resposta = requests.get(url, params=parametros, verify=False)

try:
  resposta.raise_for_status()
except requests.HTTPError as e:
  print(f"Erro no request: {e}")
  resultado = None
else:
  resultado = resposta.json()

if resultado:
  print(f"\n[+] Resultados encontrados para '{nome_usuario.capitalize()}':\n")
  for item in resultado:
    local = item.get("localidade", "BR")
    print(f"Localidade / Região: {local}")

    if "res" in item and item["res"]:
      total_local = sum(p["frequencia"] for p in item["res"])
      print(f"    -> Total de registros nesta localidade: {total_local}")
    print("-" * 40)
else:
  print(
      f"[-] Nenhum dado encontrado para '{nome_usuario}' com os filtros"
      " informados."
  )