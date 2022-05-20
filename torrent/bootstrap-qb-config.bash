#!/bin/bash

set -euo pipefail

echo "=== OPENVPN"
mkdir -p /dev/net
mknod /dev/net/tun c 10 200
mkdir -p /config/secrets
cp -v /secrets/* /config/secrets/
chown 0:0 /config/secrets/vpn.creds
chmod 400 /config/secrets/vpn.creds
openvpn --config /config/openvpn.conf &

CHECKS=10

until ip a show tun0 up > /dev/null
do
    echo "iface not up"
    sleep 1
    ((CHECKS=CHECKS-1))
    echo "$CHECKS"
    if [ $CHECKS -eq 0 ]; then
        echo "Too mani failures"
        exit 255
    fi
done

echo "nameserver 10.255.255.1" > /etc/resolv.conf
echo "=== TORRENT"
su torrent -c bash << EOS
mkdir -p ~torrent/.config/qBittorrent
if [ ! -f ~torrent/.config/qBittorrent/qBittorrent.conf ]; then
cat << EOF >> ~torrent/.config/qBittorrent/qBittorrent.conf
[LegalNotice]
Accepted=true
[Preferences]
WebUI\AuthSubnetWhitelistEnabled=true
WebUI\AuthSubnetWhitelist=0.0.0.0/0
WebUI\Port=8080
Connection\Interface=tun0
Connection\InterfaceName=tun0

EOF
fi

qbittorrent-nox
EOS
