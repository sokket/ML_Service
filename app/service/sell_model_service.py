from service.model_service import ModelService
from model.pricing_strategy import PricingStrategy
from model.answer import Answer
from model.prompt import Prompt


class SellModelService:
    model: ModelService
    pricing_strategy: PricingStrategy

    def __init__(self, model, pricing_strategy):
        self.model = model
        self.pricing_strategy = pricing_strategy

    def run_model(self, user: User, prompt: Prompt) -> Answer:
        price_per_run = self.pricing_strategy.price_per_run

        if user.balance < price_per_run:
            return Answer.error_str(prompt, "not enought points on balance")
  
        text = ''
        try:
            text = self.model.run(user.id, prompt.text)
        except Exception as e:
            # todo: log exception
            return Answer.error_str(prompt, "processing error")

        # change balance only on success
        user.balance -= price_per_run
        
        return Answer.success(prompt, text)