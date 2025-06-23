import hmac
import hashlib
import base64
import re
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY").encode("utf-8")

def generate_code_max_secure(enterprise_id: int, name: str) -> str:
    clean_name = re.sub(r'[^a-zA-Z0-9]', '', name).lower()
    timestamp = datetime.utcnow().isoformat()
    random_uuid = uuid.uuid4().hex

    message = f"{enterprise_id}:{clean_name}:{timestamp}:{random_uuid}".encode()
    hmac_digest = hmac.new(SECRET_KEY, message, hashlib.sha256).digest()

    code = base64.b32encode(hmac_digest).decode("utf-8")
    return f"ENT-{code[:20]}"
