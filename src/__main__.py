import argparse
# from pathlib import Path

def parsing() -> int:
    parser = argparse.ArgumentParser()
    path1 = "data/input/function_calling_tests.json"
    path2 = "data/input/functions_definition.json"
    parser.add_argument('--functions_definition', type=str, default=path1)
    parser.add_argument('--input', type=str, default=path2)
    parser.add_argument('--output', type=str, default=None)

    args = parser.parse_args()
    print(f"functions_definition path: {args.functions_definition}")
    print(f"input path: {args.input}")

    return 1

def main():
    if parsing():
        return None

if __name__ == "__main__":
    main()
