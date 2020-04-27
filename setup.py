from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='uncd',
    version='0.16',
    author='hpencilb',
    author_email='haemoglob.j.ben@gmail.com',
    description="A CLI tool about Unicode",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'Click', 'requests', 'BeautifulSoup4', 'lxml'
    ],
    entry_points='''
        [console_scripts]
        uncd=uncd.__init__:cli
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
