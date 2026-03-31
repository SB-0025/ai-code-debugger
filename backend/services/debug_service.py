def debug_code_logic(result: str):
    
    # Rule 1: Missing closing quote
    if "print(" in result and "'" in result and not result.endswith("')"):
        return {
            "error": "Syntax Error",
            "explanation": "Missing closing quote or bracket.",
            "fixed_code": "print('Hello')"
        }

    # Rule 2: Missing colon in if
    if "if" in result and ":" not in result:
        return {
            "error": "Syntax Error",
            "explanation": "Missing ':' after if statement.",
            "fixed_code": "if condition: \n    pass"
        }

    # Rule 3: Missing parentheses in print (Python 3)
    if "print " in result:
        return {
            "error": "Syntax Error",
            "explanation": "print should use parentheses in Python 3.",
            "fixed_code": "print('Hello')"
        }
    
    # Rule 4 : Missing for keyword in loop
    if("for" in result and "in" not in result ):
        return {
            "error" : "Syntax Error",
            "explanation": "For loop should use 'in' keyword.",
            "fixed_code": "or i in range(5):\n    pass"
        }
    
    return{
        "message" :"Its Working!!",
        "your code": result
    }
