from argparse import Namespace, ArgumentParser
from llm_sdk import Small_LLM_Model
from .loader import load_functions, load_prompts
import json
from pydantic import ValidationError
from .decoder import decoder
from .generator import generator
from .vocab import load_vocab

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


def main() -> int:
    model = Small_LLM_Model()
    path = model.get_path_to_vocab_file()
    vocab = load_vocab(path)

    args = parsing()
    try:
        functions = load_functions(args.functions_definition)
        prompts = load_prompts(args.input)
    except FileNotFoundError as e:
        print(f"Error: file not found: {e.filename}")
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON: {e}")
        return 1
    except ValidationError as e:
        print(f"Error: unexpected file structure\n{e}")
        return 1

    results = decoder(model, prompts, functions, vocab)

    return 0

if __name__ == "__main__":
    main()
