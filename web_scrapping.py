# Web Scrapping

# Imports
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from bs4 import BeautifulSoup


# Monta uma lista de links para cada UF da lista ufs
def montar_primeira_url():
    ufs = ['AC']#, 'AL', 'AM'] #'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']
    ano = '2017'
    links = []

    for uf in ufs:
        link = 'http://www.fnde.gov.br/pls/internet_pdde/internet_fnde.PDDEREX_2_PC?p_listar=S&p_ano=' + ano + '&p_prg=02&p_uf=' + uf + '&p_co_mun=&p_tipo=P'
        links.append(link)

    return links


# Função que recebe uma lista de links e transforma cada um em uma classe HTPPResponse e retorna uma lista 'paginas' de objetos com conteúdo HTML5
def get_html(link):

    try:
        url = urlopen(link)
    except HTTPError as e:
        print(e)
    except URLError:
        print('Server down or incorrect domain')
    else:
        pagina = BeautifulSoup(url.read(),'html5lib')

    return pagina;


# Atribui a 'links' o valor da função 'montar_primeira_url'
links = montar_primeira_url()


# Função qeu retorna uma lista conteúdo HTML
def lista_html(links):
    paginas = []

    for link in links:
        pagina = get_html(link)
        paginas.append(pagina)

    return paginas


# Atribui a 'paginas_html' o valor da função 'lista_html'
paginas_html = lista_html(links)


# Função que recebe uma lista de conteúdos HTML e retorna valores específico presente em uma tabela
def get_cnpj(paginas_html):
    lista_cnpj = []

    for pagina in paginas_html:
        tabela_municipios = pagina.findAll('table')[5].tbody.findAll('tr')[1:]
        for linhas_cnpj in tabela_municipios:
            cnpj = linhas_cnpj.select('td')[1]
            lista_cnpj.append(cnpj.getText())
            lista_cnpj = list(map(str.strip, lista_cnpj))

    return lista_cnpj


lista_cnpj = get_cnpj(paginas_html)


# Montar segunda url
def montar_segunda_url(lista_cnpj):
    links_2 = []

    for cnpj in lista_cnpj:
        link_2 = 'http://www.fnde.gov.br/pls/internet_pdde/internet_fnde.PDDEREX_4_PC?p_ano=2017&b_ver=3&p_cgc='+cnpj+'&p_tip=P&p_prog=02'
        links_2.append(link_2)

    return links_2

links_2 = montar_segunda_url(lista_cnpj)
lista_html2 = lista_html(links_2)

# Main function
def main():
    lista_html(links) # printa o html de todos os links
    get_cnpj(paginas_html) # printa a lista de todos os cnpj's
    print(montar_segunda_url(lista_cnpj))

main()
