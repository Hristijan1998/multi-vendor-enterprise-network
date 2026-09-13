# Network Topology

## Project Overview

This project represents a small multi-vendor enterprise network consisting of Cisco, Juniper, and Huawei network devices.

The network connects an enterprise branch network to the internet through a Cisco edge router.

## Network Devices

| Device | Vendor | Role |
|---|---|---|
| R1 | Cisco | Edge Router |
| R2 | Juniper | Core Router |
| R3 | Huawei | Branch Router |

## Network Topology

```text
                    INTERNET
                       |
                       |
              203.0.113.0/30
                       |
                       |
              +--------+--------+
              |    Cisco R1     |
              |   Edge Router   |
              |                 |
              |   NAT + ACL     |
              +--------+--------+
                       |
                  10.0.12.0/30
                       |
              +--------+--------+
              |   Juniper R2    |
              |   Core Router   |
              |                 |
              |      OSPF       |
              +--------+--------+
                       |
                  10.0.23.0/30
                       |
              +--------+--------+
              |   Huawei R3     |
              |  Branch Router  |
              |                 |
              |   DHCP + ACL    |
              +--------+--------+
                       |
                 192.168.10.0/24
                       |
                +------+------+
                |  Branch LAN |
                |   Clients   |
                +-------------+