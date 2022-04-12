from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='jiosaavndownloader',  
    version='1.1.0',
    author="Vijaymahantesh Sattigeri",
    author_email="vijaymahantesh016@gmail.com",
    description="Downloads high quality songs from JioSaavn",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vijaysattigeri/jiosaavndownloader",
    packages=find_packages(),
    install_requires = [
        'requests',
        'pyDes',
        'mutagen',
        'tqdm'
    ],
    license='Mozilla Public License Version 2.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers']
 )
