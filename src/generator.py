from llm_sdk import Small_LLM_Model
import numpy as np
from typing import Callable


def generator(
    model: Small_LLM_Model,
    input_ids: list[int],
    allowed_functions: Callable[[str, dict[int, str]], set[int]],
    vocab: dict[int, str],
    stops: set[str],
) -> str:

    prefix = ""
    ids = list(input_ids)

    for _ in range(32):
        logits = model.get_logits_from_input_ids(ids)
        allowed = allowed_functions(prefix, vocab)
        if len(allowed) == 0:
            break
        masked = np.full(len(logits), -np.inf)
        for i in allowed:
            masked[i] = logits[i]
        best = int(masked.argmax())
        text = vocab[best]
        if text in stops:
            break
        ids.append(best)
        prefix += vocab[best]

    return prefix
