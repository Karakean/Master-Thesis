terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.83.0"
    }
    tls = {
        source = "hashicorp/tls"
        version = "~> 4.0.6"
    }
    http = {
        source = "hashicorp/http"
        version = "~> 3.4.5"
    }
  }
}

provider "aws" {
  region = var.region
}

resource "aws_instance" "web_server" {
  ami           = var.debian-ami
  instance_type = "t2.micro"
  key_name      = aws_key_pair.web_key.key_name

  tags = {
    Name = "AcnTestWebServer"
  }

  vpc_security_group_ids = [aws_security_group.web_server_security_group.id]
}

output "instance_public_ip" {
  value = aws_instance.web_server.public_ip
}

data "http" "my_ip" {
  url = "http://checkip.amazonaws.com/"
}

resource "aws_security_group" "web_server_security_group" {

  ingress {
    from_port   = 5201
    to_port     = 5201
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5201
    to_port     = 5201
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # ["${trimspace(data.http.my_ip.response_body)}/32"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "tls_private_key" "ssh_key" {
  algorithm = "RSA"
  rsa_bits = 4096
}

resource "aws_key_pair" "web_key" {
  key_name   = "web-server-key"
  public_key = tls_private_key.ssh_key.public_key_openssh
}

output "private_key" {
  value     = tls_private_key.ssh_key.private_key_pem
  sensitive = true
}
