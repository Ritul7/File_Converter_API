
class BaseConverter :
    def convert(self, input_path: str, output_path: str):
        raise NotImplementedError("Convert method must be implemented")
    