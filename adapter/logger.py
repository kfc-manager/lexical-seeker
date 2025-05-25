class Logger:
    def __init__(self, prefix: str):
        self._prefix = prefix

    def log(self, message: str):
        print(f"[ERROR] ({self._prefix}) - {message}")
