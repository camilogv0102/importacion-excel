import pandas as pd
from bs4 import BeautifulSoup

INPUT_FILE = 'Localizaciones-Export-2025-June-03-2110.xlsx'
OUTPUT_FILE = 'converted.csv'

LABELS = {
    'direccion': 'Dirección',
    'coordenada': 'Coordenadas',
    'tipoligia': 'Tipología',
    'agua': 'Agua',
    'luz': 'Luz',
    'cobertura': 'Cobertura',
    'estado_conservacion': 'Estado conservación',
    'propiedad': 'Propiedad',
}

def extract_post_content(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    texts = []
    for p in soup.find_all('p'):
        if p.find('span'):
            continue
        text = p.get_text(separator=' ', strip=True)
        if text:
            texts.append(text)
    return "\n".join(texts)

def extract_field(soup: BeautifulSoup, label: str) -> str:
    strong = soup.find('strong', string=lambda x: x and label in x)
    if not strong:
        return ''
    parent_text = strong.parent.get_text(separator=' ', strip=True)
    value = parent_text.replace(strong.get_text(), '')
    value = value.lstrip(':').strip()
    return value

def main():
    df = pd.read_excel(INPUT_FILE)
    out_rows = []
    for _, row in df.iterrows():
        html = row['Content']
        soup = BeautifulSoup(html, 'html.parser')
        data = {
            'post_title': row['Title'],
            'post_content': extract_post_content(html),
        }
        for col, label in LABELS.items():
            data[col] = extract_field(soup, label)
        out_rows.append(data)
    out_df = pd.DataFrame(out_rows)
    out_df.to_csv(OUTPUT_FILE, index=False)

if __name__ == '__main__':
    main()
