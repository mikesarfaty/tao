from tao.objects import Empty


def test_empty_pagepart_parses():
    p = ["", ""]
    Empty.parse(p)
