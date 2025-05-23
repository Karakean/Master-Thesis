apt update
apt install gnupg
curl -so /etc/apt/trusted.gpg.d/oxen.gpg https://deb.oxen.io/pub.gpg
echo "deb https://deb.oxen.io $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/oxen.list
apt update
apt install lokinet

sed -i 's|#keyfile=.*|keyfile=/var/lib/lokinet/snappkey.private|' /etc/loki/lokinet.ini
sed -i 's|#ifaddr=.*|ifaddr=172.16.0.1/16|' /etc/loki/lokinet.ini
systemctl restart lokinet

host -t cname localhost.loki 127.3.2.1

