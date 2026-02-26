from pdf2image import convert_from_path
from docx import Document
from .base import BaseConverter
from pdf2docx import Converter
import logging

logger = logging.getLogger(__name__)                # __name__: It is a built-in variable and holds the name of current module(file)

class PdfToImageConverter(BaseConverter):
    def convert(self, input_path:str, output_path:str):
        try:
            images = convert_from_path(input_path, thread_count=2)
            images[0].save(output_path)                         # It will only take the first page of the pdf and then converts it into png
        
            images[0].save(output_path, "JPEG" if output_path.endswith(".jpg") else "PNG")

        except Exception as exc:
            logger.error(f"Image Conversion Error= {str(exc)}")
            raise exc

class PdfToDocxConverter(BaseConverter):
    def convert(self, input_path:str, output_path:str):

        try:
            cv = Converter(input_path)                      # input_path: jaha pr copy of pdf file store hogi
            cv.convert(output_path, start=0, end=None)      # output path: Is the path where converted file will be stored
            cv.close()
        except Exception as e:
            print(f"Conversion Error: {str(e)}")
            raise e

# ........Clearly dikh rha(uncomment krne pr dikhega) h ki, input to le nhi rha h, so basically ye library bs ek fake docs return kr rhi h, not actually converting and then returning it, so we'll be using pdf2docx library.........

# class PdfToDocxConverter(BaseConverter):
#     def convert(self, input_path:str, output_path:str):
#         document = Document()
#         document.add_paragraph("PDF to DOCX Placeholder")
#         document.save(output_path)

