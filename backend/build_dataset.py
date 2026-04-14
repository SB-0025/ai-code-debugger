import json
import os
import random
from datasets import load_dataset

# Ensure folder exists
os.makedirs("data/train", exist_ok=True)


def format_example(buggy_code, error, root_cause, fixed_code, best_practice):
    """Format a single training example"""
    return {
        "instruction": "Fix the bug in the following Python code. Explain the error, root cause, and provide the corrected code.",
        "input": buggy_code,
        "output": f"Error: {error}\nRoot Cause: {root_cause}\nFixed Code: {fixed_code}\nBest Practice: {best_practice}"
    }


# ============================================
# BUG INJECTION FUNCTIONS
# ============================================

def inject_indentation_error(code):
    """Remove indentation from first indented line"""
    lines = code.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('    '):  # 4 spaces
            original = line
            buggy = line.lstrip()
            buggy_code = '\n'.join(lines[:i] + [buggy] + lines[i+1:])
            return (
                buggy_code,
                "IndentationError",
                "Missing or incorrect indentation",
                code,  # Full original code
                "Use consistent indentation (4 spaces per level in Python)"
            )
    return None


def inject_missing_colon(code):
    """Remove colon from if/for/while/def statements"""
    lines = code.split('\n')
    for i, line in enumerate(lines):
        if any(keyword in line for keyword in ['if ', 'for ', 'while ', 'def ', 'class ']):
            if ':' in line:
                buggy = line.replace(':', '', 1)  # Remove first colon
                buggy_code = '\n'.join(lines[:i] + [buggy] + lines[i+1:])
                return (
                    buggy_code,
                    "SyntaxError",
                    "Missing colon after control statement",
                    code,  # Full original code
                    "Always add ':' after if/for/while/def/class statements"
                )
    return None


def inject_missing_parenthesis(code):
    """Remove closing parenthesis from function calls"""
    lines = code.split('\n')
    for i, line in enumerate(lines):
        if 'print(' in line and line.count('(') > line.count(')'):
            continue  # Already missing
        if 'print(' in line:
            buggy = line.replace(')', '', 1)  # Remove first )
            buggy_code = '\n'.join(lines[:i] + [buggy] + lines[i+1:])
            return (
                buggy_code,
                "SyntaxError",
                "Missing closing parenthesis",
                code,  # Full original code
                "Check that all opening parentheses have matching closing ones"
            )
    return None


def inject_missing_quote(code):
    """Remove closing quote from strings"""
    lines = code.split('\n')
    for i, line in enumerate(lines):
        if "'" in line and line.count("'") >= 2:
            # Find last quote and remove it
            last_quote_pos = line.rfind("'")
            buggy = line[:last_quote_pos] + line[last_quote_pos+1:]
            buggy_code = '\n'.join(lines[:i] + [buggy] + lines[i+1:])
            return (
                buggy_code,
                "SyntaxError",
                "Missing closing quote",
                code,  # Full original code
                "Ensure all strings have matching opening and closing quotes"
            )
    return None


def inject_type_error(code):
    """Add operation between incompatible types"""
    lines = code.split('\n')
    for i, line in enumerate(lines):
        if '=' in line and 'def ' not in line:
            buggy_line = "    result = '5' + 5  # String + Integer"
            buggy_code = '\n'.join(lines[:i] + [buggy_line] + lines[i:])
            
            # FIXED: Full code with fix, not just one line
            fixed_line = "    result = int('5') + 5  # Convert to same type"
            fixed_code = '\n'.join(lines[:i] + [fixed_line] + lines[i:])
            
            return (
                buggy_code,
                "TypeError",
                "Cannot perform operation between string and integer",
                fixed_code,  #  Full corrected code
                "Ensure operands are of compatible types"
            )
    return None


def inject_index_error(code):
    """Access list with out-of-range index"""
    lines = code.split('\n')
    for i, line in enumerate(lines):
        if 'def ' in line:
            buggy_lines = [
                "    my_list = [1, 2, 3]",
                "    value = my_list[10]  # Index out of range"
            ]
            buggy_code = '\n'.join(lines[:i+1] + buggy_lines + lines[i+1:])
            
            # FIXED: Full code with fix
            fixed_lines = [
                "    my_list = [1, 2, 3]",
                "    value = my_list[2]  # Valid index"
            ]
            fixed_code = '\n'.join(lines[:i+1] + fixed_lines + lines[i+1:])
            
            return (
                buggy_code,
                "IndexError",
                "List index out of range",
                fixed_code,  #  Full corrected code
                "Check list length before accessing indices"
            )
    return None


def inject_key_error(code):
    """Access dictionary with non-existent key"""
    lines = code.split('\n')
    for i, line in enumerate(lines):
        if 'def ' in line:
            buggy_lines = [
                "    my_dict = {'a': 1, 'b': 2}",
                "    value = my_dict['c']  # Key doesn't exist"
            ]
            buggy_code = '\n'.join(lines[:i+1] + buggy_lines + lines[i+1:])
            
            # FIXED: Full code with fix
            fixed_lines = [
                "    my_dict = {'a': 1, 'b': 2}",
                "    value = my_dict.get('c', 0)  # Safe access"
            ]
            fixed_code = '\n'.join(lines[:i+1] + fixed_lines + lines[i+1:])
            
            return (
                buggy_code,
                "KeyError",
                "Dictionary key does not exist",
                fixed_code,  #  Full corrected code
                "Use dict.get() method to safely access dictionary keys"
            )
    return None


def inject_missing_return(code):
    """Remove return statement from function"""
    lines = code.split('\n')
    for i, line in enumerate(lines):
        if 'return ' in line:
            buggy = line.replace('return ', '    ', 1)
            if buggy.strip():  # If there's something after 'return'
                buggy_code = '\n'.join(lines[:i] + [buggy] + lines[i+1:])
                return (
                    buggy_code,
                    "Logic Error",
                    "Function doesn't return expected value",
                    code,  # Full original code
                    "Explicitly return values from functions"
                )
    return None


# List of all bug injection functions
BUG_INJECTORS = [
    inject_indentation_error,
    inject_missing_colon,
    inject_missing_parenthesis,
    inject_missing_quote,
    inject_type_error,
    inject_index_error,
    inject_key_error,
    inject_missing_return,
]


def apply_random_bug(code):
    """Try to apply a random bug injection to the code"""
    # Shuffle to get random order
    injectors = BUG_INJECTORS.copy()
    random.shuffle(injectors)
    
    for injector in injectors:
        result = injector(code)
        if result:  # Successfully injected a bug
            return result
    
    return None  # Couldn't inject any bug


def build_dataset_from_codesearchnet(num_examples=500):
    """Build dataset using CodeSearchNet"""
    
    print(" Downloading CodeSearchNet dataset (this may take 10-30 minutes)...")
    print(" Grab a coffee! First time takes a while, then it's cached.")
    
    # Load Python subset of CodeSearchNet
    dataset = load_dataset("code_search_net", "python", split="train")
    
    print(f" Dataset loaded! Total functions available: {len(dataset)}")
    print(f" Generating {num_examples} training examples...")
    
    training_data = []
    attempts = 0
    max_attempts = num_examples * 3  # Try up to 3x to get desired number
    
    # Randomly sample from dataset
    indices = random.sample(range(len(dataset)), min(max_attempts, len(dataset)))
    
    for idx in indices:
        if len(training_data) >= num_examples:
            break
            
        attempts += 1
        
        # Get code from dataset
        code_entry = dataset[idx]
        original_code = code_entry['func_code_string']
        
        # Skip if code is too short or too long
        if len(original_code) < 50 or len(original_code) > 500:
            continue
        
        # Try to inject a bug
        result = apply_random_bug(original_code)
        
        if result:
            buggy_code, error, root_cause, fixed_code, best_practice = result
            training_data.append(format_example(
                buggy_code, error, root_cause, fixed_code, best_practice
            ))
            
            # Progress indicator
            if len(training_data) % 50 == 0:
                print(f"   Generated {len(training_data)}/{num_examples} examples...")
    
    print(f"\n Successfully generated {len(training_data)} examples!")
    return training_data


def build_dataset():
    """Main function to build the dataset"""
    
    print("=" * 60)
    print(" BUILDING TRAINING DATASET")
    print("=" * 60)
    
    # Generate examples from CodeSearchNet
    dataset = build_dataset_from_codesearchnet(num_examples=500)
    
    # Save to file
    output_path = "data/train/train_data.json"
    with open(output_path, "w") as f:
        json.dump(dataset, f, indent=4)
    
    print(f"\nDataset saved to: {output_path}")
    print(f"Total examples: {len(dataset)}")
    print(f"File size: {os.path.getsize(output_path) / 1024:.2f} KB")
    print("\n Dataset building complete!")


if __name__ == "__main__":
    build_dataset()