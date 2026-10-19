import sys
import json
from argparse import Namespace, ArgumentParser
from llm_sdk import Small_LLM_Model
from pydantic import ValidationError
from pathlib import Path
from .loader import load_functions, load_prompts
from .decoder import decoder
from .vocab import load_vocab
from typing import Any


def parsing() -> Namespace:
    parser = ArgumentParser()
    default_input = "data/input/function_calling_tests.json"
    default_functions = "data/input/functions_definition.json"
    default_output = "data/output/function_calling_results.json"
    parser.add_argument('--functions_definition', type=str,
                        default=default_functions)
    parser.add_argument('--input', type=str, default=default_input)
    parser.add_argument('--output', type=str, default=default_output)

    args = parser.parse_args()

    return args


def build_output(output: list[dict[str, Any]], path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w', encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)


def main() -> int:

    args = parsing()
    try:
        model = Small_LLM_Model()
        path = model.get_path_to_vocab_file()
        vocab = load_vocab(path)
        functions = load_functions(args.functions_definition)
        prompts = load_prompts(args.input)
        results = decoder(model, prompts, functions, vocab)
        build_output(results, args.output)
    except FileNotFoundError as e:
        print(f"Error: file not found: {e.filename}")
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON: {e}")
        return 1
    except ValidationError as e:
        print(f"Error: unexpected file structure\n{e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
