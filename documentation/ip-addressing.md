# IP Addressing Plan

## Network Overview

This document defines the IP addressing scheme for the Multi-Vendor Enterprise Network.

## WAN and Router Links

| Network | Purpose | Subnet |
|---|---|---|
| Internet Link | Internet → Cisco R1 | 203.0.113.0/30 |
| Cisco–Juniper Link | R1 → R2 | 10.0.12.0/30 |
| Juniper–Huawei Link | R2 → R3 | 10.0.23.0/30 |
| Branch LAN | Client Network | 192.168.10.0/24 |

---

# Device IP Addresses

## Cisco R1 — Edge Router

| Interface | IP Address | Subnet Mask | Purpose |
|---|---|---|---|
| GigabitEthernet0/0 | 203.0.113.2 | 255.255.255.252 | Internet |
| GigabitEthernet0/1 | 10.0.12.1 | 255.255.255.252 | Connection to Juniper R2 |

---

## Juniper R2 — Core Router

| Interface | IP Address | Prefix | Purpose |
|---|---|---|---|
| ge-0/0/0 | 10.0.12.2 | /30 | Connection to Cisco R1 |
| ge-0/0/1 | 10.0.23.1 | /30 | Connection to Huawei R3 |

---

## Huawei R3 — Branch Router

| Interface | IP Address | Subnet Mask | Purpose |
|---|---|---|---|
| GigabitEthernet0/0/0 | 10.0.23.2 | 255.255.255.252 | Connection to Juniper R2 |
| GigabitEthernet0/0/1 | 192.168.10.1 | 255.255.255.0 | Branch LAN Gateway |

---

# Branch LAN

Network:

```text
192.168.10.0/24