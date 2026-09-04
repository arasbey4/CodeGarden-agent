from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.markdown import Markdown
from rich.live import Live
from rich.align import Align
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style

from utils import get_logo, clear_screen
from agent import agent
from config import config

console = Console()

# Custom prompt style
style = Style.from_dict({
    'prompt': '#00ff00 bold',
    'user': '#00ffff',
    'ai': '#ff00ff',
})

session = PromptSession(style=style)

def print_logo():
    clear_screen()
    # Center the logo
    console.print(Align(Panel(get_logo(), style="bold green", expand=False), "center"))
    console.print(Align("[bold cyan]Welcome to CodeGarden! Type /help for commands.[/bold cyan]\n", "center"))

def display_message(role, text):
    # Create a styled message box
    if role == "user":
        content = Text(text, style="cyan")
        panel = Panel(content, title="[bold cyan]You[/bold cyan]", border_style="cyan", expand=False)
    elif role == "assistant":
        content = Markdown(text)
        panel = Panel(content, title="[bold magenta]CodeGarden[/bold magenta]", border_style="magenta", expand=False)
    else:
        content = Text(text, style="yellow")
        panel = Panel(content, title="[bold yellow]System[/bold yellow]", border_style="yellow", expand=False)

    # Center the message box on the screen
    console.print(Align(panel, "center"))

def handle_command(cmd_text):
    parts = cmd_text.split()
    cmd = parts[0].lower()
    args = parts[1:]

    if cmd == "/help":
        help_text = (
            "/models - List available local models\n"
            "/cloud-models - See recommended high-perf models from Ollama library\n"
            "/pull <name> - Download a model from Ollama cloud\n"
            "/model <name> - Switch to a specific model\n"
            "/cd <path> - Change the project directory\n"
            "/clear - Clear conversation history\n"
            "/exit - Close CodeGarden\n"
            "/help - Show this menu"
        )
        display_message("system", help_text)
        return True
    elif cmd == "/models":
        models = config.detect_models()
        if models:
            display_message("system", "Available local models:\n" + "\n".join(models))
        else:
            display_message("system", "No local models found in Ollama.")
        return True
    elif cmd == "/cloud-models":
        recs = config.cloud_recommendations
        text = "🌟 Recommended Models from Ollama Library:\n\n"
        for category, models in recs.items():
            text += f"[{category}]: {', '.join(models)}\n"
        text += "\nUse /pull <model_name> to download one."
        display_message("system", text)
        return True
    elif cmd == "/pull":
        if args:
            model_name = args[0]
            display_message("system", f"Pulling {model_name}... This may take a while. Please wait.")
            import ollama
            try:
                ollama.pull(model_name)
                display_message("system", f"Successfully pulled {model_name}!")
            except Exception as e:
                display_message("system", f"Error pulling model: {str(e)}")
        else:
            display_message("system", "Please specify a model name. Use /cloud-models for ideas.")
        return True
    elif cmd == "/model":
        if args:
            model_name = args[0]
            agent.set_model(model_name)
            display_message("system", f"Switched to model: {model_name}")
        else:
            display_message("system", "Please specify a model name. Use /models to see options.")
        return True
    elif cmd == "/cd":
        if args:
            path = args[0]
            from tools import change_directory
            result = change_directory(path)
            display_message("system", result)
        else:
            display_message("system", "Please specify a path. Example: /cd C:/Projects/MyApp")
        return True
    elif cmd == "/clear":
        agent.clear_history()
        clear_screen()
        print_logo()
        display_message("system", "History cleared.")
        return True
    elif cmd == "/exit":
        display_message("system", "Growing your garden... Goodbye!")
        exit(0)

    return False

def run_cli():
    print_logo()

    # Define tool callback for real-time feedback
    def tool_notify(name, args):
        # Center the tool notification as well
        console.print(Align(Text(f"🛠️  Using tool: {name} {args}", style="bold yellow"), "center"))

    agent.set_tool_callback(tool_notify)

    # Auto-detect a model to start with
    models = config.detect_models()
    if models:
        initial_model = models[0]
        agent.set_model(initial_model)
        display_message("system", f"Auto-detected model: {initial_model}")
    else:
        display_message("system", "No local models detected. Using default 'codellama'.")

    while True:
        try:
            # Prompt is harder to center perfectly in terminal,
            # but we make it look like a centered input line
            user_input = session.prompt("\n[bold green]  CodeGarden 🌿  [/bold green] > ")

            if not user_input.strip():
                continue

            if user_input.startswith("/"):
                if handle_command(user_input):
                    continue

            # Regular chat
            display_message("user", user_input)

            # Show a loading indicator
            with console.status("[bold magenta]Thinking..."):
                response = agent.chat(user_input)

            display_message("assistant", response)

        except KeyboardInterrupt:
            handle_command("/exit")
        except EOFError:
            handle_command("/exit")
