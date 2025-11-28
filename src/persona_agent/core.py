from typing import Dict, Any, Optional

from .memory import Memory, InMemoryMemory, Interaction
from .skills import SkillRegistry, SkillFn
from .models import ModelCallable
from .profiles import DEFAULT_PROFILE

class PersonaAgent:
  """
  A configurable, persona-based LLM agent with memory and skills.
  """
  
  def __init__(
    self,
    name: str,
    model: ModelCallable,
    memory: Optional[Memory] = None,
    skills: Optional[SkillRegistry] = None,
    persona: Optional[Dict[str, Any]] = None,
  ):
    self.name = name
    self.model = model
    self.memory = memory or InMemoryMemory()
    self.skills = skills or SkillRegistry()
    self.persona = persona or DEFAULT_PROFILE
    
  # --- Memory helpers ---
  
  def _remember_user(self, content: str) -> None:
    self.memory.add(Interaction(role="user", content=content))
    
  def _remember_agent(self, content: str) -> None:
    self.memory.add(Interaction(role=self.name, content=content))
    
  # --- Skills API ---
  
  def add_skill(self, name: str, fn: SkillFn) -> None:
    self.skills.add_skill(name, fn)
    
  def call_skill(self, name: str, *args, **kwargs) -> Any:
    return self.skills.call(name, *args, **kwargs)
    
  # --- Prompt construction ---
  
  def _build_system_prompt(self) -> str:
    persona_desc = (
      f"You are {self.name}, a persona-based LLM agent.\n"
      f"Role: {self.persona.get('role', 'an AI agent')}\n"
      f"Personality: {self.persona.get('personality', 'neutral')}\n"
      f"Style: {self.persona.get('style', 'clear and concise')}\n"
      f"Goals: {', '.join(self.persona.get('goals', []))}\n"
      f"Domain: {self.persona.get('domain', 'general')}\n\n"
    )
    guideline = (
      "Always respond according to the persona described above. "
      "Be explicit when you are uncertain. "
      "Do not claim abilities you do not have.\n"
    )
    return persona_desc + guideline
  
  def _build_full_prompt(self, user_input: str, memory_k: int = 5) -> str:
    system_prompt = self._build_system_prompt()
    memory_text = self.memory.as_text(memory_k)
    return (
      f"{system_prompt}\n\n"
      f"Recent conversation:\n{memory_text}\n\n"
      f"User: {user_input}\n\n"
      f"Respond as {self.name}:"
    )
    
  # --- Interaction ---
  
  def react(self, user_input: str, memory_k: int = 5, **model_kwargs) -> str:
    """
    Main entry point: takes user input, builds a persona-aware prompt, calls the model, updates memory, and returns the response.
    """
    prompt = self._build_full_prompt(user_input, memory_k)
    response = self.model(prompt, **model_kwargs)
    self._remember_user(user_input) # Do NOT put this before building the prompt to avoid duplication in prompt
    self._remember_agent(response)
    return response