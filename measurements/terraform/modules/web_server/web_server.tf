resource "aws_instance" "web_server" {
  ami           = var.debian-ami
  instance_type = "t2.micro"
  key_name      = aws_key_pair.web_server_key.key_name

  tags = {
    Name = "AcnTest"
  }

  vpc_security_group_ids = [aws_security_group.web_server_security_group.id]
}

resource "tls_private_key" "web_server_ssh_key" {
  algorithm = "RSA"
  rsa_bits = 4096
}

resource "aws_key_pair" "web_server_key" {
  key_name   = "web-server-key"
  public_key = tls_private_key.web_server_ssh_key.public_key_openssh
}

resource "aws_security_group" "web_server_security_group" {
  
  ingress {
    from_port   = 2135
    to_port     = 2135
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 2136
    to_port     = 2136
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 2138
    to_port     = 2138
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 2139
    to_port     = 2139
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
