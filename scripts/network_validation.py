from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CONFIGS = {
    "Cisco R1": BASE_DIR / "configs" / "cisco" / "R1-cisco-config.txt",
    "Juniper R2": BASE_DIR / "configs" / "juniper" / "R2-juniper-config.set",
    "Huawei R3": BASE_DIR / "configs" / "huawei" / "R3-huawei-config.txt"
}

CHECKS = {
    "Cisco R1": {
        "Interface Configuration": "interface GigabitEthernet0/0",
        "OSPF": "router ospf 1",
        "NAT": "ip nat inside source",
        "ACL": "ip access-list extended INTERNET-FILTER",
        "Default Route": "ip route 0.0.0.0 0.0.0.0"
    },
    "Juniper R2": {
        "Hostname": "set system host-name R2-JUNIPER",
        "Cisco Link": "10.0.12.2/30",
        "Huawei Link": "10.0.23.1/30",
        "OSPF": "set protocols ospf",
        "Router ID": "2.2.2.2"
    },
    "Huawei R3": {
        "Hostname": "sysname R3-HUAWEI",
        "Juniper Link": "10.0.23.2",
        "Branch LAN": "192.168.10.1",
        "OSPF": "ospf 1",
        "DHCP": "dhcp enable",
        "ACL": "acl number 3000"
    }
}


def check_configuration(device, file_path, checks):
    print(f"\nChecking {device}")
    print("-" * 40)

    if not file_path.exists():
        print(f"[FAIL] Configuration file not found: {file_path}")
        return False

    content = file_path.read_text(encoding="utf-8")

    device_passed = True

    for check_name, required_text in checks.items():
        if required_text in content:
            print(f"[PASS] {check_name}")
        else:
            print(f"[FAIL] {check_name}")
            device_passed = False

    return device_passed


def main():
    print("=" * 40)
    print("MULTI-VENDOR NETWORK VALIDATION")
    print("=" * 40)

    overall_status = True

    for device, file_path in CONFIGS.items():
        result = check_configuration(
            device,
            file_path,
            CHECKS[device]
        )

        if not result:
            overall_status = False

    print("\n" + "=" * 40)

    if overall_status:
        print("NETWORK VALIDATION PASSED")
    else:
        print("NETWORK VALIDATION FAILED")

    print("=" * 40)


if __name__ == "__main__":
    main()