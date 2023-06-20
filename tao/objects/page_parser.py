from ..utils import split_leading_whitespace
from .pp_comment import Comment, CommentCharacters

"""
A Page is a PagePart[]

A PagePart is one of:
    - LineComment
    - EmptyPagePart
    - SyntaxConstruct

A LineComment is a String that starts with # or //
An EmptyPagePart is an empty string ("")
    
A SyntaxConstruct is one of:
    - A Block
    - An Argument

A Block is a str[] that follows the pattern:
[
    'BlockType "BlockLabel"? "BlockLabel"? {'
    '\s\sArgument?',
    ...
    '\s\sArgument?',
    '}',
]

An Argument is a str[] that follows the pattern:
[
    'ArgumentName = ArgumentValue'
]
"""


class PageParser:
    def __init__(self, page) -> None:
        self.page_strarr = page
        self.weight = 0
        self.index = 0

    def parse(self):
        page = []
        while self.index < len(self.page_strarr):
            if self.is_line_comment():
                comment, self.index = Comment.parse(self.page_strarr, self.index)
                page.append(comment)

    @property
    def cur_line(self):
        return self.page[self.index]

    @property
    def cur_line_nw(self):
        _, rest = split_leading_whitespace(self.cur_line)
        return rest

    def is_line_comment(self):
        """
        Is the current index of this PageParser at a LineComment?
        """
        if not self.cur_line_nw:
            return False

        if len(self.cur_line_nw) == 1:
            return self.cur_line_nw == CommentCharacters.SINGLELINE_CONV
        else:
            return self.cur_line_nw[:2] in [CommentCharacters.SINGLELINE_UNCONV, CommentCharacters.MULTILINE]

    def is_empty_page_part(self):
        """
        Is the current index of this PageParser at an EmptyPagePart?
        """
        return False

    def is_syntax_construct(self):
        """
        Is the current index of this PageParser at a SyntaxConstruct?
        """
        return False
