from executor import Executor
from llm import Provider
from loguru import logger


# TODO: Return code from `provider.fix_code()` in json or other easily parsable format
# TODO: Cargo clippy errors do not always have an error code (e.g. unclosed delimited). Need to handle this.
# TODO: In iteration loop, need to write code somewhere and run `cargo clippy` again
# TODO: User will have a main llm prompt. The below is only the iteration process to fix errors. Add in main prompt handling.

def main():
    # Setup rust code executor and llm provider
    executor = Executor("./rust")
    provider = Provider(provider="anthropic", model="claude-3-5-sonnet-20241022")

    while True:
        # Lint code with `cargo clippy`
        stdout, errors = executor.lint_code()
        print(errors)
        if errors:
            # Attempt to fix code if there are errors
            code = executor.get_code()
            response = provider.fix_code(code, errors)

            logger.info(f"-"*50)
            logger.info(f"{len(errors)} errors found. Attempting to fix...")
            logger.info(f"Response: {response}")

            # Mock llm writing back correct code
            with open("./rust/src/main.rs", "w") as f:
                f.write("fn main() {\n    println!(\"Hello, world!\");\n}\n")

            # Mock llm writing back incorrect code to test the iteration process
            # with open("./rust/src/main.rs", "w") as f:
            #     f.write("fn main() -> Vec<String> {\n    println!(\"Hello, world!\");\n}\n")
        else:
            logger.info(f"No errors found.")
            break

    # Format code before writing correct code to file
    # This needs to apply to the llm output, not the user's existing code
    executor.format_code()    

if __name__ == "__main__":
    main()
