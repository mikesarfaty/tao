from tao.objects.page_part import PagePart
from typing import List, Tuple


class Empty(PagePart):
    def __init__(self, page_part: list[str], depth: int = 0) -> None:
        super().__init__(page_part, depth)

    def parse(page: List[str], index: int = 0, depth: int = 0) -> Tuple[int, "Empty"]:
        return Empty([page[index]], depth=depth)

    def is_empty_page_part(self) -> bool:
        return True

    def render(self) -> str:
        return ""
