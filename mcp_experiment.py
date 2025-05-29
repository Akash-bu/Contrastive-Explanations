import json
import hashlib
from openai import OpenAI
import os

allCommonAxiomsSet = [
    "ObjectPropertyAssertion(<http://www.semanticweb.org/CEX-Paper#Supervises> Alice Carol)",
    "ObjectPropertyAssertion(<http://www.semanticweb.org/CEX-Paper#Publishes> Alice ML)",
    "ClassAssertion(<http://www.semanticweb.org/CEX-Paper#AI> ML)",
    "ClassAssertion(<http://www.semanticweb.org/CEX-Paper#Qualified> Alice)"
]

missingAxioms = [
    "ClassAssertion(<http://www.semanticweb.org/CEX-Paper#AI> <http://example.org/xyz>)",
    "ObjectPropertyAssertion(<http://www.semanticweb.org/CEX-Paper#Supervises> Bob <http://example.org/xyz>)",
    "ObjectPropertyAssertion(<http://www.semanticweb.org/CEX-Paper#Publishes> Bob <http://example.org/xyz>)"
]

alice_data = {
    "individual": "Alice",
    "allCommonAxiomsSet": allCommonAxiomsSet
}

bob_data = {
    "individual": "Bob",
    "missingAxioms": missingAxioms
}

with open("alice_common.json", "w") as f:
    json.dump(alice_data, f, indent = 2)

with open("bob_missing.json", "w") as f:
    json.dump(bob_data, f, indent = 2)

def mcp_hash(file_path):
    with open(file_path, "rb") as f:
        content= f.read()
    return "context://" + hashlib.sha256(content).hexdigest()

print("Alice: ", mcp_hash("alice_common.json"))
print("Bob: ",mcp_hash("bob_missing.json"))

prompt = "Explain why Alice satisfies the query and what Bob is missing in contrast."
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
resp = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": prompt}],
    context = [
        mcp_hash("alice_common.json"),
        mcp_hash("bob_missing.json")
    ] 
)

print(resp.choices[0].message.content)