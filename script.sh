cd terraform
terraform validate
terraform apply
terraform output -raw private_key > ../shared/private_key.pem
public_ip=$(terraform output instance_public_ip | tr -d '\n' | tr -d '"')
cd ../ansible
sed -i '' "s/[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}/$public_ip/" inventory.ini
