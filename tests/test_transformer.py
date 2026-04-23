from unittest.mock import Mock, patch

import pytest
import requests

from ovos_kid_friendly_dialog_transformer import KidFriendlyDialogTransformer


@pytest.fixture
def transformer():
    """Create a basic transformer instance for testing."""
    return KidFriendlyDialogTransformer()


@pytest.fixture
def custom_transformer():
    """Create a transformer with custom config."""
    config = {
        "timeout": 20,
        "stream": True,
        "ollama_base_url": "http://custom:11434",
        "prompt": "Custom prompt: ",
        "model": "custom-model",
    }
    return KidFriendlyDialogTransformer(config=config)


def test_default_config(transformer):
    """Test default configuration values."""
    assert transformer.timeout == 10
    assert transformer.stream is False
    assert transformer.ollama_base_url == "http://localhost:11434"
    assert "kid-friendly" in transformer.prompt.lower()
    assert transformer.model == "llama3.2"


def test_custom_config(custom_transformer):
    """Test custom configuration values."""
    assert custom_transformer.timeout == 20
    assert custom_transformer.stream is True
    assert custom_transformer.ollama_base_url == "http://custom:11434"
    assert custom_transformer.prompt == "Custom prompt: "
    assert custom_transformer.model == "custom-model"


def test_empty_dialog(transformer):
    """Test handling of empty dialog."""
    dialog, context = transformer.transform("", {})
    assert dialog == ""
    assert context == {}

    dialog, context = transformer.transform("   ", {})
    assert dialog == "   "
    assert context == {}


def test_context_prompt_override(transformer):
    """Test that context can override default prompt."""
    with patch("requests.post") as mock_post:
        mock_response = Mock()
        mock_response.json.return_value = {"response": "transformed"}
        mock_post.return_value = mock_response

        context = {"prompt": "Custom prompt override"}
        dialog, new_context = transformer.transform("test", context)

        assert mock_post.call_args[1]["json"]["prompt"] == "Custom prompt override\n\n test"
        assert new_context == context


@patch("requests.post")
def test_successful_transformation(mock_post, transformer):
    """Test successful dialog transformation."""
    mock_response = Mock()
    mock_response.json.return_value = {"response": "kid friendly version"}
    mock_post.return_value = mock_response

    dialog, context = transformer.transform("original text", {})

    assert dialog == "kid friendly version"
    assert context == {}
    mock_post.assert_called_once()


@patch("requests.post")
def test_transformation_failure_returns_original(mock_post, transformer):
    """Test that original dialog is returned on transformation failure."""
    mock_post.side_effect = requests.exceptions.RequestException()

    original = "original text"
    dialog, context = transformer.transform(original, {})

    assert dialog == original
    assert context == {}


@patch("requests.post")
def test_invalid_response_format(mock_post, transformer):
    """Test handling of invalid response format."""
    mock_response = Mock()
    mock_response.json.return_value = {"invalid": "response"}
    mock_post.return_value = mock_response

    original = "original text"
    dialog, context = transformer.transform(original, {})

    assert dialog == original
    assert context == {}


@patch("requests.post")
def test_request_parameters(mock_post, transformer):
    """Test that correct parameters are sent to Ollama service."""
    mock_response = Mock()
    mock_response.json.return_value = {"response": "transformed"}
    mock_post.return_value = mock_response

    transformer.transform("test dialog", {})

    call_kwargs = mock_post.call_args[1]
    assert call_kwargs["timeout"] == transformer.timeout
    assert call_kwargs["stream"] == transformer.stream
    assert "json" in call_kwargs
    assert call_kwargs["json"]["model"] == transformer.model


def test_exception_logging(transformer):
    """Test that exceptions are properly logged."""
    with patch("ovos_utils.log.LOG.exception") as mock_log, patch("requests.post") as mock_post:
        mock_post.side_effect = Exception("Test error")

        transformer.transform("test", {})

        mock_log.assert_called_once_with("Error getting spoken answer from Ollama: Test error")
