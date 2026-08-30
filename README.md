# PacketRaft

> A community-driven reverse-engineering and reimplementation project for PacketRaft.

[![GitHub](https://img.shields.io/badge/GitHub-Testalireza%2Fpacketraft-181717?logo=github)](https://github.com/Testalireza/packetraft)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows)](https://www.microsoft.com/windows)
[![Status](https://img.shields.io/badge/Status-In%20Development-orange)](#status)

---

## About

**PacketRaft** is an experimental open-source project focused on understanding, documenting, and reimplementing the functionality of the PacketRaft client and its networking infrastructure.

The project is based on analysis of the released PacketRaft application, publicly available source code, and other community reverse-engineering projects.

The goal is to build a clean, maintainable implementation while documenting the protocols, APIs, networking behavior, routing, and other technical components involved.

> **This project is not affiliated with or endorsed by PacketRaft.ir or its operators.**

---

## Project Goals

The main goals of this project are:

* Reverse engineer the released PacketRaft client.
* Understand its internal architecture.
* Document its network protocols and APIs.
* Understand authentication and session handling.
* Understand server discovery and server selection.
* Reproduce the client-side VPN/tunneling functionality.
* Investigate Windows networking and routing behavior.
* Understand application-based split tunneling.
* Reimplement discovered functionality in clean, maintainable code.
* Provide reproducible builds and documentation.
* Make the project useful for research, interoperability, and educational purposes.

---

## Reverse Engineering Sources

This project uses several publicly available projects as technical references.

### PacketRaft

The official PacketRaft service is the primary subject being investigated.

* Website: [PacketRaft.ir](https://packetraft.ir)

### b00tkitism/packetraft

A community reverse-engineered implementation of PacketRaft functionality.

* Repository: [b00tkitism/packetraft](https://github.com/b00tkitism/packetraft)

This project is particularly useful for understanding PacketRaft's server/API behavior and VPN-related functionality.

### iMissAnubis/PacketRaftHook

A reverse-engineering project focused on PacketRaft's application-based split tunneling.

* Repository: [PacketRaftHook](https://github.com/iMissAnubis/PacketRaftHook)

It provides useful information about how PacketRaft handles application-specific traffic routing.

### peditx/packetumad

An alternative terminal-based interface for PacketRaft services.

* Repository: [peditx/packetumad](https://github.com/peditx/packetumad)

### iMissAnubis/PacketUmad

Another PacketUmad implementation and source of additional protocol and interoperability information.

* Repository: [iMissAnubis/PacketUmad](https://github.com/iMissAnubis/PacketUmad)

These projects are treated as **references rather than authoritative documentation**. Their implementations may be incomplete, outdated, or based on assumptions that need to be verified against the actual PacketRaft release.

---

## Reverse Engineering Methodology

The project follows a multi-source approach.

```text
                    PacketRaft Release
                           │
                           ▼
                  Static Binary Analysis
                           │
                           ▼
                    Runtime Analysis
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
       Network Analysis             Windows Analysis
             │                           │
             └─────────────┬─────────────┘
                           ▼
                  Protocol Reconstruction
                           │
                           ▼
              Compare Community Projects
                           │
                           ▼
                  Architecture Recovery
                           │
                           ▼
                    Reimplementation
                           │
                           ▼
                 Behavioral Comparison
```

The released application is treated as the primary target.

Reference implementations are used to corroborate findings and fill gaps where appropriate.

---

## Areas Being Investigated

### API

Investigation includes:

* API endpoints
* HTTP/HTTPS communication
* Request formats
* Response formats
* Headers
* Authentication
* Session handling
* Server discovery
* Server metadata
* Error responses

### Authentication

Investigation includes:

* Authentication flow
* Access tokens
* Refresh/session mechanisms
* Device identification
* Client identification
* Session persistence
* Authentication failures

### VPN / Tunnel

Investigation includes:

* Tunnel establishment
* Virtual network interfaces
* Packet encapsulation
* Packet forwarding
* Connection lifecycle
* Keepalive
* Reconnection
* Disconnect handling

### Windows Networking

Investigation includes:

* Network adapters
* Routes
* DNS
* Firewall behavior
* Windows Filtering Platform
* Drivers
* Services
* Network interface configuration
* Process/network interaction

### Split Tunneling

A major focus of this project is application-based traffic routing.

The investigation covers:

* Process identification
* Executable-based routing
* Application inclusion/exclusion
* Per-process traffic handling
* Route manipulation
* Packet filtering
* Child processes
* Dynamic rule changes

The PacketRaftHook project is especially useful for understanding this area. Its documentation describes injecting a DLL into the PacketRaft service and controlling which processes are routed through the VPN.

---

## Architecture

The architecture is currently being reconstructed.

The intended architecture will eventually resemble:

```text
┌──────────────────────────────┐
│            UI                │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Application Core       │
├──────────────────────────────┤
│ Configuration                │
│ Authentication               │
│ Server Management            │
│ Connection Management        │
└──────────────┬───────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
┌──────────────┐ ┌──────────────┐
│ API Client   │ │ Tunnel       │
└──────────────┘ └──────┬───────┘
                        │
               ┌────────┴────────┐
               ▼                 ▼
        ┌─────────────┐   ┌─────────────┐
        │ Routing     │   │ DNS         │
        └─────────────┘   └─────────────┘
               │
               ▼
        Windows Network Stack
               │
               ▼
            Internet
```

This diagram will be updated as the implementation is reconstructed.

---

## Status

🚧 **Active development / reverse engineering**

The project is currently under investigation and reconstruction.

Some components may be incomplete or experimental.

### Current objectives

* [ ] Analyze the latest release
* [ ] Extract and inspect release binaries
* [ ] Identify application architecture
* [ ] Identify API endpoints
* [ ] Document authentication
* [ ] Document server discovery
* [ ] Reconstruct connection flow
* [ ] Reconstruct VPN/tunnel behavior
* [ ] Investigate Windows networking
* [ ] Investigate DNS behavior
* [ ] Reconstruct split tunneling
* [ ] Implement API client
* [ ] Implement authentication
* [ ] Implement server management
* [ ] Implement tunnel
* [ ] Implement routing
* [ ] Implement DNS handling
* [ ] Implement split tunneling
* [ ] Add automated tests
* [ ] Compare implementation against original release
* [ ] Produce stable release builds

---

## Releases

Released builds will be published through the GitHub Releases page.

Each release should include:

* Application binaries
* Required dependencies
* Version information
* Changelog
* Installation instructions
* Known limitations

See:

**[Releases](https://github.com/Testalireza/packetraft/releases)**

---

## Building

Build instructions will be added once the reconstructed implementation reaches a stable state.

The project will provide reproducible build instructions for supported Windows environments.

Example structure:

```text
# Clone
git clone https://github.com/Testalireza/packetraft.git

# Enter directory
cd packetraft

# Install dependencies
# ...

# Build
# ...

# Run
# ...
```

The exact commands will depend on the final implementation language and architecture.

---

## Development

If you are interested in contributing to the reverse-engineering effort, useful areas include:

* Static analysis
* Binary analysis
* Network protocol analysis
* Windows networking
* VPN technologies
* Routing
* DNS
* Windows Filtering Platform
* API analysis
* Reverse engineering
* Protocol documentation
* Testing
* Compatibility testing

When contributing reverse-engineering findings, please distinguish between:

### Confirmed

Directly observed or conclusively established behavior.

### Highly Likely

Behavior supported by multiple independent pieces of evidence.

### Speculative

A hypothesis that has not yet been verified.

This distinction is important to prevent assumptions from becoming undocumented "facts".

---

## Important Notes

### The release is the primary reference

The source repository and the released application may not always contain identical functionality.

For reverse-engineering purposes, the released application is therefore treated as the primary behavioral reference.

### Reference repositories are not authoritative

Community implementations are extremely useful for understanding PacketRaft, but they may contain:

* Outdated implementations
* Incomplete functionality
* Experimental code
* Incorrect assumptions
* Workarounds
* Version-specific behavior

Findings should be verified whenever possible.

### Compatibility

PacketRaft's server-side infrastructure may change independently of this project.

As a result, an implementation that works with one PacketRaft version may not necessarily work with future versions.

---

## Disclaimer

This project is an independent research and interoperability project.

It is **not affiliated with, sponsored by, or endorsed by PacketRaft.ir**.

PacketRaft and related names, trademarks, and services belong to their respective owners.

This project is intended for:

* Research
* Education
* Interoperability
* Software analysis
* Networking experimentation

Users are responsible for complying with all applicable laws, regulations, service terms, and network policies when using the software.

---

## Credits

Thanks to the researchers and developers whose publicly available work provides useful technical information about PacketRaft:

* [b00tkitism/packetraft](https://github.com/b00tkitism/packetraft)
* [iMissAnubis/PacketRaftHook](https://github.com/iMissAnubis/PacketRaftHook)
* [peditx/packetumad](https://github.com/peditx/packetumad)
* [iMissAnubis/PacketUmad](https://github.com/iMissAnubis/PacketUmad)

Their projects significantly contribute to the publicly available understanding of PacketRaft's behavior.

---

## License

See the repository's `LICENSE` file for licensing information.

If no license has been added yet, please add an appropriate license before accepting external contributions.

---

## Star the Project

If you find this reverse-engineering and interoperability work useful, consider giving the repository a ⭐.

**Repository:**
https://github.com/Testalireza/packetraft
