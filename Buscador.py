import requests
import requests_cache
from bs4 import BeautifulSoup

requests_cache.install_cache('cache')
resultado = []

def busca_urls(url, depth):
    vetor_site = [url]
    matriz = [0] * (depth + 1)
    matriz[0] = vetor_site

    i = 0
    while i < depth:
        matriz[i + 1] = []
        for j in range(len(matriz[i])):

            aux = []
            response = requests.get(matriz[i][j])
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            for link in links:
                try:
                    if 'http' in link['href'] and '#' not in link['href']:
                        try:
                            if link['href'] not in matriz[i]:
                                try:
                                    if link['href'] not in aux:
                                        aux.append(link['href'])
                                except:
                                    pass
                        except:
                            pass
                except:
                    pass
            matriz[i + 1] += aux
        i += 1

    return matriz


def download(site_atual):
    response = ''
    try:
        response = requests.get(site_atual)
    except Exception as ex:
        response = None
    finally:
        return response


def salvar_site(site, html, keyword):
    soup = BeautifulSoup(html, 'html.parser')
    pagina = requests.get(site)
    soup2 = BeautifulSoup(pagina.text, 'html.parser')
    page = soup2.text
    tamanho_keyword = len(keyword)
    palavra = page.find(keyword)
    texto = page[palavra - 20:palavra + tamanho_keyword + 20:1]
    quantidade_ocorrencias = html.count(keyword)
    title = site
    try:
        title = soup.title.string
    except:
        pass

    resultado_busca = {'link': site,
                       'titulo': title,
                       'ocorrencias': quantidade_ocorrencias,
                       'texto': texto
                       }

    if resultado_busca not in resultado:
        resultado.append(resultado_busca)


def run():
    keyword = input("Digite a palavra-chave a ser buscada: ")
    url = input("Digite o endereço inicial para a busca: ")
    depth = int(input('Digite a profundidade da busca: '))
    matriz_de_urls = busca_urls(url, depth)

    for i in range(len(matriz_de_urls)):
        for j in range(len(matriz_de_urls[i])):
            site_atual = matriz_de_urls[i][j]
            try:
                response = download(site_atual)
            except:
                continue
            try:
                html = response.text
            except:
                continue
            if keyword in html:
                salvar_site(site_atual, html, keyword)
    print("\nRESULTADO")
    sorted_list = sorted(resultado, reverse=True, key=lambda k: k['ocorrencias'])
    for match in sorted_list:
        print('Site: %s \n%s\nNúmero de ocorrencias da palavra-chave: %d\n[...]%s[...]\n' % (
        match['link'], match['titulo'], match['ocorrencias'], match['texto']))

def main():
    run()
if __name__ == '__main__':
    main()