import pytest
from unittest.mock import Mock, patch
from rat_claude import ModelChain

# Mock responses
MOCK_DEEPSEEK_CHUNK = Mock()
MOCK_DEEPSEEK_CHUNK.choices = [
    Mock(
        delta=Mock(
            reasoning_content="This is a mock reasoning process",
            content="Final mock content"
        )
    )
]

class MockClaudeStream:
    def __init__(self):
        self.text_stream = ["Mock", " Claude", " response"]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "mock_deepseek_key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "mock_anthropic_key")

@pytest.fixture
def model_chain(mock_env_vars):
    with patch('openai.OpenAI'), patch('anthropic.Anthropic'):
        return ModelChain()

def test_model_initialization(model_chain):
    assert model_chain.current_model == "claude-3-5-sonnet-20241022"
    assert model_chain.show_reasoning is True
    assert model_chain.deepseek_messages == []
    assert model_chain.claude_messages == []

def test_set_model(model_chain):
    new_model = "test-model"
    model_chain.set_model(new_model)
    assert model_chain.current_model == new_model
    assert model_chain.get_model_display_name() == new_model

@patch('time.time', side_effect=[0, 30])  # Mock 30 seconds elapsed
def test_get_deepseek_reasoning(mock_time, model_chain):
    with patch.object(model_chain.deepseek_client.chat.completions, 'create') as mock_create:
        mock_create.return_value = [MOCK_DEEPSEEK_CHUNK]
        
        reasoning = model_chain.get_deepseek_reasoning("test input")
        
        assert reasoning == "This is a mock reasoning process"
        assert len(model_chain.deepseek_messages) == 1
        assert model_chain.deepseek_messages[0] == {
            "role": "user",
            "content": "test input"
        }

def test_get_claude_response(model_chain):
    with patch.object(model_chain.claude_client.messages, 'stream') as mock_stream:
        mock_stream.return_value = MockClaudeStream()
        
        response = model_chain.get_claude_response("test input", "test reasoning")
        
        assert response == "Mock Claude response"
        assert len(model_chain.claude_messages) == 2
        
        # Verify user message format
        assert model_chain.claude_messages[0] == {
            "role": "user",
            "content": [{"type": "text", "text": "test input"}]
        }
        
        # Verify assistant message format
        assert model_chain.claude_messages[1] == {
            "role": "assistant",
            "content": [{"type": "text", "text": "Mock Claude response"}]
        }

def test_message_history_clear(model_chain):
    # Add some messages
    model_chain.deepseek_messages = [{"role": "user", "content": "test"}]
    model_chain.claude_messages = [{"role": "user", "content": [{"type": "text", "text": "test"}]}]
    
    # Clear messages
    model_chain.deepseek_messages.clear()
    model_chain.claude_messages.clear()
    
    assert model_chain.deepseek_messages == []
    assert model_chain.claude_messages == []

def test_toggle_reasoning(model_chain):
    assert model_chain.show_reasoning is True
    model_chain.show_reasoning = False
    assert model_chain.show_reasoning is False

def test_claude_error_handling(model_chain):
    with patch.object(model_chain.claude_client.messages, 'stream', side_effect=Exception("Test error")):
        response = model_chain.get_claude_response("test input", "test reasoning")
        assert response == "Error occurred while getting response"
