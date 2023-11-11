from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI

from rich.console import Console
from utils import (DocsJSONLLoader, get_file_path, get_openai_api_key)

console = Console()
recreate_chroma_db=False

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


def extraction_instruction(vectorstore, llm):
    print(vectorstore.schema)


def main():
    documents = load_documents(get_file_path())
    get_openai_api_key()
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    # print(embeddings)

    vectorstore_chroma = get_chroma_db(embeddings, documents, "chroma_docs")
    console.print(f"[green]Documentos {len(documents)} cargando.[/green]")
    #print(vectorstore_chroma)

    llm = ChatOpenAI(
      model_name="gpt-3.5-turbo",
      temperature=0.2,
      max_tokens=1000,  # Queremos que las respuestas sean tan largas como el modelo lo considere, sin considerar la cantidad de tokens
    )

    extraction_instruction(vectorstore_chroma, llm)

if __name__ == "__main__":
    main()