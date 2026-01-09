import sys
import os

# Add current directory to path to allow imports from app
sys.path.append(os.getcwd())

try:
    from app.services.ai import generate_variant
    print("Successfully imported generate_variant")
    
    # Check for API Key
    if not os.environ.get("GEMINI_API_KEY"):
        print("WARNING: GEMINI_API_KEY is not set in environment variables.")
        # We can't proceed with actual generation without key, but we verified import.
    else:
        print("GEMINI_API_KEY found. Attempting generation...")
        result = generate_variant("二次関数 f(x) = x^2 + 2x + 1 の頂点を求めよ。", "math")
        print("Generation successful!")
        print("Result:", result)

except Exception as e:
    print(f"Error occurred: {e}")
