# Project: Lab Tests By Symptoms

## Overview

This repository contains two main components:

1. **gpt_analyzer**  
   Used for analyzing user symptoms and providing:
   - A list of possible diseases.
   - Recommended tests to be conducted based on the available options.
   - Total cost of the recommended tests.
   - Wich doctor to consult.

2. **lab_tests_parser**  
   Used for parsing the available lab tests from the [Sinevo](https://www.synevo.ua/) website.

## Features

### gpt_analyzer
- Symptom-based analysis powered by GPT.
- Generates a comprehensive list of potential diagnoses.
- Recommends relevant lab tests from the parsed dataset.

### lab_tests_parser
- Web scraper to fetch lab test information from the Sinevo website with name, code and price.
- Organizes data for easy access in csv and integration with the analyzer.

## Requirements
- Docker
- Docker Composer

## Installation and Usage
- Clone the repository.
- Create `.env` file in the `gpt_analyzer` directory with the following variables:
   - `OPENAI_API_KEY`: Your API key for the GPT model.
   - `GENERATION_LANGUAGE`: Language for the GPT model output generation.
   - `GPT_MODEL`: GPT model name.
   - `SYMPTOMS_DESCRIPTION`: Description of the symptoms to be analyzed.
- Run in terminal from project root `sudo docker compose up --build` to start the services.