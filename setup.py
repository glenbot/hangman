"""
Hangman
"""
from distutils.core import setup

__version__ = "0.0.1"


def pip_requirements(extra=None):
    with open('requirements.pip') as f:
        return f.readlines()
    return []


setup(
    author="Glen Zangirolami",
    author_email="glen@decisiohealth.com",
    description="hangman",
    long_description=__doc__,
    fullname="hangman",
    name="hangman",
    url="http://github.com/glenbot/hangman",
    version=__version__,
    platforms=["Linux"],
    packages=[
        "hangman",
        "hangman.bin"
    ],
    install_requires=pip_requirements(),
    entry_points={
        'console_scripts': [
            "hangman=hangman.bin.server:main"
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Server Environment",
        "Intended Audience :: Developers",
        "Operating System :: Linux",
        "Programming Language :: Python",
    ]
)
