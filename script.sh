cd terraform
terraform validate
terraform apply
terraform output -raw web_server_private_key > ../web_server_private_key.pem
# terraform output -raw client_private_key > ../client_private_key.pem
# web_server_public_ip=$(terraform output web_server_public_ip | tr -d '\n' | tr -d '"')
# client_public_ip=$(terraform output client_public_ip | tr -d '\n' | tr -d '"')
cd ..
chmod 600 web_server_private_key.pem
# chmod 600 client_private_key.pem
cd ansible
sed -i '' "s/[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}/$web_server_public_ip/" inventory.ini
