from contextvars import ContextVar, Token

# The ContextVar object `SESSION_CONTEXT` is a context variable that stores the unique session id
# (which is generated at each request by uuid.uuid4).
SESSION_CONTEXT: ContextVar[str] = ContextVar("session_context")

# The ContextVar object `NESTED_CONTEXT` is a context variable that stores the nested count
# associated with each unique session id.
NESTED_CONTEXT: ContextVar[int] = ContextVar("nested_context")


def get_current_context_session_id() -> str:
    """
    Fetches the current context session id stored in the SESSION_CONTEXT variable.

    Returns:
        str: The current session id.
    """
    return SESSION_CONTEXT.get()


def set_current_context_session_id(session_id: str) -> Token:
    """
    Sets a new session id in the SESSION_CONTEXT variable.

    Args:
        session_id (str): The new session id to be set.

    Returns:
        Token: The token representing the new state of the SESSION_CONTEXT.
    """
    return SESSION_CONTEXT.set(session_id)


def get_current_context_nested_count() -> int:
    """
    Fetches the current nested count stored in the NESTED_CONTEXT variable.

    Returns:
        int: The current nested count.
    """
    return NESTED_CONTEXT.get()


def set_current_context_nested_id(nested_context_id: int) -> Token:
    """
    Sets a new nested context id in the NESTED_CONTEXT variable.

    Args:
        nested_context_id (int): The new nested context id to be set.

    Returns:
        Token: The token representing the new state of the NESTED_CONTEXT.
    """
    return NESTED_CONTEXT.set(nested_context_id)


def increase_current_context_nested_count():
    """
    Increases the current nested count by 1 stored in the NESTED_CONTEXT variable.
    """
    current_val = NESTED_CONTEXT.get()
    NESTED_CONTEXT.set(current_val + 1)


def decrease_current_context_nested_count():
    """
    Decreases the current nested count by 1 stored in the NESTED_CONTEXT variable.
    Raises ValueError if the current nested count is already 0.
    """
    current_val = NESTED_CONTEXT.get()
    if current_val == 0:
        raise ValueError("Nested transaction count can't be negative.")
    NESTED_CONTEXT.set(current_val - 1)
