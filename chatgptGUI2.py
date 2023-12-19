import os
import sys
import tkinter as tk
from tkinter import scrolledtext, filedialog
import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma

import constants

# GUI Related Functions
def submit_query():
    user_query = entry.get()
    if user_query in ['quit', 'q', 'exit']:
        window.quit()
    else:
        result = chain({"question": user_query, "chat_history": chat_history})
        response_area.insert(tk.END, "You: " + user_query + "\nAI: " + result['answer'] + "\n\n")
        chat_history.append((user_query, result['answer']))
        entry.delete(0, tk.END)

# Function to save the conversation
def save_conversation():
    filename = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Documents", "*.txt")],
        title="Save as"
    )
    if filename:
        with open(filename, "w") as file:
            file.write(response_area.get("1.0", tk.END))

print("Current working directory:", os.getcwd())

os.environ["OPENAI_API_KEY"] = constants.APIKEY

PERSIST = False

# Setup for LangChain
if PERSIST and os.path.exists("persist"):
    vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
    index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
    loader = DirectoryLoader("./data")
    if PERSIST:
        index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": "persist"}).from_loaders([loader])
    else:
        index = VectorstoreIndexCreator().from_loaders([loader])

chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)

chat_history = []

# Create the GUI window
window = tk.Tk()
window.title("AI Chat Interface")

# Create a text entry box
entry = tk.Entry(window, width=100)
entry.pack()

# Create a submit button
submit_button = tk.Button(window, text="Submit", command=submit_query)
submit_button.pack()

# Create a text area for responses
response_area = scrolledtext.ScrolledText(window, width=100, height=20)
response_area.pack()

# Create a save button
save_button = tk.Button(window, text="Save Conversation", command=save_conversation)
save_button.pack()

# Start the GUI event loop
window.mainloop()
