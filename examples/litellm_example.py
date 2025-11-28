from persona_agent.core import PersonaAgent
from persona_agent.profiles import DOCTOR_PROFILE
from persona_agent.models import make_litellm_chat_model


def main():
  # 1. Load environment variables from .env file, which contains OPENAI_API_KEY
  from dotenv import load_dotenv
  load_dotenv()

  # 2. Create LiteLLM chat model
  chat_model = make_litellm_chat_model(
    model_name="openai/gpt-4o-mini",
    temperature=0.2,
    max_tokens=512,
  )
  
  # 3. Create PersonaAgent with doctor persona
  agent = PersonaAgent(
    name="Dr. Maple",
    model=chat_model,
    persona=DOCTOR_PROFILE,
  )
  
  # 4. Interact
  question = "Explain gMG in patient-friendly language."
  print("User:", question)
  answer = agent.react(question)
  print("\nDr. Maple:", answer)
  
if __name__ == "__main__":
  main()