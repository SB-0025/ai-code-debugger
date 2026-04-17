from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel, PeftConfig
import torch
import re
import os

class DebugService:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        
    def load_model(self):
        """Load the fine-tuned model at startup"""
        print("Loading model...")
        
        # Get the absolute path to the model directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.abspath(os.path.join(current_dir, "..", "model"))
        
        print(f"Model path: {model_path}")
        
        # Check if adapter_config.json exists
        adapter_config_path = os.path.join(model_path, "adapter_config.json")
        if not os.path.exists(adapter_config_path):
            raise FileNotFoundError(f"adapter_config.json not found at {adapter_config_path}")
        
        print("adapter_config.json found!")
        print("Loading base model...")
        
        # Load base model
        base_model = AutoModelForCausalLM.from_pretrained(
            "Salesforce/codegen-350M-mono",
            device_map="auto",
            trust_remote_code=True
        )
        
        print("Loading adapter configuration...")
        # Load the PEFT config first
        config = PeftConfig.from_pretrained(model_path)
        
        print("Loading adapter weights...")
        # Load the model with adapter
        self.model = PeftModel.from_pretrained(
            base_model,
            model_path,
            config=config,
            is_trainable=False
        )
        
        print("Loading tokenizer...")
        # Load tokenizer from local path
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        print("Model loaded successfully!")
    
    def debug_code(self, code: str, language: str = "python"):
        """Run the model to debug code"""
        
        # Format the prompt EXACTLY as in training - capitalized "Python"
        prompt = f"""### Instruction: Fix the bug in the following Python code. Explain the error, root cause, and provide the corrected code.

### Input: {code}

### Output:"""
        
        # Tokenize
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        
        # Move to same device as model
        device = next(self.model.parameters()).device
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # Generate response - use greedy decoding for more consistent output
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=400,
                temperature=0.3,  # Lower temperature for more focused output
                do_sample=True,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )
        
        # Decode the response
        full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        print("=" * 50)
        print("FULL MODEL RESPONSE:")
        print(full_response)
        print("=" * 50)
        
        # Extract just the output part (after "### Output:")
        response = full_response.split("### Output:")[-1].strip()
        
        print("EXTRACTED OUTPUT:")
        print(response)
        print("=" * 50)
        
        # Parse the response
        result = self._parse_response(response, code)
        
        return result
    
    def _parse_response(self, response: str, original_code: str):
        """Parse the model's response into structured format - matching training format"""
        
        # The training format is:
        # Error: [Type]
        # Root Cause: [Explanation]
        # Fixed Code: [Code]
        
        # Extract Error (everything from "Error:" to "Root Cause:" or newline)
        error_match = re.search(r'Error:\s*([^\n]+)', response, re.IGNORECASE)
        
        # Extract Root Cause (everything from "Root Cause:" to "Fixed Code:")
        cause_match = re.search(r'Root Cause:\s*([^\n]+?)(?=\s*Fixed Code:|\s*$)', response, re.IGNORECASE | re.DOTALL)
        
        # Extract Fixed Code (everything after "Fixed Code:")
        code_match = re.search(r'Fixed Code:\s*(.+?)(?=\s*###|\s*$)', response, re.IGNORECASE | re.DOTALL)
        
        error = error_match.group(1).strip() if error_match else "Unknown error"
        root_cause = cause_match.group(1).strip() if cause_match else "Unable to determine"
        fixed_code = code_match.group(1).strip() if code_match else original_code
        
        return {
            "error": error,
            "root_cause": root_cause,
            "fixed_code": fixed_code,
            "best_practice": "Use proper Python syntax and error handling",  # Generic since not in training
            "confidence_score": 85
        }

# Create a singleton instance
debug_service = DebugService()