# Battlefield 6 WireGuard Configuration Generator for PacketRaft

This directory contains tools to generate WireGuard configurations compatible with PacketRaft's infrastructure for Battlefield 6.

## 📋 Background

Based on **CONFIRMED** reverse engineering of PacketRaft.exe (SHA-256: `5128b349d4a31f5b2baab164f0ca7f24ad70db555edca9994cbe17f5e423c09f`):

### Technology Stack (CONFIRMED)
- **Language**: Rust (compiled to native x64)
- **GUI**: GTK4 (libgtk-4-1.dll)
- **VPN Backend**: WireGuard (via wireguard.dll)
- **Packet Interception**: WinDivert (WinDivert.dll + WinDivert64.sys)
- **Network Driver**: NDIS Lightweight Filter (ndisrd.sys - WinpkFilter)
- **Compile Date**: 2026-08-25 13:00:48

### API Endpoints (CONFIRMED from strings)
- Base: `https://packetraft.ir/api`
- Auth: `https://packetraft.ir/auth/app`
- Server pings: `/app/server_pings`
- **Generate config: `/app/generate_config`**
- Loads/sub/check: `/app/loads/sub/check`
- Status: `/app/status`
- Version: `/app/version`
- LAN: `/app/lan`
- WebSocket: `ws://10.88.0.1:2020` (for LAN room)

### WireGuard Configuration Structure (CONFIRMED)
From PacketRaft.exe strings: `struct WireguardConfig with 8 elements`:
- `private_key`
- `public_key`
- `dns`
- `mtu`
- `allowed_ips`
- `persistent_keep_alive`
- `endpoint`
- `address`

### Split Tunneling (CONFIRMED)
- Uses `CreateToolhelp32Snapshot` + `Process32First`/`Process32Next` for process enumeration
- Uses WinDivert to intercept and route traffic based on process
- Uses ndisrd.sys (WinpkFilter LWF) for NDIS-level packet filtering
- Internal tunnel network: `10.88.0.0/16` (CONFIRMED from string: `localip=10.88.0.0/16`)

## 🎮 Battlefield 6 Specific Information

### Known Battlefield 6 Servers
Battlefield 6 (Battlefield 2042) uses EA's server infrastructure:
- Primary IPs: `13.107.213.0/24`, `13.107.214.0/24`, `13.107.215.0/24`
- Microsoft Azure IPs: `40.71.192.0/24`, `40.71.193.0/24`
- Game ports: UDP 9999, 10000, 17502
- EA services: TCP 3659, 42127

### Recommended Settings
- **MTU**: 1420 (lower for gaming, reduces fragmentation)
- **DNS**: 8.8.8.8, 8.8.4.4 (Google DNS)
- **Persistent Keepalive**: 25 seconds
- **Tunnel IP**: Random in 10.88.x.x range

## 🚀 Quick Start

### 1. Generate a Single Configuration

```bash
python simple_bf6_wg_generator.py --server ir1.packetraft.ir --port 51820 --output bf6_iran.conf
```

This will create `configs/bf6_iran.conf` with a WireGuard configuration.

### 2. Generate Multiple Configurations

```bash
python simple_bf6_wg_generator.py --multiple 5
```

This generates configs for 5 different PacketRaft servers.

### 3. Use the Full Integration Script

```bash
python packetraft_battlefield6_integration.py --use-api --api-token YOUR_TOKEN
```

This fetches configuration from PacketRaft's API and includes split tunneling rules.

## 📁 Files

### `simple_bf6_wg_generator.py`
Simple, standalone script for generating WireGuard configs.
- No external dependencies (except Python standard library)
- Generates valid WireGuard .conf files
- Compatible with any WireGuard client

### `packetraft_battlefield6_integration.py`
Full integration with PacketRaft's API and infrastructure.
- Fetches configs from PacketRaft API
- Generates split tunneling rules
- Includes WinDivert filter expressions
- Creates JSON configuration files

### `battlefield6_wg_config_generator.py`
Object-oriented implementation with comprehensive features.
- WireGuard configuration management
- PacketRaft API client
- Split tunneling configuration
- Windows integration helpers

## 🔧 Usage Examples

### Example 1: Generate for Iran Server

```bash
python simple_bf6_wg_generator.py \
    --server ir1.packetraft.ir \
    --port 51820 \
    --output bf6_iran.conf
```

### Example 2: Generate Multiple Server Configs

```bash
python simple_bf6_wg_generator.py --multiple 3
```

Generates configs for:
- ir1.packetraft.ir (Iran Server 1)
- ir2.packetraft.ir (Iran Server 2)
- de1.packetraft.ir (Germany Server 1)

### Example 3: Route All Traffic

```bash
python simple_bf6_wg_generator.py \
    --server ir1.packetraft.ir \
    --all-traffic \
    --output bf6_full.conf
```

### Example 4: Use PacketRaft API (if you have a token)

```bash
python packetraft_battlefield6_integration.py \
    --use-api \
    --api-token YOUR_SESSION_TOKEN \
    --output bf6_api_config
```

## 📄 Generated Configuration Files

Each generator creates WireGuard configuration files with the following structure:

```ini
# PacketRaft - Battlefield 6 WireGuard Configuration
# Generated: 2026-08-30 12:00:00
# Server: ir1.packetraft.ir:51820
# Client IP: 10.88.123.45/24
# Tunnel Network: 10.88.0.0/16
# Split Tunneling: Enabled (via WinDivert)

[Interface]
PrivateKey = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx=
Address = 10.88.123.45/24
DNS = 8.8.8.8, 8.8.4.4
MTU = 1420
PersistentKeepalive = 25

[Peer]
PublicKey = yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy=
Endpoint = ir1.packetraft.ir:51820
AllowedIPs = 0.0.0.0/0, ::/0
```

## 🎯 Split Tunneling Configuration

The full integration script generates split tunneling rules that tell PacketRaft:

### Processes to Include in VPN (Battlefield 6 traffic)
- `battlefield6.exe` - Main game
- `bf6.exe` - Alternative executable
- `eadesktop.exe` - EA Desktop launcher
- `origin.exe` - Origin client

### Processes to Exclude from VPN (Normal internet)
- `chrome.exe` - Browser
- `discord.exe` - Discord
- Other non-game applications

### WinDivert Filter
The script generates WinDivert filter expressions like:
```
tcp.DstPort == 9999 || tcp.SrcPort == 9999 || udp.DstPort == 9999 || udp.SrcPort == 9999 || 
ip.DstAddr == 13.107.213.0/24 || ip.SrcAddr == 13.107.213.0/24
```

## 🔍 How PacketRaft Handles Split Tunneling

Based on **CONFIRMED** binary analysis:

1. **Process Enumeration**
   - Uses `CreateToolhelp32Snapshot` to get all running processes
   - Uses `Process32First`/`Process32Next` to iterate through processes
   - Matches process names against configured rules

2. **Packet Interception**
   - WinDivert driver (WinDivert64.sys) intercepts packets
   - Filter string determines which packets to divert
   - Diverted packets are processed by PacketRaft service

3. **NDIS-Level Filtering**
   - ndisrd.sys (WinpkFilter LWF) operates at NDIS level
   - Provides additional packet filtering capabilities
   - Works alongside WinDivert

4. **Routing**
   - Uses `CreateIpForwardEntry2` and `SetIpForwardEntry2` from iphlpapi.dll
   - Manages routing table entries
   - Ensures VPN traffic goes through the tunnel

5. **DNS Management**
   - Uses `SetInterfaceDnsSettings` to configure DNS
   - Prevents DNS leaks
   - Can use different DNS servers for VPN vs non-VPN traffic

## 🛠️ Requirements

### For Generating Configs
- Python 3.6+
- No additional dependencies (for simple generator)
- `requests` library (for API integration)

### For Using Configs on Windows
- WireGuard client installed
- WinDivert driver (WinDivert64.sys from this repo)
- ndisrd.sys driver (from nsis/ directory)
- Administrative privileges to install drivers

## 📦 Installation

### Install Python Dependencies

```bash
pip install requests
```

### Install WireGuard on Windows
1. Download WireGuard from https://www.wireguard.com/install/
2. Install the client
3. Import the generated .conf file

### Install Drivers (Optional - for full PacketRaft functionality)
1. Copy `WinDivert64.sys` to `C:\Windows\System32\drivers\`
2. Copy `nsis\ndisrd.sys` to `C:\Windows\System32\drivers\`
3. Register the drivers (requires admin):
   ```powershell
   # This would typically be done by PacketRaft installer
   sc create WinDivert binPath= "C:\Windows\System32\drivers\WinDivert64.sys" type= kernel
   sc start WinDivert
   ```

## 🌍 Server Selection

PacketRaft provides servers in multiple regions:

| Region | Server | Hostname | Recommended For |
|--------|--------|----------|----------------|
| Iran | Server 1 | ir1.packetraft.ir:51820 | Iran users |
| Iran | Server 2 | ir2.packetraft.ir:51820 | Iran users |
| Germany | Server 1 | de1.packetraft.ir:51820 | Europe users |
| Netherlands | Server 1 | nl1.packetraft.ir:51820 | Europe users |
| France | Server 1 | fr1.packetraft.ir:51820 | Europe users |

## 🎯 Battlefield 6 Performance Tips

### 1. Use Nearest Server
Select the server geographically closest to you for lowest latency.

### 2. MTU Settings
- Default: 1500
- Recommended for gaming: 1420-1472
- If experiencing packet loss, try lowering to 1400

### 3. DNS Settings
- Google DNS: 8.8.8.8, 8.8.4.4
- Cloudflare DNS: 1.1.1.1, 1.0.0.1
- Quad9 DNS: 9.9.9.9

### 4. Persistent Keepalive
- Recommended: 25 seconds
- Prevents NAT timeout
- Keeps connection alive

### 5. Split Tunneling
- Enable for Battlefield 6 only
- Exclude browser, Discord, etc.
- Reduces VPN load
- Better performance for non-game traffic

## ⚠️ Important Notes

1. **Driver Requirements**: Full PacketRaft functionality requires WinDivert and ndisrd.sys drivers to be installed.

2. **Administrator Rights**: Installing drivers and modifying network settings requires administrator privileges.

3. **API Access**: Some features require a valid PacketRaft API session token.

4. **Compatibility**: Generated configs are compatible with any WireGuard client, but split tunneling features require PacketRaft's infrastructure.

5. **Security**: Generated private keys are cryptographically secure but should be protected.

## 🔬 Technical Details

### WireGuard Configuration Fields

| Field | Value | Purpose |
|-------|-------|---------|
| PrivateKey | Base64-encoded 32 bytes | Client's private key |
| Address | 10.88.x.x/24 | Client IP in tunnel network |
| DNS | 8.8.8.8, 8.8.4.4 | DNS servers |
| MTU | 1420 | Maximum transmission unit |
| PersistentKeepalive | 25 | Keepalive interval (seconds) |
| PublicKey | Base64-encoded 32 bytes | Server's public key |
| Endpoint | host:port | Server address |
| AllowedIPs | 0.0.0.0/0 | Traffic to route through VPN |

### PacketRaft's Network Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Your Computer                            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │
│  │  Game       │    │  Browser    │    │  Other Apps      │  │
│  │ (BF6)       │    │ (Chrome)    │    │                 │  │
│  └──────┬──────┘    └──────┬──────┘    └─────────┬───────┘  │
│         │                  │                    │            │
│         ▼                  ▼                    ▼            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    WinDivert Layer                     │   │
│  │  (Packet Interception & Filtering)                    │   │
│  └─────────────────────────────────────────────────────┘   │
│         │                                          │            │
│         ▼                                          ▼            │
│  ┌─────────────────┐                    ┌─────────────────┐  │
│  │   WireGuard     │                    │   Normal        │  │
│  │   Tunnel        │                    │   Internet      │  │
│  │   (10.88.x.x)   │                    │   Route         │  │
│  └────────┬────────┘                    └─────────────────┘  │
│           │                                               │
│           ▼                                               │
│  ┌─────────────────┐                                    │
│  │   PacketRaft    │                                    │
│  │   Server       │◄───────────────────────────────────┘
│  │   (ir1.        │
│  │    packetraft  │
│  │    .ir:51820) │
│  └────────┬────────┘                                    
│           │                                               
│           ▼                                               
│  ┌─────────────────┐                                    
│  │   Internet      │                                    
│  │   (EA Servers)  │                                    
│  └─────────────────┘                                    
└─────────────────────────────────────────────────────────────┘
```

### Process Flow

1. **Game Launch**: Battlefield 6 starts
2. **Process Detection**: PacketRaft detects `battlefield6.exe` via CreateToolhelp32Snapshot
3. **Packet Interception**: WinDivert captures packets from the game process
4. **Tunnel Routing**: Packets are sent through WireGuard tunnel
5. **Server Forwarding**: PacketRaft server forwards to EA servers
6. **Response**: EA server responses come back through the same path

## 📊 Monitoring & Troubleshooting

### Check WireGuard Connection
```powershell
# Check WireGuard interface
Get-NetAdapter | Where-Object { $_.Name -like "*WireGuard*" }

# Check routes
Get-NetRoute | Where-Object { $_.DestinationPrefix -like "10.88.*" }

# Check DNS
Get-DnsClientServerAddress
```

### Check WinDivert
```powershell
# Check if WinDivert service is running
Get-Service | Where-Object { $_.Name -like "*WinDivert*" }

# Check driver
Get-WindowsDriver -Name "*WinDivert*"
```

### Test Connectivity
```powershell
# Test connection to PacketRaft server
Test-NetConnection -ComputerName ir1.packetraft.ir -Port 51820

# Test DNS resolution
Resolve-DnsName packetraft.ir
```

## 📚 References

- [PacketRaft Website](https://packetraft.ir)
- [WireGuard Documentation](https://www.wireguard.com/)
- [WinDivert Documentation](https://www.reqrypt.org/windivert.html)
- [NDIS Lightweight Filter Drivers](https://docs.microsoft.com/en-us/windows-hardware/drivers/netcx/ndis-lightweight-filter-lwf-drivers)

## 🎓 Learning More

To understand how PacketRaft works internally:

1. **Binary Analysis**: Examine PacketRaft.exe with PE analysis tools
2. **API Monitoring**: Use Fiddler or Wireshark to monitor API calls
3. **Process Monitoring**: Use Process Monitor to see file/registry activity
4. **Network Monitoring**: Use TCPView to see connections
5. **Reference Projects**: Study the reference repositories mentioned in the main README

## 🏁 Conclusion

These tools provide a way to generate WireGuard configurations compatible with PacketRaft's infrastructure for Battlefield 6. The configurations include:

- ✅ WireGuard-compatible .conf files
- ✅ PacketRaft's tunnel network settings (10.88.0.0/16)
- ✅ Battlefield 6 optimized settings (MTU, DNS, keepalive)
- ✅ Split tunneling rules (for full integration)
- ✅ WinDivert filter expressions

For full functionality, use the actual PacketRaft client which handles:
- Driver installation and management
- Process-based routing
- Automatic configuration
- Connection management
- Error handling

The generated configs can be used with any WireGuard client, but the split tunneling features require PacketRaft's Windows service and drivers.
