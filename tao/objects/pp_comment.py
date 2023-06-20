from tao.objects.page_part import PagePart
from tao.utils import split_leading_whitespace
from typing import Tuple, List
from enum import Enum

COMMENT_MULTILINE_END = "*/"
COMMENT_MULTILINE_MIDDLE = " *"
COMMENT_MULTILINE_SPECIALCHAR = "*"


class CommentCharacters(str, Enum):
    MULTILINE = "/*"
    SINGLELINE_CONV = "#"
    SINGLELINE_UNCONV = "//"


class Comment(PagePart):
    def __init__(
        self, page_part: List[str], comment_chars: CommentCharacters, comment: List[str], depth: int = 0
    ) -> None:
        super().__init__(page_part, depth=depth)
        self.comment_chars = comment_chars
        self.comment = comment

    def render(self):
        return ""

    @property
    def is_multiline(self):
        return self.comment_chars == CommentCharacters.MULTILINE

    def parse(page, index: int = 0, depth: int = 0):
        cur_line = page[index]
        cur_line_nw = cur_line[depth * 2 :]
        if cur_line_nw.startswith(CommentCharacters.SINGLELINE_CONV):
            comment = Comment(
                [page[index]],
                CommentCharacters.SINGLELINE_CONV,
                [cur_line_nw[1:]],
                depth=depth,
            )
        elif cur_line_nw.startswith(CommentCharacters.SINGLELINE_UNCONV):
            comment = Comment(
                [page[index]],
                CommentCharacters.SINGLELINE_UNCONV,
                [cur_line_nw[2:]],
                depth=depth,
            )
        else:
            """
            For multiline comments, we will differ from norm here by enforcing that the comments will be properly
            formatted even though Terraform doesn't enforce it. The formatting will be that it starts with /*,
            The middle lines start with *'s, the depth is correct, and it ends with */. For acceptable formats, see the tests file.
            In keeping with consistency, none of the comment syntax will be stored, only added on-render.
            """
            index, comment = Comment._parse_multiline(page, index, depth)

        return index + 1, comment

    def _parse_multiline(page, index: int, depth: int) -> Tuple[int, "Comment"]:
        cur_line = page[index]
        cur_line_nw = cur_line[depth * 2 :]
        comment = []

        if cur_line_nw.startswith(CommentCharacters.MULTILINE):
            cur_line_nw = cur_line_nw[2:]

        while not cur_line_nw.endswith(COMMENT_MULTILINE_END):
            if cur_line_nw.startswith(COMMENT_MULTILINE_MIDDLE):
                comment.append(cur_line_nw[2:])
            else:
                comment.append(cur_line_nw)
            index += 1
            cur_line_nw = page[index][depth * 2 :]

        final_line = cur_line_nw[:-2]
        if final_line == " ":
            comment.append("")
        else:
            comment.append(final_line)

        return index, Comment([page[index]], CommentCharacters.MULTILINE, comment, depth=depth)

    def is_comment(self) -> bool:
        return True

    def render(self) -> str:
        if not self.is_multiline:
            return f"{self.comment_chars}{self.comment[0]}"
        else:
            multiline_unclosed = "/*" + f"\n{COMMENT_MULTILINE_MIDDLE}".join(self.comment)
            if not multiline_unclosed[-1] == COMMENT_MULTILINE_SPECIALCHAR:
                return multiline_unclosed + COMMENT_MULTILINE_END
            else:
                return multiline_unclosed + "/"


def is_comment(page_part_str: str) -> bool:
    _, cur_line_nw = split_leading_whitespace(page_part_str)
    return (
        cur_line_nw.startswith(CommentCharacters.SINGLELINE_CONV)
        or cur_line_nw.startswith(CommentCharacters.SINGLELINE_UNCONV)
        or cur_line_nw.startswith(CommentCharacters.MULTILINE)
    )
