from typing import Protocol

class ModelCallable(Protocol):
  def __call__(self, prompt: str, **kwargs) -> str:
    ...
    
def make_litellm_chat_model(
  model_name: str = "openai/gpt-4o-mini",
  **default_kwargs,
) -> ModelCallable:
  """
  Create a chat model callable using LiteLLM.
  
  Example:
    chat_model = make_litellm_chat_model(
      model_name="openai/gpt-4o-mini",
      temperature=0.2,
      max_tokens=512,
    )
    response = chat_model("Hello, how are you?")
  """
  from litellm import completion, CustomStreamWrapper, StreamingChoices # Import here to avoid hard dependency
  
  def _call(prompt: str, **kwargs) -> str:
    combined_kwargs = {**default_kwargs, **kwargs, "stream": False} # Ensure stream is False for simplicity
    response = completion(
      model=model_name,
      messages=[
        {"role": "user", "content": prompt} # We treat the entire prompt as a user message
      ],
      **combined_kwargs
    )
    if isinstance(response, CustomStreamWrapper) or isinstance(response.choices[0], StreamingChoices): # Hypothetical check for streaming
      raise ValueError("Streaming responses are not supported in this callable.")
    
    # LiteLLM guarantees OpenAI-style response structure
    message = response.choices[0].message
    # message can be a dict or object with .content; handle both
    content = getattr(message, "content", None)
    if content is None and isinstance(message, dict):
      content = message.get("content", "")
    return content or ""
  return _call