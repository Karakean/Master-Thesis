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

data "http" "current_ip" {
  url = "http://checkip.amazonaws.com/"
}

module "web_server" {
  source = "./modules/web_server"
  current_ip = "${trimspace(data.http.current_ip.response_body)}/32"
}

# module "client" {
#   source = "./modules/client"
#   current_ip = "${trimspace(data.http.current_ip.response_body)}/32"
# }

output "web_server_public_ip" {
  value = module.web_server.web_server_public_ip
}

output "web_server_private_key" {
  value     = module.web_server.web_server_private_key
  sensitive = true
}

# output "client_public_ip" {
#   value = module.client.client_public_ip
# }

# output "client_private_key" {
#   value     = module.client.client_private_key
#   sensitive = true
# }