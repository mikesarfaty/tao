from textwrap import dedent
from typing import List
from pathlib import Path
from tao.objects import Block, Argument, Empty, tokenize_line


# Helpers
def read_testfile(test_file_name: str) -> List[str]:
    test_file_path = Path(__file__).resolve().parent / "test_files" / test_file_name
    with open(test_file_path) as test_file:
        content = test_file.read()

    return content.split("\n")


# Tests
def test_tokenize():
    to_tokenize = "hello     my name        \t is"
    assert tokenize_line(to_tokenize) == ["hello", "my", "name", "is"]


def test_tokenize_braces():
    to_tokenize = "hello{ }} my name{ }\t\t\t{is"
    assert tokenize_line(to_tokenize) == ["hello", "{", "}", "}", "my", "name", "{", "}", "{", "is"]


def test_parse_singleline_block():
    page = ['data "aws_caller_identity" "current" {}']
    idx, block = Block.parse(page)

    assert block.contents == []
    assert block.block_type == "data"
    assert block.labels == (
        "aws_caller_identity",
        "current",
    )
    assert block.depth == 0
    assert block.page_part == page
    assert idx == 1


def test_parse_a_local_block():
    page = dedent(
        """\
        locals {
          foo = 100
        }"""
    ).split("\n")
    idx, block = Block.parse(page)

    assert block.block_type == "locals"
    assert len(block.contents) == 1
    arg = block.contents[0]
    assert isinstance(arg, Argument)
    assert arg.depth == 1
    assert arg.name == "foo"
    assert arg.value == "100"
    assert idx == 3


def test_parse_nested_blocks():
    page = read_testfile("eks_cluster.tf")
    _, block = Block.parse(page)

    assert len(block.contents) == 8
    arg_name, arg_role, empty1, block_vpc_config, empty2, arg_tags, empty3, arg_depends_on, *_ = block.contents

    assert arg_name.name == "name"
    assert arg_name.value == "var.cluster_name"

    assert arg_role.name == "role_arn"
    assert arg_role.value == "aws_iam_role.cluster_role.arn"

    assert isinstance(empty1, Empty)
    assert isinstance(empty2, Empty)
    assert isinstance(empty3, Empty)

    # Check the nested vpc_config{} block
    assert isinstance(block_vpc_config, Block)
    assert block_vpc_config.block_type == "vpc_config"
    assert block_vpc_config.labels == ()
    assert len(block_vpc_config.contents) == 3
    for block_content in block_vpc_config.contents:
        assert block_content.name in ["endpoint_private_access", "endpoint_public_access", "subnet_ids"]

    assert arg_tags.name == "tags"
    assert arg_tags.value == "var.tags"

    assert arg_depends_on.name == "depends_on"
    assert arg_depends_on.value == dedent(
        """\
          [
            aws_iam_role_policy_attachment.eks_cluster_policy,
            aws_iam_role_policy_attachment.vpc_resource_controller,
          ]"""
    )
