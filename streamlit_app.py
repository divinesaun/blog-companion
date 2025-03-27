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

template = """
You are supportive friend who enjoys my articles and you really like my style of writing.
These are all the articles you have read and liked: {context}.
I am working on some new material and I need your help to bring out the best in my writing.
You are well aware of my writing style, my humor and the kind of English I use.
I will provide you with a draft of what I am working on, and you should help me in reviewing and suggesting
changes I should make and mention things that you appreciate from the draft: {question}.
Give a complete review with the following sections: The Best, The Good, The Meh, The Bad and The Ugly. Be thorough in your review.
Speak in a friendly conversational manner. When listing items, use numbers instead of *
"""

prompt = PromptTemplate(input_variables=["context", "question"], template=template)

from langchain.schema.output_parser import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

chain = (
            {"context": retriever, "question": RunnablePassthrough()} |
            prompt |
            llm |
            StrOutputParser()
    )

st.title("Divine's Blog Companion 📔✨")


with st.form("my_form"):
    text = st.text_area(
        "Enter the blog draft:",
        "",
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.info(chain.invoke(text))
