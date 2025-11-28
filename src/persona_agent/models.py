from typing import Protocol

class ModelCallable(Protocol):
  def __call__(self, prompt: str, **kwargs) -> str:
    ...