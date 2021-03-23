import setuptools

setuptools.setup(
    name="nrn-subprocess",
    author="Robin De Schepper",
    version="1.3.2",
    packages=["nrnsub"],
    install_requires=["dill", "tblib"]
)
