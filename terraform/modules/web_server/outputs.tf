output "web_server_public_ip" {
  value = aws_instance.web_server.public_ip
}

output "web_server_private_key" {
  value     = tls_private_key.web_server_ssh_key.private_key_pem
  sensitive = true
}
