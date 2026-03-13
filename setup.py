import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-urn-randomizer",
    version="0.0.1",
    author="Research Computing Group",
    description="Urn randomization for group assignment in randomized experiments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include=["urand"]),
    include_package_data=True,
    license_file="LICENSE",
    install_requires=[
        "Flask>=3.0",
        "click>=8.0",
        "confuse>=2.0",
        "SQLAlchemy>=1.4",
        "pandas>=2.0",
        "numpy>=2.0",
        "scipy>=1.10",
        "pluginbase>=1.0",
        "Flask-Login>=0.6",
        "Flask-SQLAlchemy>=3.1",
        "Flask-WTF>=1.2",
        "Flask-Dance>=7.0",
        "bootstrap-flask>=2.3",
        "WTForms>=3.1",
        "WTForms-Alchemy>=0.18",
        "WTForms-Components>=0.10",
        "bokeh>=3.0",
        "sqlalchemy-datatables>=2.0",
        "gunicorn>=22.0",
    ],
    python_requires=">=3.13",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_data={"urand": ["config_default.yaml"]},
    entry_points="""
        [console_scripts]
        urn=urand.cli:cli
    """,
)
