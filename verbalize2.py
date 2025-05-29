from openai import OpenAI
import os

allCommonAxiomsSet = [
    "ObjectPropertyAssertion(<http://www.semanticweb.org/CEX-Paper#Supervises> Alice Carol)",
    "ObjectPropertyAssertion(<http://www.semanticweb.org/CEX-Paper#Publishes> Alice ML)",
    "ClassAssertion(<http://www.semanticweb.org/CEX-Paper#AI> ML)",
    "ClassAssertion(<http://www.semanticweb.org/CEX-Paper#Qualified> Alice)"
]
missingAxiomsForBob = [
    "ClassAssertion(<http://www.semanticweb.org/CEX-Paper#AI> <http://example.org/xyz>)",
    "ObjectPropertyAssertion(<http://www.semanticweb.org/CEX-Paper#Supervises> Bob <http://example.org/xyz>)",
    "ObjectPropertyAssertion(<http://www.semanticweb.org/CEX-Paper#Publishes> Bob <http://example.org/xyz>)"
]

prompt = """I ran a contrastive explanation on an OWL ontology.  
Explain in plain English:
1) Why 'Alice' satisfies the query (based on the common axioms).
2) What 'Bob' is missing in contrast.

Just explain it in 100 to 150 words. Give proper reasons for why one satisfies and the other doesn't. Also
explain what should the unsatisifed person do to make him/her qualied. Explain it in paragraphs so that it looks clean and easy to read.

Common axioms for Alice:
{common}

Missing axioms for Bob:
{missing}
""".format(
    common="\n".join(f"- {ax}" for ax in allCommonAxiomsSet),
    missing="\n".join(f"- {ax}" for ax in missingAxiomsForBob),
)

print(prompt)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
resp = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": prompt}]
)


print(resp.choices[0].message.content)
