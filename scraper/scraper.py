import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

# Configurações
BASE_URL = ''
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': ''
}
OUTPUT_FILE = 'data/imoveis.csv'

# Função para fazer a requisição e obter o HTML
def get_html(url):
    print(f"Fazendo requisição para {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        print("Página carregada com sucesso!")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a página: {e}")
        return None

# Função para salvar o HTML para depuração
def save_html_for_debug(html, filename='debug.html'):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"HTML salvo em {filename} para depuração.")

# Função para parsear o HTML e extrair dados
def parse_html(html):
    print("Iniciando parsing do HTML...")
    soup = BeautifulSoup(html, 'html.parser')
    imoveis = []

    # Inspecione o site para atualizar essas classes
    for item in soup.find_all('div', class_='ListingCell_ListingCell__container__3e_5V'):  # Ajuste conforme o site
        try:
            # Extrair dados (ajuste conforme o site)
            preco = item.find('p', class_='ListingCell_Price__3iFyv').text.strip()  # Ajuste para pegar o preço
            descricao = item.find('h2', class_='ListingCell_Title__2sS7G').text.strip()  # Ajuste para pegar a descrição
            localizacao = item.find('span', class_='ListingCell_Location__3n7_4').text.strip()  # Ajuste para pegar a localização
            link = '' + item.find('a', class_='ListingCell_ListingCell__link__1nQ4J')['href']  # Ajuste para pegar o link

            imoveis.append({
                'preco': preco,
                'descricao': descricao,
                'localizacao': localizacao,
                'link': link,
                'data_coleta': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        except AttributeError as e:
            print(f"Erro ao extrair dados de um item: {e}")
            continue

    if not imoveis:
        print("Nenhum dado encontrado.")
    return imoveis

# Função principal
def main():
    url = BASE_URL
    html = get_html(url)
    if html:
        save_html_for_debug(html)  # Salva o HTML para depuração
        imoveis = parse_html(html)
        if imoveis:
            save_to_csv(imoveis)

# Rodando o script
if __name__ == "__main__":
    main()