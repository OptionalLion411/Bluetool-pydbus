from setuptools import setup

setup(
    name="bluetool-pydbus",
    version="0.1",
    description="A modified version of the Bluetool library "
                "using newer pydbus instead of dbus-python without agent and server",
    url="https://github.com/OptionalLion411/Bluetool-pydbus",
    author="Milosch Füllgraf",
    author_email="milosch.fuellgraf@testws.de",
    license="MIT",
    packages=["bluetool"],
    python_requires=">=3.9",
    install_requires=[
        "pydbus",
        "PyGObject"
    ]
)
