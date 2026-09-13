# Network Security Design

## Overview

This document describes the basic security design of the Multi-Vendor Enterprise Network.

The network uses security controls on Cisco, Juniper, and Huawei devices.

The main security mechanisms include:

* Access Control Lists (ACLs)
* Firewall filtering
* Basic traffic restrictions
* Controlled access between the Internet and the internal network

---

# Security Architecture

The network security design is distributed across the three network devices.

```text
                    INTERNET
                       |
                       |
                [ Cisco R1 ]
                 NAT + ACL
                       |
                [ Juniper R2 ]
                  Core Router
                       |
                [ Huawei R3 ]
                    ACL
                       |
                 Branch LAN
```

---

# Cisco R1 Security

Cisco R1 is the Internet-facing edge router.

The router provides the first layer of protection between the Internet and the internal enterprise network.

## Security Features

Cisco R1 uses:

* NAT/PAT
* Extended Access Control Lists
* Default routing
* Traffic filtering

The Internet-facing interface is protected using the following ACL:

```text
ip access-list extended INTERNET-FILTER

 permit tcp any any established
 permit icmp any any echo-reply
 permit ip 192.168.10.0 0.0.0.255 any
 deny ip any any log
```

The ACL is applied to the Internet-facing interface.

## Security Purpose

The ACL allows:

* Established TCP return traffic
* ICMP echo replies
* Traffic originating from the internal Branch LAN

All other traffic is denied and logged.

---

# NAT Security

Network Address Translation is configured on Cisco R1.

The internal Branch LAN uses private addressing:

```text
192.168.10.0/24
```

Private addresses are translated when accessing the Internet.

The Cisco NAT configuration uses PAT (Port Address Translation):

```text
ip nat inside source list 10 interface GigabitEthernet0/0 overload
```

PAT allows multiple internal devices to share one public-facing IP address.

---

# Juniper R2 Security

Juniper R2 acts as the core router.

In this project, the primary responsibility of R2 is routing traffic between Cisco R1 and Huawei R3.

In a production environment, Juniper firewall filters could be used to control traffic.

Example concept:

```text
set firewall family inet filter CORE-PROTECTION term ALLOW-OSPF from protocol ospf
set firewall family inet filter CORE-PROTECTION term ALLOW-OSPF then accept

set firewall family inet filter CORE-PROTECTION term DEFAULT-DENY then discard
```

This demonstrates how Juniper firewall filters can be used to protect network traffic.

---

# Huawei R3 Security

Huawei R3 provides connectivity to the Branch LAN.

A basic ACL is configured to identify and control Branch LAN traffic.

Example:

```text
acl number 3000
 rule 5 permit ip source 192.168.10.0 0.0.0.255
 rule 10 deny ip
```

The ACL represents a basic security policy for Branch LAN traffic.

---

# Security Layers

The network uses multiple security layers.

```text
Layer 1

Internet
   |
   v

Cisco R1
ACL + NAT
   |
   v

Layer 2

Juniper R2
Core Traffic Control
   |
   v

Layer 3

Huawei R3
Branch ACL
   |
   v

Branch LAN
```

---

# Security Summary

| Device     | Security Feature        | Purpose                     |
| ---------- | ----------------------- | --------------------------- |
| Cisco R1   | ACL                     | Filter Internet traffic     |
| Cisco R1   | NAT/PAT                 | Translate private addresses |
| Juniper R2 | Firewall Filter Concept | Protect core traffic        |
| Huawei R3  | ACL                     | Control Branch LAN traffic  |

---

# Security Considerations

For a production environment, additional security features could include:

* SSH-only management access
* AAA authentication
* SNMPv3
* Syslog logging
* Network monitoring
* VPN connectivity
* Zone-based firewalls
* Intrusion Prevention Systems
* Management VLANs
* Control Plane Protection

These features are outside the scope of this small portfolio project but could be implemented in a larger enterprise network design.




## Implementation Status

This project is a configuration and network design exercise.

The Cisco, Juniper, and Huawei configurations represent vendor-specific
configuration examples and are not deployed on physical or licensed virtual
network devices in this project.

The Juniper core protection firewall filter is documented as a proposed
security policy and is intentionally not applied to production-facing
interfaces in the design-only environment.

Security controls that would require additional production validation include:

- ACL behavior verification
- Firewall filter ordering
- OSPF adjacency validation
- NAT behavior
- Management-plane restrictions
- Logging and monitoring
- SSH authentication and authorization
- Anti-spoofing controls