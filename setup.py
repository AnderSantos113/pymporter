import os
from setuptools import setup, find_packages

# Leer el README.md automáticamente para que PyPI lo muestre en tu página
here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Lightweight module to install and import runtime requirements from a requirements file."

setup(
    name="pymporter",
    version="1.0.0",  
    description="Dynamic requirements loader for Python projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",  
    author="Ander Emiliano Santos Ponce",
    author_email="ander.santos4134@alumnos.udg.mx",
    url="https://github.com/AnderSantos113/pymporter",
    
    packages=find_packages(), 
    
    python_requires=">=3.8",

    classifiers=[
        "Development Status :: 5 - Production/Stable", 
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],

    install_requires=[],
)