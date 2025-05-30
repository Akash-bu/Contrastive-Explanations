from openai import OpenAI
import os
import re

# def build_ce_prompt_with_paper_context(prompt, fact_name, foil_name, fact_mappings, foil_mappings, difference_axioms):
#     fact_map = "\n".join([f"- {k} → {v}" for k, v in fact_mappings.items()])
#     foil_map = "\n".join([f"- {k} → {v}" for k, v in foil_mappings.items()])
#     diffs = "\n".join([f"- {a}" for a in difference_axioms])
#     prompt += f"""
#
#     \n**Fact Individual**: {fact_name}
#     **Foil Individual**: {foil_name}
#
#     **Variable Mappings for Fact**:
#     {fact_map}
#
#     **Variable Mappings for Foil**:
#     {foil_map}
#
#     **Differences (q₂)**:
#     {diffs}
#     """
#
#     return prompt

def extract_all_fact_foil_blocks(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    blocks = []
    current_block = {
        "fact_name": None,
        "foil_name": None,
        "fact_mappings": {},
        "foil_mappings": {},
        "difference_axioms": []
    }

    for line in lines:
        line = line.strip()

        if "Fact:" in line:
            fact_match = re.search(r"Fact:\s*([^,]+)", line)
            if fact_match:
                current_block["fact_name"] = fact_match.group(1).strip()

        if "Foil:" in line:
            foil_match = re.search(r"Foil:\s*([^\s,]+)", line)
            if foil_match:
                current_block["foil_name"] = foil_match.group(1).strip()

        elif line.startswith("Fact mapping:"):
            pairs = line.split("Fact mapping:")[1].strip().split(", ")
            for pair in pairs:
                if "->" in pair:
                    var, val = pair.split("->")
                    current_block["fact_mappings"][var.strip()] = val.strip()

        elif line.startswith("Foil mapping:"):
            pairs = line.split("Foil mapping:")[1].strip().split(", ")
            for pair in pairs:
                if "->" in pair:
                    var, val = pair.split("->")
                    current_block["foil_mappings"][var.strip()] = val.strip()

        elif line.startswith("Different:"):
            diff = line.split("Different:")[1].strip()
            if diff:
                current_block["difference_axioms"].append(diff)

        elif line.startswith("Conflicts:"):
            blocks.append(current_block)
            current_block = {
                "fact_name": None,
                "foil_name": None,
                "fact_mappings": {},
                "foil_mappings": {},
                "difference_axioms": []
            }

    if current_block["fact_name"] or current_block["foil_name"]:
        blocks.append(current_block)

    return blocks


# Example usage
if __name__ == "__main__":

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

    And finally "Explain ALL THE BLOCKS NOT JUST 1".

    ### Input Details:

    """

    results = extract_all_fact_foil_blocks("ore_ont_16723.owl.log")
    for i, block in enumerate(results):
        prompt += f"\n--- Block {i+1} ---\n"
        prompt += str(block)

#     print(prompt)

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.chat.completions.create(
        model="o3-2025-04-16",
        messages=[{"role": "user", "content": prompt}]
    )

    with open("output.txt", "w",encoding="utf-8") as file:
        file.write(resp.choices[0].message.content)