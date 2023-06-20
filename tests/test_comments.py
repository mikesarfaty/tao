from typing import List
from tao.objects import Comment
import pytest


def test_singleline_conventional_comment():
    c_str = ["# this is a terraform comment"]
    _, c = Comment.parse(c_str)

    assert c.comment == [" this is a terraform comment"]
    assert c.comment_chars == "#"
    assert c.page_part == c_str
    assert not c.is_multiline
    assert c.render() == "".join(c_str)


def test_singleline_unconventional_comment():
    c_str = ["// this is another terraform comment"]
    _, c = Comment.parse(c_str)

    assert c.comment == [" this is another terraform comment"]
    assert c.comment_chars == "//"
    assert c.page_part == c_str
    assert not c.is_multiline
    assert c.render() == "".join(c_str)


def test_multiline_comment():
    c_str = [
        "/*",
        " * this is the first line of a ML comment",
        " * here is the second line",
        " * and here is the final line",
        " */",
    ]
    _, c = Comment.parse(c_str)
    assert len(c.comment) == 5
    assert c.comment[0] == ""
    assert c.comment[2] == " here is the second line"
    assert c.comment[4] == ""
    assert c.render() == "\n".join(c_str)


def test_multiline_poorly_formatted_comment():
    c_str = ["/*", "this should have a preceeding star", " */"]
    _, c = Comment.parse(c_str)
    assert len(c.comment) == 3
    assert c.comment[0] == ""
    assert c.comment[1] == "this should have a preceeding star"
    assert c.comment[2] == ""

    c_str_preferable = ["/*", " *this should have a preceeding star", " */"]
    assert c.render() == "\n".join(c_str_preferable)


def test_multiline_inline_comment_start():
    c_str = ["/* starting the comment right away", " */"]
    _, c = Comment.parse(c_str)
    assert len(c.comment) == 2
    assert c.comment[0] == " starting the comment right away"
    assert c.comment[1] == ""
    assert c.is_multiline

    assert c.render() == "\n".join(c_str)


def test_multiline_syntax_singleline_comment():
    c_str = ["/* using a multiline comment */"]
    _, c = Comment.parse(c_str)
    assert len(c.comment) == 1
    assert c.comment[0] == " using a multiline comment "
    assert c.is_multiline
    assert c.render() == "\n".join(c_str)


def test_singleline_comment_double_comment():
    c_str = ["## a comment pattern I hate"]
    _, c = Comment.parse(c_str)
    assert len(c.comment) == 1
    assert c.comment[0] == "# a comment pattern I hate"
    assert c.render() == "\n".join(c_str)


def test_singleline_comment_different_comment():
    c_str = ["#// this is a crime"]
    _, c = Comment.parse(c_str)
    assert c.comment[0] == "// this is a crime"


def test_multiple_multiline_start():
    c_str = ["/*", "/* this is weirdly valid", "*/"]
    _, c = Comment.parse(c_str)
    assert c.comment[1] == "/* this is weirdly valid"


def test_singleline_with_index_and_depth():
    c_str = [
        "this line could be whatever, maybe a module",
        "  # a depth of one, like inside of a block",
        "this line also doesn't matter",
    ]
    next_idx, c = Comment.parse(c_str, depth=1, index=1)
    assert len(c.comment) == 1
    assert c.comment[0] == " a depth of one, like inside of a block"
    assert next_idx == 2
