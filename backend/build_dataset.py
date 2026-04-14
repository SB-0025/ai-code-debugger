import json
import os

# Ensure folder exists
os.makedirs("data/train", exist_ok=True)


def format_example(buggy_code, error, root_cause, fixed_code, best_practice):
    return {
        "instruction": "Fix the bug in the following Python code. Explain the error, root cause, and provide the corrected code.",
        "input": buggy_code,
        "output": f"Error: {error}",
        "Root Cause": root_cause,
        "Fixed Code": fixed_code, 
        "Best Practice": best_practice
    }


def build_dataset():
    dataset = []

    # Example 1
    dataset.append(format_example(
        "print('Hello World'",
        "SyntaxError",
        "Missing closing parenthesis",
        "print('Hello World')",
        "Always check matching brackets"
    ))

    # Example 2
    dataset.append(format_example(
        "def add(a, b):\nprint(a + b)",
        "IndentationError",
        "Function body is not indented",
        "def add(a, b):\n    print(a + b)",
        "Use proper indentation in Python"
    ))

    # Example 3
    dataset.append(format_example(
        "a = '5' + 5",
        "TypeError",
        "Cannot concatenate string and integer",
        "a = int('5') + 5",
        "Ensure data types are compatible"
    ))

    # Example 4
    dataset.append(format_example(
        "lst = [1,2,3]\nprint(lst[5])",
        "IndexError",
        "Index out of range",
        "print(lst[2])",
        "Check list length before accessing index"
    ))

    # Example 5
    dataset.append(format_example(
        "d = {'a': 1}\nprint(d['b'])",
        "KeyError",
        "Key does not exist in dictionary",
        "print(d.get('b', 0))",
        "Use dict.get() to avoid KeyError"
    ))

    # Example 6
    dataset.append(format_example(
        "for i in range(5):\n    while True:\n        break",
        "Logic Error",
        "Unnecessary loop structure",
        "for i in range(5):\n    pass",
        "Avoid redundant loops"
    ))

    # Example 7
    dataset.append(format_example(
        "def func(x=[]):\n    x.append(1)\n    return x",
        "Mutable Default Argument",
        "Default list is shared across calls",
        "def func(x=None):\n    if x is None:\n        x = []\n    x.append(1)\n    return x",
        "Avoid mutable default arguments"
    ))

    # Example 8
    dataset.append(format_example(
        "def add(a, b):\n    a + b",
        "Missing Return",
        "Function does not return value",
        "def add(a, b):\n    return a + b",
        "Always return expected values"
    ))

    # Example 9
    dataset.append(format_example(
        "for i in range(1,5):\n    print(i)",
        "Off-by-one Error",
        "Range excludes last number",
        "for i in range(1,6):\n    print(i)",
        "Understand how range() works"
    ))

    # Example 10
    dataset.append(format_example(
        "while True:\n    pass",
        "Infinite Loop",
        "Loop has no termination condition",
        "while False:\n    pass",
        "Ensure loop exit condition"
    ))

    # Save dataset
    with open("data/train/train_data.json", "w") as f:
        json.dump(dataset, f, indent=4)

    print("✅ Dataset created with", len(dataset), "examples")


if __name__ == "__main__":
    build_dataset()

    