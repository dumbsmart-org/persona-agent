from persona_agent.core import PersonaAgent
from persona_agent.profiles import DEFAULT_PROFILE

def echo_model(prompt: str, **_) -> str:
  # Replace with real LLM call.
  return f"[ECHO MODEL OUTPUT]\n{prompt}"

def main():
  agent = PersonaAgent(
    name="EchoBot",
    model=echo_model,
    persona=DEFAULT_PROFILE,
  )
  
  print("PersonaAgent demo. Type 'quit' to exit.\n")
  while True:
    text = input("You: ")
    if text.lower() in {"quit", "exit"}:
      print("Exiting. Goodbye!")
      break
    response = agent.react(text)
    print(f"{agent.name}: {response}\n")
    
if __name__ == "__main__":
  main()