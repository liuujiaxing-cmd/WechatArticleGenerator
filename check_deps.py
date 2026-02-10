
try:
    from volcenginesdkarkruntime import Ark
    print("✅ volcenginesdkarkruntime found")
except ImportError:
    print("❌ volcenginesdkarkruntime NOT found")

try:
    import volcengine
    print(f"✅ volcengine found: {volcengine.__file__}")
except ImportError:
    print("❌ volcengine NOT found")
