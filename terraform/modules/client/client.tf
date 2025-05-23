resource "aws_instance" "client" {
  ami           = var.debian-ami
  instance_type = "t2.micro"
  key_name      = aws_key_pair.client_key.key_name

  tags = {
    Name = "AcnTest"
  }

  vpc_security_group_ids = [aws_security_group.client_security_group.id]
}

resource "tls_private_key" "client_ssh_key" {
  algorithm = "RSA"
  rsa_bits = 4096
}

resource "aws_key_pair" "client_key" {
  key_name   = "client-key"
  public_key = tls_private_key.client_ssh_key.public_key_openssh
}

resource "aws_security_group" "client_security_group" {
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] #[var.current_ip]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
