import setuptools

setuptools.setup(
    name="text_summarizer",
    version="0.0.0",
    author="Nayan",
    description="AI text summarizer pipeline",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)
