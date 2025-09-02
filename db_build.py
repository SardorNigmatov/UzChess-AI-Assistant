from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
import os
from dotenv import load_dotenv

load_dotenv()


# Fayllar yo‘llari
file_paths = [
    "data/courses.txt",
    "data/bots.txt",
    "data/puzzles.txt",
    "data/about.txt",
    "data/books.txt",
]

# Fayllarni yuklash
docs = []
for path in file_paths:
    loader = TextLoader(path, encoding="utf-8")
    docs.extend(loader.load())

# Embedding
emb = OpenAIEmbeddings(model="text-embedding-3-small")

# Chroma DB papkasi
persist_directory = "./chroma_db"
os.makedirs(persist_directory, exist_ok=True)

# Vektor bazasini yaratish
vs = Chroma.from_documents(
    documents=docs,
    embedding=emb,
    collection_name="my_collection",
    persist_directory=persist_directory,
)

print("✅ Vektor baza yaratildi va saqlandi:", persist_directory)
