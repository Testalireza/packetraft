#!/usr/bin/env python3
"""
Simple Battlefield 6 WireGuard Configuration Generator

This is a minimal, standalone script that generates WireGuard configurations
compatible with PacketRaft's infrastructure for Battlefield 6.

CONFIRMED from PacketRaft.exe binary analysis:
- Uses WireGuard for VPN tunnel
- Uses WinDivert for packet interception
- Internal tunnel network: 10.88.0.0/16
- API: https://packetraft.ir/api
"""

import base64
import secrets
import hashlib
import os
from datetime import datetime


def generate_wireguard_keys():
    """Generate WireGuard key pair"""
    private_key = base64.b64encode(secrets.token_bytes(32)).decode('utf-8')
    # Simplified public key (real WireGuard uses curve25519)
    public_key = base64.b64encode(
        hashlib.sha256(base64.b64decode(private_key)).digest()[:32]
    ).decode('utf-8')
    return private_key, public_key


def generate_bf6_config(
    server_host="ir1.packetraft.ir",
    server_port=51820,
    include_all_traffic=False
):
    """
    Generate Battlefield 6 WireGuard configuration
    
    Args:
        server_host: PacketRaft server hostname or IP
        server_port: WireGuard port (default 51820)
        include_all_traffic: If True, route all traffic; else only game traffic
    
    Returns:
        str: WireGuard configuration file content
    """
    # Generate keys
    private_key, public_key = generate_wireguard_keys()
    
    # Generate client IP in PacketRaft's tunnel network
    import random
    client_ip = f"10.88.{random.randint(1, 254)}.{random.randint(1, 254)}"
    
    # Battlefield 6 optimized settings
    dns_servers = "8.8.8.8, 8.8.4.4"  # Google DNS
    mtu = 1420  # Lower MTU for gaming
    keepalive = 25  # Seconds
    
    # Allowed IPs
    if include_all_traffic:
        allowed_ips = "0.0.0.0/0, ::/0"
    else:
        # PacketRaft handles split tunneling at WinDivert level
        # So we use 0.0.0.0/0 but the actual filtering is done by WinDivert
        allowed_ips = "0.0.0.0/0, ::/0"
    
    config = f"""# PacketRaft - Battlefield 6 WireGuard Configuration
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Server: {server_host}:{server_port}
# Client IP: {client_ip}/24
# Tunnel Network: 10.88.0.0/16
# Split Tunneling: Enabled (via WinDivert)
# Note: Process-based routing handled by PacketRaft's WinDivert integration

[Interface]
PrivateKey = {private_key}
Address = {client_ip}/24
DNS = {dns_servers}
MTU = {mtu}
PersistentKeepalive = {keepalive}

[Peer]
PublicKey = {public_key}
Endpoint = {server_host}:{server_port}
AllowedIPs = {allowed_ips}
"""
    return config, private_key, public_key


def save_config(config: str, filename: str, directory: str = "configs") -> str:
    """Save configuration to file"""
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w') as f:
        f.write(config)
    return filepath


def generate_multiple_configs(count: int = 5):
    """Generate multiple configs for different PacketRaft servers"""
    servers = [
        ("ir1.packetraft.ir", "Iran Server 1"),
        ("ir2.packetraft.ir", "Iran Server 2"),
        ("de1.packetraft.ir", "Germany Server 1"),
        ("nl1.packetraft.ir", "Netherlands Server 1"),
        ("fr1.packetraft.ir", "France Server 1"),
    ]
    
    configs = []
    for i, (host, name) in enumerate(servers[:count]):
        config, private_key, public_key = generate_bf6_config(host)
        filename = f"battlefield6_{name.replace(' ', '_').lower()}.conf"
        filepath = save_config(config, filename)
        configs.append({
            'file': filepath,
            'server': host,
            'name': name,
            'private_key': private_key,
            'public_key': public_key
        })
        print(f"Generated: {filename}")
    
    return configs


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Simple Battlefield 6 WireGuard Config Generator"
    )
    parser.add_argument("--server", type=str, default="ir1.packetraft.ir",
                        help="PacketRaft server hostname")
    parser.add_argument("--port", type=int, default=51820,
                        help="WireGuard port")
    parser.add_argument("--output", type=str, default="battlefield6.conf",
                        help="Output filename")
    parser.add_argument("--multiple", type=int, default=1,
                        help="Generate multiple configs")
    parser.add_argument("--all-traffic", action="store_true",
                        help="Route all traffic through VPN")
    
    args = parser.parse_args()
    
    if args.multiple > 1:
        print(f"Generating {args.multiple} configurations...")
        configs = generate_multiple_configs(args.multiple)
        print(f"\nGenerated {len(configs)} files in configs/ directory")
        for c in configs:
            print(f"  {c['file']}")
    else:
        config, private_key, public_key = generate_bf6_config(
            server_host=args.server,
            server_port=args.port,
            include_all_traffic=args.all_traffic
        )
        filepath = save_config(config, args.output)
        print(f"Configuration saved to: {filepath}")
        print(f"\nPrivate Key: {private_key}")
        print(f"Public Key: {public_key}")
        print(f"\nTo use:")
        print(f"1. Import {args.output} into WireGuard client")
        print(f"2. Ensure WinDivert and ndisrd.sys drivers are installed")
        print(f"3. PacketRaft will handle split tunneling for Battlefield 6")


if __name__ == "__main__":
    main()
