import json
from llm_sdk import Small_LLM_Model
from .models import PromptEntry, FunctionDefinition
from .generator import generator
from .vocab import allowed_number_ids, allowed_string_ids, allowed_ids

def build_header(functions: list[FunctionDefinition]) -> str:
    """
    transforme une liste en str pour la fonction encode()
    """
    lines = []
    for f in functions:
        lines.append(f"{f.name}: {f.description}")
    return "\n".join(lines)

def build_prompt_ft(header: str, prompt: str) -> str:
    return f'Choose the most suitable function for the request.\nRequest: {prompt}\n{header}\nCall: {{"name": "'

def build_prompt_js(json_partial: str, prompt: str) -> str:
    return f'Complete the JSON object by extracting the appropriate parameter values from the prompt.\nPrompt:{prompt}\n{json_partial}'

def fetch_function(name: str, functions: list[FunctionDefinition]) -> FunctionDefinition:
    for f in functions:
        if f.name == name:
            return f
    return None

def decoder(model: Small_LLM_Model, prompts: list[PromptEntry], functions: list[FunctionDefinition], vocab: dict[int, str]) -> list[str]:
    header = build_header(functions)
    ft_targets = [f.name for f in functions]
    by_name = {f.name: f for f in functions}

    results = []
    for entry in prompts:
        prompt_ft = build_prompt_ft(header, entry.prompt)
        prompt_ft_ids = model.encode(prompt_ft)[0].tolist()
        name = generator(model, prompt_ft_ids, allowed_ids, vocab, '"', ft_targets)

        definition = by_name[name]
        json_partial = f'{{"name": "{name}", "parameters": {{'

        for i, (key, spec) in enumerate(definition.parameters.items()):
            if i > 0:
                json_partial += ", "
            json_partial += f'"{key}":'
            if spec.type == "string":
                json_partial += '"'
            prompt_js = build_prompt_js(json_partial, entry.prompt)
            prompt_js_ids = model.encode(prompt_js)[0].tolist()
            if spec.type == "number":
                temp = generator(model, prompt_js_ids, allowed_number_ids, vocab, {',', '}'}, None)
                json_partial += temp
            else:
                temp = generator(model, prompt_js_ids, allowed_string_ids, vocab,{'"'}, None)
                json_partial += temp
                json_partial += '"'

        json_partial += '}'
        # json.dump() pour echapper la valeure du prompt correctement
        # [1:-1] permet de retirer les guillements exterieurs ajoutes par json.dumps()
        secure_prompt = json.dumps(entry.prompt, ensure_ascii=False)[1:-1]
        json_partial += f', "prompt":"{secure_prompt}"}}'
        results.append(json_partial)

    return results
