import os
import sys

# DEBUG: Stampa i percorsi nel log per vedere cosa vede Flask
print(f"DEBUG: Current working directory: {os.getcwd()}")
print(f"DEBUG: Template folder path: {os.path.join('/home/marcomanzo/webapp-autismo', 'templates')}")
print(f"DEBUG: Files in templates: {os.listdir(os.path.join('/home/marcomanzo/webapp-autismo', 'templates'))}")
