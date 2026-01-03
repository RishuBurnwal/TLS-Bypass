import json
import yaml
from typing import List, Dict, Any
from datetime import datetime
import re


class Exporter:
    """Class for handling rule exports in various formats."""
    
    def __init__(self, rule_manager):
        self.rule_manager = rule_manager
    
    def export_to_txt(self, enabled_only: bool = True) -> str:
        """Export rules to plain text format."""
        hosts, rules = self.rule_manager.read_rules()
        
        content = []
        content.append("# TLS Bypass Rules Export")
        content.append(f"# Exported: {datetime.now()}")
        content.append("# For authorized testing only")
        content.append("")
        
        if hosts:
            content.append("[BLOCK_HOSTS]")
            content.extend(hosts)
            content.append("")
        
        if rules:
            content.append("[BLOCK_RULES]")
            content.extend(rules)
        
        return "\n".join(content)
    
    def export_to_burp_format(self) -> str:
        """Export enabled rules in Burp Suite compatible format."""
        all_rules = self.rule_manager.get_all_rules()
        enabled_rules = [rule for rule in all_rules if rule["enabled"]]
        
        content = []
        content.append("# Burp Suite TLS Bypass Rules")
        content.append(f"# Exported: {datetime.now()}")
        content.append("# For authorized testing only")
        content.append("")
        
        for rule in enabled_rules:
            content.append(rule["pattern"])
        
        return "\n".join(content)
    
    def export_to_json(self) -> str:
        """Export rules to JSON format."""
        all_rules = self.rule_manager.get_all_rules()
        
        export_data = {
            "metadata": {
                "version": "2.0",
                "exported_at": datetime.now().isoformat(),
                "description": "TLS Bypass Rules Export",
                "for_authorized_testing_only": True
            },
            "rules": []
        }
        
        for rule in all_rules:
            export_data["rules"].append({
                "pattern": rule["pattern"],
                "type": rule["type"],
                "enabled": rule["enabled"]
            })
        
        return json.dumps(export_data, indent=2)
    
    def export_to_yaml(self) -> str:
        """Export rules to YAML format."""
        all_rules = self.rule_manager.get_all_rules()
        
        export_data = {
            "metadata": {
                "version": "2.0",
                "exported_at": datetime.now().isoformat(),
                "description": "TLS Bypass Rules Export",
                "for_authorized_testing_only": True
            },
            "rules": []
        }
        
        for rule in all_rules:
            export_data["rules"].append({
                "pattern": rule["pattern"],
                "type": rule["type"],
                "enabled": rule["enabled"]
            })
        
        return yaml.dump(export_data, default_flow_style=False)
    
    def export_to_dict(self) -> Dict[str, Any]:
        """Export rules to a Python dictionary."""
        all_rules = self.rule_manager.get_all_rules()
        
        return {
            "metadata": {
                "version": "2.0",
                "exported_at": datetime.now().isoformat(),
                "description": "TLS Bypass Rules Export",
                "for_authorized_testing_only": True
            },
            "rules": all_rules
        }


class Importer:
    """Class for handling rule imports from various formats."""
    
    def __init__(self, rule_manager):
        self.rule_manager = rule_manager
    
    def import_from_json(self, json_content: str) -> bool:
        """Import rules from JSON format."""
        try:
            data = json.loads(json_content)
            
            if "rules" not in data:
                return False
            
            # Clear existing rules and import new ones
            # For simplicity, we'll append the imported rules
            for rule in data["rules"]:
                pattern = rule.get("pattern", "")
                rule_type = rule.get("type", "regex")
                enabled = rule.get("enabled", True)
                
                if pattern:
                    self.rule_manager.add_rule(pattern, rule_type, enabled)
            
            return True
        except json.JSONDecodeError:
            return False
    
    def import_from_yaml(self, yaml_content: str) -> bool:
        """Import rules from YAML format."""
        try:
            data = yaml.safe_load(yaml_content)
            
            if "rules" not in data:
                return False
            
            for rule in data["rules"]:
                pattern = rule.get("pattern", "")
                rule_type = rule.get("type", "regex")
                enabled = rule.get("enabled", True)
                
                if pattern:
                    self.rule_manager.add_rule(pattern, rule_type, enabled)
            
            return True
        except yaml.YAMLError:
            return False
    
    def import_from_txt(self, txt_content: str) -> bool:
        """Import rules from plain text format."""
        lines = txt_content.splitlines()
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if "[BLOCK_HOSTS]" in line:
                current_section = "host"
            elif "[BLOCK_RULES]" in line:
                current_section = "regex"
            elif line and not line.startswith("#"):
                # Add rule based on current section
                if current_section:
                    rule_type = current_section
                    enabled = True
                    pattern = line
                    
                    # Check if the line is commented out (disabled)
                    if line.startswith("#DISABLED"):
                        pattern = line[10:].strip()
                        enabled = False
                    elif line.startswith("#"):
                        pattern = line[1:].strip()
                        enabled = False
                    
                    self.rule_manager.add_rule(pattern, rule_type, enabled)
        
        return True
    
    def import_from_dict(self, data: Dict[str, Any]) -> bool:
        """Import rules from a Python dictionary."""
        if "rules" not in data:
            return False
        
        for rule in data["rules"]:
            pattern = rule.get("pattern", "")
            rule_type = rule.get("type", "regex")
            enabled = rule.get("enabled", True)
            
            if pattern:
                self.rule_manager.add_rule(pattern, rule_type, enabled)
        
        return True


class RuleExporterImporter:
    """Main class that combines export and import functionality."""
    
    def __init__(self, rule_manager):
        self.rule_manager = rule_manager
        self.exporter = Exporter(rule_manager)
        self.importer = Importer(rule_manager)
    
    def export(self, format_type: str, **kwargs) -> str:
        """Export rules in the specified format."""
        format_type = format_type.lower()
        
        if format_type == "txt":
            return self.exporter.export_to_txt(**kwargs)
        elif format_type == "burp":
            return self.exporter.export_to_burp_format()
        elif format_type == "json":
            return self.exporter.export_to_json()
        elif format_type == "yaml":
            return self.exporter.export_to_yaml()
        else:
            raise ValueError(f"Unsupported export format: {format_type}")
    
    def import_rules(self, format_type: str, content: str) -> bool:
        """Import rules from the specified format."""
        format_type = format_type.lower()
        
        if format_type == "txt":
            return self.importer.import_from_txt(content)
        elif format_type == "json":
            return self.importer.import_from_json(content)
        elif format_type == "yaml":
            return self.importer.import_from_yaml(content)
        else:
            raise ValueError(f"Unsupported import format: {format_type}")
    
    def get_supported_formats(self) -> Dict[str, str]:
        """Get supported import/export formats."""
        return {
            "txt": "Plain Text",
            "json": "JSON Format",
            "yaml": "YAML Format",
            "burp": "Burp Suite Format"
        }