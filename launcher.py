"""
TLS Bypass Rule Manager - Single Launcher
=========================================

This is a single entry point for the TLS Bypass Rule Manager project.
It provides a menu-driven interface to launch different components
of the application.

Features:
- Launch CLI interface
- Launch GUI interface
- View project information
- Run tests
- View documentation
"""

import os
import sys
import subprocess
import json
from datetime import datetime


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Print the application header."""
    print("=" * 60)
    print("           TLS BYPASS RULE MANAGER - LAUNCHER")
    print("=" * 60)
    print("A professional tool for managing TLS bypass/exclusion rules")
    print("for authorized security testing environments.")
    print("=" * 60)


def show_menu():
    """Display the main menu."""
    print("\nSELECT AN OPTION:")
    print("1. Run CLI Interface")
    print("2. Run GUI Interface")
    print("3. View Project Information")
    print("4. View Documentation")
    print("5. Run Tests")
    print("6. View Help/Playbook")
    print("7. Version Control Check")
    print("8. Exit")
    print()


def view_project_info():
    """Display project information."""
    clear_screen()
    print_header()
    print("\nPROJECT INFORMATION")
    print("=" * 30)
    print("Name: TLS Bypass Rule Manager")
    print("Version: 2.0")
    print("Author: Security Tools Team")
    print("License: MIT")
    print(f"Current Directory: {os.getcwd()}")
    print(f"Python Version: {sys.version}")
    print("\nFEATURES:")
    print("• Rule Management (Host & Regex rules)")
    print("• Guided Rule Templates (No regex knowledge required)")
    print("• Regex Safety & Validation")
    print("• Dual Interface (CLI & GUI)")
    print("• Burp Suite Integration (Safe auto-sync)")
    print("• Export/Import Support (TXT, JSON, YAML)")
    print("• Conflict Detection")
    print("• Auto-backup Functionality")
    print("\nETHICS:")
    print("• Designed for authorized testing only")
    print("• No TLS bypass functionality")
    print("• Safe for public GitHub hosting")
    print("• For authorized security testing environments")


def view_documentation():
    """Display documentation options."""
    clear_screen()
    print_header()
    print("\nDOCUMENTATION")
    print("=" * 20)
    print("Available Documentation:")
    print("1. Rules Guide")
    print("2. Ethics Guidelines")
    print("3. Bug Hunter Guide")
    print("4. Back to Main Menu")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        show_doc_file("docs/RULES.md")
    elif choice == "2":
        show_doc_file("docs/ETHICS.md")
    elif choice == "3":
        show_doc_file("docs/BUG_HUNTER_GUIDE.md")
    elif choice == "4":
        return
    else:
        print("Invalid option.")


def show_doc_file(filepath):
    """Display content of a documentation file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        clear_screen()
        print_header()
        print(f"\n{filepath.upper()}")
        print("=" * 60)
        print(content)
        input("\nPress Enter to continue...")
    except FileNotFoundError:
        print(f"Documentation file not found: {filepath}")
        input("Press Enter to continue...")


def run_tests():
    """Run the test suite."""
    clear_screen()
    print_header()
    print("\nRUNNING TESTS")
    print("=" * 20)
    
    # Create a temporary test script to run all functionality tests
    test_script = '''
import sys
sys.path.append('src')

from rules import RuleManager, RuleTemplate
from exports import RuleExporterImporter

def run_functionality_tests():
    print("Running functionality tests...")
    
    # Test rule management
    rm = RuleManager('test_launch.txt')
    print("✓ RuleManager initialized")
    
    # Test adding rules
    rm.add_rule('example.com', 'host', True)
    rm.add_rule(r'.*\\.test\\.com', 'regex', True)
    print("✓ Rules added successfully")
    
    # Test getting all rules
    rules = rm.get_all_rules()
    print(f"✓ Retrieved {len(rules)} rules")
    
    # Test rule templates
    templates = RuleTemplate.get_templates()
    print(f"✓ Found {len(templates)} rule templates")
    
    # Test template generation
    pattern = RuleTemplate.generate_pattern('Match all subdomains', 'example.com')
    print(f"✓ Generated pattern: {pattern}")
    
    # Test export/import functionality
    exporter = RuleExporterImporter(rm)
    exported = exporter.export('json')
    print(f"✓ Exported to JSON, length: {len(exported)}")
    
    # Test Burp sync functionality
    burp_sync_exists = rm.update_burp_sync()
    print(f"✓ Burp sync updated: {burp_sync_exists}")
    
    # Clean up
    import os
    if os.path.exists('test_launch.txt'):
        os.remove('test_launch.txt')
    if os.path.exists('burp_tls_autosync.txt'):
        os.remove('burp_tls_autosync.txt')
    
    print("✓ All functionality tests passed")
    return True

if __name__ == "__main__":
    run_functionality_tests()
'''
    
    # Write test script to a temporary file and run it
    with open('temp_test.py', 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    try:
        result = subprocess.run([sys.executable, 'temp_test.py'], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
    except Exception as e:
        print(f"Error running tests: {e}")
    finally:
        # Clean up temp file
        if os.path.exists('temp_test.py'):
            os.remove('temp_test.py')
    
    input("\nPress Enter to continue...")


def view_help():
    """Display help information."""
    clear_screen()
    print_header()
    print("\nTLS BYPASS RULE MANAGER - HELP")
    print("=" * 40)
    print("""
WHAT IS THIS TOOL?
This tool manages TLS bypass rule files used for authorized
testing environments (example: Burp Suite exclusions).

It DOES NOT bypass TLS by itself.

TYPES OF ENTRIES
1) BLOCK HOST - Matches one exact hostname
   Example: example.com, api.dev.local
   Use when the domain is fixed and known.

2) BLOCK RULE (REGEX) - Pattern-based matching
   Useful for multiple hosts
   Examples: .*\\.internal\\.corp, ^dev-.*\\.example\\.com$

RULE TEMPLATES
The tool provides guided templates for common patterns:
- Match all subdomains
- Match specific prefix
- Match keyword anywhere
- Match IP-style hostname
- Custom regex

ETHICAL NOTICE
Only use TLS bypass rules on systems you own or are
explicitly authorized to test.
    """)
    input("Press Enter to continue...")


def check_git_remote():
    """Check the Git remote repository."""
    print("\nCHECKING GIT REMOTE REPOSITORY")
    print("=" * 35)
    
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("Git is not installed or not in PATH")
            input("Press Enter to continue...")
            return
        print(f"Git version: {result.stdout.strip()}")
    except FileNotFoundError:
        print("Git is not installed or not in PATH")
        input("Press Enter to continue...")
        return
    
    # Check if we're in a Git repository
    result = subprocess.run(["git", "status"], capture_output=True, text=True)
    in_repo = result.returncode == 0
    
    if not in_repo:
        print("Not in a Git repository")
        print("Initializing repository with remote...")
        
        # Initialize git repo and add the remote
        subprocess.run(["git", "init"], capture_output=True)
        subprocess.run(["git", "remote", "add", "origin", "https://github.com/RishuBurnwal/TLS-Bypass.git"], capture_output=True)
        print("Initialized new repository with remote: https://github.com/RishuBurnwal/TLS-Bypass.git")
    else:
        # Check current remote
        result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            print("Current remotes:")
            print(result.stdout)
        else:
            # Add the remote if none exists
            subprocess.run(["git", "remote", "add", "origin", "https://github.com/RishuBurnwal/TLS-Bypass.git"], capture_output=True)
            print("Added remote: https://github.com/RishuBurnwal/TLS-Bypass.git")
    
    # Show the configured remote
    result = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"\nRemote origin URL: {result.stdout.strip()}")
    else:
        print("\nNo remote origin configured")
    
    input("Press Enter to continue...")


def git_version_control():
    """Handle Git version control operations."""
    clear_screen()
    print_header()
    print("\nGIT VERSION CONTROL")
    print("=" * 30)
    
    # Check if Git is installed
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("Git is not installed or not in PATH")
            input("Press Enter to continue...")
            return
        print(f"Git version: {result.stdout.strip()}")
    except FileNotFoundError:
        print("Git is not installed or not in PATH")
        input("Press Enter to continue...")
        return
    
    # Check if we're in a Git repository
    result = subprocess.run(["git", "status"], capture_output=True, text=True)
    in_repo = result.returncode == 0
    
    while True:
        print("\nGIT OPTIONS:")
        print("1. Check Repository Status")
        print("2. Show Current Branch")
        print("3. Show Recent Commits")
        print("4. Check for Updates (git fetch)")
        print("5. Pull Latest Changes (git pull)")
        print("6. Show Project Version")
        print("7. Check/Update Rule File Version")
        print("8. Undo/Restore Previous Versions")
        print("9. Reset Files to Default")
        print("10. Check Git Remote Repository")
        print("11. Back to Main Menu")
        
        choice = input("\nSelect option (1-11): ").strip()
        
        if choice == "1":
            if in_repo:
                result = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
                if result.stdout.strip():
                    print("\nUncommitted changes:")
                    print(result.stdout)
                else:
                    print("\nWorking directory is clean")
            else:
                print("\nNot in a Git repository")
        
        elif choice == "2":
            if in_repo:
                result = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
                print(f"\nCurrent branch: {result.stdout.strip()}")
            else:
                print("\nNot in a Git repository")
        
        elif choice == "3":
            if in_repo:
                result = subprocess.run(["git", "log", "--oneline", "-10"], capture_output=True, text=True)
                print("\nRecent commits:")
                print(result.stdout if result.stdout.strip() else "No commits found")
            else:
                print("\nNot in a Git repository")
        
        elif choice == "4":
            if in_repo:
                print("\nFetching updates...")
                result = subprocess.run(["git", "fetch"], capture_output=True, text=True)
                if result.returncode == 0:
                    print("Fetched updates successfully")
                    # Show if there are updates available
                    local_result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
                    remote_result = subprocess.run(["git", "rev-parse", "@{u}"], capture_output=True, text=True)
                    
                    if local_result.stdout.strip() != remote_result.stdout.strip():
                        print("Updates are available!")
                        print(f"Local:  {local_result.stdout.strip()[:8]}")
                        print(f"Remote: {remote_result.stdout.strip()[:8]}")
                    else:
                        print("Repository is up to date")
                else:
                    print(f"Error fetching: {result.stderr}")
            else:
                print("\nNot in a Git repository")
        
        elif choice == "5":
            if in_repo:
                confirm = input("\nThis will pull the latest changes. Continue? (y/N): ").strip().lower()
                if confirm in ['y', 'yes']:
                    print("\nPulling latest changes...")
                    result = subprocess.run(["git", "pull"], capture_output=True, text=True)
                    if result.returncode == 0:
                        print("Pulled updates successfully")
                        print(result.stdout)
                    else:
                        print(f"Error pulling: {result.stderr}")
                else:
                    print("Pull operation cancelled")
            else:
                print("\nNot in a Git repository")
        
        elif choice == "6":
            # Show project version
            print(f"\nProject Version: 2.0")
            print(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            if in_repo:
                result = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"Git Commit: {result.stdout.strip()}")
        
        elif choice == "7":
            # Automatically update rule file version and timestamp
            auto_update_rule_file_version()
        
        elif choice == "8":
            # Undo/Restore previous versions
            undo_restore_versions()
        
        elif choice == "9":
            # Reset files to default
            reset_files_to_default()
        
        elif choice == "10":
            # Check Git remote repository
            check_git_remote()
        
        elif choice == "11":
            break
        
        else:
            print("Invalid option")
        
        input("\nPress Enter to continue...")


def auto_update_rule_file_version():
    """Automatically update the version and last updated information in the rule file."""
    print("\nAUTOMATICALLY UPDATING RULE FILE VERSION")
    print("=" * 45)
    
    rule_file = "tls_bypass_rule.txt"
    
    # Create backup before modification
    if os.path.exists(rule_file):
        import shutil
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f"tls_bypass_rule_backup_{timestamp}.txt"
        shutil.copy2(rule_file, backup_file)
        print(f"Backup created: {backup_file}")
        
        # Clean up old backups, keeping only the 10 most recent
        cleanup_old_backups()
    
    # Check if rule file exists
    if not os.path.exists(rule_file):
        print(f"Rule file '{rule_file}' does not exist. Creating with default content...")
        create_default_rule_file(rule_file)
    
    # Read the current rule file
    try:
        with open(rule_file, 'r', encoding="utf-8") as f:
            lines = f.readlines()
        
        # Find version and last updated information
        version_line = None
        last_updated_line = None
        
        for i, line in enumerate(lines):
            if line.startswith("# Version:"):
                version_line = i
            elif line.startswith("# Last Updated:"):
                last_updated_line = i
        
        # Automatically update both version and timestamp
        new_version = "2.0"
        new_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Update version line
        if version_line is not None:
            lines[version_line] = f"# Version: {new_version}\n"
            print(f"Version updated to {new_version}")
        else:
            # Insert after the first line if no version line exists
            lines.insert(1, f"# Version: {new_version}\n")
            print(f"Version added: {new_version}")
        
        # Update last updated line
        if last_updated_line is not None:
            lines[last_updated_line] = f"# Last Updated: {new_timestamp}\n"
            print(f"Last updated timestamp updated to {new_timestamp}")
        else:
            # Insert after the version line
            insert_pos = version_line + 1 if version_line is not None else 2
            if len(lines) >= insert_pos:
                lines.insert(insert_pos, f"# Last Updated: {new_timestamp}\n")
            else:
                lines.append(f"# Last Updated: {new_timestamp}\n")
            print(f"Last updated timestamp added: {new_timestamp}")
        
        # Write back to file
        with open(rule_file, 'w', encoding="utf-8") as f:
            f.writelines(lines)
        
        print(f"\nRule file '{rule_file}' updated successfully")
        print(f"New version: {new_version}")
        print(f"New timestamp: {new_timestamp}")
        
    except Exception as e:
        print(f"Error reading or updating rule file: {e}")


def create_default_rule_file(rule_file):
    """Create a default rule file with version information."""
    with open(rule_file, 'w', encoding="utf-8") as f:
        f.write(
            "# TLS BYPASS RULE\n"
            "# Version: 2.0\n"
            f"# Last Updated: {datetime.now()}\n"
            "# For authorized security testing only\n\n"
            "[BLOCK_HOSTS]\n\n"
            "[BLOCK_RULES]\n"
        )


def get_backup_files():
    """Get list of backup files for the rule file, up to 10 most recent."""
    import glob
    backup_pattern = "tls_bypass_rule_backup_*.txt"
    backup_files = glob.glob(backup_pattern)
    
    # Sort by modification time, newest first
    backup_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    
    # Return up to 10 most recent backups
    return backup_files[:10]


def cleanup_old_backups():
    """Clean up old backup files, keeping only the 10 most recent."""
    backups = get_backup_files()
    if len(backups) > 10:
        for backup in backups[10:]:
            os.remove(backup)
            print(f"Removed old backup: {backup}")


def undo_restore_versions():
    """Allow user to undo to a previous version with selection option."""
    print("\nUNDO/RESTORE PREVIOUS VERSIONS")
    print("=" * 35)
    
    # Get list of backup files
    backups = get_backup_files()
    
    if not backups:
        print("No backup files found.\n")
        print("Note: Backups are created automatically before each modification.")
        return
    
    print(f"Found {len(backups)} backup file(s):")
    print("\nSELECT A VERSION TO RESTORE:")
    
    for i, backup in enumerate(backups, 1):
        # Extract timestamp from filename
        import re
        match = re.search(r'tls_bypass_rule_backup_(\d{8}_\d{6})', backup)
        if match:
            timestamp = match.group(1)
            # Format timestamp nicely
            formatted_time = f"{timestamp[:4]}-{timestamp[4:6]}-{timestamp[6:8]} {timestamp[9:11]}:{timestamp[11:13]}:{timestamp[13:15]}"
        else:
            formatted_time = "Unknown"
        
        # Get file size
        size = os.path.getsize(backup)
        print(f"{i}. {backup} (Created: {formatted_time}, Size: {size} bytes)")
    
    print(f"{len(backups) + 1}. Cancel")
    
    try:
        choice = int(input(f"\nSelect version to restore (1-{len(backups) + 1}): ").strip())
        
        if 1 <= choice <= len(backups):
            selected_backup = backups[choice - 1]
            
            # Confirm restoration
            confirm = input(f"\nRestore from '{selected_backup}'? This will overwrite the current rule file. (y/N): ").strip().lower()
            if confirm in ['y', 'yes']:
                # Copy backup to main rule file
                import shutil
                shutil.copy2(selected_backup, "tls_bypass_rule.txt")
                print(f"\nSuccessfully restored from '{selected_backup}'")
                print("Rule file has been reverted to previous version.")
            else:
                print("Restore operation cancelled.")
        elif choice == len(backups) + 1:
            print("Operation cancelled.")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    except Exception as e:
        print(f"Error during restore: {e}")


def reset_files_to_default():
    """Reset all files to default state."""
    print("\nRESET FILES TO DEFAULT")
    print("=" * 25)
    
    confirm = input("\nThis will reset the rule file to default. All current rules will be lost. Continue? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Reset operation cancelled.")
        return
    
    # Create default rule file
    create_default_rule_file("tls_bypass_rule.txt")
    print("\nRule file has been reset to default.")
    
    # Also reset burp sync file
    if os.path.exists("burp_tls_autosync.txt"):
        os.remove("burp_tls_autosync.txt")
        print("Burp sync file has been removed.")
    
    print("\nAll files have been reset to default state.")


def run_cli():
    """Run the CLI interface."""
    print("Starting CLI Interface...")
    try:
        # Import and run the CLI
        sys.path.append('src')
        from cli import CLIRuleManager
        app = CLIRuleManager()
        app.run()
    except ImportError as e:
        print(f"Error importing CLI: {e}")
        print("Make sure all dependencies are installed (run: pip install -r requirements.txt)")
    except Exception as e:
        print(f"Error running CLI: {e}")


def run_gui():
    """Run the GUI interface."""
    print("Starting GUI Interface...")
    try:
        # Import and run the GUI
        sys.path.append('src')
        from gui import TLSBypassRuleGUI
        app = TLSBypassRuleGUI()
        app.run()
    except ImportError as e:
        print(f"Error importing GUI: {e}")
        print("Make sure all dependencies are installed (run: pip install -r requirements.txt)")
    except Exception as e:
        print(f"Error running GUI: {e}")


def main():
    """Main function to run the launcher."""
    while True:
        clear_screen()
        print_header()
        show_menu()
        
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == "1":
            run_cli()
        elif choice == "2":
            run_gui()
        elif choice == "3":
            view_project_info()
        elif choice == "4":
            view_documentation()
        elif choice == "5":
            run_tests()
        elif choice == "6":
            view_help()
        elif choice == "7":
            git_version_control()
        elif choice == "8":
            print("\nThank you for using TLS Bypass Rule Manager!")
            print("Remember: Use only for authorized testing.")
            break
        else:
            print("Invalid option. Please select 1-8.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()