import setuptools


with open("readme.md", "r", encoding='utf8') as fh:
    long_description = fh.read()


setuptools.setup(
    name="mocking_restful_api",
    version="0.0.1",
    install_requires=[
        "requests",
    ],
    # entry_points={
    #     'console_scripts': [
    #         'corona=corona:main',
    #     ],
    # },
    author="tatsuya.nakajima",
    author_email="tatsuya.nakajima@jp.ricoh.com",
    description="RESTful API for unit test.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/---/---",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
