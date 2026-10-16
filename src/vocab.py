import json

def load_vocab(path: str) -> dict[int, str]:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    vocab = {value: key.replace("Ġ", " ").replace("Ċ", "\n") for key, value in raw.items()}

    return vocab

def allowed_ids(prefix: str, vocab: dict[int, str], targets: list[str]) -> set[int]:
    allowed = set()
    for id, text in vocab.items():
        if any(target.startswith(prefix + text) for target in targets):
            allowed.add(id)

    return allowed

def is_number_prefix(string: str) -> bool:
    if string == "":
        return True

    has_dot = False

    for i, c in enumerate(string):
        if c == "-":
            if i != 0:
                return False
        elif c == ".":
            if i == 1 and string[0] == "-":
                return False
            if has_dot:
                return False
            if i == 0:
                return False

            has_dot = True

        elif c in "0123456789":
            continue
        else:
            return False
    return True

def is_number_complete(number: str) -> bool:
    if number.endswith((".", "-")):
        return False
    for n in number:
        if n in ("0123456789"):
            return True
    else:
        return False

def allowed_number_ids(prefix: str, vocab: dict[int, str], _targets: list[str]) -> set[int]:
    allowed = set()
    stop = set()
    for id, text in vocab.items():
        if is_number_prefix(prefix + text):
            allowed.add(id)
        if text == ',' or text == '}':
            stop.add(id)
    if is_number_complete(prefix):
        allowed.update(stop)
    return allowed

def is_string_prefix(text: str) -> bool:
    for c in text:
        if c in '"\\' or ord(c) < 0x20:
            return False
    return True

def allowed_string_ids(prefix: str, vocab: dict[int, str], _targets: list[str]) -> set[int]:
    allowed = set()
    for id, text in vocab.items():
        if is_string_prefix(prefix + text):
            allowed.add(id)
        if text == '"':
            allowed.add(id)
    return allowed
