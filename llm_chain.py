# LLM
from langchain.llms import HuggingFaceTextGenInference
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


# RetrievalQA chain
from langchain.chains import RetrievalQA

# Qdrant
from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant

# BGE on Hugging Face
from langchain.embeddings import HuggingFaceBgeEmbeddings

model_name = "BAAI/bge-base-en-v1.5"
model_kwargs = {"device": "cuda"}
encode_kwargs = {"normalize_embeddings": True}
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)


# Store
url = "http://localhost:6333"

client = QdrantClient("localhost", port=6333)
vectorstore = Qdrant(
    client=client,
    collection_name="docs",
    embeddings=embeddings,
)

# llm model loading
llm = HuggingFaceTextGenInference(
    inference_server_url="http://localhost:8080/",
    max_new_tokens=3072,
    top_k=50,
    top_p=0.95,
    typical_p=0.95,
    temperature=0.01,
    repetition_penalty=1.03,
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
)

# RetrievalQA
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_type="mmr", k=20)
)


# RAG Query
question = "How do I get create RDS?"

query = f"""<|system|>
You are a Terraform expert.</s>
<|user|>
{question}
</s>
<|assistant|>
"""

response = qa.run(query)
print(response)
