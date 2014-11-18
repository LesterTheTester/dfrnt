from distutils.core import setup

setup(
    name="dfrnt",
    version="0.1",
    author="Bryan Lester",
    author_email="lester@bittorrent.com",
    packages=["dfrnt"],
    url="https://github.com/LesterTheTester/dfrnt",
    download_url="https://github.com/LesterTheTester/dfrnt/tarball/0.1",
    license="LICENSE.txt",
    description="A Library for visual diffs",
    long_description=open("README.txt").read(),
    keywords = ['testing', 'visual diff', 'visdiff', 'automation', 'screenshot'],
    install_requires=[
        "Pillow",
    ],
)
