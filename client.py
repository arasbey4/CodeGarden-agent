import ollama

class OllamaClient:
    def __init__(self, model="codellama", host="http://localhost:11434"):
        self.host = host
        # Use the Client class to allow custom hosts (Remote Ollama Servers)
        self.client = ollama.Client(host=self.host)
        self.model = model
        self.messages = [
            {
                "role": "system",
                "content": "You are CodeGarden, a helpful coding agent. You provide concise, accurate, and high-quality code snippets and architectural advice. You are running via Ollama."
            }
        ]

    def set_model(self, model_name):
        self.model = model_name

    def set_host(self, new_host):
        self.host = new_host
        self.client = ollama.Client(host=self.host)

    def get_models(self):
        try:
            models_info = self.client.list()
            # Handle different Ollama response formats
            if hasattr(models_info, 'models'):
                return [m['name'] for m in models_info.models]
            elif isinstance(models_info, dict) and 'models' in models_info:
                return [m['name'] for m in models_info['models']]
            return []
        except Exception:
            return []

    def chat(self, user_input):
        self.messages.append({"role": "user", "content": user_input})

        response = self.client.chat(
            model=self.model,
            messages=self.messages,
            stream=True
        )

        full_response = ""
        for chunk in response:
            content = chunk['message']['content']
            full_response += content
            yield content

        self.messages.append({"role": "assistant", "content": full_response})
