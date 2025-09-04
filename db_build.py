from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
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

# FAISS bazasini yaratish
faiss_index = FAISS.from_documents(docs, emb)

# Saqlash
faiss_index.save_local("faiss_index")

print("✅ FAISS baza yaratildi va saqlandi: faiss_index")
