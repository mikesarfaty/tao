from typing import List, Tuple


class PagePart:
    def __init__(self, page_part: list[str], depth: int = 0) -> None:
        self.page_part = page_part
        self.depth = depth

    def parse(page: List[str], index: int = 0, depth: int = 0) -> Tuple[int, "PagePart"]:
        raise NotImplementedError("PagePart")

    def render(self):
        raise NotImplementedError("PagePart")

    def is_comment(self) -> bool:
        return False

    def is_syntax_construct(self) -> bool:
        return False

    def is_empty_page_part(self) -> bool:
        return False
