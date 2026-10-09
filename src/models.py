from pydantic import BaseModel
from typing import Literal

class ParameterSpec(BaseModel):
    type: Literal["number", "string", "boolean"]

class FunctionDefinition(BaseModel):
    name: str
    description: str
    parameters: dict[str, ParameterSpec]
    returns: ParameterSpec

class PromptEntry(BaseModel):
    prompt: str
