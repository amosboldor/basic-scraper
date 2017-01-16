"""Setup file for a quick install."""


from setuptools import setup

setup(
    name="basic-scraper",
    description="Basic scraper for Health Inspection Data from King County.",
    version=0.1,
    author=["Amos Boldor"],
    author_email=["amosboldor@gmail.com"],
    license="MIT",
    package_dir={'': '.'},
    py_modules=[
        "beautifulsoup4",
        "html5lib",
        "requests",
        "geocoder"
    ]
)
