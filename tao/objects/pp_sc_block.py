from typing import Tuple, Optional, List, Union
from tao.objects.page_part import PagePart
from tao.objects.sc_argument import Argument
from tao.objects.pp_empty import Empty
from tao.objects.pp_comment import Comment, is_comment
from tao.utils import WHITESPACE_CHARS

BlockLabels = Tuple[Optional[str], Optional[str]]
BlockContent = Union["Block", Argument]

BLOCK_OPEN = "{"
BLOCK_CLOSE = "}"
ARG_ASSIGN_OP = "="


def tokenize_line(page_part_str: str) -> List[str]:
    """
    Tokenizes a Block definition line. Tokens are "{", "}", or non-whitespaced words.
    """
    tokens = []
    cur_token = ""
    for char in page_part_str:
        if char == '"':
            continue
        if char in WHITESPACE_CHARS:
            if cur_token:
                tokens.append(cur_token)
                cur_token = ""
        elif char in [BLOCK_OPEN, BLOCK_CLOSE]:
            if cur_token:
                tokens.append(cur_token)
                cur_token = ""
            tokens.append(char)
        else:
            cur_token += char

    if cur_token:
        tokens.append(cur_token)
    return tokens


class Block(PagePart):
    def __init__(
        self,
        page_part: List[str],
        block_type: str,
        labels: BlockLabels,
        contents: List[BlockContent],
        depth: int = 0,
    ) -> None:
        super().__init__(page_part, depth)
        self.block_type = block_type
        self.labels = labels
        self.contents = contents

    def parse(page: List[str], index: int = 0, depth: int = 0) -> Tuple[int, "Block"]:
        line_tokens = tokenize_line(page[index][depth * 2 :])  # "Title" line

        block_type = line_tokens[0]
        labels = tuple(line_tokens[1 : line_tokens.index(BLOCK_OPEN)])
        contents = []
        if line_tokens[-1] == BLOCK_CLOSE:  # Block open/closed in same line
            return index + 1, Block([page[index]], block_type, labels, contents)

        starting_index = index
        index += 1
        line_tokens = tokenize_line(page[index][depth * 2 :])
        while (not line_tokens) or (line_tokens[-1] != BLOCK_CLOSE):
            if BLOCK_OPEN in line_tokens:
                index, block = Block.parse(page, index=index, depth=depth + 1)
                contents.append(block)
            elif ARG_ASSIGN_OP in line_tokens:
                index, arg = Argument.parse(page, page_index=index, depth=depth + 1)
                contents.append(arg)
            elif not line_tokens:
                contents.append(Empty([page[index]], depth=depth + 1))
                index += 1
            elif is_comment(page[index][depth * 2 :]):
                index, comment = Comment.parse(page, index=index, depth=depth + 1)
                contents.append(comment)
            else:
                raise RuntimeError("Problem tokenizing/parsing line: %s" % str(line_tokens))

            line_tokens = tokenize_line(page[index][depth * 2 :])

        return index + 1, Block(page[starting_index : index + 1], block_type, labels, contents, depth=depth)

    def is_syntax_construct(self) -> bool:
        return True

    def render(self) -> str:
        labels = "".join([f"{label} " for label in self.labels])
        block_header = "%(block_type)s %(labels)s %(block_open)s" % {
            "block_type": self.block_type,
            "labels": labels,
            "block_open": BLOCK_OPEN,
        }
        if not self.contents:
            return "%(block_header)s%(block_close)s" % {"block_header": block_header, "block_close": BLOCK_CLOSE}
        else:
            content_rendered = "\n".join([content.render() for content in self.contents])
            return "\n".join([block_header, content_rendered, BLOCK_CLOSE])
