import json
from llm_sdk import Small_LLM_Model
from .models import PromptEntry, FunctionDefinition

def build_header(functions: list[FunctionDefinition]) -> str:
    """
    transforme une liste en str pour la fonction encode()
    """
    lines = []
    for f in functions:
        lines.append(f"{f.name}: {f.description}")
    return "\n".join(lines)

def decoder(prompts: list[PromptEntry], functions: list[FunctionDefinition]):
    model = Small_LLM_Model()
    header = build_header(functions)

    for entry in prompts:
        """
        
        """
        full = f'{header}\nRequest: {entry.prompt}\nCall: {{"name:" "'
        input_ids = model.encode(full)[0].tolist()
        print(input_ids)

    return input_ids