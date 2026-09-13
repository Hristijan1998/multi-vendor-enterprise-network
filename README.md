# Multi-Vendor Enterprise Network

A multi-vendor enterprise network design project demonstrating interoperability between Cisco, Juniper, and Huawei network devices.

The project focuses on enterprise network architecture, IP addressing, dynamic routing, NAT, DHCP, Access Control Lists, network security, troubleshooting, and Python-based configuration validation.

> **Project Type:** Network Design and Configuration Portfolio Project
> **Environment:** Visual Studio Code + Python
> **Vendors:** Cisco IOS, Juniper Junos, Huawei VRP

---

# Project Overview

This project demonstrates the design of a small enterprise network using devices from three different network vendors.

The network consists of:

* Cisco R1 — Edge Router
* Juniper R2 — Core Router
* Huawei R3 — Branch Router

The routers are connected using a single-area OSPF design.

The Huawei router provides connectivity to the Branch LAN, while the Cisco router provides Internet connectivity using NAT/PAT.

---

# Network Architecture

```text
                         INTERNET
                            |
                     203.0.113.0/30
                            |
                    +----------------+
                    |   Cisco R1     |
                    |   Edge Router  |
                    |                |
                    | OSPF / NAT     |
                    | ACL / Default  |
                    +--------+-------+
                             |
                        10.0.12.0/30
                             |
                    +--------+-------+
                    |   Juniper R2   |
                    |   Core Router  |
                    |                |
                    | OSPF / Routing |
                    +--------+-------+
                             |
                        10.0.23.0/30
                             |
                    +--------+-------+
                    |   Huawei R3    |
                    |  Branch Router |
                    |                |
                    | OSPF / DHCP    |
                    | ACL            |
                    +--------+-------+
                             |
                       192.168.10.0/24
                             |
                         Branch LAN
```

---

# Network Devices

| Device | Vendor  | Role          | Router ID |
| ------ | ------- | ------------- | --------- |
| R1     | Cisco   | Edge Router   | 1.1.1.1   |
| R2     | Juniper | Core Router   | 2.2.2.2   |
| R3     | Huawei  | Branch Router | 3.3.3.3   |

---

# Project Features

## Multi-Vendor Network Design

The project demonstrates a network architecture involving:

* Cisco IOS configuration syntax
* Juniper Junos configuration syntax
* Huawei VRP configuration syntax

The project shows how different network vendors can participate in the same enterprise routing architecture.

---

# IP Addressing

| Network         | Purpose                |
| --------------- | ---------------------- |
| 10.0.12.0/30    | Cisco R1 ↔ Juniper R2  |
| 10.0.23.0/30    | Juniper R2 ↔ Huawei R3 |
| 192.168.10.0/24 | Branch LAN             |
| 203.0.113.0/30  | Internet/WAN           |

## Device Addresses

| Device     | Interface  | IP Address      |
| ---------- | ---------- | --------------- |
| Cisco R1   | Link to R2 | 10.0.12.1/30    |
| Juniper R2 | Link to R1 | 10.0.12.2/30    |
| Juniper R2 | Link to R3 | 10.0.23.1/30    |
| Huawei R3  | Link to R2 | 10.0.23.2/30    |
| Huawei R3  | Branch LAN | 192.168.10.1/24 |

---

# Dynamic Routing — OSPF

The network uses OSPF as the dynamic routing protocol.

## OSPF Design

* OSPF Process ID: 1
* OSPF Area: 0
* Single-Area Design
* Dynamic Route Advertisement
* Default Route Propagation

## OSPF Domain

```text
Cisco R1
Router ID: 1.1.1.1
       |
       | OSPF Area 0
       |
Juniper R2
Router ID: 2.2.2.2
       |
       | OSPF Area 0
       |
Huawei R3
Router ID: 3.3.3.3
```

Huawei R3 advertises the Branch LAN:

```text
192.168.10.0/24
```

Cisco R1 advertises the default route into the OSPF domain.

---

# Internet Connectivity

Cisco R1 acts as the enterprise edge router.

The default route points toward the Internet gateway:

```text
0.0.0.0/0 → 203.0.113.1
```

Cisco R1 advertises the default route through OSPF.

The expected traffic path is:

```text
Branch Client
      |
      v
Huawei R3
      |
      v
Juniper R2
      |
      v
Cisco R1
      |
      v
Internet
```

---

# NAT/PAT

Cisco R1 provides Network Address Translation.

The Branch LAN uses private addressing:

```text
192.168.10.0/24
```

PAT allows multiple Branch clients to access the Internet using the Cisco R1 Internet-facing address.

Conceptually:

```text
192.168.10.x
      |
      v
Huawei R3
      |
      v
Juniper R2
      |
      v
Cisco R1
      |
     NAT
      |
      v
Internet
```

---

# DHCP

Huawei R3 provides DHCP services for the Branch LAN.

## DHCP Network

```text
Network: 192.168.10.0/24
Gateway: 192.168.10.1
```

Example DHCP allocation:

```text
192.168.10.100 - 192.168.10.200
```

Reserved addresses:

```text
192.168.10.1        Default Gateway
192.168.10.2-99     Reserved
192.168.10.201-254  Reserved
```

---

# Network Security

The project includes several basic network security mechanisms.

## Cisco R1

* Internet-facing ACL
* NAT/PAT
* RFC1918 source-address filtering
* Established TCP return traffic
* ICMP echo-reply handling

## Juniper R2

* SSH management service
* Proposed core protection firewall filter
* OSPF traffic handling
* Internal network traffic policy

> The Juniper firewall filter is documented as a proposed security policy and is not applied to interfaces in this design-only project.

## Huawei R3

* Branch LAN ACL
* Basic source-address filtering
* DHCP address segmentation

---

# Python Network Validation

The project includes a Python-based configuration validation script.

Location:

```text
scripts/network_validation.py
```

The script checks the Cisco, Juniper, and Huawei configuration files for expected network components.

## Cisco Validation

The script checks for:

* Interface configuration
* OSPF
* NAT
* ACL
* Default route

## Juniper Validation

The script checks for:

* Hostname
* Cisco link
* Huawei link
* OSPF
* Router ID

## Huawei Validation

The script checks for:

* Hostname
* Juniper link
* Branch LAN
* OSPF
* DHCP
* ACL

## Run the Validation

From the project root:

```powershell
py scripts\network_validation.py
```

Example result:

```text
========================================
MULTI-VENDOR NETWORK VALIDATION
========================================

Checking Cisco R1
----------------------------------------
[PASS] Interface Configuration
[PASS] OSPF
[PASS] NAT
[PASS] ACL
[PASS] Default Route

Checking Juniper R2
----------------------------------------
[PASS] Hostname
[PASS] Cisco Link
[PASS] Huawei Link
[PASS] OSPF
[PASS] Router ID

Checking Huawei R3
----------------------------------------
[PASS] Hostname
[PASS] Juniper Link
[PASS] Branch LAN
[PASS] OSPF
[PASS] DHCP
[PASS] ACL

========================================
NETWORK VALIDATION PASSED
========================================
```

---

# Project Structure

```text
Multi-Vendor Enterprise Network
│
├── configs
│   ├── cisco
│   │   └── R1-cisco-config.txt
│   │
│   ├── juniper
│   │   └── R2-juniper-config.set
│   │
│   └── huawei
│       └── R3-huawei-config.txt
│
├── documentation
│   ├── ip-addressing.md
│   ├── routing.md
│   ├── security.md
│   └── troubleshooting.md
│
├── scripts
│   └── network_validation.py
│
├── topology
│   ├── network-diagram.txt
│   └── topology.md
│
├── .gitignore
│
└── README.md
```

---

# Troubleshooting

The project includes a troubleshooting guide covering common enterprise network problems.

Scenarios include:

* Branch client cannot access the Internet
* OSPF neighbor is down
* DHCP clients do not receive an IP address
* NAT is not working
* ACL is blocking legitimate traffic
* Branch LAN route is missing
* Default route is missing

See:

```text
documentation/troubleshooting.md
```

---

# Technologies Used

* Cisco IOS
* Juniper Junos
* Huawei VRP
* OSPF
* NAT/PAT
* DHCP
* ACLs
* Firewall Filtering
* IPv4
* Python
* Visual Studio Code
* Git
* GitHub

---

# Skills Demonstrated

This project demonstrates knowledge of:

* Multi-vendor network environments
* Enterprise network architecture
* IPv4 subnetting
* IP addressing
* OSPF routing
* Dynamic route propagation
* Default route advertisement
* NAT/PAT
* DHCP
* Access Control Lists
* Network security concepts
* Cisco configuration syntax
* Juniper configuration syntax
* Huawei configuration syntax
* Network troubleshooting
* Python automation
* Configuration validation
* Git and GitHub

---

# Project Limitations

This is a network design and configuration portfolio project.

The project does not run actual Cisco, Juniper, or Huawei operating system images.

The configurations are written using vendor-specific syntax and represent the intended network design.

The Python validation script checks the presence of expected configuration components but does not:

* Emulate network devices
* Form real OSPF adjacencies
* Test actual packet forwarding
* Perform real NAT translations
* Provide DHCP services
* Apply real ACL policies

A future version could use a network emulation environment to test parts of the design.

---

# Future Improvements

Possible future improvements include:

* Network device emulation
* Containerlab integration
* FRRouting integration
* Ansible network automation
* Automated configuration deployment
* Configuration backup automation
* Network monitoring
* SNMP
* Syslog server
* Prometheus monitoring
* Grafana dashboards
* VPN connectivity
* AAA authentication
* SSH key authentication
* CI/CD pipeline for configuration validation

---

# Project Status

**Status: Completed**

The core design, vendor configurations, security design, documentation, and Python configuration validation have been completed.

Latest validation result:

```text
NETWORK VALIDATION PASSED
```

---

# Author

**Hristijan Chaushoski**

Aspiring Network / Infrastructure Engineer

---

## Portfolio Note

This project was created as a hands-on portfolio exercise to demonstrate the design and documentation of a small multi-vendor enterprise network using Cisco, Juniper, and Huawei configuration concepts.
