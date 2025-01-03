from anthropic import Anthropic
from openai import OpenAI
from common import RustError

from dotenv import load_dotenv
import os
from typing import List

class Provider:
    def __init__(self, provider: str = "openai", model: str = "gpt-4-turbo-preview"):
        load_dotenv()
        self.provider = provider.lower()
        self.model = model
        
        # Get the appropriate API key based on provider
        if self.provider == "openai":
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            self.client = OpenAI(api_key=self.api_key)
        elif self.provider == "anthropic":
            self.api_key = os.getenv("ANTHROPIC_API_KEY")
            if not self.api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
            self.client = Anthropic(api_key=self.api_key)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        
    def get_response(self, prompt: str) -> str:
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        
        elif self.provider == "anthropic":
            response = self.client.messages.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024
            )
            return response.content[0].text
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
        
    def fix_code(self, code: str, errors: List[RustError]) -> str:
        # prompt = f"Fix this Rust code that has the following compiler \
        #     errors:\n\n{errors}\n\nRequirements:\n- Fix all errors\n- \
        #     Follow Rust idioms and formatting standards\n- Use proper error \
        #     handling\n- Add documentation where needed\n\nReturn:\n- Fixed \
        #     code with brief comments\n- Summary of key changes"
        prompt = f"{code}\n\nFix this Rust code that has the following compiler errors:\n\n{errors}\n\nRequirements:\n- Fix all errors\n- Follow basic Rust idioms\n- Focus on simplicity over abstraction\n\nReturn code with brief comments on changes made"
        return self.get_response(prompt)