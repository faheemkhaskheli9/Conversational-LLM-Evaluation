"""Offline, deterministic conversation evaluation primitives."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Message:
    role: str
    content: str

    def __post_init__(self):
        if self.role not in {"user", "assistant", "system"}:
            raise ValueError("Unsupported role")
        if not isinstance(self.content, str):
            raise TypeError("Content must be text")

@dataclass(frozen=True)
class EndpointContract:
    message_key: str = "message"
    history_key: str = "history"
    attributes_key: str = "attributes"
    response_path: tuple[str, ...] = ("response",)

    def build(self, message: str, history: list[Message], attributes: dict) -> dict:
        keys = (self.message_key, self.history_key, self.attributes_key)
        if len(set(keys)) != 3 or not all(keys):
            raise ValueError("Request keys must be distinct and nonempty")
        return {keys[0]: message, keys[1]: [
            {"role": m.role, "content": m.content} for m in history
        ], keys[2]: dict(attributes)}

    def parse(self, payload: dict) -> str:
        value = payload
        for key in self.response_path:
            if not isinstance(value, dict) or key not in value:
                raise ValueError("Missing response path")
            value = value[key]
        if not isinstance(value, str):
            raise ValueError("Response must be text")
        return value

def evaluate(history: list[Message], required_terms: tuple[str, ...] = ()) -> dict:
    replies = [m.content for m in history if m.role == "assistant"]
    text = " ".join(replies).casefold()
    return {"assistant_turns": len(replies),
            "nonempty_ratio": sum(bool(r.strip()) for r in replies) / len(replies) if replies else None,
            "required_term_ratio": sum(t.casefold() in text for t in required_terms) / len(required_terms) if required_terms else None}
