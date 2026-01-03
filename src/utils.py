import os
import re
import json
import yaml
from datetime import datetime
from typing import Any, Dict, List, Optional
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


class ColorPrinter:
    """Utility class for colored console output."""
    
    @staticmethod
    def success(message: str):
        print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {message}")
    
    @staticmethod
    def error(message: str):
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {message}")
    
    @staticmethod
    def warning(message: str):
        print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} {message}")
    
    @staticmethod
    def info(message: str):
        print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {message}")
    
    @staticmethod
    def highlight(message: str):
        print(f"{Fore.MAGENTA}{message}{Style.RESET_ALL}")
    
    @staticmethod
    def bold(message: str):
        print(f"{Style.BRIGHT}{message}{Style.RESET_ALL}")


def validate_hostname(hostname: str) -> bool:
    """Validate if a string is a valid hostname."""
    if len(hostname) > 253:
        return False
    
    # Check each label (separated by dots)
    labels = hostname.split('.')
    
    for label in labels:
        if not label or len(label) > 63:
            return False
        
        # Check if label starts or ends with hyphen
        if label.startswith('-') or label.endswith('-'):
            return False
        
        # Check if label contains only allowed characters
        if not re.match(r'^[a-zA-Z0-9-]+$', label):
            return False
    
    return True


def is_valid_regex(pattern: str) -> bool:
    """Check if a pattern is a valid regex."""
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False


def safe_regex_test(pattern: str, test_string: str) -> Optional[bool]:
    """Safely test a regex pattern against a string."""
    try:
        return bool(re.search(pattern, test_string))
    except re.error:
        return None


def format_rule_display(rule: Dict) -> str:
    """Format a rule for display purposes."""
    status = "ENABLED" if rule["enabled"] else "DISABLED"
    return f"[{status}] {rule['type'].upper()}: {rule['pattern']}"


def get_file_size(file_path: str) -> str:
    """Get human-readable file size."""
    if not os.path.exists(file_path):
        return "0 B"
    
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"


def create_safe_filename(base_name: str) -> str:
    """Create a safe filename by removing dangerous characters."""
    # Remove or replace dangerous characters
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', base_name)
    # Limit length to avoid filesystem issues
    return safe_name[:200]


def generate_export_filename(export_type: str) -> str:
    """Generate a filename for exports."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = f"tls_rules_export_{timestamp}.{export_type.lower()}"
    return create_safe_filename(safe_name)


def check_file_permissions(file_path: str) -> Dict[str, bool]:
    """Check read/write permissions for a file."""
    return {
        "readable": os.access(file_path, os.R_OK),
        "writable": os.access(file_path, os.W_OK),
        "executable": os.access(file_path, os.X_OK)
    }


def normalize_path(path: str) -> str:
    """Normalize a file path."""
    return os.path.normpath(os.path.abspath(path))


def validate_export_format(format_type: str) -> bool:
    """Validate if the export format is supported."""
    supported_formats = ["txt", "json", "yaml", "burp"]
    return format_type.lower() in supported_formats


def calculate_similarity(str1: str, str2: str) -> float:
    """Calculate similarity between two strings (0.0 to 1.0)."""
    if not str1 and not str2:
        return 1.0
    if not str1 or not str2:
        return 0.0
    
    # Simple character-based similarity
    common_chars = sum(min(str1.count(c), str2.count(c)) for c in set(str1 + str2))
    total_chars = len(str1) + len(str2)
    
    return (2 * common_chars) / total_chars if total_chars > 0 else 0.0


def format_timestamp(dt: datetime) -> str:
    """Format a datetime object to a readable string."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to a maximum length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def escape_for_regex(text: str) -> str:
    """Escape special characters in text for use in regex."""
    return re.escape(text)


class ProgressBar:
    """Simple progress bar for CLI operations."""
    
    def __init__(self, total: int, width: int = 50):
        self.total = total
        self.width = width
        self.current = 0
    
    def update(self, value: int = 1):
        """Update progress bar."""
        self.current += value
        percent = self.current / self.total
        filled = int(self.width * percent)
        bar = "█" * filled + "░" * (self.width - filled)
        print(f"\r|{bar}| {percent:.1%}", end="", flush=True)
    
    def finish(self):
        """Complete the progress bar."""
        print()  # New line when done