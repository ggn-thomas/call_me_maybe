import json
from llm_sdk import Small_LLM_Model
from .models import PromptEntry, FunctionDefinition, ParameterSpec
from .generator import generator

def build_ouput(parameters: dict[str, ParameterSpec]) -> str:
    output = []
    ouput.append(f"name: {name}, ")
    for name, spec in parameters.items():
        signature.append(f"{name}: {spec.type}")
    return ", ".join(signature)

def build_header(functions: list[FunctionDefinition]) -> str:
    """
    transforme une liste en str pour la fonction encode()
    """
    lines = []
    for f in functions:
        lines.append(f"{f.name}: {f.description}")
    return "\n".join(lines)

def build_prompt(header: str, prompt: str) -> str:
    return f'Choose the most suitable function for the request.\nRequest: {prompt}\n{header}\nCall: {{"name": "'

def fetch_function(name: str, functions: list[FunctionDefinition]) -> FunctionDefinition:
    for f in functions:
        if f.name == name:
            return f
    return None
    
def decoder(model: Small_LLM_Model, prompts: list[PromptEntry], functions: list[FunctionDefinition], vocab: dict[int, str]) -> list[str]:
    header = build_header(functions)
    targets = [f.name for f in functions]

    results = []
    for entry in prompts:
        full = build_prompt(header, entry.prompt)
        input_ids = model.encode(full)[0].tolist()
        name = generator(model, input_ids, targets, vocab)

        f = fetch_function(name, functions)
        output = f"prompt: {entry.prompt}\nname: {f.name}\nparameters:{"
        f

        results.append(name)


    return results
