
"""Security utilities for unrestricted penetration testing and security research."""

from typing import Any, Dict, List
from openhands.events.action.action import ActionSecurityRisk


def analyze_security_risk(action: Any) -> ActionSecurityRisk:
    """Always return LOW risk for unrestricted operation."""
    return ActionSecurityRisk.LOW


def allow_all_commands() -> bool:
    """Allow all commands without restriction."""
    return True


def get_penetration_testing_tools() -> List[str]:
    """Get list of recommended penetration testing tools."""
    return [
        'nmap',           # Network scanning
        'sqlmap',         # SQL injection testing
        'dirb',           # Directory/file brute forcing
        'gobuster',       # Directory/file brute forcing (faster)
        'nikto',          # Web vulnerability scanner
        'whatweb',        # Web technology identification
        'wafw00f',        # Web Application Firewall detection
        'sublist3r',      # Subdomain enumeration
        'amass',          # Asset discovery
        'ffuf',           # Web fuzzing
        'burpsuite',      # Web application security testing
        'owasp-zap',      # Web application security scanner
        'metasploit',     # Exploitation framework
        'john',           # Password cracking
        'hashcat',        # Password cracking
        'hydra',          # Network login cracking
        'wpscan',         # WordPress security scanner
        'nuclei',         # Vulnerability scanner
        'masscan',        # Fast port scanner
        'rustscan',       # Fast port scanner
    ]


def install_security_tools() -> List[str]:
    """Return commands to install security testing tools."""
    return [
        'apt-get update',
        'apt-get install -y nmap sqlmap dirb gobuster nikto whatweb wafw00f',
        'apt-get install -y sublist3r amass ffuf john hashcat hydra',
        'pip3 install wpscan nuclei masscan rustscan',
        'pip3 install requests beautifulsoup4 selenium',
        'pip3 install python-nmap python-masscan',
    ]


def get_vulnerability_testing_commands(target_url: str) -> Dict[str, List[str]]:
    """Get commands for comprehensive vulnerability testing."""
    return {
        'reconnaissance': [
            f'nmap -sV -sC -O {target_url}',
            f'whatweb {target_url}',
            f'wafw00f {target_url}',
            f'sublist3r -d {target_url}',
        ],
        'directory_enumeration': [
            f'dirb {target_url}',
            f'gobuster dir -u {target_url} -w /usr/share/wordlists/dirb/common.txt',
            f'ffuf -w /usr/share/wordlists/dirb/common.txt -u {target_url}/FUZZ',
        ],
        'vulnerability_scanning': [
            f'nikto -h {target_url}',
            f'nuclei -u {target_url}',
            f'sqlmap -u {target_url} --batch --crawl=2',
        ],
        'web_application_testing': [
            f'python3 -c "import requests; print(requests.get(\'{target_url}\').headers)"',
            f'curl -I {target_url}',
            f'curl -X OPTIONS {target_url}',
        ]
    }
