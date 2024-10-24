# Search With AI

[![Python Version](https://img.shields.io/badge/python-~3.12-blue.svg)](https://www.python.org/downloads/)
[![Gradio Version](https://img.shields.io/badge/gradio-5.3.0-green.svg)](https://gradio.app/)
[![Poetry Version](https://img.shields.io/badge/poetry-1.8.3-orange.svg)](https://python-poetry.org/)

This chatbot combines the power of real-time web search with advanced AI summarization to deliver accurate, contextual responses to user questions.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)

## Introduction

This chatbot leverages web search to find relevant information in response to user queries. It automatically searches the web, extracts key information, and uses a Large Language Model (LLM) to summarize the results. The LLM then analyzes the summary and provides a coherent and insightful answer based on the gathered information.

## Installation

### Prerequisites

- **Python**: Version ~3.12
- **Poetry**: Version 1.8.3

### Clone the Repository

```bash
git clone https://github.com/mbyta/search-with-ia.git
cd search-with-ia
```

### Install Dependencies
```bash
poetry install
```

### Set environment variables
Create a `.env` file from `.env.example` and set the key values

## Usage
Start the application by running the following command:
```bash
poetry run python src/search_with_ia/main.py
```
