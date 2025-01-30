def validate_model_available(model_name: str) -> bool:
    try:
        ollama.show(model_name)
        return True
    except:
        return False
    