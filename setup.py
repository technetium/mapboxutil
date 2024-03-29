import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mapboxutil",
    version="1.1.1",
    author="Toni Cornelissen",
    author_email="mapboxutil@technetium.be",
    description="Module with utility functions to generate static choropleth maps with Mapbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://mapboxutil.technetium.be",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics :: Presentation",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    python_requires='>=3.5',
)   

'''
https://www.codementor.io/@ajayagrawal295/how-to-publish-your-own-python-package-12tbhi20tf
python setup.py sdist bdist_wheel
python -m twine upload -rtestpypi dist/*
'''    
