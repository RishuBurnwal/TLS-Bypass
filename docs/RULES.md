# TLS Bypass Rule Management Guide

## What are TLS Bypass Rules?

TLS bypass rules (also known as exclusion rules) are patterns used by security testing tools like Burp Suite to exclude certain hosts or URLs from interception. When traffic matches these rules, the tool allows it to pass through without interception.

## When to Use TLS Bypass Rules

### Host Rules (Exact Matches)
- Use for specific, known hostnames
- When you want to exclude a single domain completely
- Example: `example.com` - matches only this exact hostname

### Regex Rules (Pattern Matches)
- Use when you need to match multiple similar hosts
- When dealing with dynamic or changing hostnames
- Example: `.*\.internal\.corp` - matches all subdomains ending with `.internal.corp`

## Rule Templates

### Match All Subdomains
- **Purpose**: Match all subdomains of a specific domain
- **Template**: `.*\.example\.com`
- **Example**: Matches `api.example.com`, `dev.example.com`, etc.

### Match Specific Prefix
- **Purpose**: Match hosts with a specific prefix pattern
- **Template**: `^dev-.*\.example\.com$`
- **Example**: Matches `dev-api.example.com`, `dev-www.example.com`, etc.

### Match Keyword Anywhere
- **Purpose**: Match hosts containing a specific keyword
- **Template**: `.*staging.*`
- **Example**: Matches `staging.example.com`, `api-staging.dev`, etc.

### Match IP-Style Hostname
- **Purpose**: Match hostnames that look like IP addresses
- **Template**: `^\d+\.\d+\.\d+\.\d+$`
- **Example**: Matches `192.168.1.100`, `10.0.0.1`, etc.

## Rule Management Best Practices

1. **Always test your regex** using the built-in regex tester
2. **Use specific patterns** to avoid unintended matches
3. **Comment out rules** instead of deleting them when testing
4. **Group related rules** together for better organization
5. **Document complex rules** with inline comments

## Security Considerations

- Only use rules on systems you own or are authorized to test
- Regularly review and audit your rule sets
- Remove rules when testing is complete
- Never use rules on production systems without proper authorization