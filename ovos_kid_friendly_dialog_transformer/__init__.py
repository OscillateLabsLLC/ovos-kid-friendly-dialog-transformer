from typing import Optional, Tuple

import requests
from ovos_plugin_manager.templates.transformers import DialogTransformer
from ovos_utils.log import LOG

from .version import __version__


__all__ = ["KidFriendlyDialogTransformer", "__version__"]


class KidFriendlyDialogTransformer(DialogTransformer):
    """OVOS Dialog Transformer plugin to make dialog more kid-friendly using an Ollama service."""

    def __init__(self, name="ovos-kid-friendly-dialog-transformer", priority=10, config=None):
        super().__init__(name=name, priority=priority, config=config)
        LOG.debug("Loaded with config: %s", self.config)

    @property
    def timeout(self):
        """Timeout for requests to the Ollama service. Increase if Ollama is running on slow hardware."""
        return self.config.get("timeout", 10)

    @property
    def stream(self):
        """Whether to stream the response from the Ollama service."""
        return self.config.get("stream", False)

    @property
    def ollama_base_url(self):
        """Base URL for the Ollama service the plugin should use."""
        return self.config.get("ollama_base_url", "http://localhost:11434")

    @property
    def prompt(self):
        """Prompt to use for the Ollama service."""
        default_prompt = (
            "Rewrite the following text to be more kid-friendly, assuming a movie rating of G. "
            "When in doubt, make it more kid-friendly. All responses should be short, "
            "concise, friendly, and helpful. Do not respond conversationally. Simply rewrite the text "
            "and add no additional commentary or prompt information. If there is no dialog, please "
            "simply say 'Hang on'. Don't mention anything about rewriting text. "
            "The dialog to rewrite is as follows:"
        )
        return self.config.get("prompt", default_prompt)

    @property
    def model(self):
        """Model to use for the Ollama service."""
        return self.config.get("model", "llama3.2")

    def transform(self, dialog: str, context: Optional[dict] = None) -> Tuple[str, dict]:
        """Transform dialog to be kid-friendly."""
        if not dialog or not dialog.strip():
            return dialog, context or {}

        context = context if context is not None else {}
        prompt = context.get("prompt") or self.prompt

        try:
            return self._get_spoken_answer(prompt, dialog), context
        except Exception as e:
            LOG.error(f"Failed to transform dialog: {e}")
            return dialog, context

    def _get_spoken_answer(self, prompt, dialog):
        """Get a spoken answer from the Ollama service."""
        payload = {"prompt": prompt + "\n\n " + dialog, "stream": self.stream, "model": self.model}
        LOG.debug(f"Getting spoken answer from Ollama: {payload}")
        try:
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json=payload,
                timeout=self.timeout,
                stream=self.stream,
            )
            response.raise_for_status()
            return response.json().get("response", dialog)
        except Exception as e:
            LOG.exception(f"Error getting spoken answer from Ollama: {e}")
            return dialog
