from pydantic import TypeAdapter
from .models import FunctionDefinition, PromptEntry
import json

def load_functions(path: str) -> list[FunctionDefinition]:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    return TypeAdapter(list[FunctionDefinition]).validate_python(raw)

def load_prompts(path: str) -> list[PromptEntry]:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    return TypeAdapter(list[PromptEntry]).validate_python(raw)

