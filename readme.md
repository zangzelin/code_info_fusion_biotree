# Paper Relevance Analysis with Parallel Processing

This project is designed to analyze the relevance of scientific papers to a specific topic using a language model (e.g., `deepseek-r1:70b`). The program processes a dataset of paper abstracts, evaluates their relevance to a given topic, and calculates relevance scores. It uses parallel processing to speed up the analysis by distributing tasks across multiple API endpoints.

---

## Features

- **Relevance Analysis**: Uses a language model to evaluate the relevance of paper abstracts to a specific topic.
- **Parallel Processing**: Distributes tasks across multiple API endpoints for faster processing.
- **Customizable Topics**: Allows users to define a list of topics for relevance analysis.
- **Error Handling**: Handles invalid scores and exceptions gracefully.
- **Yearly Aggregation**: Aggregates and calculates average relevance scores by year.

---

## Requirements

### Python Libraries
The following Python libraries are required to run the project:
- `openai`
- `pandas`
- `tqdm`
- `multiprocessing`
- `ollama`

You can install the required libraries using `pip`:
```bash
pip install openai pandas tqdm ollama
