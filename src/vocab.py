import json

def load_vocab(path: str) -> dict[int, str]:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    vocab = {value: key.replace("Ġ", " ").replace("Ċ", "\n") for key, value in raw.items()}

    return vocab

def allowed_ids(prefix: str, targets: list[str], vocab: dict[int, str]) -> set[int]:
    allowed = set()
    for id, text in vocab.items():
        if any(target.startswith(prefix + text) for target in targets):
            allowed.add(id)

    return allowed
