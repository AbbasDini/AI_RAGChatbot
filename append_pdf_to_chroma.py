import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma

# تنظیم مسیرها
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE_DIR, "Med_doc", "doctor_abbasi", "erfani.pdf")
CHROMA_DB_DIR = os.path.join(BASE_DIR, "chroma_db")

# متادیتا پزشک
doctor_attrs = {
    "doctor": "doctor_abbasi",
    "city": "hamedan",
    "specialty": "neurologist",
    "experience": "10+",
    "source": PDF_PATH
}

# بارگذاری و پردازش PDF
loader = PyPDFLoader(PDF_PATH)
docs = loader.load()
for doc in docs:
    doc.metadata.update(doctor_attrs)

# تقسیم‌بندی متن
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(docs)

# مدل embedding
embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# بارگذاری دیتابیس موجود و افزودن داده جدید
db = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embedding_model)
db.add_documents(chunks)
db.persist()

print("erfani.pdf با موفقیت به ChromaDB اضافه شد.") 