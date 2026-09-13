# Network Troubleshooting Guide

## Overview

This document provides troubleshooting procedures for common problems in the Multi-Vendor Enterprise Network.

The troubleshooting process follows a structured approach, starting with basic connectivity and continuing through routing, NAT, DHCP, and security policies.

---

# Troubleshooting Methodology

The network path should be checked step by step:

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

When troubleshooting connectivity problems, identify the first point where communication fails.

---

# Scenario 1: Branch Client Cannot Access the Internet

## Symptoms

* The client cannot browse the Internet.
* The client cannot reach external IP addresses.
* Internal connectivity may still work.

## Step 1: Check the Client IP Configuration

Verify that the client received a valid IP address.

Expected network:

```text
Network:         192.168.10.0/24
Default Gateway: 192.168.10.1
```

The client should receive an address from the DHCP range:

```text
192.168.10.100 - 192.168.10.200
```

## Step 2: Check the Default Gateway

Test connectivity to Huawei R3:

```text
ping 192.168.10.1
```

If the ping fails, investigate:

* Client network configuration
* Physical connection
* LAN interface status
* DHCP configuration

## Step 3: Check Huawei R3 Connectivity

Verify the connection between Huawei R3 and Juniper R2.

Expected network:

```text
10.0.23.0/30
```

Addresses:

```text
Huawei R3:  10.0.23.2
Juniper R2: 10.0.23.1
```

Example Huawei command:

```text
ping 10.0.23.1
```

## Step 4: Check Juniper R2 Connectivity

Verify connectivity between Juniper R2 and Cisco R1.

Expected network:

```text
10.0.12.0/30
```

Addresses:

```text
Juniper R2: 10.0.12.2
Cisco R1:   10.0.12.1
```

Example Juniper command:

```text
ping 10.0.12.1
```

## Step 5: Check the Cisco Internet Connection

Verify the Cisco R1 default route:

```text
0.0.0.0/0 → 203.0.113.1
```

Example Cisco command:

```text
show ip route
```

Test connectivity to the Internet gateway:

```text
ping 203.0.113.1
```

---

# Scenario 2: OSPF Neighbor Is Down

## Symptoms

* Remote networks are missing from the routing table.
* Branch LAN cannot reach other networks.
* Default route is not learned.
* OSPF adjacency is not established.

---

## Cisco R1 Checks

Check OSPF neighbors:

```text
show ip ospf neighbor
```

Check OSPF routes:

```text
show ip route ospf
```

Check the OSPF configuration:

```text
show running-config | section router ospf
```

Verify:

* OSPF process configuration
* Area number
* Network statements
* Interface status
* IP addressing

---

## Juniper R2 Checks

Check OSPF neighbors:

```text
show ospf neighbor
```

Check OSPF routes:

```text
show route protocol ospf
```

Verify the configuration:

```text
show configuration protocols ospf
```

Check interfaces:

```text
show interfaces terse
```

Verify:

* Interface IP addresses
* OSPF Area 0 configuration
* Router ID
* Interface operational status

---

## Huawei R3 Checks

Check OSPF neighbors:

```text
display ospf peer
```

Check OSPF routes:

```text
display ip routing-table protocol ospf
```

Check the OSPF configuration:

```text
display current-configuration | include ospf
```

Verify:

* OSPF process
* Router ID
* Area configuration
* Network statements
* Interface status

---

# Scenario 3: DHCP Clients Do Not Receive an IP Address

## Symptoms

The Branch client receives:

```text
169.254.x.x
```

or does not receive an IP address.

## Step 1: Verify DHCP Is Enabled

On Huawei R3:

```text
display current-configuration | include dhcp
```

Verify that DHCP is enabled:

```text
dhcp enable
```

## Step 2: Check the DHCP Pool

Verify the Branch DHCP pool:

```text
display ip pool
```

Expected pool:

```text
BRANCH-DHCP
```

Verify:

* Network: `192.168.10.0/24`
* Gateway: `192.168.10.1`
* DHCP range: `192.168.10.100 - 192.168.10.200`

## Step 3: Verify the LAN Interface

Check the Branch LAN interface:

```text
display interface GigabitEthernet0/0/1
```

Verify that the interface is operational.

## Step 4: Verify DHCP Configuration on the Interface

The interface should use the global DHCP pool:

```text
dhcp select global
```

---

# Scenario 4: NAT Is Not Working

## Symptoms

* Branch clients can reach internal routers.
* Branch clients cannot access the Internet.
* The Cisco Internet connection works.

## Step 1: Verify NAT Configuration

On Cisco R1:

```text
show running-config | include ip nat
```

Verify:

```text
ip nat inside
ip nat outside
ip nat inside source list 10 interface GigabitEthernet0/0 overload
```

## Step 2: Verify NAT ACL

Check ACL 10:

```text
show access-lists 10
```

Expected internal network:

```text
192.168.10.0 0.0.0.255
```

## Step 3: Check NAT Translations

```text
show ip nat translations
```

Check NAT statistics:

```text
show ip nat statistics
```

## Step 4: Verify Interface Roles

Cisco R1 interfaces must have the correct NAT roles:

```text
GigabitEthernet0/0 → ip nat outside
GigabitEthernet0/1 → ip nat inside
```

---

# Scenario 5: ACL Is Blocking Legitimate Traffic

## Symptoms

* A specific service is unavailable.
* Internet access fails unexpectedly.
* Routing works but traffic is blocked.

## Cisco R1

Check ACL configuration:

```text
show access-lists
```

Check which interface uses the ACL:

```text
show running-config interface GigabitEthernet0/0
```

Verify:

```text
ip access-group INTERNET-FILTER in
```

Check ACL counters and logs to identify matching rules.

---

## Huawei R3

Check ACL configuration:

```text
display acl 3000
```

Verify the ACL:

```text
acl number 3000
```

Check the LAN interface configuration:

```text
display current-configuration interface GigabitEthernet0/0/1
```

Verify:

```text
traffic-filter inbound acl 3000
```

---

# Scenario 6: Branch LAN Route Is Missing

## Symptoms

Cisco R1 or Juniper R2 cannot reach:

```text
192.168.10.0/24
```

## Step 1: Check Huawei OSPF

Verify that Huawei R3 advertises:

```text
network 192.168.10.0 0.0.0.255
```

## Step 2: Check Juniper Routes

```text
show route protocol ospf
```

Juniper R2 should learn:

```text
192.168.10.0/24
```

## Step 3: Check Cisco Routes

```text
show ip route ospf
```

Cisco R1 should learn the Branch LAN through OSPF.

---

# Scenario 7: Default Route Is Missing

## Symptoms

The Branch LAN can communicate internally but cannot reach external networks.

## Step 1: Check Cisco Default Route

Cisco R1 should have:

```text
0.0.0.0/0 → 203.0.113.1
```

Cisco command:

```text
show ip route
```

## Step 2: Verify Default Route Advertisement

Cisco R1 uses:

```text
default-information originate
```

Verify the OSPF configuration:

```text
show running-config | section router ospf
```

## Step 3: Check Juniper and Huawei

Juniper R2 should learn the default route through OSPF.

Huawei R3 should receive the default route through the OSPF domain.

Check the routing tables for:

```text
0.0.0.0/0
```

---

# Troubleshooting Flow

Use the following order when investigating connectivity problems:

```text
1. Physical / Interface Status
            |
            v
2. IP Addressing
            |
            v
3. Local Gateway Connectivity
            |
            v
4. Router-to-Router Connectivity
            |
            v
5. OSPF Neighbors
            |
            v
6. Routing Table
            |
            v
7. NAT
            |
            v
8. ACL / Security Policies
            |
            v
9. Internet Connectivity
```

---

# Key Troubleshooting Principles

* Start with the simplest connectivity test.
* Verify interface status before investigating routing.
* Check IP addressing before checking routing protocols.
* Verify OSPF neighbors before investigating missing routes.
* Verify routing before troubleshooting NAT.
* Check ACLs after confirming routing.
* Use logs and counters where available.
* Identify the first point where traffic fails.

---

# Project Limitation

This project is a multi-vendor network design and configuration portfolio project.

Cisco IOS, Juniper Junos, and Huawei VRP devices are not running in an emulated environment.

The troubleshooting commands documented in this guide represent the expected vendor-specific commands that would be used on real network devices.

The Python validation script validates the presence of expected configuration components but does not establish real network connectivity or emulate OSPF, NAT, DHCP, or ACL behavior.
