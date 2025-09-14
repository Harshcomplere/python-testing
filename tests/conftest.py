import sys
import os

# This ensures the root of your repo is added to the Python path before tests run
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


print("File path:", __file__)
print("Dirname:", os.path.dirname(__file__))
print("Parent dir:", os.path.join(os.path.dirname(__file__), ".."))
print("Absolute path:", os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

print("Final path:", sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))))
print("Python path:", sys.path[:3])  # show first 3 entries

