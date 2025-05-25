import os
from typing import List


class Storage:
    def __init__(self, folder_path: str):
        self._path = os.path.abspath(folder_path)
        os.makedirs(self._path, exist_ok=True)

    def put(self, key: str, data: str):
        file_path = os.path.join(self._path, key)
        with open(file_path, "wb") as f:
            f.write(data.encode("utf-8"))

    def get(self, key: str) -> str:
        file_path = os.path.join(self._path, key)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No such key: {key}")
        with open(file_path, "r", encoding="utf-8") as f:
            return f

    def list(self, relative: bool = False) -> List[str]:
        file_list = []
        for dirpath, _, filenames in os.walk(self._path):
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                if relative:
                    path = os.path.relpath(path, self._path)
                file_list.append(path)
        return file_list
