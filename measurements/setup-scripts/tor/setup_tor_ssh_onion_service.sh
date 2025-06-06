#!/bin/bash

CPU_ARCHITECTURE=$(dpkg --print-architecture)
DISTRIBUTION=$(lsb_release -c | awk '{print $2}')

apt update && apt install -y apt-transport-https gnupg openssl basez

tee /etc/apt/sources.list.d/tor.list > /dev/null <<EOF
   deb     [signed-by=/usr/share/keyrings/deb.torproject.org-keyring.gpg] https://deb.torproject.org/torproject.org $DISTRIBUTION main
   deb-src [signed-by=/usr/share/keyrings/deb.torproject.org-keyring.gpg] https://deb.torproject.org/torproject.org $DISTRIBUTION main
EOF

wget -qO- https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc | gpg --dearmor | tee /usr/share/keyrings/deb.torproject.org-keyring.gpg >/dev/null

apt update
apt install tor deb.torproject.org-keyring

openssl genpkey -algorithm x25519 -out /tmp/ssh_key.prv.pem
cat /tmp/ssh_key.prv.pem | grep -v " PRIVATE KEY" | base64pem -d | tail --bytes=32 | base32 | sed 's/=//g' > /tmp/ssh_key.prv.key
openssl pkey -in /tmp/ssh_key.prv.pem -pubout | grep -v " PUBLIC KEY" | base64pem -d | tail --bytes=32 | base32 | sed 's/=//g' > /tmp/ssh_key.pub.key

mkdir -p /var/lib/tor/ssh_onion_service/authorized_clients/
tee /var/lib/tor/ssh_onion_service/authorized_clients/ssh.auth > /dev/null <<EOF
descriptor:x25519:$(cat /tmp/ssh_key.pub.key)
EOF
chown -R debian-tor /var/lib/tor/
chmod 700 -R /var/lib/tor/

cat <<EOF >> /etc/tor/torrc
HiddenServiceDir /var/lib/tor/ssh_onion_service/
HiddenServicePort 22 127.0.0.1:22
EOF

systemctl restart tor
cat /var/lib/tor/ssh_onion_service/hostname

# journalctl -e -u tor@default