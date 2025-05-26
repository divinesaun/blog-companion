import streamlit as st
from faiss import (
    IndexFlatL2
)
from langchain_community.docstore.in_memory import (
    InMemoryDocstore
)
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
load_dotenv()

embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
dimensions: int = len(embedding_function.embed_query("dummy"))

db = FAISS(
            embedding_function=embedding_function,
            index=IndexFlatL2(dimensions),
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
            normalize_L2=False
        )

vectorstore = db.load_local("articles",
                                    embedding_function,
                                    allow_dangerous_deserialization=True)

retriever = vectorstore.as_retriever()
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")


from langchain.prompts import PromptTemplate

with open("prompt.txt", "r") as f:
    template = f.read()


prompt = PromptTemplate(input_variables=["context", "question"], template=template)

from langchain.schema.output_parser import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

chain = (
            {"context": retriever, "question": RunnablePassthrough()} |
            prompt |
            llm |
            StrOutputParser()
    )

st.title("Divine's Blog Companion 🫤")


with st.form("my_form"):
    text = st.text_area(
        "Enter the blog draft:",
        "",
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.info(chain.invoke(text))