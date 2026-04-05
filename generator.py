import os
from groq import Groq
from typing import List

# ==============================
# CONFIG
# ==============================
MODEL = "llama-3.3-70b-versatile"
MAX_QUERIES = 5

# ==============================
# INIT CLIENT
# ==============================
def init_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("❌ GROQ_API_KEY not found in environment variables")
    return Groq(api_key=api_key)

# ==============================
# CORE FUNCTION
# ==============================
def generate_queries(client: Groq, product: str) -> List[str]:
    prompt = f"""
You are an elite SEO strategist trained on real human search behavior.

Generate {MAX_QUERIES} ultra-realistic Google search queries for:
"{product}"

STRICT RULES:
- Include 1 query with a common typo
- Include 1 comparison with a trending 2026 competitor
- Include 1 high-buying-intent query
- Make them look human (not robotic)
- Short, natural, and clickable
- No numbering, no explanations

Output only queries (one per line)
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You simulate real human search intent."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        content = response.choices[0].message.content.strip()

        # Clean output
        queries = [q.strip("-• ").strip() for q in content.split("\n") if q.strip()]
        return queries

    except Exception as e:
        print(f"❌ Error generating queries for {product}: {e}")
        return []

# ==============================
# MULTI PRODUCT PIPELINE
# ==============================
def generate_for_products(products: List[str]):
    client = init_client()

    all_results = {}

    for product in products:
        print(f"\n🔍 Generating for: {product}")
        queries = generate_queries(client, product)

        for q in queries:
            print(f"  → {q}")

        all_results[product] = queries

    return all_results

# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    products = [
        "Dyson Airwrap i.d.",
        "Shark FlexStyle",
        "GHD Duet Style"
    ]

    results = generate_for_products(products)
