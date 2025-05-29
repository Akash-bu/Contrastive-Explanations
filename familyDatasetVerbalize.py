from openai import OpenAI
import os

allCommonAxiomsSet = [
"ClassAssertion(<http://www.benchmark.org/family#Sister> <http://www.benchmark.org/family#F10F195>)", 
"ClassAssertion(<http://www.benchmark.org/family#Mother> <http://www.benchmark.org/family#F10F195>)", 
"ClassAssertion(<http://www.benchmark.org/family#Daughter> <http://www.benchmark.org/family#F10F195>)"
]

MissingAxioms = [
"ClassAssertion(<http://www.benchmark.org/family#Sister> <http://www.benchmark.org/family#F10F198>)", 
"ClassAssertion(<http://www.benchmark.org/family#Daughter> <http://www.benchmark.org/family#F10F198>)"
]

prompt = """I ran a contrastive explanation on an OWL ontology using pellet reasoner. I got a Decription Logics output explaining the output.  
I want you to explain the DL output in simple plain English so that a common person without any technical knowledge of DL understands your explanations without any difficulty.
1) Why one person satisfies a query (based on the common axioms).
2) What the other person is missing in contrast.

Just explain it in less than 100 words. Give proper reasons for why one satisfies and the other doesn't. Also
explain what should the unsatisifed person do to make him/her qualified. Explain it in paragraphs so that it looks clean and easy to read.

Split it into 3 sentences. First, explaining qualifying person. Second, explaining contrastive person and the third, explaining what the contrastive person must have so that he is considered into allCommonAxiomsSet.
Give a space after each paragraph. Mark instances as bold characters.

Dont add any extra sentences like "sure here is the explanations" etc. Just explain and end it. Dont use any ** or anything similar.
Common axioms:
{common}

Missing axioms:
{missing}
""".format(
    common="\n".join(f"- {ax}" for ax in allCommonAxiomsSet),
    missing="\n".join(f"- {ax}" for ax in MissingAxioms),
)


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
resp = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": prompt}]
)


print(resp.choices[0].message.content)
