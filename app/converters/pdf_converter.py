from pdf2image import convert_from_path
from docx import Document
from .base import BaseConverter

class PdfToImageConverter(BaseConverter):
    def convert(self, input_path:str, output_path:str):
        images = convert_from_path(input_path)
        images[0].save(output_path)

class PdfToDocxConverter(BaseConverter):
    def convert(self, input_path:str, output_path:str):
        document = Document()
        document.add_paragraph("PDF to DOCX Placeholder")
        document.save(output_path)

