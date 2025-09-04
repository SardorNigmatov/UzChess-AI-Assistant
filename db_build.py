import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader

# ======================
# 1. Konfiguratsiya
# ======================

load_dotenv()

DATA_FILES = [
    "data/courses.txt",
    "data/bots.txt",
    "data/puzzles.txt",
    "data/about.txt",
    "data/books.txt",
]
FAISS_PATH = "faiss_index"


# ======================
# 2. FAISS yaratish funksiyasi
# ======================

def build_faiss_index(file_paths, output_path: str) -> None:
    """
    Matn fayllardan hujjatlarni yuklab, FAISS indeks yaratadi va saqlaydi.

    Args:
        file_paths (list[str]): Yuklanadigan fayllar ro‘yxati.
        output_path (str): Saqlash papkasi nomi.
    """
    documents = []
    for path in file_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"❌ Fayl topilmadi: {path}")
        loader = TextLoader(path, encoding="utf-8")
        documents.extend(loader.load())

    embedding = OpenAIEmbeddings(model="text-embedding-3-small")
    faiss_index = FAISS.from_documents(documents, embedding)
    faiss_index.save_local(output_path)

    print(f"✅ FAISS baza yaratildi va saqlandi: {output_path}")


# ======================
# 3. Main
# ======================

if __name__ == "__main__":
    build_faiss_index(DATA_FILES, FAISS_PATH)
