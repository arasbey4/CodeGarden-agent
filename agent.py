import ollama
from config import config
from tools import TOOLS_MAP, OLLAMA_TOOLS

class CodingAgent:
    def __init__(self):
        self.history = []
        self.tool_callback = None  # Callback to notify CLI of tool usage
        self.system_prompt = (
            "You are CodeGarden, a powerful local AI coding agent. "
            "You can read files, write files, list directories, and execute terminal commands. "
            "Use your tools to explore the codebase, fix bugs, and build features. "
            "Always double-check file paths before writing. Be precise and professional."
        )

    def set_tool_callback(self, callback):
        self.tool_callback = callback


    def set_model(self, model_name):
        config.set_model(model_name)

    def chat(self, user_input):
        """
        Sends a message to Ollama and handles the tool-use loop.
        """
        model = config.current_model or config.default_model

        if not self.history:
            self.history.append({'role': 'system', 'content': self.system_prompt})

        self.history.append({'role': 'user', 'content': user_input})

        # The loop allows the agent to call multiple tools in sequence
        # until it has enough information to answer the user.
        iteration = 0
        while True:
            iteration += 1
            try:
                response = ollama.chat(
                    model=model,
                    messages=self.history,
                    tools=OLLAMA_TOOLS,
                    stream=False
                )

                message = response['message']
                self.history.append(message)

                # Check if the model wants to use a tool
                if not message.get('tool_calls'):
                    return message.get('content', "I'm not sure how to respond to that.")

                # Handle all requested tool calls
                for tool in message['tool_calls']:
                    function_name = tool['function']['name']
                    arguments = tool['function']['arguments']

                    # Notify CLI via callback
                    if self.tool_callback:
                        self.tool_callback(function_name, arguments)

                    # Execute the tool
                    if function_name in TOOLS_MAP:
                        # Execute function with unpacked arguments
                        result = TOOLS_MAP[function_name](**arguments)
                    else:
                        result = f"Error: Tool {function_name} not found."

                    # Add tool result to history
                    self.history.append({
                        'role': 'tool',
                        'content': result,
                        'name': function_name
                    })
            except Exception as e:
                return f"Error during agent loop: {str(e)}"

    def clear_history(self):
        self.history = [{'role': 'system', 'content': self.system_prompt}]

agent = CodingAgent()
