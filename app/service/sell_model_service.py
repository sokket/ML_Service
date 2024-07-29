from service.model_service import ModelService
from model.pricing_strategy import PricingStrategy
from model.prompt import Prompt
from model.user import User
from datetime import datetime as dt

class SellModelService:
    model: ModelService
    pricing_strategy: PricingStrategy

    def __init__(self, model, pricing_strategy):
        self.model = model
        self.pricing_strategy = pricing_strategy

    def run_model(self, session, user: User, prompt_text: str) -> Prompt:
        prompt = Prompt(user.id, prompt_text)
        session.add(prompt) 
        session.commit() 
        session.refresh(prompt)
        prompt = self.__run_model(session, user, prompt)
        session.add(prompt) 
        session.commit() 
        session.refresh(prompt)
        return prompt
    
    def get_user_prompts(self, session, user: User) -> list[Prompt]:
        return session.query(Prompt).filter(Prompt.user_id == user.id).all()

    def get_prompts(self, session) -> list[Prompt]:
        return session.query(Prompt).all()
    
    def get_prompt(self, session, id) -> Prompt:
        return session.query(Prompt).filter(Prompt.id == id).first()
    
    def delete_prompt(self, session, prompt):
       session.delete(prompt)
       session.commit()

    def delete_all_prompts(self, session, prompts):
       session.query(Prompt).delete()

    def __run_model(self, session, user: User, prompt: Prompt) -> Prompt:
        price_per_run = self.pricing_strategy.price_per_run

        if user.balance < price_per_run:
            prompt.error = "not enought points on balance"
            return prompt
  
        text = ''
        try:
            text = self.model.run(user.id, prompt.text)
        except Exception as e:
            # todo: log exception
            prompt.error = "processing error"
            return prompt

        # change balance only on success
        user.balance -= price_per_run
        session.add(user) 
        session.commit() 
        session.refresh(user)

        prompt.answer = text
        prompt.answered_at = dt.now()
        prompt.cost = price_per_run
        return prompt