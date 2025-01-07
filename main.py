import json
from bs4 import BeautifulSoup

# Lendo o conteúdo HTML do arquivo local
with open('elemento.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Analisando o HTML com BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Encontrando todas as tabelas
tables = soup.find_all('table')

# Extraindo os dados das células de cada tabela
data = []
for table in tables:
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        cell_data = []
        score = None
        for cell in cells:
            # Ignorando divs com a classe 'text-right text-gray font9' e extraindo a pontuação
            for div in cell.find_all('div', class_='text-right text-gray font9'):
                score_text = div.get_text().replace('\xa0', '')
                try:
                    score = int(score_text)
                except ValueError:
                    score = None
                div.decompose()
            # Obtendo o texto dentro da célula, incluindo o texto de elementos filhos
            text = ' '.join(cell.stripped_strings)
            cell_data.append(text)
        if cell_data:  # Adiciona apenas se houver dados
            if score is not None:
                cell_data.insert(1, score)  # Insere a pontuação na posição correta
            data.append(cell_data)

# Convertendo os dados para JSON
json_data = json.dumps(data, indent=4, ensure_ascii=False)

# Salvando os dados em um arquivo JSON
with open('data.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)

print("Dados salvos em data.json")