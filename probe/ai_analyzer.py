# universal_connector/probe/ai_analyzer.py
import os, json
try:
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")
except ImportError:
    openai = None

def analyze_with_ai(src_schema, dst_schema) -> dict:
    """
    If OpenAI is configured, attempt a schema analysis;
    otherwise return a minimal default.
    """
    if openai and openai.api_key:
        prompt = (
            f"Given these API schemas:\nSRC: {json.dumps(src_schema)}\n"
            f"DST: {json.dumps(dst_schema)}\n"
            "Return JSON with operations, auth type, fieldMappings."
        )
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role":"user","content":prompt}]
            )
            return json.loads(resp.choices[0].message.content)
        except Exception as e:
            print("AI analyzer failed, falling back:", e)

    # Fallback default
    return {
        "auth": {},
        "fieldMappings": {}
    }
