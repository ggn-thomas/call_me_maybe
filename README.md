*This project has been created as part of the 42 curriculum by thgaugai*

# call me maybe

## Description

This project introduces function calling in Large Language Models by building a system that translates natural language prompts into structured function calls with typed arguments. 

Goal: Implement constrained decoding

Function calling enables LLMs to:

- Interact with external systems: Call APIs, query databases, control devices
- Execute code: Perform calculations, data transformations, file operations
- Chain operations: Break complex tasks into executable steps
- Provide structured output: Generate JSON, XML, or other machine-readable formats
- Extract structured data from unstructured text: given a large book, extract fields

Overview: Prompt -> Tokenization -> Input IDs -> LLM -> Logits -> Next Token Selection

## Instructions

- make install: Install project dependencies using pip, uv, pipx, or any other package manager of your choice
- make run: Execute the main script
- make debug: Run the main script in debug mode using Python’s built-in debugger
- make clean: Remove temporary files or cache
- make lint: Execute the commands flake8 . and mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
- make lint-strict: Execute the commands flake8 . and mypy . --strict

## Resources

- W3Schools (model pydantic, numpy)
- https://huggingface.co/Qwen/Qwen3-0.6B (docs du modèle Qwen3)
- https://youtu.be/kCc8FmEb1nY?si=qTSb3vK4hne_P5uW (transformers)

- claude code -> was used as a tutor, explaining tokenization and the ids/logits distinction, diagnosing errors from tracebacks, reviewing architecture choices.

## Algorithm explanation

I write every structural character of the JSON myself. The model only fills the holes: the function name and the argument values. At each generation step, i mask every logit to -inf except the tokens whose text keeps the accumulated prefix of at least one target.

## Design decisions

- `llm_sdk` is excluded from strict typing: it's provided without annotation and must not be modified.

- Quotation marks and backslashes are excluded from generated content. This guarantees valid JSON without implementing escape handling.

## Performance analysis

Moving the function catalog after the request raised function-name accuracy from 73% to 100% (8/11 -> 11/11). In an autoregressive transformer, the tokens closest to the generation point carry the most weight: with the catalog last, the fives names are fresh when the model must choose one.

test with: time make run

## Challenges faced

- find the right way to build the prompt with parameters values to have the exact output intented

- how we can stop the generation, for example using delimiter like " for string or , and }

## Testing strategy

- parsing: is there valid json in ouput, does files exist, check path if they're valid or not

- llm/generator: run with short and long prompt with different value. run with very confused prompt/value

- Renaming every function in functions_definition.json and rerunning without touching the code verifies that nothing is hardcoded to the provided examples.

## Example usage

try different way to build the file/prompt

be especially confused to test the llm

function_calling_test.json:

```json
[
  {
    "prompt": "What is the sum of 2 and 3?"
  },
  {
    "prompt": "What is the sum of 265 and 345?"
  },
  {
    "prompt": "Greet shrek"
  },
]
```

```json
functions_definition.json:

[
  {
    "name": "fn_add_numbers",
    "description": "Add two numbers together and return their sum.",
    "parameters": {
      "a": {
        "type": "number"
      },
      "b": {
        "type": "number"
      }
    },
    "returns": {
      "type": "number"
    }
  },
  {
    "name": "fn_greet",
    "description": "Generate a greeting message for a person by name.",
    "parameters": {
      "name": {
        "type": "string"
      }
    },
    "returns": {
      "type": "string"
    }
  },
  {
    "name": "fn_reverse_string",
    "description": "Reverse a string and return the reversed result.",
    "parameters": {
      "s": {
        "type": "string"
      }
    },
    "returns": {
      "type": "string"
    }
  },
]
```

```json
function_calling_results.json:

[
    {
        "name": "fn_add_numbers",
        "parameters": {
            "a": 2.0,
            "b": 3.0
        },
        "prompt": "What is the sum of 2 and 3?"
    },
    {
        "name": "fn_add_numbers",
        "parameters": {
            "a": 265.0,
            "b": 345.0
        },
        "prompt": "What is the sum of 265 and 345?"
    },
    {
        "name": "fn_greet",
        "parameters": {
            "name": "shrek"
        },
        "prompt": "Greet shrek"
    },
]
```