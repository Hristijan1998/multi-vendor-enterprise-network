# Routing Design

## Overview

This document describes the routing architecture used in the Multi-Vendor Enterprise Network.

The network uses **OSPF (Open Shortest Path First)** as the dynamic routing protocol between Cisco, Juniper, and Huawei routers.

All routers participate in the same OSPF Area 0.

---

# Routing Topology

```text
                    INTERNET
                       |
                       |
                  Cisco R1
                 Edge Router
                       |
                 10.0.12.0/30
                       |
                  Juniper R2
                  Core Router
                       |
                 10.0.23.0/30
                       |
                  Huawei R3
                 Branch Router
                       |
               192.168.10.0/24
                       |
                  Branch LAN