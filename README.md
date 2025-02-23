# ovos-kid-friendly-dialog-transformer

Dialog transformer for OVOS, designed to return kid-friendly responses from Ollama.

The default model to use is llama3.2, which is a 3B parameter model and has a difficult time following instructions. You will probably need to adjust your prompt for best results.

## Configuration

To enable the Kid-Friendly Dialog Transformer Plugin, add the following to your `mycroft.conf` (typically found at `~/.config/mycroft/mycroft.conf`):

```json
"dialog_transformers": {
    "ovos-kid-friendly-dialog-transformer": {
        "prompt": "Rewrite the following text to be more kid-friendly, assuming a movie rating of G. When in doubt, make it more kid-friendly. All responses should be short, concise, friendly, and helpful. Do not respond conversationally. Simply rewrite the text and add no additional commentary or prompt information. If there is no dialog, please simply say 'Hang on'. Don't mention anything about rewriting text. The dialog to rewrite is as follows:",
        "model": "llama3.2",
        "timeout": 10,
        "stream": false,
        "ollama_base_url": "http://localhost:11434"
    }
}
```

Note that these are all default values, so a minimal configuration would be:

```json
"dialog_transformers": {
    "ovos-kid-friendly-dialog-transformer": {}
}
```
