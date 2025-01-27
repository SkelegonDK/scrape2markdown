# model_context.py
DEFAULT_CONTEXT_SIZE = 128000  # Default to maximum available

MODEL_CONTEXTS = {
    # All models default to maximum context unless specifically limited
    "llava:7b-v1.6": 4096,  # Known limited context
    "phi4:latest": 8192,  # Known limited context
    "nomic-embed-text:latest": 8192,  # Embedding model
}


def get_model_context(model_name):
    """Get the context size for a given model"""
    # Use specific limits only for known restricted models
    if model_name in MODEL_CONTEXTS:
        return MODEL_CONTEXTS[model_name]

    # Default to maximum context for all other models
    return DEFAULT_CONTEXT_SIZE
