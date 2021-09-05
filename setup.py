import setuptools

setuptools.setup(
    name="es2es",
    version="1.0.0.1",
    author="Umit YILMAZ",
    author_email="umutyilmaz44@gmail.com",
    description="ElasticSearch data read and write to other ElasticSearch library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    platforms="all",
    url="https://github.com/umutyilmaz44/es2es",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Internet",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
	"Topic :: Software Development :: Testing",
        "Intended Audience :: Developers",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: Microsoft",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    install_requires=['elasticsearch'],
    python_requires=">3.6.*, <4",
    packages=['es2es'],
    scripts=['bin/es2es']
)

