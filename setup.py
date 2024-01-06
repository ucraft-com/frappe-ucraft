from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# get version from __version__ variable in raven/__init__.py

setup(
    name="ucraft",
    version='0.0.1',
    description="Ucraft Integration for ERPNext",
    author="Webisoft",
    author_email="utkarsh@webisoft.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
