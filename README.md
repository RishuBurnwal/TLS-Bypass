# 🛡️ TLS Bypass Manager for BurpSuite

> A professional, open-source tool for managing TLS bypass/exclusion rules for authorized security testing environments. This tool helps security professionals and bug bounty hunters manage rule files for tools like Burp Suite, without bypassing TLS or intercepting traffic directly.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Made%20with-Python-3776ab.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Cross--Platform-green.svg)](https://en.wikipedia.org/wiki/Cross-platform_software)

## ⚠️ Important Notice

> ⚠️ **CRITICAL**: This tool does NOT bypass TLS, intercept traffic, or modify any security controls. It only manages rule files that users may manually import into tools like Burp Suite, with proper authorization.

## 🎯 Features

- ✅ **Rule Management**: Manage both exact host blocking and regex-based rules
- ✅ **Guided Rule Builder**: No regex expertise required - templates for common use cases
- ✅ **Regex Safety**: Validation and testing before saving rules
- ✅ **Dual Interface**: Both CLI and GUI modes available
- ✅ **Burp Suite Integration**: Safe auto-sync file generation
- ✅ **Export/Import**: Support for multiple formats (TXT, JSON, YAML)
- ✅ **Cross-Platform**: Works on Windows, Linux, and macOS
- ✅ **File Version Control**: Automatic backup and restore functionality
- ✅ **Undo/Redo**: Up to 10 previous versions maintained
- ✅ **Awesome Banner**: CyberScorpion-themed startup banner with loading animation

## 🛠️ Installation

```bash
git clone https://github.com/RishuBurnwal/TLS-Bypass.git
cd TLS-Bypass
cd tls-bypass-rule-manager
pip install -r requirements.txt
```

## 🚀 Usage

### Launch the Application
```bash
# Run the unified launcher
python launcher.py
```

### CLI Mode
```bash
python src/cli.py
```

### GUI Mode
```bash
python src/gui.py
```

## 📋 Rule Types

### Host Rules
Exact hostname matching:
```
example.com
api.dev.local
```

### Regex Rules
Pattern-based matching:
```
.*\.internal\.corp
^dev-.*\.example\.com$
.*staging.*
```

## 🧩 Rule Templates

The tool provides guided templates for:
- Match all subdomains
- Match specific prefix
- Match keyword anywhere
- Match IP-style hostname
- Custom regex

## 📊 Interactive Menu Options

### Main Menu
```
SELECT AN OPTION:
1. Run CLI Interface
2. Run GUI Interface
3. View Project Information
4. View Documentation
5. Run Tests
6. View Help/Playbook
7. File Backup/Restore
8. Exit
```

### File Backup/Restore Menu
```
FILE BACKUP/RESTORE OPTIONS:
1. Show Rule File Info
2. Restore Previous Version
3. Reset Files to Default
4. Back to Main Menu
```

## 🛡️ Ethics & Safety

- Designed for authorized testing only
- No network activity or traffic interception
- Clear ethical guidelines included
- Safe for public GitHub hosting
- No actual TLS bypass functionality

## 📁 Project Structure

```
tls-bypass-rule-manager/
├── launcher.py         # Unified launcher with option-wise menu
├── src/
│   ├── cli.py          # Command-line interface
│   ├── gui.py          # Graphical user interface
│   ├── rules.py        # Rule management logic
│   ├── exports.py      # Export/import functionality
│   └── utils.py        # Utility functions
├── backups/            # Automatic rule backups
├── docs/               # Documentation
│   ├── RULES.md        # Rule management guide
│   ├── ETHICS.md       # Ethical guidelines
│   └── BUG_HUNTER_GUIDE.md # Bug hunter specific guide
├── README.md
├── LICENSE
└── requirements.txt
```

## 🤝 Contributing

Contributions are welcome! Please read the contributing guidelines before submitting a pull request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📖 Usage Examples

### CLI Mode
```bash
# Run the CLI interface
python src/cli.py

# The CLI provides a menu-driven interface for:
# - Adding, removing, and toggling rules
# - Using guided rule templates
# - Testing regex patterns
# - Exporting/importing rules
# - Checking for conflicts
```

### GUI Mode
```bash
# Run the GUI interface
python src/gui.py

# The GUI provides:
# - Visual rule management
# - Guided rule builder
# - Regex testing tools
# - Export/import functionality
# - Conflict detection
```

### Quick Start Example
```python
from src.rules import RuleManager

# Initialize the rule manager
rule_manager = RuleManager()

# Add a host rule
rule_manager.add_rule("example.com", "host", enabled=True)

# Add a regex rule
rule_manager.add_rule(r".*\.internal\.corp", "regex", enabled=True)

# Toggle a rule
rule_manager.toggle_rule("example.com")

# Check for conflicts
conflicts = rule_manager.find_rule_conflicts()
print(f"Found {len(conflicts)} potential conflicts")
```

### Burp Suite Integration
The tool automatically creates a `burp_tls_autosync.txt` file containing only enabled rules. Simply import this file into Burp Suite's TLS settings when needed.

## 📞 Contact & Support

- **Author**: Rishu Burnwal
- **LinkedIn**: [RishuBurnwal](https://linkedin.com/in/rishuburnwal)
- **GitHub**: [RishuBurnwal](https://github.com/rishuburnwal)
- **Repository**: [https://github.com/rishuBurnwal/TLS-Bypass](https://github.com/rishuBurnwal/TLS-Bypass)

## 📄 License

MIT License - see the LICENSE file for details.

## 🚀 Deployment

Ready for GitHub upload at: [https://github.com/rishuBurnwal/TLS-Bypass](https://github.com/rishuBurnwal/TLS-Bypass)