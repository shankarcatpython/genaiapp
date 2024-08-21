import sqlite3
import pypdf
from pypdf import PdfReader
import spacy
import numpy as np


# Initialize spaCy
nlp = spacy.load('en_core_web_sm')

# Read and process the PDF
with open('mynovel.pdf', 'rb') as f:
    pdf_reader = PdfReader(f)
    chunks = []
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        for i in range(0, len(text), 1000):
            chunks.append(text[i:i+1000])

# Generate embedding vectors
embedding_vectors = []
for chunk in chunks:
    doc = nlp(chunk)
    embedding_vector = doc.vector
    embedding_vectors.append(embedding_vector)

# Create an SQLite database and save the data
conn = sqlite3.connect('../../../genieai.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS embeddings
             (id INTEGER PRIMARY KEY, chunk TEXT, embedding BLOB)''')

# Insert the chunks and embeddings into the database
for i, chunk in enumerate(chunks):
    c.execute("INSERT INTO embeddings (chunk, embedding) VALUES (?, ?)",
              (chunk, embedding_vectors[i].tobytes()))

conn.commit()
conn.close()

print("Data has been successfully saved to the database.")
