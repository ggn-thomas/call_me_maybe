from .vocab import allowed_ids
from llm_sdk import Small_LLM_Model
import numpy as np
from typing import Callable

def generator(
    model: Small_LLM_Model,
    input_ids: list[int],
    allowed_functions: Callable,
    vocab: dict[int, str],
    functions_targets: list[str]
) -> str:

    prefix = ""
    ids = list(input_ids)

    while True:
        logits = model.get_logits_from_input_ids(ids)
        allowed = allowed_functions(prefix, vocab, functions_targets)
        if len(allowed) == 0:
            break
        masked = np.full(len(logits), -np.inf)
        for i in allowed:
            masked[i] = logits[i]
        best = int(masked.argmax())

        ids.append(best)
        prefix += vocab[best]
    return prefix
