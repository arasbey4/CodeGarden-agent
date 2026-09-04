import ollama

class Config:
    def __init__(self):
        self.default_model = "codellama"
        self.current_model = None
        # Recommended high-performance models from the Ollama library (Cloud)
        self.cloud_recommendations = {
            "Coding": ["codellama", "deepseek-coder", "starcoder2", "phind-codellama"],
            "General": ["llama3", "mistral", "mixtral", "gemma"],
            "Lightweight": ["phi3", "tinyllama", "qwen"]
        }

    def detect_models(self):
        """
        Detects available models in local Ollama instance.
        """
        try:
            models_info = ollama.list()
            models = [m['name'] for m in models_info['models']]
            return models
        except Exception as e:
            print(f"Error detecting models: {e}")
            return []

    def set_model(self, model_name):
        self.current_model = model_name

config = Config()
