apt-get update
apt-get install apt-transport-https
apt-get install gnupg
wget -q -O - https://repo.i2pd.xyz/.help/add_repo | sudo bash -s -
apt-get update
apt-get install i2pd

cat <<EOF >> /etc/i2pd/tunnels.conf
[UDP-server]
type = udpserver
keys = udp_server.dat
host = 127.0.0.1
port = 2138
EOF

# cat <<EOF >> /etc/i2pd/tunnels.conf
# [UDP-client]
# type = udpclient
# destination = something.b32.i2p
# port = 2138
# EOF

systemctl restart i2pd
