import sys
import os
import importlib
import pkg_resources

# Function to check if a module exists
def check_module_exists(module_name):
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

# Print Python version and path
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}\n")

# Check protobuf installation
print("=== PROTOBUF INFORMATION ===")
try:
    import google.protobuf
    print(f"Protobuf version: {google.protobuf.__version__}")
    print(f"Protobuf location: {os.path.dirname(google.protobuf.__file__)}")
except ImportError:
    print("Google protobuf is not installed or cannot be imported")

# Check if builder module exists
print("\n=== CHECKING SPECIFIC MODULES ===")
print(f"google.protobuf.internal exists: {check_module_exists('google.protobuf.internal')}")
try:
    from google.protobuf.internal import builder
    print("builder module exists and can be imported")
except ImportError as e:
    print(f"builder module import error: {e}")

# List all modules in google.protobuf.internal
print("\n=== MODULES IN GOOGLE.PROTOBUF.INTERNAL ===")
try:
    import google.protobuf.internal
    internal_path = os.path.dirname(google.protobuf.internal.__file__)
    print(f"Internal modules path: {internal_path}")
    
    modules = [f for f in os.listdir(internal_path) 
              if f.endswith('.py') and not f.startswith('__')]
    print("Available modules:")
    for module in sorted(modules):
        print(f"  - {module}")
except Exception as e:
    print(f"Error listing internal modules: {e}")

# Check Streamlit installation
print("\n=== STREAMLIT INFORMATION ===")
try:
    import streamlit
    print(f"Streamlit version: {streamlit.__version__}")
    print(f"Streamlit location: {os.path.dirname(streamlit.__file__)}")
except ImportError:
    print("Streamlit is not installed or cannot be imported")

# List installed packages that might be relevant
print("\n=== INSTALLED PACKAGES ===")
relevant_packages = ['protobuf', 'streamlit', 'grpcio', 'googleapis-common-protos']
installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}

for package in relevant_packages:
    version = installed_packages.get(package, "Not installed")
    print(f"{package}: {version}")