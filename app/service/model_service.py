# это сущность для ML модели
# предполагается использовать https://github.com/ggerganov/llama.cpp
class ModelService:
    def run(self, user_id: int, prompt: str) -> str:
        # LLM context could be loaded from binary file '{user_id}.ctx'
        return 'dummy answer'