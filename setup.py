
from setuptools import find_packages, setup

# Lê o conteúdo do README para long_description
with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

# Lê as dependências do requirements.txt (se existir)
requirements_path = "requirements.txt"
with open(requirements_path, encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="zettel_update",
    version="0.1.0",
    author="Felipe Marcelino",
    author_email="felipe.marcelino1991@gmail.com",
    description="Update my zettel blog with every ocred note from my tablet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=requirements,
)
