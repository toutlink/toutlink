# 🔐 toutlink | Offensive Security Portfolio

> **Building. Breaking. Defending.**  
> A comprehensive security engineering portfolio showcasing offensive security, red teaming, and exploit development capabilities.

![Security](https://img.shields.io/badge/Security-Offensive-red)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Platform](https://img.shields.io/badge/Platform-Web%20%7C%20Cloud%20%7C%20Mobile%20%7C%20Network-lightgrey)
![Status](https://img.shields.io/badge/Status-Active%20Development-brightgreen)
![OSCP](https://img.shields.io/badge/OSCP-In%20Progress-orange)
![HTB](https://img.shields.io/badge/HackTheBox-Active_Learner-blue)

---

## 🎯 Portfolio Overview

This repository represents my journey to elite offensive security mastery. Every tool, writeup, and lab reflects real-world security workflows from reconnaissance to advanced persistence.

**Core Philosophy:** *Understand systems by building them, then break them to defend better.*

---

## 🏗️ Repository Structure

| Directory | Purpose | Status |
|-----------|---------|---------|
| [`docker/`](./docker/) | Pentest containers & vulnerable apps | 🟢 Active |
| [`projects/`](./projects/) | Custom tools & security research | 🟢 Active |
| [`writeups/`](./writeups/) | Penetration test reports | 🟡 In Progress |
| [`labs/`](./labs/) | Home lab environments | 🟢 Active |
| [`tools/`](./tools/) | Recon & exploitation utilities | 🟢 Active |
| [`src/`](./src/) | Portfolio website (Django) | 🟡 Building |
| [`docs/`](./docs/) | Methodologies & techniques | 🟢 Active |
| [`certifications/`](./certifications/) | OSCP Preparation | 🟡 Studying |

---

## 🔥 Featured Projects

### 🛠️ Custom Security Tools
- **[Custom Vulnerability Scanner](./projects/custom_scanner/)** - Modular Python-based scanner with plugin architecture
- **Red Team C2 Framework** - Custom command and control infrastructure
- **Exploit Development Kit** - Buffer overflow, ROP chains, and modern exploitation

### 🎯 Attack Simulations
- **Windows AD Domain Lab** - Full enterprise environment for red team practice
- **Cloud Misconfiguration Labs** - AWS, Azure, GCP attack scenarios
- **Mobile Security Lab** - Android/iOS application testing environment

### 📊 Detection Engineering
- **ELK + Wazuh Stack** - Security monitoring and detection lab
- **Atomic Red Team** - Detection testing and validation

---

## 🎓 Core Competencies

### **Web & API Security**
```python
# Advanced vulnerability discovery
- XSS | SQLi | SSRF | Injection chains
- OAuth/SSO exploitation | JWT attacks
- Business logic abuse | API security
- GraphQL | WebSockets | HTTP/2+ attacks

Cloud & Infrastructure
# Multi-cloud security assessment
☁️ AWS IAM privilege escalation
☁️ Azure service exploitation  
☁️ GCP metadata abuse
☁️ Kubernetes & container security

Red Teaming
# Adversary simulation
- Persistence mechanisms
- Lateral movement techniques
- EDR/AV evasion
- C2 infrastructure

Exploit Development
// Modern exploitation
📟 Binary exploitation
📟 Memory corruption
📟 WebAssembly attacks
📟 Browser security research

📚 Learning Journey
🎯 Current Focus: OSCP Preparation & Foundations
Penetration testing methodology

Privilege escalation techniques

Buffer overflow exploitation

Network penetration testing

📖 Complete Curriculum: The toutlink Elite Offensive Security Handbook
I'm systematically progressing through my 300-chapter elite security curriculum:

📘 The Complete toutlink Elite Offensive Security Handbook | Roadmap 01–300

Progress: 45/300 Chapters (15% Complete)

Phase	Chapters	Focus Areas	Status
1. Foundations	1-50	Web App Security, Reconnaissance	🟢 90%
2. Core Vulnerabilities	51-100	API Security, Cloud, Mobile	🟡 Next
3. Advanced Techniques	101-150	Red Teaming, Exploit Dev	⏳ Planned
4. Elite Mastery	151-300	Zero-day Research, AI Security	⏳ Future
🏆 Hack The Box Progress
🎖️ HTB Academy Achievements
https://academy.hackthebox.com/achievement/badge/93461297-b300-11f0-9254-bea50ffe6cb4

Active HTB Academy Student - Systematically building penetration testing skills through structured learning paths and hands-on labs.

🔥 Current HTB Learning Tracks
# Completed Modules & Skills
✅ Linux Fundamentals
✅ Network Enumeration with Nmap
✅ Web Requests & Authentication
✅ Introduction to Penetration Testing
🔄 Active Directory Basics
⏳ Buffer Overflow Exploitation
⏳ Privilege Escalation Techniques

📊 HTB Machine Progress
Recent Machine Solves:

Starting Point Tier 0-2: Complete

Easy Rated Machines: 8+ machines rooted

Web Application Challenges: Multiple completed

Active Directory Labs: In progress

Skills Demonstrated Through HTB:

Enumeration Mastery: Thorough network and service discovery

Web Application Testing: XSS, SQLi, file upload vulnerabilities

Privilege Escalation: Linux and Windows escalation techniques

Methodology Development: Systematic approach to penetration testing

🎯 HTB Learning Objectives

OSCP Alignment: Practice exam-relevant techniques and methodologies

Real-World Simulation: Develop muscle memory for common attack vectors

Tool Proficiency: Master industry-standard penetration testing tools

Documentation Skills: Improve reporting and evidence collection

🏆 OSCP Certification Goal

🎯 Target: Offensive Security Certified Professional
Status: 🔄 Active Preparation
Timeline: Q2 2024
Focus Areas: Penetration Testing, Exploitation, Post-Exploitation

📚 OSCP Preparation Progress

# Current Study Focus
✅ Penetration Testing Methodology
✅ Network Enumeration & Scanning
✅ Web Application Attacks
✅ Privilege Escalation (Linux/Windows)
🔄 Buffer Overflow Exploitation
⏳ Active Directory Attacks
⏳ Exam Strategy & Time Management

🛠️ OSCP-Lab Aligned Projects
Buffer Overflow Practice - Windows & Linux exploitation

Privilege Escalation Scripts - Auto-enumeration tools

Active Directory Lab - Full AD attack environment

Penetration Test Reports - Real-world methodology practice

📖 Study Materials
Official PWK Courseware - In progress

HTB Academy & Machines - Regular practice

Proving Grounds Practice - Supplemental practice

Custom Cheatsheets - View Here

🛠️ Technical Stack
Category	Technologies
Languages	Python, JavaScript, C, SQL, Assembly
Security Tools	Burp Suite, Metasploit, Nmap, Wireshark
Cloud	AWS, Azure, GCP, Kubernetes, Docker
Platforms	Linux, Windows, Android, iOS
Defense	ELK Stack, Wazuh, Security Onion, YARA
📊 Project Status
Component	Status	Progress
Custom Scanner	🟢 Active	85%
Red Team Tools	🟢 Active	70%
Exploit Development	🟡 In Progress	60%
OSCP Preparation	🟡 Active Study	65%
HTB Practice	🟢 Regular	Ongoing
Documentation	🟢 Active	80%

🚀 Getting Started
Quick Setup

# Clone repository
git clone https://github.com/yourusername/toutlink_portfolio.git
cd toutlink_portfolio

# Optional: virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements/development.txt

Explore Key Components

# Run custom vulnerability scanner
cd projects/custom_scanner/
python src/core/scanner.py --help

# Deploy OSCP practice lab
cd labs/windows_domain/
docker-compose up -d

# Check security dashboard
cd src/
python manage.py runserver

🌐 Connect With Me

| Platform | Link | Focus |
|----------|------|-------|
| **🌐 Website** | [www.toutlink.com](https://www.toutlink.com) | Security Tools Distribution • Python Education |
| **💼 LinkedIn** | [Kossi Agode](https://www.linkedin.com/in/kossi-agode-07831b339/) | Professional Network |
| **🐦 Twitter** | [@iamtoutlink](https://twitter.com/iamtoutlink) | Security Insights & Tool Releases |
| **📧 Email** | `iamtoutlink@toutlink.com` | Direct Contact & Opportunities |
| **📱 Phone** | `612-800-4664` | Urgent Security Matters |
| **🎯 HTB** | [ToutLink](https://app.hackthebox.com/profile/your-profile-id) | Practical Penetration Testing |
| **🏆 HTB Academy** | [Achievements](https://academy.hackthebox.com/achievement/badge/93461297-b300-11f0-9254-bea50ffe6cb4) | Structured Security Learning |

---

## 🚀 Future Vision: Security Tools Platform

### 🌐 [www.toutlink.com](https://www.toutlink.com) → **Future Security Tools Hub**

**Current:** French-language Python and digital education platform  
**Future:** Open-source offensive security tools distribution center

**Planned Tool Distribution:**
- All portfolio projects available for public download
- Comprehensive installation guides and documentation
- Video tutorials and usage demonstrations
- Community support and contribution system
- Regular updates and new tool releases

**Available Soon:**
```bash
# Tools Coming to toutlink.com
🔧 Custom Vulnerability Scanner
🔧 Red Team C2 Framework  
🔧 Exploit Development Kits
🔧 Mobile Security Tools
🔧 API Testing Utilities
🔧 Cloud Assessment Scripts

Mission: Create an open-source security tools platform where cybersecurity professionals and learners can access, use, and contribute to offensive security utilities.

🛠️ Tool Availability Roadmap
Tool Category	Status	Website Release
Custom Vulnerability Scanner	🟢 Active	Q3 2024
Red Team C2 Framework	🟡 In Progress	Q4 2024
Exploit Development Kit	🟡 In Progress	Q4 2024
API Security Testing Suite	⏳ Planned	Q1 2025
Cloud Security Assessment	⏳ Planned	Q1 2025
Note: All tools will be freely available on toutlink.com with comprehensive documentation, installation guides, and usage examples.



📚 Documentation
Methodologies - Testing approaches and frameworks

Techniques - ATT&CK-style attack techniques

Cheatsheets - OSCP & penetration testing guides

Roadmap - Complete 300-chapter curriculum

⚠️ Legal & Ethical Notice
Important: All tools, techniques, and research in this repository are intended for:

Educational purposes

Authorized security testing

Professional development

Security research

❌ Never use for unauthorized testing
✅ Always obtain proper authorization
🔒 Follow responsible disclosure practices

📄 License
This repository is for portfolio purposes. Individual projects may have their own licenses. All tools are provided "as-is" for educational use.


