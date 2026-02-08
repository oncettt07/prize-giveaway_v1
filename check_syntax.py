
import re

def check_structure(content):
    lines = content.split('\n')
    stack = []
    
    for i, line in enumerate(lines):
        line_num = i + 1
        # Remove strings and comments to avoid false positives
        # Simple regex for strings (this is a heuristic, not a full parser)
        clean_line = re.sub(r'([\'"`])(?:(?=(\\?))\2.)*?\1', '', line)
        clean_line = re.sub(r'//.*', '', clean_line)
        
        for char in clean_line:
            if char == '{':
                stack.append(('}', line_num))
            elif char == '(':
                stack.append((')', line_num))
            elif char == '[':
                stack.append((']', line_num))
            elif char in '}])':
                if not stack:
                    return f"Error: Unexpected '{char}' at line {line_num}"
                expected, open_line = stack.pop()
                if char != expected:
                    return f"Error: Expected '{expected}' (opened at {open_line}) but found '{char}' at line {line_num}"
    
    if stack:
        expected, open_line = stack[-1]
        return f"Error: Unclosed '{expected}' (opened at line {open_line})"
        
    return "Syntax OK (Braces balanced)"

try:
    with open('app.js', 'r', encoding='utf-8') as f:
        content = f.read()
    print(check_structure(content))
except Exception as e:
    print(f"Error reading file: {e}")
