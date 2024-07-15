from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import Language

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader

# Qdrant
from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant

# BGE on Hugging Face
from langchain.embeddings import HuggingFaceBgeEmbeddings

repo_path = "docs"

model_name = "BAAI/bge-large-en-v1.5"
# model_name = "BAAI/bge-base-en-v1.5"
model_kwargs = {"device": "cuda"}
encode_kwargs = {"normalize_embeddings": True}
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)

# Load
loader = GenericLoader.from_filesystem(
    repo_path+"/",
    glob="**/**/*",
    suffixes=[".md", ".mdx"],
    parser=LanguageParser(language=Language.PYTHON, parser_threshold=500)
)
documents = loader.load()
# len(documents)


client = QdrantClient("localhost", port=6333)
client.delete_collection("docs")

# Split
from langchain.text_splitter import RecursiveCharacterTextSplitter
python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.MARKDOWN,
    chunk_size=1000,
    chunk_overlap=100
)
texts = python_splitter.split_documents(documents)
# len(texts)

# Store
url = "http://localhost:6333"
vectorstore = Qdrant.from_documents(
    texts,
    embeddings,
    url=url,
    prefer_grpc=True,
    collection_name="docs"
)
