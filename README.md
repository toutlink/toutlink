🔐 toutlink – Offensive Security | Python | AppSec | Red Teaming | Exploit Development | Mobile Security

This repository is my complete security engineering, offensive security, and red team portfolio.
Everything here is designed to show how I think, how I build, how I break and defend systems.

The structure reflects a real-world offensive security workflow:
recon → exploitation → post-exploitation → persistence → cloud → mobile → detection → automation.


🧱 Repository Structure

docker/         → Pentest containers, vulnerable apps, monitoring stack
projects/       → Custom scanners, exploit dev, red team tools, research
writeups/       → Web, infra, mobile, and red team reports
certifications/ → Working toward OSCP
labs/           → Home lab (Windows domain, cloud, detection lab, CTFs)
tools/          → Recon, post-exploitation, forensics, automation
src/            → Portfolio website (Django) to present projects/writeups
docs/           → Methodologies, ATT&CK-style techniques, cheatsheets, roadmap
scripts/        → Setup, automation, monitoring, and maintenance scripts
config/         → Burp, Nmap, Metasploit, and tool configs
tests/          → Unit, integration, penetration, and performance tests
requirements/   → Python dependencies per area (tools, research, etc.)

🎯 Focus Areas

This portfolio showcases my capabilities across:

Web & API Security

XSS, SQLi, SSRF, Injection Chains

OAuth, SSO, JWT, MFA bypass

Logic abuse and complex multi-step workflows

API BOLA, GraphQL, WebSockets

Cloud Security

AWS, Azure, GCP misconfigurations

IAM privilege escalation

Serverless exploitation

CI/CD & supply chain attacks

Red Teaming

Persistence, lateral movement

EDR/AV evasion

C2 frameworks and implants

Adversary simulation workflows

Exploit Development

Binary exploitation

Memory corruption

Web assembly abuse

Modern browser and backend exploitation

Mobile Security (Android & iOS)

APK/IPA reversing

Frida & Objection dynamic analysis

Mobile API exploitation

Certificate pinning bypass

Mobile malware behavior analysis

Detection Engineering

SIEM (ELK / Wazuh / Security Onion)

Log analysis

Atomic Red Team

Detection logic and correlation development

Python Tooling

Custom scanners

Recon automation

Fuzzers

API enumeration tools

Exploit helpers

🧭 Roadmap (Long-Term Curriculum)

My full 300-chapter offensive security roadmap lives here:

📘 docs/roadmap/ROADMAP.md

Covers:

Web, API, Cloud, Mobile

Red Teaming

Exploit Development

AI/LLM security

Ultra-elite multi-stage exploitation chains

🔍 Highlighted Directories
projects/custom_scanner/

My modular Python vulnerability scanner:

src/core/ – engine, fuzzer, payload generator

src/modules/ – SQLi, XSS, SSRF, deserialization, etc.

src/utils/ – HTTP client, report generators

tests/ – unit tests

docs/ – scanner design documentation

tools/recon_suite/

Standalone recon utilities:

subdomain_enum.py

port_scanner.py

web_analyzer.py

cloud_enum.py

labs/

Hands-on attack environments:

Windows AD domain lab

Cloud misconfiguration lab

Detection lab (ELK, Wazuh, Security Onion)

CTF challenges: web, pwn, forensics, mobile

docs/

Knowledge base:

Methodology

Techniques (ATT&CK-style)

Compliance (NIST, ISO 27001, PCI-DSS)

Cheatsheets

Roadmap

🚧 Current Implementation Status

This repo is fully scaffolded and now undergoing live development:

Building out real working tools

Writing deep documentation and methodologies

Adding exploit labs

Producing detailed writeups with evidence

Expanding mobile, cloud, and red team sub-projects

You can track progress through commits and the roadmap.

🧪 Local Setup

git clone git@github.com:toutlink/toutlink.git
cd toutlink

# Optional: virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies (as they get populated)
pip install -r requirements/development.txt

Each project contains its own README for usage details.


🏅 Certifications

OSCP → In progress

OSWE → Planned

OSCE3 → Long-term goal

📬 Contact

📱 Phone: 612-800-4664
📧 Email: iamtoutlink@toutlink.com

Subject to use:
Offensive Security / Python | AppSec | Red Teaming | Exploit Development | Mobile Security 🌍

