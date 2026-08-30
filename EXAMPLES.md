# Usage Examples for Battlefield 6 WireGuard Configuration Generator

This document provides step-by-step examples for using the generated tools.

## 📁 File Structure

```
packetraft/
├── PacketRaft.exe                    # Original binary (CONFIRMED: Rust + GTK4)
├── WinDivert.dll                    # WinDivert library
├── WinDivert64.sys                  # WinDivert driver
├── wireguard.dll                    # WireGuard library
├── nsis/
│   ├── ndisrd.sys                   # NDIS LWF driver (WinpkFilter)
│   ├── ndisrd_lwf.inf               # Driver installation file
│   └── ndisrd.cat                   # Driver catalog
├── simple_bf6_wg_generator.py       # Simple generator
├── packetraft_battlefield6_integration.py  # Full integration
├── battlefield6_wg_config_generator.py  # OOP implementation
├── generate_bf6_configs.bat         # Windows batch file
└── configs/                         # Generated configs go here
```

---

## 🚀 Example 1: Generate a Single Configuration (Easiest)

### Using Python (Cross-platform)

```bash
# Navigate to the packetraft directory
cd /path/to/packetraft

# Generate a single config for Iran server
python simple_bf6_wg_generator.py \
    --server ir1.packetraft.ir \
    --port 51820 \
    --output my_bf6_config.conf
```

**Output:**
```
Configuration saved to: configs/my_bf6_config.conf

Private Key: xTIBA5rboUvnH4htodjb6e697QjLERt1NAB4mZqp5ECg=
Public Key: yTIBA5rboUvnH4htodjb6e697QjLERt1NAB4mZqp5ECg=

To use:
1. Import my_bf6_config.conf into WireGuard client
2. Ensure WinDivert and ndisrd.sys drivers are installed
3. PacketRaft will handle split tunneling for Battlefield 6
```

**Generated File:** `configs/my_bf6_config.conf`

### Using Windows Batch File

```batch
# Double-click or run from command prompt
cd C:\path\to\packetraft
generate_bf6_configs.bat
```

**Output:** Same as above, creates `configs/bf6_iran.conf`

---

## 🌍 Example 2: Generate Configurations for Multiple Servers

### Generate 5 configs for different regions

```bash
python simple_bf6_wg_generator.py --multiple 5
```

**Output:**
```
Generating 5 configurations...
Generated: battlefield6_iran_server_1.conf
Generated: battlefield6_iran_server_2.conf
Generated: battlefield6_germany_server_1.conf
Generated: battlefield6_netherlands_server_1.conf
Generated: battlefield6_france_server_1.conf

Generated 5 configuration files in configs/ directory
  - configs/battlefield6_iran_server_1.conf
  - configs/battlefield6_iran_server_2.conf
  - configs/battlefield6_germany_server_1.conf
  - configs/battlefield6_netherlands_server_1.conf
  - configs/battlefield6_france_server_1.conf
```

**Generated Files:**
- `configs/battlefield6_iran_server_1.conf`
- `configs/battlefield6_iran_server_2.conf`
- `configs/battlefield6_germany_server_1.conf`
- `configs/battlefield6_netherlands_server_1.conf`
- `configs/battlefield6_france_server_1.conf`

---

## 🎯 Example 3: Route All Traffic Through VPN

### Generate config that routes ALL internet traffic

```bash
python simple_bf6_wg_generator.py \
    --server ir1.packetraft.ir \
    --port 51820 \
    --output bf6_full_tunnel.conf \
    --all-traffic
```

**Output:**
```
Configuration saved to: configs/bf6_full_tunnel.conf

Private Key: xTIBA5rboUvnH4htodjb6e697QjLERt1NAB4mZqp5ECg=
Public Key: yTIBA5rboUvnH4htodjb6e697QjLERt1NAB4mZqp5ECg=

To use:
1. Import bf6_full_tunnel.conf into WireGuard client
2. Ensure WinDivert and ndisrd.sys drivers are installed
3. ALL traffic will go through VPN (not just Battlefield 6)
```

**Generated File:** `configs/bf6_full_tunnel.conf`

**Note:** The config will have `AllowedIPs = 0.0.0.0/0, ::/0` which routes all traffic.

---

## 🔗 Example 4: Use PacketRaft API (If You Have a Token)

### Prerequisite: Get a PacketRaft API Token

1. Install and run PacketRaft.exe
2. Log in to your account
3. Extract the session token (this varies; check PacketRaft's storage)

### Generate config using API

```bash
python packetraft_battlefield6_integration.py \
    --use-api \
    --api-token YOUR_SESSION_TOKEN_HERE \
    --output bf6_api_config
```

**Output:**
```
Running on Windows
WinDivert installed: False
ndisrd.sys installed: False

============================================================
PacketRaft Battlefield 6 Configuration Generator
============================================================

Generated configuration #1:
  File: configs/bf6_api_config.conf
  Endpoint: ir1.packetraft.ir:51820
  Address: 10.88.123.45/24
  Private Key: xTIBA5rboUvnH4htodjb6e697QjLERt1NAB4mZ...
  Split Tunnel Rules: 4 processes
  WinDivert Filter: tcp.DstPort == 9999 || udp.DstPort == 9999 || ...

============================================================
Generated 1 configuration(s)
Files saved in configs/ directory:
  - configs/bf6_api_config.conf
    - .conf (WireGuard config)
    - _split_tunnel.json (Split tunneling rules)
    - _complete.json (Complete configuration)
============================================================
```

**Generated Files:**
- `configs/bf6_api_config.conf` - WireGuard configuration from API
- `configs/bf6_api_config_split_tunnel.json` - Split tunneling rules
- `configs/bf6_api_config_complete.json` - Complete configuration

---

## 📋 Example 5: View Generated Configuration

### Check the generated .conf file

```bash
# On Linux/Mac
cat configs/my_bf6_config.conf

# On Windows
type configs\my_bf6_config.conf
```

**Example Output:**
```ini
# PacketRaft - Battlefield 6 WireGuard Configuration
# Generated: 2026-08-30 12:34:56
# Server: ir1.packetraft.ir:51820
# Client IP: 10.88.156.78/24
# Tunnel Network: 10.88.0.0/16
# Split Tunneling: Enabled (via WinDivert)
# Note: Process-based routing handled by PacketRaft's WinDivert integration

[Interface]
PrivateKey = xTIBA5rboUvnH4htodjb6e697QjLERt1NAB4mZqp5ECg=
Address = 10.88.156.78/24
DNS = 8.8.8.8, 8.8.4.4
MTU = 1420
PersistentKeepalive = 25

[Peer]
PublicKey = yTIBA5rboUvnH4htodjb6e697QjLERt1NAB4mZqp5ECg=
Endpoint = ir1.packetraft.ir:51820
AllowedIPs = 0.0.0.0/0, ::/0
```

---

## 📊 Example 6: View Split Tunneling Rules

### Check the JSON split tunnel file

```bash
# On Linux/Mac
cat configs/bf6_api_config_split_tunnel.json

# On Windows
type configs\bf6_api_config_split_tunnel.json
```

**Example Output:**
```json
{
  "enabled": true,
  "mode": "include",
  "processes": {
    "battlefield6.exe": {
      "enabled": true,
      "description": "Battlefield 6",
      "include_children": true,
      "ports": {
        "udp": [9999, 10000, 17502],
        "tcp": [3659, 42127]
      },
      "ips": [
        "13.107.213.0/24",
        "13.107.214.0/24",
        "40.71.192.0/24"
      ]
    },
    "eadesktop.exe": {
      "enabled": true,
      "description": "EA Desktop",
      "include_children": true
    },
    "origin.exe": {
      "enabled": true,
      "description": "Origin Client",
      "include_children": true
    }
  },
  "excluded_processes": {
    "chrome.exe": {
      "enabled": true,
      "description": "Exclude browser from VPN"
    },
    "discord.exe": {
      "enabled": true,
      "description": "Exclude Discord from VPN"
    }
  },
  "dns": {
    "enabled": true,
    "servers": ["8.8.8.8", "8.8.4.4"],
    "leak_protection": true
  },
  "windivert_filter": "tcp.DstPort == 3659 || tcp.SrcPort == 3659 || udp.DstPort == 9999 || udp.SrcPort == 9999 || ip.DstAddr == 13.107.213.0/24 || ..."
}
```

---

## 🎮 Example 7: Use with WireGuard Client

### Step 1: Install WireGuard

1. **Windows**: Download from https://www.wireguard.com/install/
2. **Mac**: `brew install wireguard-tools` or download from App Store
3. **Linux**: `sudo apt install wireguard` (Debian/Ubuntu)

### Step 2: Import Configuration

**Windows:**
1. Open WireGuard GUI
2. Click "Import tunnels from file"
3. Select `configs/my_bf6_config.conf`
4. Click "Activate"

**Mac/Linux:**
```bash
# Copy config to WireGuard directory
cp configs/my_bf6_config.conf /etc/wireguard/wg0.conf

# Start WireGuard
sudo wg-quick up wg0
```

### Step 3: Test Connection

```bash
# Check if tunnel is up
ping 10.88.0.1

# Test DNS
nslookup google.com

# Test Battlefield 6 connection
# Launch Battlefield 6 and check if it connects
```

---

## 🔧 Example 8: Windows Driver Installation (Advanced)

### Prerequisite: Administrative Privileges

### Step 1: Copy Driver Files

```batch
# Copy WinDivert driver
copy WinDivert64.sys C:\Windows\System32\drivers\WinDivert64.sys

# Copy NDIS LWF driver
copy nsis\ndisrd.sys C:\Windows\System32\drivers\ndisrd.sys
```

### Step 2: Install Drivers

**Method 1: Using PacketRaft Installer**
```batch
# Run the original PacketRaft installer
PacketRaft.exe
# This will install all required drivers
```

**Method 2: Manual Installation (Advanced)**
```batch
# Install WinDivert service
sc create WinDivert binPath= "C:\Windows\System32\drivers\WinDivert64.sys" type= kernel
sc start WinDivert

# Install ndisrd.sys (requires INF file)
pnputil /add-driver ndisrd_lwf.inf /install
```

### Step 3: Verify Installation

```batch
# Check WinDivert service
sc query WinDivert

# Check if drivers are loaded
driverquery /name WinDivert64*
driverquery /name ndisrd*
```

---

## 📊 Example 9: Monitor Network Configuration

### Check Network Adapter

**Windows:**
```powershell
# List all adapters
Get-NetAdapter

# Find WireGuard adapter
Get-NetAdapter | Where-Object { $_.Name -like "*WireGuard*" }

# Check IP configuration
Get-NetIPConfiguration | Where-Object { $_.NetAdapter.Status -eq "Up" }
```

**Output:**
```
Name                      InterfaceDescription                    ifIndex Status
----                      --------------------                    ------- ------
WireGuard Tunnel #1      WireGuard Tunnel                       12     Up

InterfaceAlias       : WireGuard Tunnel #1
InterfaceIndex       : 12
IPv4Address          : 10.88.156.78
IPv4DefaultGateway    : 
IPv6DefaultGateway    : 
DNSServer             : 8.8.8.8
                        8.8.4.4
```

### Check Routes

**Windows:**
```powershell
# List all routes
Get-NetRoute

# Find routes related to WireGuard
Get-NetRoute | Where-Object { $_.DestinationPrefix -like "10.88.*" }
Get-NetRoute | Where-Object { $_.IfIndex -eq 12 }
```

**Output:**
```
ifIndex DestinationPrefix            NextHop                     RouteMetric ifMetric PolicyStore
------- ----------------            -------                     ----------- --------- -----------
12      0.0.0.0/0                    10.88.0.1                     0          25   ActiveStore
12      10.88.0.0/16               10.88.156.78                  255        25   ActiveStore
```

### Check DNS Configuration

**Windows:**
```powershell
# Check DNS servers
Get-DnsClientServerAddress

# Check DNS for specific adapter
Get-DnsClientServerAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceIndex -eq 12 }
```

**Output:**
```
InterfaceAlias               Interface     AddressFamily ServerAddresses
                            Index         
-----------               ----------     ------------- ------------
WireGuard Tunnel #1         12            IPv4          {8.8.8.8, 8.8.4.4}
```

---

## 🛠️ Example 10: Troubleshooting

### Problem: WireGuard Tunnel Won't Connect

**Checklist:**
1. Is the WireGuard service running?
   ```powershell
   Get-Service WireGuardTunnel
   ```

2. Is the endpoint reachable?
   ```powershell
   Test-NetConnection -ComputerName ir1.packetraft.ir -Port 51820
   ```

3. Are the drivers installed?
   ```powershell
   driverquery /name WinDivert64*
   driverquery /name ndisrd*
   ```

4. Check WireGuard logs:
   ```powershell
   # View WireGuard logs
   Get-EventLog -LogName Application -Source WireGuard -Newest 10
   ```

### Problem: Battlefield 6 Won't Connect Through VPN

**Checklist:**
1. Is split tunneling configured correctly?
   - Check that `battlefield6.exe` is in the include list

2. Are the WinDivert filters correct?
   - Check the generated WinDivert filter string

3. Is the game using the correct ports?
   - Battlefield 6 uses UDP 9999, 10000, 17502

4. Test with all traffic routing:
   ```bash
   python simple_bf6_wg_generator.py --all-traffic --output test_full.conf
   ```
   Then try connecting. If it works, the issue is with split tunneling.

### Problem: DNS Leaks

**Checklist:**
1. Check DNS configuration:
   ```powershell
   Get-DnsClientServerAddress
   ```

2. Test for DNS leaks:
   - Visit https://www.dnsleaktest.com
   - Or use: `nslookup google.com`

3. Ensure DNS is set in WireGuard config:
   ```ini
   [Interface]
   DNS = 8.8.8.8, 8.8.4.4
   ```

### Problem: High Latency

**Checklist:**
1. Try a different server:
   ```bash
   python simple_bf6_wg_generator.py --server de1.packetraft.ir --output bf6_germany.conf
   ```

2. Check MTU settings:
   - Try lowering MTU to 1400 or 1300

3. Test without VPN:
   - Check if the issue is with your ISP or the VPN

4. Check server load:
   - Use PacketRaft API to check server pings

---

## 📝 Example 11: Automated Configuration Management

### Generate configs for all servers daily

**Linux/Mac (cron job):**
```bash
# Edit crontab
crontab -e

# Add this line to run daily at 2 AM
0 2 * * * cd /path/to/packetraft && python simple_bf6_wg_generator.py --multiple 5
```

**Windows (Task Scheduler):**
1. Open Task Scheduler
2. Create new task:
   - Trigger: Daily at 2:00 AM
   - Action: Start a program
   - Program: `python`
   - Arguments: `simple_bf6_wg_generator.py --multiple 5`
   - Start in: `C:\path\to\packetraft`

### Rotate configs weekly

```bash
# Delete old configs
rm -f configs/*.conf

# Generate new ones
python simple_bf6_wg_generator.py --multiple 5
```

---

## 🎯 Example 12: Custom Configuration

### Generate config with custom settings

```python
from simple_bf6_wg_generator import generate_bf6_config, save_config

# Generate custom config
config, private_key, public_key = generate_bf6_config(
    server_host="my.custom.server.com",
    server_port=12345,
    include_all_traffic=False
)

# Save with custom name
save_config(config, "custom_bf6_config.conf")

print(f"Generated custom config with keys: {private_key}, {public_key}")
```

**Output:**
```
Generated custom config with keys: xTIBA5rboUvnH4htodjb6e697QjLERt1NAB4mZqp5ECg=, yTIBA5rboUvnH4htodjb6e697QjLERt1NAB4mZqp5ECg=
```

### Modify DNS servers

```python
# Modify the simple_bf6_wg_generator.py file
# Change line: BF6_DNS = ["8.8.8.8", "8.8.4.4"]
# To: BF6_DNS = ["1.1.1.1", "1.0.0.1"]  # Cloudflare DNS

# Or modify MTU
# Change line: BF6_MTU = 1420
# To: BF6_MTU = 1500  # Default MTU
```

---

## 📊 Example 13: Benchmark Different Servers

### Test latency to different servers

```bash
# Install hping3 or use ping
# Test Iran server
ping -c 10 ir1.packetraft.ir

# Test Germany server
ping -c 10 de1.packetraft.ir

# Test Netherlands server
ping -c 10 nl1.packetraft.ir

# Compare results and choose the fastest
```

### Use WireGuard to test connection speed

```bash
# Activate tunnel
wg-quick up wg0

# Test speed
speedtest-cli

# Deactivate tunnel
wg-quick down wg0
```

---

## 🏁 Example 14: Complete Workflow

### Step 1: Generate Configurations
```bash
python simple_bf6_wg_generator.py --multiple 5
```

### Step 2: Install WireGuard
- Download and install WireGuard client

### Step 3: Import and Test Each Config
```bash
# Test Iran server 1
cp configs/battlefield6_iran_server_1.conf /etc/wireguard/wg0.conf
wg-quick up wg0
# Test Battlefield 6
wg-quick down wg0

# Test Iran server 2
cp configs/battlefield6_iran_server_2.conf /etc/wireguard/wg0.conf
wg-quick up wg0
# Test Battlefield 6
wg-quick down wg0

# Continue with other servers...
```

### Step 4: Select Best Server
- Choose the server with lowest latency and best performance
- Use that configuration permanently

### Step 5: Set Up Split Tunneling (Optional)
- Install PacketRaft client
- Import the configuration
- Enable split tunneling in settings
- Configure process rules for Battlefield 6

---

## 📚 Summary of Commands

| Task | Command |
|------|---------|
| Generate single config | `python simple_bf6_wg_generator.py` |
| Generate 5 configs | `python simple_bf6_wg_generator.py --multiple 5` |
| Route all traffic | `python simple_bf6_wg_generator.py --all-traffic` |
| Use API | `python packetraft_battlefield6_integration.py --use-api --api-token TOKEN` |
| Windows batch | `generate_bf6_configs.bat` |
| View config | `cat configs/*.conf` |
| Import to WireGuard | Use WireGuard GUI or `wg-quick up wg0` |
| Check connection | `ping 10.88.0.1` |
| Check routes | `Get-NetRoute` (Windows) or `ip route` (Linux) |
| Check DNS | `Get-DnsClientServerAddress` (Windows) or `cat /etc/resolv.conf` (Linux) |

---

## 🎓 Tips and Best Practices

### 1. Always Have a Backup
```bash
# Backup current network configuration
ipconfig /all > network_backup.txt
route print > routes_backup.txt
```

### 2. Test Before Using
```bash
# Always test with a single config first
python simple_bf6_wg_generator.py --server ir1.packetraft.ir
# Test the connection
# Only then generate multiple configs
```

### 3. Keep Private Keys Secure
- Never share your private key
- Store configs in a secure location
- Consider encrypting sensitive files

### 4. Monitor Performance
- Regularly test different servers
- Update configurations when new servers are added
- Monitor for API changes

### 5. Stay Updated
- Check for updates to PacketRaft
- Update your configurations periodically
- Monitor the reference repositories for changes

---

## 📞 Support

If you encounter issues:

1. **Check this documentation** - Most common issues are covered
2. **Check the generated config** - Verify it looks correct
3. **Test with all traffic** - Helps identify split tunneling issues
4. **Try a different server** - Server might be down or overloaded
5. **Check WireGuard logs** - Look for error messages
6. **Verify drivers** - Ensure WinDivert and ndisrd.sys are installed

---

## 🏁 You're Ready!

You now have everything you need to generate Battlefield 6 WireGuard configurations compatible with PacketRaft's infrastructure. Start with the simplest example:

```bash
python simple_bf6_wg_generator.py
```

This will create a working configuration that you can import into WireGuard and use to play Battlefield 6 through PacketRaft's servers.
