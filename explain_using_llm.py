from openai import OpenAI
import os 

triples = [ "Albert Einstein was born in Ulm.", "Albert Einstein was awarded the Nobel Prize in 1921.", "Albert Einstein developed the theory of relativity." ]

client  = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

prompt = "Generate a paragraph based on the following RDF triples:\n" + "\n".join(triples)
print(prompt)
completion = client.chat.completions.create(
    model = "gpt-4.1",
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]
)


print(completion.choices[0].message.content)
