from uuid import uuid4


def source_id() -> str:
    return f"src_{uuid4()}"
