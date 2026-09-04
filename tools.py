import os
import subprocess
import shutil

def write_file(path, content):
    """Writes content to a file at the specified path. Creates directories if they don't exist."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing to {path}: {str(e)}"

def read_file(path):
    """Reads the content of a file at the specified path."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading {path}: {str(e)}"

def execute_command(command):
    """Executes a shell command and returns the output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        output = result.stdout if result.stdout else ""
        error = result.stderr if result.stderr else ""

        if result.returncode == 0:
            return output if output else "Command executed successfully (no output)."
        else:
            return f"Command failed with exit code {result.returncode}.\nError: {error}"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 60 seconds."
    except Exception as e:
        return f"Error executing command: {str(e)}"

def list_files(path="."):
    """Lists files and directories in the given path."""
    try:
        files = os.listdir(path)
        return "\n".join(files) if files else "Directory is empty."
    except Exception as e:
        return f"Error listing files in {path}: {str(e)}"

def change_directory(path):
    """Changes the current working directory of the agent."""
    try:
        os.chdir(path)
        return f"Changed directory to: {os.getcwd()}"
    except Exception as e:
        return f"Error changing directory to {path}: {str(e)}"

# Mapping tools to functions for the agent
TOOLS_MAP = {
    "write_file": write_file,
    "read_file": read_file,
    "execute_command": execute_command,
    "list_files": list_files,
    "change_directory": change_directory,
}

# Ollama tool definitions (JSON schema)
OLLAMA_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file. Use this to create new files or overwrite existing ones.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "The absolute or relative path to the file."},
                    "content": {"type": "string", "description": "The text content to write into the file."}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "The path to the file to read."}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_command",
            "description": "Run a terminal command. Use this for git, npm, pip, or any other shell operation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The full shell command to execute."}
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files and folders in a directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "The directory path to list (defaults to current)."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "change_directory",
            "description": "Change the current working directory of the agent to a new path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "The path to change to."}
                },
                "required": ["path"]
            }
        }
    }
]
