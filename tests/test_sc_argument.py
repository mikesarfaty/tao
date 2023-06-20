from tao.objects import Argument
from textwrap import dedent


def test_argument_parses_correctly():
    page = ["some_arg_name = 5"]
    _, arg = Argument.parse(page)

    assert arg.name == "some_arg_name"
    assert arg.value == "5"


def test_argument_parses_correctly_strings():
    page = ['foo = "bar"']
    _, arg = Argument.parse(page)

    assert arg.name == "foo"
    assert arg.value == '"bar"'


def test_argument_with_depth():
    page = ["  foobar = 6"]
    _, arg = Argument.parse(page, depth=1)

    assert arg.name == "foobar"
    assert arg.value == "6"


def test_argument_with_multiline():
    page = dedent(
        """\
        me = {
          name = "Mike Sarfaty"
          dob = "1998-02-11"
        }
        """
    ).split("\n")
    idx, arg = Argument.parse(page)
    assert arg.name == "me"
    assert arg.value == dedent(
        """\
        {
          name = "Mike Sarfaty"
          dob = "1998-02-11"
        }"""
    )


def test_hyphenated_argname():
    page = ["something-with-hypens = 5"]
    _, arg = Argument.parse(page)

    assert arg.name == "something-with-hypens"
    assert arg.value == "5"


def test_parens():
    page = ["six = add1(5)"]
    _, arg = Argument.parse(page)

    assert arg.name == "six"
    assert arg.value == "add1(5)"


def test_many_nested():
    page = dedent(
        """\
            a_value = function(
              {
                Name = "hello"
                Value = "goodbye"
              },
              [
                "a", "list", "of", "things
              ],
              another_function()
            )"""
    ).split("\n")
    expected = dedent(
        """\
        function(
          {
            Name = "hello"
            Value = "goodbye"
          },
          [
            "a", "list", "of", "things
          ],
          another_function()
        )"""
    )
    _, arg = Argument.parse(page)
    assert arg.name == "a_value"
    assert arg.value == expected


def test_arr():
    page = ['myArray = ["some", "array", "of", "strings"]']
    _, arg = Argument.parse(page)

    assert arg.name == "myArray"
    assert arg.value == '["some", "array", "of", "strings"]'


def test_parses_correctly_at_index():
    page = ['foo = "bar"', 'somethingelse = "another-value"']
    _, arg = Argument.parse(page, page_index=1, depth=0)

    assert arg.name == "somethingelse"
    assert arg.value == '"another-value"'
