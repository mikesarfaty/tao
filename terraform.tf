resource "aws_ec2_instance" "foo" {
  tags = {
    "Name" = "AName"
  }
}
