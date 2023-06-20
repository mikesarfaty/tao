from typing import List, Tuple
from string import ascii_letters, digits

IDENTIFIER_CHARS = set(ascii_letters + digits + "_" + "-")
SEPARATOR_CHARS = set(" =")  # Characters that separate the identifier (name) and value of an argument


class Argument:
    """
    In Terraform, an Argument is an identifier that is assigned a specific value

    identifier_foo = "identifier value"
    """

    def __init__(self, arg_name: str, arg_value: str, depth=0) -> None:
        self.depth = depth
        self.name = arg_name
        self.value = arg_value

    def parse(page: List[str], page_index: int = 0, depth: int = 0) -> Tuple[int, "Argument"]:
        cur_line = page[page_index][depth * 2 :]
        arg_name = ""
        line_index = 0

        while (char := cur_line[line_index]) in IDENTIFIER_CHARS:
            arg_name += char
            line_index += 1

        arg_value = ""
        while cur_line[line_index] in SEPARATOR_CHARS:
            line_index += 1

        open_braces = 0
        open_parens = 0
        open_brackets = 0
        while line_index < len(cur_line) or open_braces or open_parens or open_brackets:
            if line_index == len(cur_line):
                page_index += 1
                cur_line = page[page_index][depth * 2 :]
                line_index = 0
                arg_value += "\n"

            char = cur_line[line_index]
            if char == "{":
                open_braces += 1
            if char == "}":
                open_braces -= 1
            if char == "(":
                open_parens += 1
            if char == ")":
                open_parens -= 1
            if char == "[":
                open_brackets += 1
            if char == "]":
                open_brackets -= 1

            arg_value += char
            line_index += 1

        return page_index + 1, Argument(arg_name, arg_value, depth=depth)

    def render(self, padding=1) -> str:
        return f"{self.name}{' ' * padding}= {self.value}"
