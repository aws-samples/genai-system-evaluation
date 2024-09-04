# GenAI System Evaluation

This repository contains sample notebooks to demonstrate how to evaluate an LLM-augmented system. It provides tools and methods for local evaluation.

## PreRequisites
These notebooks were tested with Python 3.12. If you're running locally, ensure you're using 3.12 (preferably using pyenv). Also ensure that you have the AWS CLI setup with the credentials you want set to the default profile

## Table of Contents

- [Folder Structure](#folder-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [CI/CD Integration](#cicd-integration)
- [Authors](#authors)
- [Acknowledgements](#acknowledgements)
- [Contributing](#contributing)
- [License](#license)

## Folder Structure

```
LLM-System-Validation/
├── data/                  # RAG context and validation datasets
├── example-notebooks/     # Notebooks for evaluating various components
|__ script/                # Various scripts for setting up environment.
|__ .github/               # Example github actions
```

### Details

- `data/`: Contains the datasets used for Retrieval-Augmented Generation (RAG) context and validation.
- `example-notebooks/`: Jupyter notebooks demonstrating the evaluation of:
  - Embeddings
  - Chunking strategies
  - Reranking methods
  - Prompt engineering
  - LLM-as-Judge evaluation recipes

## Getting Started

This notebook was tested with Python 3.12

1. Clone the repository:
   ```
   git clone git@github.com:aws-samples/genai-system-evaluation.git
   cd genai-system-evaluation
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Download opensearch docs for RAG context.
   ``` bash
   $ cd data && mkdir opensearch-docs && cd  opensearch-docs
   $ git clone https://github.com/opensearch-project/documentation-website.git
   ```

4. Go to notebook examples & start jupyter notebooks!
   ``` bash
   $ cd ../../example-notebooks
   $ jupyter notebook
   ```

5. Start at notebook 1 and work your way through them!

## Usage

1. Explore the example notebooks in the `example-notebooks/` directory to understand different evaluation techniques.

## Authors

- Tanner McRae - *Initial work* - [github](https://github.com/tannermcrae)
- Felix Huthmacher  - *Initial work* - [github](https://github.com/fhuthmacher)

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

