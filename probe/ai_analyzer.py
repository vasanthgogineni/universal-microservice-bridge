import openai, json
openai.api_key = ""

def analyze_with_ai(src_schema, dst_schema):
    prompt = f"Given these schemas:\nSRC: {src_schema}\nDST: {dst_schema}\nOutput JSON with operations, auth, mappings."
    resp = openai.ChatCompletion.create(model="gpt-4", messages=[{"role":"user","content":prompt}])
    return json.loads(resp.choices[0].message.content)
