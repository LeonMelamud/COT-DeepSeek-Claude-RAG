import pytest
from unittest.mock import Mock, patch
from rat.rat import ModelChain

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

MOCK_OPENROUTER_CHUNK = Mock()
MOCK_OPENROUTER_CHUNK.choices = [
    Mock(
        delta=Mock(
            content="Mock OpenRouter response"
        )
    )
]

@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "mock_deepseek_key")
    monkeypatch.setenv("OPENROUTER_API_KEY", "mock_openrouter_key")

@pytest.fixture
def model_chain(mock_env_vars):
    with patch('openai.OpenAI'):
        return ModelChain()

def test_model_initialization(model_chain):
    assert model_chain.current_model == "openai/gpt-4o-mini"
    assert model_chain.show_reasoning is True
    assert model_chain.deepseek_messages == []
    assert model_chain.openrouter_messages == []

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

def test_get_openrouter_response(model_chain):
    with patch.object(model_chain.openrouter_client.chat.completions, 'create') as mock_create:
        mock_create.return_value = [MOCK_OPENROUTER_CHUNK]
        
        response = model_chain.get_openrouter_response("test input", "test reasoning")
        
        assert response == "Mock OpenRouter response"
        assert len(model_chain.openrouter_messages) == 2
        assert model_chain.openrouter_messages[0] == {
            "role": "user",
            "content": "<question>test input</question>\n\n<thinking>test reasoning</thinking>\n\n"
        }
        assert model_chain.openrouter_messages[1] == {
            "role": "assistant",
            "content": "Mock OpenRouter response"
        }

def test_invalid_deepseek_key():
    with patch('os.getenv', return_value="your_deepseek_api_key_here"):
        with pytest.raises(ValueError) as exc_info:
            ModelChain()
        assert "Invalid or missing DEEPSEEK_API_KEY" in str(exc_info.value)

def test_invalid_openrouter_key():
    with patch('os.getenv', side_effect=["valid_deepseek_key", "your_openrouter_api_key_here"]):
        with pytest.raises(ValueError) as exc_info:
            ModelChain()
        assert "Invalid or missing OPENROUTER_API_KEY" in str(exc_info.value)

def test_message_history_clear(model_chain):
    # Add some messages
    model_chain.deepseek_messages = [{"role": "user", "content": "test"}]
    model_chain.openrouter_messages = [{"role": "user", "content": "test"}]
    
    # Clear messages
    model_chain.deepseek_messages.clear()
    model_chain.openrouter_messages.clear()
    
    assert model_chain.deepseek_messages == []
    assert model_chain.openrouter_messages == []

def test_toggle_reasoning(model_chain):
    assert model_chain.show_reasoning is True
    model_chain.show_reasoning = False
    assert model_chain.show_reasoning is False
