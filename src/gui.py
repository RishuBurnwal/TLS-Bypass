import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import os
import sys
from typing import Optional

# Add the project root to the Python path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from rules import RuleManager, RuleTemplate
from exports import RuleExporterImporter


class TLSBypassRuleGUI:
    """Graphical user interface for the TLS Bypass Rule Manager."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TLS Bypass Rule Manager")
        self.root.geometry("900x700")
        
        # Initialize managers
        self.rule_manager = RuleManager()
        self.exporter_importer = RuleExporterImporter(self.rule_manager)
        
        # Create the GUI
        self.create_widgets()
        self.refresh_rules()
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="TLS Bypass Rule Manager", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Stats frame
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding="5")
        stats_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.stats_label = ttk.Label(stats_frame, text="")
        self.stats_label.grid(row=0, column=0, sticky=(tk.W,))
        
        # Rules list
        list_frame = ttk.LabelFrame(main_frame, text="Rules", padding="5")
        list_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Create treeview with scrollbars
        columns = ("#", "Status", "Type", "Pattern")
        self.rules_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Define headings
        self.rules_tree.heading("#", text="#")
        self.rules_tree.heading("Status", text="Status")
        self.rules_tree.heading("Type", text="Type")
        self.rules_tree.heading("Pattern", text="Pattern")
        
        # Define column widths
        self.rules_tree.column("#", width=40)
        self.rules_tree.column("Status", width=80)
        self.rules_tree.column("Type", width=80)
        self.rules_tree.column("Pattern", width=400)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.rules_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient="horizontal", command=self.rules_tree.xview)
        self.rules_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid the treeview and scrollbars
        self.rules_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=2, sticky=(tk.N, tk.W), padx=(0, 10))
        
        # Rule management buttons
        ttk.Button(buttons_frame, text="Add Rule", command=self.add_rule_dialog).pack(fill=tk.X, pady=2)
        ttk.Button(buttons_frame, text="Toggle Rule", command=self.toggle_rule).pack(fill=tk.X, pady=2)
        ttk.Button(buttons_frame, text="Remove Rule", command=self.remove_rule).pack(fill=tk.X, pady=2)
        ttk.Button(buttons_frame, text="Guided Rule Builder", command=self.guided_rule_builder).pack(fill=tk.X, pady=2)
        ttk.Button(buttons_frame, text="Regex Tester", command=self.regex_tester).pack(fill=tk.X, pady=2)
        ttk.Button(buttons_frame, text="Check Conflicts", command=self.check_conflicts).pack(fill=tk.X, pady=2)
        ttk.Button(buttons_frame, text="Refresh", command=self.refresh_rules).pack(fill=tk.X, pady=2)
        
        # Export/Import frame
        export_frame = ttk.LabelFrame(main_frame, text="Export/Import", padding="5")
        export_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(export_frame, text="Export Rules", command=self.export_rules).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(export_frame, text="Import Rules", command=self.import_rules).pack(side=tk.LEFT, padx=(0, 5))
        
        # Help button
        help_button = ttk.Button(main_frame, text="Help", command=self.show_help)
        help_button.grid(row=4, column=0, columnspan=3, pady=(10, 0))
    
    def refresh_rules(self):
        """Refresh the rules list."""
        # Clear existing items
        for item in self.rules_tree.get_children():
            self.rules_tree.delete(item)
        
        # Get all rules
        all_rules = self.rule_manager.get_all_rules()
        
        # Insert rules into the treeview
        for i, rule in enumerate(all_rules, 1):
            status = "ENABLED" if rule["enabled"] else "DISABLED"
            self.rules_tree.insert("", "end", values=(i, status, rule["type"].upper(), rule["pattern"]))
        
        # Update stats
        stats = self.rule_manager.get_rule_stats()
        stats_text = (f"Total: {stats['total_all']} | "
                     f"Enabled: {stats['enabled']} | "
                     f"Disabled: {stats['disabled']} | "
                     f"Hosts: {stats['total_hosts']} | "
                     f"Regex: {stats['total_rules']}")
        self.stats_label.config(text=stats_text)
    
    def add_rule_dialog(self):
        """Dialog for adding a new rule."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Rule")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx()+50, self.root.winfo_rooty()+50))
        
        # Rule type
        ttk.Label(dialog, text="Rule Type:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        rule_type = tk.StringVar(value="regex")
        ttk.Radiobutton(dialog, text="Host (exact match)", variable=rule_type, value="host").grid(row=1, column=0, sticky=tk.W, padx=20, pady=2)
        ttk.Radiobutton(dialog, text="Regex (pattern match)", variable=rule_type, value="regex").grid(row=2, column=0, sticky=tk.W, padx=20, pady=2)
        
        # Pattern
        ttk.Label(dialog, text="Pattern:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        pattern_var = tk.StringVar()
        pattern_entry = ttk.Entry(dialog, textvariable=pattern_var, width=50)
        pattern_entry.grid(row=4, column=0, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        # Enabled status
        enabled_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(dialog, text="Enabled", variable=enabled_var).grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        
        # Validate and test buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=6, column=0, pady=10)
        
        def validate_regex():
            pattern = pattern_var.get()
            if rule_type.get() == "regex":
                is_valid, error_msg = self.rule_manager.validate_regex(pattern)
                if is_valid:
                    messagebox.showinfo("Validation", "Regex is valid!")
                else:
                    messagebox.showerror("Validation", f"Invalid regex: {error_msg}")
        
        def test_regex():
            pattern = pattern_var.get()
            if rule_type.get() == "regex":
                test_input = simpledialog.askstring("Test Regex", "Enter test string:")
                if test_input:
                    matches = self.rule_manager.test_regex(pattern, test_input)
                    if matches:
                        messagebox.showinfo("Test Result", f"Pattern matches: {test_input}")
                    else:
                        messagebox.showinfo("Test Result", f"Pattern does not match: {test_input}")
        
        ttk.Button(button_frame, text="Validate Regex", command=validate_regex).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Test Regex", command=test_regex).pack(side=tk.LEFT, padx=5)
        
        # OK and Cancel buttons
        def add_rule():
            pattern = pattern_var.get().strip()
            if not pattern:
                messagebox.showerror("Error", "Pattern cannot be empty")
                return
            
            if rule_type.get() == "regex":
                is_valid, error_msg = self.rule_manager.validate_regex(pattern)
                if not is_valid:
                    messagebox.showerror("Error", f"Invalid regex: {error_msg}")
                    return
            
            if self.rule_manager.add_rule(pattern, rule_type.get(), enabled_var.get()):
                messagebox.showinfo("Success", f"Rule added: {pattern}")
                dialog.destroy()
                self.refresh_rules()
            else:
                messagebox.showerror("Error", "Failed to add rule")
        
        ttk.Button(button_frame, text="OK", command=add_rule).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Configure column weight
        dialog.columnconfigure(0, weight=1)
    
    def toggle_rule(self):
        """Toggle the selected rule's status."""
        selected = self.rules_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a rule to toggle")
            return
        
        item = self.rules_tree.item(selected[0])
        values = item['values']
        pattern = values[3]  # Pattern is in the 4th column
        
        if self.rule_manager.toggle_rule(pattern):
            messagebox.showinfo("Success", f"Toggled rule: {pattern}")
            self.refresh_rules()
        else:
            messagebox.showerror("Error", "Failed to toggle rule")
    
    def remove_rule(self):
        """Remove the selected rule."""
        selected = self.rules_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a rule to remove")
            return
        
        item = self.rules_tree.item(selected[0])
        values = item['values']
        pattern = values[3]  # Pattern is in the 4th column
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to remove rule: {pattern}?"):
            if self.rule_manager.remove_rule(pattern):
                messagebox.showinfo("Success", f"Removed rule: {pattern}")
                self.refresh_rules()
            else:
                messagebox.showerror("Error", "Failed to remove rule")
    
    def guided_rule_builder(self):
        """Guided rule builder dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Guided Rule Builder")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx()+50, self.root.winfo_rooty()+50))
        
        # Template selection
        ttk.Label(dialog, text="Select Rule Template:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        template_var = tk.StringVar()
        templates = RuleTemplate.get_templates()
        template_names = [t['name'] for t in templates]
        
        template_combo = ttk.Combobox(dialog, textvariable=template_var, values=template_names, state="readonly", width=50)
        template_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        template_combo.bind("<<ComboboxSelected>>", lambda e: update_template_info())
        
        # Template info frame
        info_frame = ttk.LabelFrame(dialog, text="Template Info", padding="5")
        info_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        description_label = ttk.Label(info_frame, text="", wraplength=550)
        description_label.grid(row=0, column=0, sticky=tk.W)
        
        usage_label = ttk.Label(info_frame, text="", wraplength=550)
        usage_label.grid(row=1, column=0, sticky=tk.W)
        
        preview_label = ttk.Label(info_frame, text="", wraplength=550, font=("Consolas", 10))
        preview_label.grid(row=2, column=0, sticky=tk.W)
        
        def update_template_info():
            selected_template_name = template_var.get()
            for template in templates:
                if template['name'] == selected_template_name:
                    description_label.config(text=f"Description: {template['description']}")
                    usage_label.config(text=f"Usage: {template['usage']}")
                    preview_label.config(text=f"Preview: {template['preview']}")
                    break
        
        # User input
        input_frame = ttk.LabelFrame(dialog, text="User Input", padding="5")
        input_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        input_label = ttk.Label(input_frame, text="Input (if required):")
        input_label.grid(row=0, column=0, sticky=tk.W)
        
        input_var = tk.StringVar()
        input_entry = ttk.Entry(input_frame, textvariable=input_var, width=50)
        input_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Generated pattern
        pattern_frame = ttk.LabelFrame(dialog, text="Generated Pattern", padding="5")
        pattern_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        pattern_var = tk.StringVar()
        pattern_entry = ttk.Entry(pattern_frame, textvariable=pattern_var, width=50, state="readonly")
        pattern_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        def generate_pattern():
            selected_template_name = template_var.get()
            if not selected_template_name:
                return
            
            user_input = input_var.get()
            
            # Handle special cases
            if selected_template_name == "Match IP-style hostname":
                # No user input needed
                pattern = RuleTemplate.generate_pattern(selected_template_name, "")
            else:
                pattern = RuleTemplate.generate_pattern(selected_template_name, user_input)
            
            pattern_var.set(pattern)
            
            # Validate the pattern
            if pattern:
                is_valid, error_msg = self.rule_manager.validate_regex(pattern)
                if not is_valid:
                    messagebox.showerror("Validation Error", f"Generated pattern is invalid: {error_msg}")
        
        ttk.Button(input_frame, text="Generate Pattern", command=generate_pattern).grid(row=1, column=1)
        
        # Test frame
        test_frame = ttk.LabelFrame(dialog, text="Test Generated Pattern", padding="5")
        test_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        test_input_var = tk.StringVar()
        ttk.Label(test_frame, text="Test String:").grid(row=0, column=0, sticky=tk.W)
        test_entry = ttk.Entry(test_frame, textvariable=test_input_var, width=50)
        test_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        def test_pattern():
            pattern = pattern_var.get()
            test_string = test_input_var.get()
            
            if not pattern or not test_string:
                messagebox.showwarning("Warning", "Both pattern and test string are required")
                return
            
            matches = self.rule_manager.test_regex(pattern, test_string)
            if matches:
                messagebox.showinfo("Test Result", f"Pattern matches: {test_string}")
            else:
                messagebox.showinfo("Test Result", f"Pattern does not match: {test_string}")
        
        ttk.Button(test_frame, text="Test Pattern", command=test_pattern).grid(row=1, column=1)
        
        # Add rule button
        def add_generated_rule():
            pattern = pattern_var.get()
            if not pattern:
                messagebox.showerror("Error", "No pattern generated")
                return
            
            # Validate the pattern
            is_valid, error_msg = self.rule_manager.validate_regex(pattern)
            if not is_valid:
                messagebox.showerror("Error", f"Invalid pattern: {error_msg}")
                return
            
            if self.rule_manager.add_rule(pattern, "regex", True):
                messagebox.showinfo("Success", f"Rule added: {pattern}")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to add rule")
        
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=6, column=0, pady=10)
        
        ttk.Button(button_frame, text="Add Rule", command=add_generated_rule).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Configure column weights
        dialog.columnconfigure(0, weight=1)
        info_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(0, weight=1)
        pattern_frame.columnconfigure(0, weight=1)
        test_frame.columnconfigure(0, weight=1)
    
    def regex_tester(self):
        """Regex tester dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Regex Tester")
        dialog.geometry("500x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx()+50, self.root.winfo_rooty()+50))
        
        # Pattern input
        ttk.Label(dialog, text="Regex Pattern:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        pattern_var = tk.StringVar()
        pattern_entry = ttk.Entry(dialog, textvariable=pattern_var, width=60)
        pattern_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        # Test string input
        ttk.Label(dialog, text="Test String:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        test_var = tk.StringVar()
        test_entry = ttk.Entry(dialog, textvariable=test_var, width=60)
        test_entry.grid(row=3, column=0, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        # Result label
        result_var = tk.StringVar(value="Result will appear here")
        result_label = ttk.Label(dialog, textvariable=result_var, font=("Arial", 10, "bold"))
        result_label.grid(row=4, column=0, pady=10)
        
        def test_regex():
            pattern = pattern_var.get()
            test_string = test_var.get()
            
            if not pattern or not test_string:
                result_var.set("Both pattern and test string are required")
                return
            
            # Validate regex
            is_valid, error_msg = self.rule_manager.validate_regex(pattern)
            if not is_valid:
                result_var.set(f"Invalid regex: {error_msg}")
                return
            
            # Test the pattern
            matches = self.rule_manager.test_regex(pattern, test_string)
            if matches is None:
                result_var.set("Error testing regex")
            elif matches:
                result_var.set(f"MATCH: '{test_string}' matches pattern '{pattern}'")
            else:
                result_var.set(f"NO MATCH: '{test_string}' does not match pattern '{pattern}'")
        
        ttk.Button(dialog, text="Test Regex", command=test_regex).grid(row=5, column=0, pady=10)
        
        ttk.Button(dialog, text="Close", command=dialog.destroy).grid(row=6, column=0, pady=5)
        
        # Configure column weight
        dialog.columnconfigure(0, weight=1)
    
    def check_conflicts(self):
        """Check for rule conflicts."""
        conflicts = self.rule_manager.find_rule_conflicts()
        
        if not conflicts:
            messagebox.showinfo("Conflicts", "No conflicts found between rules.")
            return
        
        # Create conflicts dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Rule Conflicts")
        dialog.geometry("600x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx()+50, self.root.winfo_rooty()+50))
        
        ttk.Label(dialog, text="Potential Rule Conflicts:", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Create treeview for conflicts
        columns = ("Rule 1", "Rule 2", "Test String", "Type")
        conflicts_tree = ttk.Treeview(dialog, columns=columns, show="headings", height=10)
        
        for col in columns:
            conflicts_tree.heading(col, text=col)
            conflicts_tree.column(col, width=140)
        
        # Add conflicts to treeview
        for conflict in conflicts:
            conflicts_tree.insert("", "end", values=(
                conflict['rule1'],
                conflict['rule2'], 
                conflict['test_string'],
                conflict['type']
            ))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=conflicts_tree.yview)
        conflicts_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        conflicts_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=5)
    
    def export_rules(self):
        """Export rules to a file."""
        filetypes = [
            ("Text files", "*.txt"),
            ("JSON files", "*.json"),
            ("YAML files", "*.yaml"),
            ("Burp files", "*.txt"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.asksaveasfilename(
            title="Export Rules",
            filetypes=filetypes,
            defaultextension=".txt"
        )
        
        if not filename:
            return
        
        # Determine format from file extension
        if filename.endswith('.json'):
            format_type = 'json'
        elif filename.endswith('.yaml') or filename.endswith('.yml'):
            format_type = 'yaml'
        elif 'burp' in filename.lower():
            format_type = 'burp'
        else:
            format_type = 'txt'
        
        try:
            exported_content = self.exporter_importer.export(format_type)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(exported_content)
            
            messagebox.showinfo("Success", f"Rules exported to: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def import_rules(self):
        """Import rules from a file."""
        filetypes = [
            ("Text files", "*.txt"),
            ("JSON files", "*.json"),
            ("YAML files", "*.yaml"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Import Rules",
            filetypes=filetypes
        )
        
        if not filename:
            return
        
        # Determine format from file extension
        if filename.endswith('.json'):
            format_type = 'json'
        elif filename.endswith('.yaml') or filename.endswith('.yml'):
            format_type = 'yaml'
        else:
            format_type = 'txt'
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if self.exporter_importer.import_rules(format_type, content):
                messagebox.showinfo("Success", f"Rules imported from: {filename}")
                self.refresh_rules()
            else:
                messagebox.showerror("Error", "Import failed. Invalid format or content.")
        except Exception as e:
            messagebox.showerror("Error", f"Import failed: {str(e)}")
    
    def show_help(self):
        """Show help dialog."""
        help_text = """
TLS BYPASS RULE MANAGER - HELP

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
        """
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Help")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx()+50, self.root.winfo_rooty()+50))
        
        # Text widget with scrollbar
        text_frame = ttk.Frame(dialog)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Consolas", 10))
        text_widget.insert(tk.END, help_text.strip())
        text_widget.config(state=tk.DISABLED)  # Make read-only
        
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)
    
    def run(self):
        """Run the GUI application."""
        self.root.mainloop()


def main():
    """Main entry point."""
    app = TLSBypassRuleGUI()
    app.run()


if __name__ == "__main__":
    main()