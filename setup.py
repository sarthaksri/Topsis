from setuptools import setup, find_packages

setup(
    name="topsis-Sarthak_Srivastava_102217018",
    version="1.0.0",
    author="Sarthak Srivastava",
    description="This Python package implements the TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) method for rank calculation. It helps in ranking alternatives based on multiple criteria by determining their proximity to the ideal and negative-ideal solutions. The package is efficient and easy to use for decision-making tasks.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",  
    packages=find_packages(),  
    install_requires=[
        "numpy",
        "pandas"
    ],
    entry_points={
        "console_scripts": [
            "topsis=topsis.102217018:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
