from cli import run_cli

if __name__ == "__main__":
    try:
        run_cli()
    except Exception as e:
        print(f"A critical error occurred: {e}")
