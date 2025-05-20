"""Package installer"""

from setuptools import find_packages, setup  # type: ignore

setup(
    name="price-elasticity-rl",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "ipykernel",
        "scikit-learn",
        "keras",
        "tensorflow",
        "jupyter",
        "gym",
        "imageio"
    ],
)