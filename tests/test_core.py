from persona_agent import PersonaAgent, DEFAULT_PROFILE

def test_persona_agent_basic():
  def mock_model(prompt: str, **kwargs) -> str:
    assert "You are" in prompt
    assert "Role:" in prompt
    return "Hello from mock model."
  
  agent = PersonaAgent(
    name="TestAgent",
    model=mock_model,
    persona=DEFAULT_PROFILE,
  )
  
  response = agent.react("Hello, agent!")
  assert response == "Hello from mock model."
  # Memory should have two interactions now
  interactions = agent.memory.recent(2)
  assert len(interactions) == 2
  assert interactions[0].role == "user"
  assert interactions[0].content == "Hello, agent!"
  assert interactions[1].role == "TestAgent"
  assert interactions[1].content == "Hello from mock model."
  