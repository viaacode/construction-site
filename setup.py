from setuptools import setup

setup(
    name="construction_site",
    version="0.0.1",
    description="A usable and scalable API for RDF construction.",
    url="https://github.com/viaacode/constructionsite",
    author="Miel Vander Sande",
    author_email="miel.vandersande@meemoo.be",
    license="BSD 2-clause",
    packages=["construction_site"],
    install_requires=["rdflib>=5.0.0"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
)
