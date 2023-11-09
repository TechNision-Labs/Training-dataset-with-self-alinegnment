import datetime
import json
import re
import requests
import emoji
import PyPDF2
from io import BytesIO

from utils import create_dir, remove_existing_file


def preprocess_text(text: str) -> str:
    """
    Preprocesa el texto eliminando ciertos patrones y caracteres.

    Args:
        text (str): Texto a preprocesar.

    Returns:
        El texto preprocesado.
    """
    text = re.sub(r"<[^>]*>", "", text)
    text = re.sub(r"http\S+|www.\S+", "", text)
    text = re.sub(r"Copyright.*", "", text)
    text = text.replace("\n", " ")
    text = emoji.demojize(text)
    text = re.sub(r":[a-z_&+-]+:", "", text)
    return text


def download_file(url: str, jsonl_file_name: str) -> None:
    """
    Descarga un archivo desde una URL y lo guarda en un archivo JSONL.

    Args:
        url (str): URL desde donde se descarga el archivo.
        jsonl_file_name (str): Nombre del archivo JSONL donde se guarda el archivo descargado.
    """
    response = requests.get(url)
    pdf_data = response.content
    pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_data))

    json_objects = []
    # Itera a través de las páginas del PDF
    for page_num, page in enumerate(pdf_reader.pages):
        page_text = page.extract_text()

        if page_text is not None and isinstance(page_text, str):
           page_text = preprocess_text(page_text)
            # Crea un objeto JSON con el texto de la página
           json_object = {
               "page": page_num + 1, 
                "text": page_text
                }
           json_objects.append(json_object)

    with open(jsonl_file_name, 'w') as jsonl_file:
        # Escribe cada objeto JSON en una línea separada
        for json_obj in json_objects:
            jsonl_file.write(json.dumps(json_obj) + '\n')

def main():
    """
    Función principal que se ejecuta cuando se inicia el script.
    """

    current_date = datetime.date.today().strftime("%Y_%m_%d")
    jsonl_file_name = f"data/gse_{current_date}.jsonl"

    create_dir("data/")
    remove_existing_file(jsonl_file_name)

    url = 'https://cdn.www.gob.pe/uploads/document/file/4999791/CEPLAN%20-%20Guia%20de%20seguimiento%20y%20evaluacion%2018082023.pdf?v=1692376022'

    download_file(url, jsonl_file_name)


if __name__ == "__main__":
    main()
