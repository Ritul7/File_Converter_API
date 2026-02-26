import pandas as pd
from .base import BaseConverter

class CsvToJsonConverter(BaseConverter):
    def convert(self, input_path:str, output_path:str):
        df = pd.read_csv(input_path)
        df.to_json(output_path, orient="records")

class JsonToCsvConverter(BaseConverter):
    def convert(self, input_path:str, output_path:str):
        df = pd.read_json(input_path)
        df.to_csv(output_path, index=False)