"""Input validation utilities for the Council application."""


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_input(
    input_text: str,
    max_length: int = 10000,
    min_length: int = 1,
    allow_empty: bool = False
) -> str:
    """
    Validate user input text.
    
    Args:
        input_text: The input text to validate
        max_length: Maximum allowed length
        min_length: Minimum allowed length
        allow_empty: Whether to allow empty input
        
    Returns:
        Validated and sanitized input text
        
    Raises:
        ValidationError: If validation fails
    """
    if input_text is None:
        raise ValidationError("Input cannot be None")
    
    # Strip whitespace
    input_text = input_text.strip()
    
    # Check empty
    if not input_text and not allow_empty:
        raise ValidationError("Input cannot be empty")
    
    # Check length
    if len(input_text) > max_length:
        raise ValidationError(
            f"Input exceeds maximum length of {max_length} characters. "
            f"Current length: {len(input_text)}"
        )
    
    if len(input_text) < min_length and not allow_empty:
        raise ValidationError(
            f"Input must be at least {min_length} characters long. "
            f"Current length: {len(input_text)}"
        )
    
    # Basic sanity check for malicious content
    # Check for excessive newlines (potential DOS attack)
    if len(input_text) > 1000 and input_text.count('\n') > len(input_text) * 0.9:
        raise ValidationError("Input appears to be malformed (too many line breaks)")
    
    return input_text


def validate_model_config(config: dict) -> bool:
    """
    Validate model configuration.
    
    Args:
        config: Model configuration dictionary
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If validation fails
    """
    required_keys = ["name", "provider"]
    
    for key in required_keys:
        if key not in config:
            raise ValidationError(f"Model config missing required key: {key}")
    
    if not isinstance(config["name"], str) or not config["name"].strip():
        raise ValidationError("Model name must be a non-empty string")
    
    valid_providers = ["ollama", "groq", "google", "together", "cohere", "huggingface"]
    if config["provider"] not in valid_providers:
        raise ValidationError(
            f"Invalid provider: {config['provider']}. "
            f"Valid providers: {', '.join(valid_providers)}"
        )
    
    return True

