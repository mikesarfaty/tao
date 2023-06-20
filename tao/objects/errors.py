class ParsingError(Exception):
    def __init__(self, parser_type, msg) -> None:
        self.parser_type = parser_type
        super().__init__(msg)