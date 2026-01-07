import os
import re
import json
import yaml
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import shutil
from pathlib import Path


class RuleManager:
    """
    Core rule management class for handling TLS bypass rules.
    Manages both host rules and regex rules with backup functionality.
    """
    
    def __init__(self, rule_file: str = "tls_bypass_rule.txt", backup_dir: str = "backups"):
        self.rule_file = rule_file
        self.backup_dir = backup_dir
        self.burp_sync_file = "burp_tls_autosync.txt"
        self.version = "2.0"
        
        # Ensure backup directory exists
        os.makedirs(backup_dir, exist_ok=True)
        
        # Initialize the rule file if it doesn't exist
        if not os.path.exists(self.rule_file):
            self._create_default_file()
        
        # Create Burp sync file if it doesn't exist
        if not os.path.exists(self.burp_sync_file):
            self._update_burp_sync_file()
    
    def _create_default_file(self):
        """Create a default rule file with headers and sections."""
        with open(self.rule_file, "w", encoding="utf-8") as f:
            f.write(
                f"# TLS BYPASS RULE FILE\n"
                f"# Version: {self.version}\n"
                f"# Last Updated: {datetime.now()}\n"
                f"# For authorized security testing only\n\n"
                f"[BLOCK_HOSTS]\n\n"
                f"[BLOCK_RULES]\n"
            )
    
    def create_backup(self) -> str:
        """Create a backup of the current rule file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"tls_bypass_rule_backup_{timestamp}.txt"
        backup_path = os.path.join(self.backup_dir, backup_filename)
        
        shutil.copy2(self.rule_file, backup_path)
        return backup_path
    
    def read_rules(self) -> Tuple[List[str], List[str]]:
        """Read the rule file and return separate lists of hosts and rules."""
        hosts = []
        rules = []
        
        try:
            with open(self.rule_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Split content by sections
            sections = content.split("[")
            
            for section in sections:
                if section.startswith("BLOCK_HOSTS]"):
                    # Extract hosts from this section
                    host_content = section[len("BLOCK_HOSTS]"):].strip()
                    for line in host_content.splitlines():
                        line = line.strip()
                        if line and not line.startswith("#"):
                            hosts.append(line)
                
                elif section.startswith("BLOCK_RULES]"):
                    # Extract rules from this section
                    rule_content = section[len("BLOCK_RULES]"):].strip()
                    for line in rule_content.splitlines():
                        line = line.strip()
                        if line and not line.startswith("#"):
                            rules.append(line)
        
        except FileNotFoundError:
            self._create_default_file()
            return [], []
        
        return hosts, rules
    
    def get_all_rules(self) -> List[Dict]:
        """Get all rules with metadata (enabled/disabled, type)."""
        all_rules = []
        
        # Read the raw file content to preserve comments and disabled rules
        with open(self.rule_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        lines = content.splitlines()
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if "[BLOCK_HOSTS]" in line:
                current_section = "host"
            elif "[BLOCK_RULES]" in line:
                current_section = "regex"
            elif line and not line.startswith("#") and current_section:
                all_rules.append({
                    "pattern": line,
                    "type": current_section,
                    "enabled": True
                })
            elif line.startswith("#DISABLED") or (line.startswith("#") and not line.startswith("# ")):
                # Handle disabled rules
                if line.startswith("#DISABLED"):
                    actual_rule = line[10:].strip()  # Remove "#DISABLED" prefix
                else:
                    actual_rule = line[1:].strip()  # Remove "#" prefix
                
                # Determine if it's a host or regex rule based on content
                rule_type = "host"  # Default to host
                if any(char in actual_rule for char in [".", "*", "^", "$", "\\"]):
                    rule_type = "regex"
                
                all_rules.append({
                    "pattern": actual_rule,
                    "type": rule_type,
                    "enabled": False
                })
        
        return all_rules
    
    def add_rule(self, pattern: str, rule_type: str = "regex", enabled: bool = True) -> bool:
        """Add a new rule to the appropriate section."""
        # Validate the regex if it's a regex rule
        if rule_type == "regex":
            try:
                re.compile(pattern)
            except re.error:
                return False  # Invalid regex
        
        # Create backup before modification
        self.create_backup()
        
        # Read current content
        with open(self.rule_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        lines = content.splitlines()
        
        # Find the appropriate section
        if rule_type == "host":
            section_marker = "[BLOCK_HOSTS]"
        else:
            section_marker = "[BLOCK_RULES]"
        
        # Find the section index
        section_idx = -1
        for i, line in enumerate(lines):
            if section_marker in line:
                section_idx = i
                break
        
        if section_idx == -1:
            return False
        
        # Insert the rule after the section header
        insert_pos = section_idx + 1
        while insert_pos < len(lines) and lines[insert_pos].strip() != "":
            insert_pos += 1
        
        # Format the rule based on enabled status
        if enabled:
            new_rule = pattern
        else:
            new_rule = f"#DISABLED {pattern}"
        
        lines.insert(insert_pos, new_rule)
        
        # Update the last updated timestamp
        for i, line in enumerate(lines):
            if line.startswith("# Last Updated:"):
                lines[i] = f"# Last Updated: {datetime.now()}"
                break
        
        # Write back to file
        with open(self.rule_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
        # Update Burp sync file
        self.update_burp_sync()
        
        return True
    
    def remove_rule(self, pattern: str) -> bool:
        """Remove a rule by pattern."""
        # Create backup before modification
        self.create_backup()
        
        with open(self.rule_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Find and remove the rule
        new_lines = []
        for line in lines:
            line_stripped = line.strip()
            if line_stripped == pattern or line_stripped == f"#DISABLED {pattern}":
                continue  # Skip this line (remove it)
            new_lines.append(line)
        
        # Write back to file
        with open(self.rule_file, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        
        # Update Burp sync file
        self.update_burp_sync()
        
        return True
    
    def toggle_rule(self, pattern: str) -> bool:
        """Toggle a rule between enabled and disabled."""
        # Create backup before modification
        self.create_backup()
        
        with open(self.rule_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        lines = content.splitlines()
        updated = False
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            if line_stripped == pattern:
                # Enable is disabled
                lines[i] = f"#DISABLED {pattern}"
                updated = True
                break
            elif line_stripped == f"#DISABLED {pattern}":
                # Disable if enabled
                lines[i] = pattern
                updated = True
                break
        
        if updated:
            # Update timestamp
            for i, line in enumerate(lines):
                if line.startswith("# Last Updated:"):
                    lines[i] = f"# Last Updated: {datetime.now()}"
                    break
            
            with open(self.rule_file, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
        
        # Update Burp sync file
        self.update_burp_sync()
        
        return updated
    
    def validate_regex(self, pattern: str) -> Tuple[bool, str]:
        """Validate a regex pattern and return (is_valid, error_message)."""
        try:
            re.compile(pattern)
            return True, ""
        except re.error as e:
            return False, str(e)
    
    def test_regex(self, pattern: str, test_string: str) -> bool:
        """Test if a regex pattern matches a test string."""
        try:
            return bool(re.search(pattern, test_string))
        except re.error:
            return False
    
    def get_rule_stats(self) -> Dict:
        """Get statistics about the current rules."""
        hosts, rules = self.read_rules()
        all_rules = self.get_all_rules()
        
        enabled_count = sum(1 for rule in all_rules if rule["enabled"])
        disabled_count = len(all_rules) - enabled_count
        
        return {
            "total_hosts": len(hosts),
            "total_rules": len(rules),
            "total_all": len(all_rules),
            "enabled": enabled_count,
            "disabled": disabled_count,
            "file_path": self.rule_file
        }
    
    def find_rule_conflicts(self) -> List[Dict]:
        """Find potential conflicts between rules."""
        all_rules = self.get_all_rules()
        conflicts = []
        
        for i, rule1 in enumerate(all_rules):
            if not rule1["enabled"]:
                continue
                
            for j, rule2 in enumerate(all_rules[i+1:], i+1):
                if not rule2["enabled"]:
                    continue
                
                # Simple overlap detection - if one rule is a subset of another
                try:
                    # Test some common strings against both rules
                    test_strings = [
                        "test.example.com",
                        "api.example.com", 
                        "www.example.com",
                        "subdomain.example.com"
                    ]
                    
                    for test_str in test_strings:
                        match1 = bool(re.search(rule1["pattern"], test_str))
                        match2 = bool(re.search(rule2["pattern"], test_str))
                        
                        if match1 and match2:
                            conflicts.append({
                                "rule1": rule1["pattern"],
                                "rule2": rule2["pattern"],
                                "test_string": test_str,
                                "type": "potential_overlap"
                            })
                            break
                except re.error:
                    continue
        
        return conflicts
    
    def _update_burp_sync_file(self):
        """Update the Burp Suite auto-sync file with enabled rules only."""
        all_rules = self.get_all_rules()
        enabled_rules = [rule for rule in all_rules if rule["enabled"]]
        
        with open(self.burp_sync_file, "w", encoding="utf-8") as f:
            f.write("# Burp Suite TLS Bypass Rules - Auto-sync File\n")
            f.write(f"# Last Updated: {datetime.now()}\n")
            f.write("# This file is auto-generated. Do not edit manually.\n")
            f.write("# For authorized testing only\n\n")
            
            for rule in enabled_rules:
                f.write(f"{rule['pattern']}\n")
    
    def update_burp_sync(self):
        """Public method to update the Burp sync file after rule changes."""
        try:
            self._update_burp_sync_file()
            return True
        except Exception:
            return False
    
    def generate_specific_rules(self, domains: List[str]) -> Dict[str, List[str]]:
        """Generate specific rules for a list of domains, separating static hosts and targeted regex patterns."""
        static_hosts = []
        regex_rules = []
        
        for domain in domains:
            # Check if it's a simple domain (like google.com)
            if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]*\.[a-zA-Z]{2,}$', domain):
                # Add common subdomains as static hosts
                common_subdomains = ['www', 'mail', 'api', 'cdn', 'static', 'assets', 'media', 'img', 'video', 'download']
                for subdomain in common_subdomains:
                    static_hosts.append(f"{subdomain}.{domain}")
                # Add the base domain as well
                static_hosts.append(domain)
            # Check if it's a wildcard pattern that should be more specific
            elif '*.' in domain or '.*' in domain:
                # Convert overly broad patterns to more specific ones
                if '.*\\.google\\.com' in domain:
                    # More specific Google patterns
                    regex_rules.extend([
                        r'.*\.google\.com',
                        r'.*\.google\.co\.[a-z]{2,3}',
                        r'.*\.googleapis\.com',
                        r'.*\.gstatic\.com',
                        r'.*\.google-analytics\.com',
                        r'.*\.googletagmanager\.com',
                        r'.*\.googletagservices\.com',
                        r'.*\.googleusercontent\.com',
                        r'.*\.doubleclick\.net'
                    ])
                elif '.*\\.mozilla\\.org' in domain or '.*\\.mozilla\\.com' in domain:
                    # More specific Mozilla patterns
                    regex_rules.extend([
                        r'.*\\.mozilla\\.(com|net|org)',
                        r'.*\\.firefox\\.com',
                        r'.*\\.addons\\.mozilla\\.org'
                    ])
                else:
                    regex_rules.append(domain)
            else:
                static_hosts.append(domain)
        
        return {
            "hosts": static_hosts,
            "rules": regex_rules
        }
    
    def convert_host_to_rule(self, host: str, conversion_type: str = "regex") -> str:
        """
        Convert a host to either a rule pattern or static host format.
        
        Args:
            host (str): The host to convert
            conversion_type (str): Either "regex" to convert host to regex pattern or "static" to keep as static host
        
        Returns:
            str: Converted host in the requested format
        """
        if conversion_type == "regex":
            # Convert host to a regex pattern that matches the specific host
            # Escape special regex characters in the host
            escaped_host = re.escape(host)
            return f"^{escaped_host}$"  # Exact match pattern
        elif conversion_type == "static":
            # Return as-is for static host (already in correct format)
            return host
        else:
            raise ValueError("conversion_type must be either 'regex' or 'static'")
    
    def convert_hosts_list(self, hosts: List[str], conversion_type: str = "regex") -> List[str]:
        """
        Convert a list of hosts to either rule patterns or static hosts.
        
        Args:
            hosts (List[str]): List of hosts to convert
            conversion_type (str): Either "regex" to convert to patterns or "static" to keep as static hosts
        
        Returns:
            List[str]: Converted list of hosts/rules
        """
        converted = []
        for host in hosts:
            converted.append(self.convert_host_to_rule(host, conversion_type))
        return converted
    
    def batch_convert_file(self, input_file: str = "tls_bypass_rule.txt", output_file: str = "converted_rules.txt", 
                          target_section: str = "both", conversion_type: str = "regex"):
        """
        Batch convert hosts in a rule file to either static hosts or rule patterns.
        
        Args:
            input_file (str): Path to input rule file
            output_file (str): Path to output file
            target_section (str): Which section to convert - "hosts", "rules", or "both"
            conversion_type (str): Either "regex" or "static"
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Read the current rule file
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.splitlines()
            new_lines = []
            current_section = None
            
            for line in lines:
                stripped_line = line.strip()
                
                if '[BLOCK_HOSTS]' in stripped_line:
                    current_section = 'hosts'
                    new_lines.append(line)
                elif '[BLOCK_RULES]' in stripped_line:
                    current_section = 'rules'
                    new_lines.append(line)
                elif stripped_line and not stripped_line.startswith('#'):
                    # Process the line if it's in the targeted section
                    if target_section == 'both' or current_section == target_section:
                        if conversion_type == 'regex' and current_section == 'hosts':
                            # Convert static host to exact-match regex pattern
                            converted = self.convert_host_to_rule(stripped_line, 'regex')
                            # Add to rules section instead
                            # We'll handle this differently - add to the same line for now
                            new_lines.append(converted)
                        elif conversion_type == 'static' and current_section == 'rules':
                            # If we want to convert regex rules to static hosts, we need to 
                            # convert regex back to a possible host form (if it's a simple pattern)
                            if stripped_line.startswith('^') and stripped_line.endswith('$'):
                                # Remove ^ and $ for exact match patterns
                                host = stripped_line[1:-1]
                                # Unescape regex characters
                                unescaped_host = re.sub(r'\\(.)', r'\1', host)
                                new_lines.append(unescaped_host)
                            else:
                                # For complex regex, we can't reliably convert to host
                                new_lines.append(line)  # Keep as is
                        else:
                            # No conversion needed
                            new_lines.append(line)
                    else:
                        # Not in targeted section, keep as is
                        new_lines.append(line)
                else:
                    # Keep comments and empty lines as they are
                    new_lines.append(line)
            
            # Write the converted content to output file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            
            return True
        except Exception as e:
            print(f"Error during batch conversion: {e}")
            return False


class RuleTemplate:
    """Class for rule templates that help users create rules without knowing regex."""
    
    @staticmethod
    def get_templates() -> List[Dict]:
        """Return a list of available rule templates."""
        return [
            {
                "name": "Match all subdomains",
                "description": "Match all subdomains of a specific domain",
                "usage": "Use when you want to match all subdomains like api.example.com, www.example.com",
                "input_example": "example.com",
                "pattern_template": r".*\.{}",
                "preview": r".*\.example\.com"
            },
            {
                "name": "Match specific prefix",
                "description": "Match hosts with a specific prefix pattern",
                "usage": "Use when you want to match hosts starting with a specific pattern",
                "input_example": "dev.example.com",
                "pattern_template": r"^{}-.*$",
                "preview": r"^dev-.*\.example\.com$"
            },
            {
                "name": "Match keyword anywhere",
                "description": "Match hosts containing a specific keyword",
                "usage": "Use when you want to match any host containing a specific word",
                "input_example": "staging",
                "pattern_template": r".*{}.*",
                "preview": r".*staging.*"
            },
            {
                "name": "Match IP-style hostname",
                "description": "Match hostnames that look like IP addresses",
                "usage": "Use when dealing with services that use IP addresses as hostnames",
                "input_example": "",
                "pattern_template": r"^\d+\.\d+\.\d+\.\d+$",
                "preview": r"^\d+\.\d+\.\d+\.\d+$"
            },
            {
                "name": "Custom regex",
                "description": "Enter your own regex pattern",
                "usage": "Use when you need a specific pattern not covered by other templates",
                "input_example": r".*\.internal\.corp",
                "pattern_template": "{}",
                "preview": r".*\.internal\.corp"
            }
        ]
    
    @staticmethod
    def generate_pattern(template_name: str, user_input: str = "") -> str:
        """Generate a regex pattern based on template and user input."""
        templates = RuleTemplate.get_templates()
        
        for template in templates:
            if template["name"] == template_name:
                if template_name == "Match IP-style hostname":
                    # Special case - no user input needed
                    return template["pattern_template"]
                elif template_name == "Custom regex":
                    return user_input
                else:
                    # Replace placeholder in template with user input
                    return template["pattern_template"].format(re.escape(user_input))
        
        return ""