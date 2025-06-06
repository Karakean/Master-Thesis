apt-get update
apt-get install apt-transport-https lsb-release curl

echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/i2p.list

curl -o i2p-archive-keyring.gpg https://geti2p.net/_static/i2p-archive-keyring.gpg

gpg --keyid-format long --import --import-options show-only --with-fingerprint i2p-archive-keyring.gpg

cp i2p-archive-keyring.gpg /usr/share/keyrings

apt-get update
apt-get install i2p i2p-keyring
