output "client_public_ip" {
  value = aws_instance.client.public_ip
}

output "client_private_key" {
  value     = tls_private_key.client_ssh_key.private_key_pem
  sensitive = true
}
