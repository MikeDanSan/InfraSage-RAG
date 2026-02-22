"""
Document ingestion pipeline.

Responsibilities:
- Accept a PDF file path
- Extract text from PDF (using pdfplumber or PyPDF)
- Clean extracted text (whitespace, encoding issues)
- Chunk text into pieces of configurable size with configurable overlap
- Return a list of text chunks ready for embedding
"""
