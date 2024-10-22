class NotImplementedException(Exception):
    def __init__(self, method_name, class_name) -> None:
        super().__init__(f'{method_name} not implemented for {class_name}')