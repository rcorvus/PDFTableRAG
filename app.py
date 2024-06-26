from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError
from unstructured.staging.base import dict_to_elements

client = UnstructuredClient(
    api_key_auth="your_api_key_here",
    server_url="https://api.unstructuredapp.io",
)

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
folder_path = "db"
embeddings = OpenAIEmbeddings()
vector_store = Chroma(persist_directory=folder_path, embedding_function=embeddings)

from langchain.llms import OpenAI

def extract_tables_from_pdf(filename):
    with open(filename, "rb") as f:
        files=shared.Files(
            content=f.read(),
            file_name=filename,
        )

    req = shared.PartitionParameters(
        files=files,
        strategy="hi_res",
        hi_res_model_name="yolox",
        skip_infer_table_types=[],
        pdf_infer_table_structure=True,
    )

    try:
        resp = client.general.partition(req)
        elements = dict_to_elements(resp.elements)
    except SDKError as e:
        print(e)
    tables = [el for el in elements if el.category == "Table"]

    for table in tables:
        table.text
        table_html = table.metadata.text_as_html
        table_metadata = table.metadata.to_dict()
        del table_metadata["languages"]
        table_metadata["source"] = table_metadata["filename"]

        from io import StringIO 
        from lxml import etree

        parser = etree.XMLParser(remove_blank_text=True)
        file_obj = StringIO(table_html)
        tree = etree.parse(file_obj, parser)
        print(etree.tostring(tree, pretty_print=True).decode())

        from IPython.core.display import HTML
        HTML(table_html)

        print(table_html)

        document = Document(page_content=table_html, metadata=table_metadata)

        embed_vector_store(document)


documents = []
def embed_vector_store(document):
    documents.append(document)
    vector_store = Chroma.from_documents(
        documents=documents, embedding=embeddings, persist_directory=folder_path
    )
    vector_store.persist()
    

def evaluate_answer(given_answer, correct_answer):
    openai_client = OpenAI(temperature=0.0, max_tokens=100)
    evaluator_prompt = f"Does the Given answer have the same information as the Correct answer? \nGiven answer: {given_answer}\nCorrect answer: {correct_answer}"
    response = openai_client(prompt=evaluator_prompt)
    print(evaluator_prompt)
    print(response)

def ask_vector_store():
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )
    from langchain.prompts.prompt import PromptTemplate
    from langchain_openai import OpenAI
    from langchain.chains import ConversationalRetrievalChain, LLMChain
    from langchain.chains.qa_with_sources import load_qa_with_sources_chain


    template = """You are an AI assistant for answering questions about the Electrical Code.
    You are given the following extracted parts of a long document and a question. Provide a conversational answer.
    If you don't know the answer, just say "Hmm, I'm not sure." Don't try to make up an answer.
    If the question is not about the Electrical Code, politely inform them that you are tuned to only answer questions about the Electrical Code.
    Question: {question}
    =========
    {context}
    =========
    Answer in Markdown:"""
    prompt = PromptTemplate(template=template, input_variables=["question", "context"])

    llm = OpenAI(temperature=0)

    doc_chain = load_qa_with_sources_chain(llm, chain_type="map_reduce")
    question_generator_chain = LLMChain(llm=llm, prompt=prompt)
    qa_chain = ConversationalRetrievalChain(
        retriever=retriever,
        question_generator=question_generator_chain,
        combine_docs_chain=doc_chain,
        return_source_documents=True
    )


    question1 = "What is the Current limitations of an Alternating-Current Inherently Limited Power Source (Overcurrent Protection Not Required) with a source voltage of 10 volts?"
    answer1 = qa_chain.invoke({
        "question": question1,
        "chat_history": []
    })["answer"]

    print(question1)
    print(answer1)

    question2 = "What is the Maximum overcurrent protection (amperes) for a Direct-Current Not Inherently Limited Power Source (Overcurrent Protection Required) with a source voltage of 75 volts?"
    answer2 = qa_chain.invoke({
        "question": question2,
        "chat_history": [],
        "filter": filter,
    })["answer"]

    print(question2)
    print(answer2)
    correctAnswer2 = "The Maximum overcurrent protection in amperes for a Direct-Current Not Inherently Limited Power Source (requiring Overcurrent Protection) with a source voltage of 75 volts is 100/V, max."
    evaluate_answer(answer2, correctAnswer2)

    question3 = "What is the capital of France?"
    answer3 = qa_chain.invoke({
        "question": question3,
        "chat_history": [],
        "filter": filter,
    })["answer"]

    print(question3)
    print(answer3)
    correctAnswer3 = "Hmm, I'm not sure."
    evaluate_answer(answer3, correctAnswer3)

    # What if we got an answer that was incorrect by only one character, would our ChatGpt evaluator catch it?
    incorrectAnswer1 = "The current limitation for an Alternating-Current Inherently Limited Power Source with a source voltage of 10 volts is 9.0."
    correctAnswer1 = "The current limitation for an Alternating-Current Inherently Limited Power Source with a source voltage of 10 volts is 8.0."
    print(question1)
    print(incorrectAnswer1)
    evaluate_answer(incorrectAnswer1, correctAnswer1)


if __name__ == "__main__":
    # extract_tables_from_pdf("2017-NEC-Code-2-table11AandB.pdf")
    ask_vector_store()