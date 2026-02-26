from .csv_json_converter import CsvToJsonConverter, JsonToCsvConverter
from .pdf_converter import PdfToDocxConverter, PdfToImageConverter

CONVERTER_MAP = {
    ("csv", "json"): CsvToJsonConverter,
    ("json", "csv"): JsonToCsvConverter,
    ("pdf","docx"): PdfToDocxConverter,
    ("pdf","png"): PdfToImageConverter,
    ("pdf","jpg"): PdfToImageConverter   
}



