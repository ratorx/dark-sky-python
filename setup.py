from setuptools import setup

setup(name="darksky",
      version="1.0",
      description="A wrapper for the Dark Sky (formerly forecast.io) weather API.",
      url="https://github.com/ratorx/dark-sky-python",
      author="Reetobrata Chatterjee",
      author_email="reetobratachatterjee@gmail.com",
      license="MIT",
      packages=["darksky"],
      install_requires=["requests"])
