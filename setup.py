from setuptools import setup

setup(
    name="python-langsax",
    version="0.1",
    author="Sven Haardiek",
    author_email="sven@haardiek.de",
    license="GPLv2",
    py_modules=['langsax'],
    entry_points={'console_scripts': ['langsax = langsax:main']}
)
