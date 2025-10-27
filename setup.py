"""
Setup configuration for MCP-OpenAI Bridge
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_long_description():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mcp-openai-bridge",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Bridge between MCP servers and OpenAI's function calling for Salesforce Data Cloud",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mcp-openai-bridge",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/mcp-openai-bridge/issues",
        "Documentation": "https://github.com/yourusername/mcp-openai-bridge/docs",
        "Source Code": "https://github.com/yourusername/mcp-openai-bridge",
    },
    packages=find_packages(exclude=["tests", "docs", "examples"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
        ],
        "streamlit": [
            "streamlit>=1.28.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "mcp-chat=interactive_chat:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="mcp openai salesforce data-cloud llm ai chatbot",
)
