import openai
from flask import Flask, request, jsonify
from utils import Terminal3
import faiss
import numpy as np
import pickle
from tqdm import tqdm
import argparse
import os

import re
import time
from io import BytesIO
from typing import Any, Dict, List

from langchain import LLMChain, OpenAI
from langchain.agents import AgentExecutor, Tool, ZeroShotAgent
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain
from langchain.docstore.document import Document
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import VectorStore
from langchain.vectorstores.faiss import FAISS
from pypdf import PdfReader


# os.environ["http_proxy"] = "http://127.0.0.1:7890"
# os.environ["https_proxy"] = "http://127.0.0.1:7890"

api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def parse_pdf(file: BytesIO) -> List[str]:
    pdf = PdfReader(file)
    output = []
    for page in pdf.pages:
        text = page.extract_text()
        # Merge hyphenated words
        text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
        # Fix newlines in the middle of sentences
        text = re.sub(r"(?<!\n\s)\n(?!\s\n)", " ", text.strip())
        # Remove multiple newlines
        text = re.sub(r"\n\s*\n", "\n\n", text)
        output.append(text)
    return output

def text_to_docs(text: str) -> List[Document]:
    """Converts a string or list of strings to a list of Documents
    with metadata."""
    if isinstance(text, str):
        # Take a single string as one page
        text = [text]
    page_docs = [Document(page_content=page) for page in text]

    # Add page numbers as metadata
    for i, doc in enumerate(page_docs):
        doc.metadata["page"] = i + 1

    # Split pages into chunks
    doc_chunks = []

    for doc in page_docs:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
            chunk_overlap=0,
        )
        chunks = text_splitter.split_text(doc.page_content)
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk, metadata={"page": doc.metadata["page"], "chunk": i}
            )
            # Add sources a metadata
            doc.metadata["source"] = f"{doc.metadata['page']}-{doc.metadata['chunk']}"
            doc_chunks.append(doc)
    return doc_chunks

def test_embed():
    global api_key
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    doc = parse_pdf('input.pdf')
    pages = text_to_docs(doc)
    # Indexing
    # Save in a Vector DB
    index = FAISS.from_documents(pages, embeddings)
    return index



class QA():
    def __init__(self) -> None:
        self.index = test_embed()

    def __call__(self, query):
        global api_key
        # Set up the question-answering system
        qa = RetrievalQA.from_chain_type(
            llm=OpenAI(openai_api_key=api_key),
            chain_type = "map_reduce",
            retriever=self.index.as_retriever(),
        )
        # Set up the conversational agent
        tools = [
            Tool(
                name="State of Union QA System",
                func=qa.run,
                description="Useful for when you need to answer questions about the aspects asked. Input may be a partial or fully formed question.",
            )
        ]
        prefix = """Have a conversation with a human, answering the following questions as best you can based on the context and memory available. 
                    You have access to a single tool:"""
        suffix = """Begin!"

        {chat_history}
        Question: {input}
        {agent_scratchpad}"""

        prompt = ZeroShotAgent.create_prompt(
            tools,
            prefix=prefix,
            suffix=suffix,
            input_variables=["input", "chat_history", "agent_scratchpad"],
        )

        llm_chain = LLMChain(
            llm=OpenAI(
                temperature=0, openai_api_key=api_key, model_name="gpt-3.5-turbo"
            ),
            prompt=prompt,
        )
        agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
        agent_chain = AgentExecutor.from_agent_and_tools(
            agent=agent, tools=tools, verbose=True, memory=self.session_state.memory
        )
            
        res = agent_chain.run(query)


@app.route('/test', methods=['POST'])
def test():
    data = request.json

    return data


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    if not data or 'prompt' not in data:
        return jsonify({"error": "Invalid request. Provide wallet_address and prompt."}), 400

    query = data['prompt']

    try:
        answer,context = qa(query)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return answer

if __name__ == '__main__':
    qa = QA()
    app.run(host="0.0.0.0", debug=True, port=5298)
