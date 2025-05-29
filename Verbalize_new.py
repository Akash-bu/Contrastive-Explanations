from openai import OpenAI
import os

def build_ce_prompt_with_paper_context(fact_name, foil_name, fact_mappings, foil_mappings, difference_axioms):
    fact_map = "\n".join([f"- {k} → {v}" for k, v in fact_mappings.items()])
    foil_map = "\n".join([f"- {k} → {v}" for k, v in foil_mappings.items()])
    diffs = "\n".join([f"- {a}" for a in difference_axioms])

    prompt = f"""
You are given a contrastive explanation result produced from an OWL ontology using a Description Logics (DL) reasoner. This system uses logical axioms (facts and rules) to determine how concepts and individuals are classified.

The task is to explain why **one individual** (called the *fact*) is considered to belong to a certain concept class, and why **another individual** (called the *foil*) is not.

This process is modeled formally as a **Contrastive Explanation Problem (CEP)**:

⟨K, C, a, b⟩

Where:
- **K** is the knowledge base (includes both the ontology schema — TBox — and instance data — ABox)
- **C** is a complex class expression
- **a** is the individual (*fact*) such that **K ⊨ C(a)** (i.e., a satisfies C)
- **b** is the individual (*foil*) such that **K ⊭ C(b)** (i.e., b does not satisfy C)

The explanation consists of:
- A **difference pattern q₂(x⃗)**: a set of instance-level facts that apply to the fact but not the foil
- A **variable mapping σ**: mapping placeholder variables (e.g. _X0, _X3) to concrete individuals

Your job is to generate a simple, intuitive explanation in **natural language**, suitable for someone without any background in OWL, logic, or computer science.

### Instructions for Explanation:

Write **three short paragraphs**, with a line break between each:

1. Describe **why the fact qualifies** — what it has or is connected to.
2. Describe **why the foil does not qualify** — what it is missing.
3. Describe **what the foil would need** in order to be treated like the fact.

Avoid technical words like "axiom", "ontology", or "class expression". Use plain English: “has”, “lacks”, “needs”, “is connected to”, etc. Refer to individuals by their names. Treat them as real-world objects or agents.

---

### Input Details:

**Fact Individual**: {fact_name}  
**Foil Individual**: {foil_name}

**Variable Mappings for Fact**:
{fact_map}

**Variable Mappings for Foil**:
{foil_map}

**Differences (q₂)**:
{diffs}
"""
    return prompt


fact_name = "test_fo_res_proof"
foil_name = "RELAPPROXI-205"
fact_mappings = {"_X0": "fol_plus_equ", "_X3": "test_fo_res_proof"}
foil_mappings = {"_X0": "RELAPPROXI-205", "_X3": "RELAPPROXI-205"}
difference_axioms = [
    "_X3 proofLogic _X0",
    "_X0 is of type FOLogic"
]

prompt = build_ce_prompt_with_paper_context(fact_name, foil_name, fact_mappings, foil_mappings, difference_axioms)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
resp = client.chat.completions.create(
    model="o3-2025-04-16",
    messages=[{"role": "user", "content": prompt}]
)

print(resp.choices[0].message.content)
