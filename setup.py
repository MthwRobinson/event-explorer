from setuptools import setup, find_packages

setup(
    name="event_explorer",
    description="Application for viewing events form multiple sources",
    author="Fiddler Analytics",
    author_email="info@fiddleranalytics.com",
    packages=find_packages(),
    version="0.1.1",
    entry_points={"console_scripts": "event_explorer=event_explorer.cli:main"},
)
