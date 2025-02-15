import openai
import pandas as pd
import tqdm
from multiprocessing import Pool
from ollama import ChatResponse
import ollama

# Define a list of custom API Base URLs for distributed processing
utl_list = [
    "http://127.0.0.1:11440",
    "http://127.0.0.1:11441",
    "http://127.0.0.1:11442",
    "http://127.0.0.1:11443",
    "http://127.0.0.1:11444",
    "http://127.0.0.1:11445",
    "http://127.0.0.1:11446",
    "http://127.0.0.1:11447",
    "http://127.0.0.1:11450",
    "http://127.0.0.1:11451",
    "http://127.0.0.1:11452",
    "http://127.0.0.1:11453",
    "http://127.0.0.1:11454",
    "http://127.0.0.1:11455",
    "http://127.0.0.1:11456",
    "http://127.0.0.1:11457",
]

# Set the OpenAI API key
openai.api_key = "sk-bTxDIYUAspAvG0qi18B9Db216a5640D59eE0627333693835"

def analyze_relevance(abstract, topic, utl):
    """
    Analyze the relevance of a paper's abstract to a given topic using a language model.

    Parameters:
        abstract (str): The abstract of the paper to analyze.
        topic (str): The topic to evaluate relevance against.
        utl (str): The API base URL for the language model.

    Returns:
        str: The response from the language model, including the relevance score.
    """
    # Define the prompt for the language model
    prompt = f"""
    You are an expert in scientific research and information analysis. 
    Analyze the following paper abstract and determine the strength of its association with the topic "{topic}". 
    Provide a detailed explanation of the relevance, including specific points of connection or lack thereof.

    Abstract:
    {abstract}

    Topic: {topic}
    Any word or phrase related to the above should be considered relevant. Give me a float score from 0 to 1, 0 means no relevance, 1 means highly relevant.
    The format is: 
    **score=0.8**
    """
    # Initialize the client for the language model
    client = ollama.Client(host=utl, headers={'x-some-header': 'some-value'})
    # Send the prompt to the model and get the response
    response: ChatResponse = client.chat(
        model='deepseek-r1:70b', messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response['message']['content']

def task_single(args):
    """
    Process a single paper to analyze its relevance to the topic.

    Parameters:
        args (tuple): A tuple containing the abstract, index, year, title, save file path, API URL, and topic.

    Returns:
        tuple: The year and the relevance score for the paper.
    """
    abstract, i, year, title, path_save_file, url, topic = args
    try:
        # Analyze the relevance of the paper
        result = analyze_relevance(abstract, topic, url)
        # Extract the score from the response
        score_str = result.split('score=')[-1].split('**')[0]
        if len(score_str) < 10 and ('.' in score_str or '0' in score_str or '1' in score_str):
            score = float(score_str)
        else:
            score = -1  # Invalid score
            print('Invalid score string:', score_str)
    except Exception as e:
        score = -1  # Handle errors gracefully
        print(f"Error processing {title}: {e}")
    
    # Print the result for debugging
    print("Relevance Analysis Result: ", score, "Year: ", year)
    # Save the result to the output file
    with open(path_save_file, 'a') as f:
        f.write(f"{i},{year},{score}
")
    return year, score

def process_data_in_parallel(data, topic, path_save_file, utl_list):
    """
    Process a dataset of papers in parallel to analyze their relevance to a topic.

    Parameters:
        data (DataFrame): The dataset containing paper abstracts, years, and titles.
        topic (str): The topic to evaluate relevance against.
        path_save_file (str): The path to save the results.
        utl_list (list): A list of API base URLs for distributed processing.

    Returns:
        None
    """
    # Prepare arguments for each task
    tasks = []
    for i in range(len(data)):
        abstract = data['Abstract'][i]  # Paper abstract
        year = data['Year'][i]         # Year of publication
        title = data['TITLE'][i]       # Paper title
        url = utl_list[i % len(utl_list)]  # Distribute URLs evenly across tasks
        tasks.append((abstract, i, year, title, path_save_file, url, topic))
    
    # Use multiprocessing to process tasks in parallel
    with Pool(processes=len(utl_list)) as pool:
        results = list(tqdm.tqdm(pool.imap(task_single, tasks), total=len(tasks)))
    
    # Aggregate results by year
    year_score_dict = {}
    for year, score in results:
        if year in year_score_dict:
            year_score_dict[year].append(score)
        else:
            year_score_dict[year] = [score]
    
    # Print average scores by year
    for year, scores in year_score_dict.items():
        print(f"Year: {year}, Average Score: {sum(scores) / len(scores)}")

if __name__ == "__main__":
    # Load the dataset of papers
    data = pd.read_csv('papers.csv')

    # Define a list of topics to analyze
    topic_list = [
        "data fusion",
        "information fusion",
        "sensor fusion",
        "multisource data integration",
        "multi-modal data fusion",
        "fusion algorithms",
        "knowledge fusion",
        "feature fusion",
        "cross-modal fusion",
        "information integration",
        "fusion",
        "tree",
        "information",
    ]
    # Combine topics into a single string with "or" for relevance analysis
    topic = ' or '.join(topic_list)
    print('Analyzing topic:', topic)

    # Define the output file path
    path_save_file = 'paper_score.csv'

    # Process the dataset in parallel
    process_data_in_parallel(data, topic, path_save_file, utl_list)
