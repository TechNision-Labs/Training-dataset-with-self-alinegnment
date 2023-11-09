from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from rich.console import Console
from utils import (DocsJSONLLoader, get_file_path, get_openai_api_key)

console = Console()
recreate_chroma_db=True

def load_documents(file_path: str):
    loader = DocsJSONLLoader(file_path)
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1600, length_function=len, chunk_overlap=160
    )

    return text_splitter.split_documents(data)

def get_chroma_db(embeddings, documents, path):
    if recreate_chroma_db:
        console.print("RECREANDO CHROMA DATABASE")
        return Chroma.from_documents(
            documents=documents, embedding=embeddings, persist_directory=path
        )
    else:
        console.print("CARGANDO CHROMA EXISTENTE")
        return Chroma(persist_directory=path, embedding_function=embeddings)
    

def main():
    documents = load_documents(get_file_path())
    get_openai_api_key()
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    # print(embeddings)

    vectorstore_chroma = get_chroma_db(embeddings, documents, "chroma_docs")
    console.print(f"[green]Documentos {len(documents)} cargando.[/green]")
    print(vectorstore_chroma)


if __name__ == "__main__":
    main()