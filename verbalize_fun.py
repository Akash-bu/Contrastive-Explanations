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

def generate_contrastive_explanations(common_axioms, missing_axioms, satisfied, unsatisfied):
        prompt = f"""I ran a contrastive explanation on an OWL ontology.  
        Explain in plain English:
        1) Why '{satisfied}' satisfies the query (based on the common axioms).
        2) What '{unsatisfied}' is missing in contrast.

        Just explain it in 100 to 150 words. Give proper reasons for why one satisfies and the other doesn't. Also
        explain what should the unsatisfied person do to become qualified. Explain it in paragraphs so that it looks clean and easy to read.

        Common axioms for {satisfied}:
        {"\n".join(f"- {ax}" for ax in common_axioms)}

        Missing axioms for {unsatisfied}:
        {"\n".join(f"- {ax}" for ax in missing_axioms)}
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

print(generate_contrastive_explanations(allCommonAxiomsSet, missingAxiomsForBob, "Alice", "Bob"))
