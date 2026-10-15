from pprint import pprint
import requests

def pegar_id_estados():
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    params = {
        'view': 'nivelado',
    }
    dados_estados = fazer_request(url=url, params=params)
    dict_estado = {}
    
    if dados_estados:
        for dados in dados_estados:
            id_estado = dados["UF-id"]
            nome_estado = dados["UF-nome"]
            dict_estado[id_estado] = nome_estado
    return dict_estado


def pegar_frequencia_nome_por_estado(nome):
    url = f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}"    
    params = {
        'groupBy': 'UF',
    }
    dados_frequencias = fazer_request(url=url, params=params)
    dict_frequencias = {}
    for dados in dados_frequencias:
        id_estado = int(dados['localidade'])
        frequencia = dados['res'][0]['proporcao']
        dict_frequencias[id_estado] = frequencia
    return dict_frequencias

def fazer_request(url, params=None):
    resposta = requests.get(url, params=params, verify=False)    
    try:
        resposta.raise_for_status()
    except requests.HTTPError as e:
        print(f'Erro no request: {e}')
        resultado = None
    else: 
        resultado = resposta.json()
    return resultado

def main(nome):
    dict_estados = pegar_id_estados()
    dict_frequencia = pegar_frequencia_nome_por_estado(nome)
    print(f'frequencia do nome {nome} nos estados por 100.000 habitantes')
    for id_estado, nome_estado in dict_estados.items():
        frequencia_estado = dict_frequencia.get(id_estado, 0)
        print(f'--> {nome_estado} {frequencia_estado}')


if __name__ == '__main__': 
    nome = input('Digite o nome').strip()
    if nome:
     main(nome)
    else:
        print('Nenhum nome informado.')

