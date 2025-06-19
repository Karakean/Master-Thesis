#!/bin/bash

CPU_ARCHITECTURE=$(dpkg --print-architecture)
DISTRIBUTION=$(lsb_release -c | awk '{print $2}')

apt update
apt install apt-transport-https

tee /etc/apt/sources.list.d/tor.list > /dev/null <<EOF
   deb     [signed-by=/usr/share/keyrings/deb.torproject.org-keyring.gpg] https://deb.torproject.org/torproject.org $DISTRIBUTION main
   deb-src [signed-by=/usr/share/keyrings/deb.torproject.org-keyring.gpg] https://deb.torproject.org/torproject.org $DISTRIBUTION main
EOF

apt update
apt install gnupg
wget -qO- https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc | gpg --dearmor | tee /usr/share/keyrings/deb.torproject.org-keyring.gpg >/dev/null

apt update
apt install tor deb.torproject.org-keyring

mkdir /var/lib/tor/tcp_latency_onion_service
mkdir /var/lib/tor/tcp_throughput_onion_service

chown -R debian-tor /var/lib/tor/
chmod 700 -R /var/lib/tor/

cat <<EOF >> /etc/tor/torrc
HiddenServiceDir /var/lib/tor/tcp_latency_onion_service/
HiddenServicePort 2135 127.0.0.1:2135

HiddenServiceDir /var/lib/tor/tcp_throughput_onion_service/
HiddenServicePort 2136 127.0.0.1:2136
EOF

systemctl restart tor

# cat /var/lib/tor/onion_service/hostname
# journalctl -e -u tor@default