from transformers import pipeline, set_seed
import openai
import json
import time

# Set up your OpenAI API key
openai.api_key = 'ukey'

# Set up the models you want to experiment with, including ChatGPT
# model_names = ["gpt2", "MaziyarPanahi/calme-2.1-qwen2-7b", "facebook/opt-350m","microsoft/Phi-3-medium-4k-instruct","google/gemma-7b-it", "chatgpt"]
model_names = [ "chatgpt"]

# Define the learning tasks (replace these with your actual tasks)
task1 = "Detect bug in given code."
task2 = "Solve a math problem."

# Define your queries/prompts for each task
queries_task1 = [
    # Zero-Shot Prompting
    "Q: Solve the following math problem: 1237 * 5321 A: ",  
    
    # One-Shot Prompting
    "Q: What is 12 * 34? A: 408. Q: Solve the following math multiplication and give me an answer: 1237 * 5321 A: ",  
    
    # Few-Shot Prompting
    "Q: What is 12 * 34? A: 408. Q: What is 56 * 78? A: 4368. Q: What is 23 * 45? A: 1035. Q: Solve the following math multiplication and give me an answer: 1237 * 5321 A: ",  
    
    # Chain-of-Thought (CoT) Prompting
    "Q: Solve the following math problem: 1237 * 5321 Let's think step by step. First, multiply the digits of 1237 by the digits of 5321. Calculate each part of the multiplication. Add the partial results together to get the final answer. A: ",  
    
    # Tree-of-Thought (ToT) Prompting
    "Q: Solve the following math problem: 1237 * 5321 Let's explore the possible steps: Scenario 1: Break down the multiplication into smaller parts. Multiply 1237 by 1. Multiply 1237 by 20 (which is 2 with an added zero). Multiply 1237 by 300. Multiply 1237 by 5000. Conclusion: After considering these approaches, sum the results of the partial multiplications to get the final answer. A: "
]

queries_task2 = [
    """Q: what is the bug in blow code? Code: 
    #include <iostream>
    int main() {
        int x = 10;
        int y = 0;
        int result = x / y; // Division by zero error

        std::cout << "Result: " << result << std::endl;

        return 0;
    } 
    A:
    """,  # Zero-shot example
    "Q: Here is an example of a sentiment analysis: ... Now, classify this text: ... A:",  # One-shot example
]
# Define the hyperparameter settings you want to experiment with
hyperparameters = [
    {"do_sample": True, "temperature": 0.7, "max_length": 500, "truncation": True},
]

# Set a seed for reproducibility
set_seed(42)

# Function to run the queries with different models and hyperparameters
def run_experiments(model_name, task, queries):
        results = {}
        if model_name == "chatgpt":
            for query in queries:
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": query}
                        ],
                        temperature=0.7,  # You can adjust this based on your needs
                        max_tokens=500
                    )
                    results[query] = response.choices[0].message["content"]
                    time.sleep(20)  # Wait 20 seconds between requests to avoid rate limit
                except openai.error.RateLimitError as e:
                    print(f"Rate limit error: {e}. Waiting 20 seconds before retrying...")
                    time.sleep(20)
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": query}
                        ],
                        temperature=0.7,
                        max_tokens=500
                    )
                    results[query] = response.choices[0].message["content"]
        else:
            generator = pipeline("text-generation", model=model_name)
            
            for query in queries:
                results[query] = {}
                for params in hyperparameters:
                    output = generator(query, **params)
                    results[query][str(params)] = output[0]["generated_text"]
        
        return results

# Function to write results to a file in a pretty-printed format
def write_results_to_file(filename, content):
    # Convert the JSON content to a string with indentation
    json_string = json.dumps(content, indent=4)
    
    # Replace the escaped newline characters with actual newlines
    json_string = json_string.replace("\\n", "\n")
    
    # Write the modified string to the file
    with open(filename, 'w') as file:
        file.write(json_string)

# Running experiments for Task 1
task1_results = {}
print("Running experiments for Task 1")
for model_name in model_names:
    print(f"Using model: {model_name}")
    results_task1 = run_experiments(model_name, task1, queries_task1)
    task1_results[model_name] = results_task1

# Save Task 1 results to a file
write_results_to_file("task1_results.json", task1_results)

# Running experiments for Task 2
task2_results = {}
print("Running experiments for Task 2")
for model_name in model_names:
    print(f"Using model: {model_name}")
    results_task2 = run_experiments(model_name, task2, queries_task2)
    task2_results[model_name] = results_task2

# Save Task 2 results to a file
write_results_to_file("task2_results.json", task2_results)

print("Results have been written to task1_results.json and task2_results.json")
