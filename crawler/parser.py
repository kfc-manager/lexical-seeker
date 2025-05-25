import hashlib
from typing import List
from bs4 import BeautifulSoup
from adapter.logger import Logger


class Parser:
    def __init__(self, strip: List[str] = []):
        self._strip = strip
        self._logger = Logger("parser")

    def parse(self, html: str) -> str:
        try:
            soup = BeautifulSoup(html, "html.parser")
            full_text = ""

            for p in soup.find_all("p"):
                # ignore paragraphs found in tables as they
                # destroy the text flow
                if p.find_parent("table"):
                    continue
                # handle super scripts
                for sup in p.find_all("sup"):
                    sup_text = sup.get_text()
                    # remove references
                    if "[" in sup_text or "]" in sup_text:
                        sup.decompose()
                    # signal super script with ^
                    else:
                        sup.replace_with(f"^{sup_text}")
                full_text += p.get_text()
        except Exception as e:
            self._logger.log(f"exception parsing html: {e}")

        # strip specified substrings
        for substring in self._strip:
            full_text = full_text.replace(substring, "")
        return full_text

    def hash(self, text: str) -> str:
        hash = hashlib.sha256(text.encode("utf-8"))
        return hash.hexdigest()
