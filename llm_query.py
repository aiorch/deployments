 llm
from langchain.llms import HuggingFaceTextGenInference
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

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

question = "What is climate change?"

query = f"""<|system|>
You are a helpful chatbot.</s>
<|user|>
{question}
</s>
<|assistant|>
"""
response = llm(query)
print(response)
~               
