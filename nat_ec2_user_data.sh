#!/bin/bash -x
yum update -y
yum install -y iptables iproute
echo "net.ipv4.ip_forward = 1" | tee -a /etc/sysctl.conf
sysctl -p
iptables -t nat -A POSTROUTING -o ens5 -s 0.0.0.0/0 -j MASQUERADE