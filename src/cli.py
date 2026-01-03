import os
import sys
from typing import Optional
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Add the project root to the Python path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from rules import RuleManager, RuleTemplate
from utils import ColorPrinter
from exports import RuleExporterImporter


class CLIRuleManager:
    """Command-line interface for the TLS Bypass Rule Manager."""
    
    def __init__(self):
        self.rule_manager = RuleManager()
        self.exporter_importer = RuleExporterImporter(self.rule_manager)
        self.running = True
    
    def print_header(self):
        """Print the application header."""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN} TLS BYPASS RULE MANAGER - CLI INTERFACE")
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}Version: {self.rule_manager.version}")
        print(f"{Fore.YELLOW}Rule File: {os.path.abspath(self.rule_manager.rule_file)}")
        print(f"{Fore.CYAN}{'='*60}")
    
    def print_help(self):
        """Print help information."""
        print(f"\n{Fore.CYAN}TLS BYPASS RULE MANAGER - HELP")
        print(f"{Fore.CYAN}{'-'*50}")
        print(f"{Fore.GREEN}WHAT IS THIS TOOL?{Style.RESET_ALL}")
        print("This tool manages TLS bypass rule files used for authorized")
        print("testing environments (example: Burp Suite exclusions).")
        print()
        print(f"{Fore.RED}It DOES NOT bypass TLS by itself.{Style.RESET_ALL}")
        print()
        print(f"{Fore.GREEN}TYPES OF ENTRIES{Style.RESET_ALL}")
        print("1) BLOCK HOST - Matches one exact hostname")
        print("   Example: example.com, api.dev.local")
        print("   Use when the domain is fixed and known.")
        print()
        print("2) BLOCK RULE (REGEX) - Pattern-based matching")
        print("   Useful for multiple hosts")
        print("   Examples: .*\\.internal\\.corp, ^dev-.*\\.example\\.com$")
        print()
        print(f"{Fore.GREEN}RULE TEMPLATES{Style.RESET_ALL}")
        print("The tool provides guided templates for common patterns:")
        print("- Match all subdomains")
        print("- Match specific prefix")
        print("- Match keyword anywhere")
        print("- Match IP-style hostname")
        print("- Custom regex")
        print()
        print(f"{Fore.GREEN}ETHICAL NOTICE{Style.RESET_ALL}")
        print("Only use TLS bypass rules on systems you own or are")
        print("explicitly authorized to test.")
        print(f"{'-'*50}")
    
    def show_stats(self):
        """Show rule statistics."""
        stats = self.rule_manager.get_rule_stats()
        
        print(f"\n{Fore.CYAN}RULE STATISTICS")
        print(f"{Fore.CYAN}{'-'*30}")
        print(f"{Fore.YELLOW}Total Host Rules: {stats['total_hosts']}")
        print(f"{Fore.YELLOW}Total Regex Rules: {stats['total_rules']}")
        print(f"{Fore.YELLOW}Total All Rules: {stats['total_all']}")
        print(f"{Fore.GREEN}Enabled Rules: {stats['enabled']}")
        print(f"{Fore.RED}Disabled Rules: {stats['disabled']}")
        print(f"{Fore.YELLOW}File Path: {stats['file_path']}")
    
    def list_rules(self):
        """List all rules."""
        all_rules = self.rule_manager.get_all_rules()
        
        if not all_rules:
            ColorPrinter.info("No rules found.")
            return
        
        print(f"\n{Fore.CYAN}CURRENT RULES")
        print(f"{Fore.CYAN}{'-'*50}")
        
        for i, rule in enumerate(all_rules, 1):
            status_color = Fore.GREEN if rule["enabled"] else Fore.RED
            type_color = Fore.YELLOW if rule["type"] == "host" else Fore.MAGENTA
            status = "ENABLED" if rule["enabled"] else "DISABLED"
            
            print(f"{i:2d}. [{status_color}{status}{Style.RESET_ALL}] "
                  f"[{type_color}{rule['type'].upper()}{Style.RESET_ALL}] "
                  f"{rule['pattern']}")
    
    def add_rule_menu(self):
        """Menu for adding new rules."""
        print(f"\n{Fore.CYAN}ADD NEW RULE")
        print(f"{Fore.CYAN}{'-'*20}")
        
        print("Choose rule type:")
        print("1. Host Rule (exact match)")
        print("2. Regex Rule (pattern match)")
        print("3. Guided Rule Template")
        
        choice = input(f"\nSelect option (1-3): ").strip()
        
        if choice == "1":
            self.add_host_rule()
        elif choice == "2":
            self.add_regex_rule()
        elif choice == "3":
            self.guided_rule_creation()
        else:
            ColorPrinter.error("Invalid choice.")
    
    def add_host_rule(self):
        """Add a host rule."""
        host = input("Enter hostname: ").strip()
        
        if not host:
            ColorPrinter.error("Hostname cannot be empty.")
            return
        
        if self.rule_manager.add_rule(host, "host"):
            ColorPrinter.success(f"Host rule '{host}' added successfully.")
        else:
            ColorPrinter.error("Failed to add host rule.")
    
    def add_regex_rule(self):
        """Add a regex rule."""
        pattern = input("Enter regex pattern: ").strip()
        
        if not pattern:
            ColorPrinter.error("Pattern cannot be empty.")
            return
        
        # Validate the regex
        is_valid, error_msg = self.rule_manager.validate_regex(pattern)
        if not is_valid:
            ColorPrinter.error(f"Invalid regex pattern: {error_msg}")
            return
        
        # Test the regex
        test_input = input("Test string (optional, press Enter to skip): ").strip()
        if test_input:
            matches = self.rule_manager.test_regex(pattern, test_input)
            if matches:
                ColorPrinter.success(f"Pattern matches test string: {test_input}")
            else:
                ColorPrinter.warning(f"Pattern does not match test string: {test_input}")
        
        if self.rule_manager.add_rule(pattern, "regex"):
            ColorPrinter.success(f"Regex rule '{pattern}' added successfully.")
        else:
            ColorPrinter.error("Failed to add regex rule.")
    
    def guided_rule_creation(self):
        """Create a rule using guided templates."""
        templates = RuleTemplate.get_templates()
        
        print(f"\n{Fore.CYAN}GUIDED RULE TEMPLATES")
        print(f"{Fore.CYAN}{'-'*40}")
        
        for i, template in enumerate(templates, 1):
            print(f"{i}. {template['name']}")
            print(f"   Description: {template['description']}")
            print(f"   Usage: {template['usage']}")
            if template['input_example']:
                print(f"   Example: {template['input_example']}")
            print(f"   Preview: {template['preview']}")
            print()
        
        try:
            choice = int(input("Select template (1-{}): ".format(len(templates))))
            if 1 <= choice <= len(templates):
                selected_template = templates[choice - 1]
                
                print(f"\n{Fore.YELLOW}Creating: {selected_template['name']}")
                print(f"Description: {selected_template['description']}")
                
                user_input = ""
                if selected_template['name'] != "Match IP-style hostname" and selected_template['name'] != "Custom regex":
                    user_input = input(f"Enter value (example: {selected_template['input_example']}): ").strip()
                elif selected_template['name'] == "Custom regex":
                    user_input = input("Enter your regex pattern: ").strip()
                
                if selected_template['name'] == "Match IP-style hostname":
                    # Special case - no user input needed
                    pattern = selected_template['pattern_template']
                else:
                    pattern = RuleTemplate.generate_pattern(selected_template['name'], user_input)
                
                if not pattern:
                    ColorPrinter.error("Failed to generate pattern.")
                    return
                
                print(f"\n{Fore.CYAN}Generated Pattern: {pattern}")
                
                # Validate the generated pattern
                is_valid, error_msg = self.rule_manager.validate_regex(pattern)
                if not is_valid:
                    ColorPrinter.error(f"Generated pattern is invalid: {error_msg}")
                    return
                
                # Test the pattern
                test_input = input("Test string (optional, press Enter to skip): ").strip()
                if test_input:
                    matches = self.rule_manager.test_regex(pattern, test_input)
                    if matches:
                        ColorPrinter.success(f"Pattern matches test string: {test_input}")
                    else:
                        ColorPrinter.warning(f"Pattern does not match test string: {test_input}")
                
                # Add the rule
                if self.rule_manager.add_rule(pattern, "regex"):
                    ColorPrinter.success(f"Rule added successfully: {pattern}")
                else:
                    ColorPrinter.error("Failed to add rule.")
            else:
                ColorPrinter.error("Invalid selection.")
        except ValueError:
            ColorPrinter.error("Invalid input. Please enter a number.")
    
    def toggle_rule(self):
        """Toggle a rule's enabled/disabled status."""
        all_rules = self.rule_manager.get_all_rules()
        
        if not all_rules:
            ColorPrinter.info("No rules to toggle.")
            return
        
        self.list_rules()
        
        try:
            choice = int(input(f"\nSelect rule to toggle (1-{len(all_rules)}): ").strip())
            if 1 <= choice <= len(all_rules):
                rule = all_rules[choice - 1]
                pattern = rule['pattern']
                
                if self.rule_manager.toggle_rule(pattern):
                    new_status = "disabled" if rule['enabled'] else "enabled"
                    ColorPrinter.success(f"Rule {new_status}: {pattern}")
                else:
                    ColorPrinter.error("Failed to toggle rule.")
            else:
                ColorPrinter.error("Invalid selection.")
        except ValueError:
            ColorPrinter.error("Invalid input. Please enter a number.")
    
    def remove_rule(self):
        """Remove a rule."""
        all_rules = self.rule_manager.get_all_rules()
        
        if not all_rules:
            ColorPrinter.info("No rules to remove.")
            return
        
        self.list_rules()
        
        try:
            choice = int(input(f"\nSelect rule to remove (1-{len(all_rules)}): ").strip())
            if 1 <= choice <= len(all_rules):
                rule = all_rules[choice - 1]
                pattern = rule['pattern']
                
                confirm = input(f"Confirm removal of '{pattern}'? (y/N): ").strip().lower()
                if confirm in ['y', 'yes']:
                    if self.rule_manager.remove_rule(pattern):
                        ColorPrinter.success(f"Rule removed: {pattern}")
                    else:
                        ColorPrinter.error("Failed to remove rule.")
                else:
                    ColorPrinter.info("Removal cancelled.")
            else:
                ColorPrinter.error("Invalid selection.")
        except ValueError:
            ColorPrinter.error("Invalid input. Please enter a number.")
    
    def regex_tester(self):
        """Test a regex pattern against a string."""
        print(f"\n{Fore.CYAN}REGEX TESTER")
        print(f"{Fore.CYAN}{'-'*20}")
        
        pattern = input("Enter regex pattern: ").strip()
        if not pattern:
            ColorPrinter.error("Pattern cannot be empty.")
            return
        
        test_string = input("Enter test string: ").strip()
        if not test_string:
            ColorPrinter.error("Test string cannot be empty.")
            return
        
        # Validate the regex
        is_valid, error_msg = self.rule_manager.validate_regex(pattern)
        if not is_valid:
            ColorPrinter.error(f"Invalid regex pattern: {error_msg}")
            return
        
        # Test the pattern
        matches = self.rule_manager.test_regex(pattern, test_string)
        
        if matches:
            ColorPrinter.success(f"MATCH: '{test_string}' matches pattern '{pattern}'")
        else:
            ColorPrinter.warning(f"NO MATCH: '{test_string}' does not match pattern '{pattern}'")
    
    def export_rules(self):
        """Export rules in various formats."""
        print(f"\n{Fore.CYAN}EXPORT RULES")
        print(f"{Fore.CYAN}{'-'*20}")
        
        formats = self.exporter_importer.get_supported_formats()
        print("Available formats:")
        for key, value in formats.items():
            print(f"  {key}: {value}")
        
        format_type = input("\nEnter format type: ").strip().lower()
        
        if format_type not in formats:
            ColorPrinter.error(f"Unsupported format: {format_type}")
            return
        
        try:
            exported_content = self.exporter_importer.export(format_type)
            
            filename = input(f"Enter filename (or press Enter for default): ").strip()
            if not filename:
                from utils import generate_export_filename
                filename = generate_export_filename(format_type)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(exported_content)
            
            ColorPrinter.success(f"Rules exported to: {filename}")
        except Exception as e:
            ColorPrinter.error(f"Export failed: {str(e)}")
    
    def import_rules(self):
        """Import rules from various formats."""
        print(f"\n{Fore.CYAN}IMPORT RULES")
        print(f"{Fore.CYAN}{'-'*20}")
        
        formats = self.exporter_importer.get_supported_formats()
        print("Available formats:")
        for key, value in formats.items():
            print(f"  {key}: {value}")
        
        format_type = input("\nEnter format type: ").strip().lower()
        
        if format_type not in formats:
            ColorPrinter.error(f"Unsupported format: {format_type}")
            return
        
        filename = input("Enter filename to import: ").strip()
        
        if not os.path.exists(filename):
            ColorPrinter.error(f"File does not exist: {filename}")
            return
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if self.exporter_importer.import_rules(format_type, content):
                ColorPrinter.success(f"Rules imported from: {filename}")
            else:
                ColorPrinter.error("Import failed. Invalid format or content.")
        except Exception as e:
            ColorPrinter.error(f"Import failed: {str(e)}")
    
    def show_conflicts(self):
        """Show potential rule conflicts."""
        conflicts = self.rule_manager.find_rule_conflicts()
        
        if not conflicts:
            ColorPrinter.success("No conflicts found between rules.")
            return
        
        print(f"\n{Fore.CYAN}POTENTIAL RULE CONFLICTS")
        print(f"{Fore.CYAN}{'-'*30}")
        
        for i, conflict in enumerate(conflicts, 1):
            print(f"{i}. Rule 1: {conflict['rule1']}")
            print(f"   Rule 2: {conflict['rule2']}")
            print(f"   Both match: {conflict['test_string']}")
            print(f"   Type: {conflict['type']}")
            print()
    
    def main_menu(self):
        """Display the main menu and handle user input."""
        while self.running:
            self.print_header()
            
            print(f"\n{Fore.YELLOW}MAIN MENU")
            print(f"{Fore.YELLOW}{'-'*15}")
            print("1. Show rule statistics")
            print("2. List all rules")
            print("3. Add new rule")
            print("4. Toggle rule status")
            print("5. Remove rule")
            print("6. Regex tester")
            print("7. Export rules")
            print("8. Import rules")
            print("9. Check for conflicts")
            print("10. Help / Playbook")
            print("11. Exit")
            
            choice = input(f"\nSelect option (1-11): ").strip()
            
            if choice == "1":
                self.show_stats()
            elif choice == "2":
                self.list_rules()
            elif choice == "3":
                self.add_rule_menu()
            elif choice == "4":
                self.toggle_rule()
            elif choice == "5":
                self.remove_rule()
            elif choice == "6":
                self.regex_tester()
            elif choice == "7":
                self.export_rules()
            elif choice == "8":
                self.import_rules()
            elif choice == "9":
                self.show_conflicts()
            elif choice == "10":
                self.print_help()
            elif choice == "11":
                print(f"\n{Fore.CYAN}Thank you for using TLS Bypass Rule Manager!")
                print(f"{Fore.YELLOW}Remember: Use only for authorized testing.")
                self.running = False
            else:
                ColorPrinter.error("Invalid option. Please select 1-11.")
            
            if self.running:
                input(f"\n{Fore.CYAN}Press Enter to continue...")
    
    def run(self):
        """Run the CLI application."""
        try:
            self.main_menu()
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Application interrupted by user.")
        except Exception as e:
            ColorPrinter.error(f"An error occurred: {str(e)}")
            sys.exit(1)


def main():
    """Main entry point."""
    app = CLIRuleManager()
    app.run()


if __name__ == "__main__":
    main()