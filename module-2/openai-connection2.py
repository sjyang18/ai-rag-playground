import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

load_dotenv()

from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

llm = AzureChatOpenAI(
    azure_deployment="gpt-4o-deployment",
    model_name="gpt-4o",
    model_version="2024-11-20",
    azure_endpoint="https://veai4sfinpe-local.openai.azure.com/",
    azure_ad_token_provider=token_provider,
    api_version="2024-05-01-preview",
)

message = HumanMessage(content="Please generate me a 60 word essay summarizing Star Wars Revenge of the Sith")
print(message)

a = llm.invoke([message])
print("after invoking llm")
print(a.content)

embeddings: AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(
    azure_deployment="text-embedding-3-small-deployment",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_ad_token_provider=token_provider,
    api_version="2024-05-01-preview",
)

text = "this is a test document"
query_result = embeddings.embed_query(text)
doc_result = embeddings.embed_documents([text])
print(doc_result[0][:5])
