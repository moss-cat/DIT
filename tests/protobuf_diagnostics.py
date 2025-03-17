import sys
import os
import importlib
import pkg_resources

<<<<<<< HEAD

=======
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
# Function to check if a module exists
def check_module_exists(module_name):
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

<<<<<<< HEAD

=======
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
# Print Python version and path
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}\n")

# Check protobuf installation
print("=== PROTOBUF INFORMATION ===")
try:
    import google.protobuf
<<<<<<< HEAD

=======
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
    print(f"Protobuf version: {google.protobuf.__version__}")
    print(f"Protobuf location: {os.path.dirname(google.protobuf.__file__)}")
except ImportError:
    print("Google protobuf is not installed or cannot be imported")

# Check if builder module exists
print("\n=== CHECKING SPECIFIC MODULES ===")
<<<<<<< HEAD
print(
    f"google.protobuf.internal exists: {check_module_exists('google.protobuf.internal')}"
)
try:
    from google.protobuf.internal import builder

=======
print(f"google.protobuf.internal exists: {check_module_exists('google.protobuf.internal')}")
try:
    from google.protobuf.internal import builder
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
    print("builder module exists and can be imported")
except ImportError as e:
    print(f"builder module import error: {e}")

# List all modules in google.protobuf.internal
print("\n=== MODULES IN GOOGLE.PROTOBUF.INTERNAL ===")
try:
    import google.protobuf.internal
<<<<<<< HEAD

    internal_path = os.path.dirname(google.protobuf.internal.__file__)
    print(f"Internal modules path: {internal_path}")

    modules = [
        f
        for f in os.listdir(internal_path)
        if f.endswith(".py") and not f.startswith("__")
    ]
=======
    internal_path = os.path.dirname(google.protobuf.internal.__file__)
    print(f"Internal modules path: {internal_path}")
    
    modules = [f for f in os.listdir(internal_path) 
              if f.endswith('.py') and not f.startswith('__')]
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
    print("Available modules:")
    for module in sorted(modules):
        print(f"  - {module}")
except Exception as e:
    print(f"Error listing internal modules: {e}")

# Check Streamlit installation
print("\n=== STREAMLIT INFORMATION ===")
try:
    import streamlit
<<<<<<< HEAD

=======
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
    print(f"Streamlit version: {streamlit.__version__}")
    print(f"Streamlit location: {os.path.dirname(streamlit.__file__)}")
except ImportError:
    print("Streamlit is not installed or cannot be imported")

# List installed packages that might be relevant
print("\n=== INSTALLED PACKAGES ===")
<<<<<<< HEAD
relevant_packages = ["protobuf", "streamlit", "grpcio", "googleapis-common-protos"]
=======
relevant_packages = ['protobuf', 'streamlit', 'grpcio', 'googleapis-common-protos']
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}

for package in relevant_packages:
    version = installed_packages.get(package, "Not installed")
<<<<<<< HEAD
    print(f"{package}: {version}")
=======
    print(f"{package}: {version}")
>>>>>>> 2c70e2e173fc9249e33d250b2482cc5e5dcd3211
