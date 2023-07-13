from langchain.vectorstores import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

openai_api_key = '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'
pinecone_api_key = 'f6168b1c-24f5-44cc-88a2-49526e1e5b45'
pinecone_environment_region = 'us-west4-gcp-free'
pinecone_inde_name = 'openai-database'
import pinecone

pinecone.init(
        api_key = pinecone_api_key,
        environment = pinecone_environment_region
    )
index_name = pinecone_inde_name
index = pinecone.Index(index_name)
EMBEDDING_MODEL = 'text-embedding-ada-002'
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

vectorstore = Pinecone(index, embeddings.embed_query, "text")

def store_data(text):    
    global vectorstore
    vectorstore = Pinecone.from_texts([text], embeddings, index_name=index_name)


def search_database(query):

    llm = OpenAI(temperature=0, openai_api_key = openai_api_key)
    qa_chain = load_qa_chain(llm, chain_type='stuff')
    docs = vectorstore.similarity_search(query,8)
    result = qa_chain.run(input_documents=docs, question=query)
    return result