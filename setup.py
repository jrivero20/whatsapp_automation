from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="whatsapp-automation",
    version="2.0.0",
    author="Jose Rivero",
    author_email="jasealexander14@gmail.com",
    description="Librería Python y Bot RPA para automatizar WhatsApp Web con Playwright",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jrivero20/whatsapp_automation",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "playwright>=1.40.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "whatsapp-send=whatsapp_automation.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)