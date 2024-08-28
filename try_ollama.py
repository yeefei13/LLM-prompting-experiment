from langchain_ollama import ChatOllama
import json

# Define the LLM models and temperature settings you want to experiment with
models = ["llama3.1", "phi3", "deepseek-coder-v2", "qwen2:7b"]
temperatures = [0.0, 0.5, 0.7]

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

# Function to run the queries with different models and temperatures
def run_experiments(models, temperatures, queries):
    results = {}
    
    for model_name in models:
        llm = ChatOllama(
            model=model_name,
            temperature=0,  # Set initial temperature, it will be overridden
        )
        print(model_name)
        results[model_name] = {}
        for temp in temperatures:
            results[model_name][f"temperature={temp}"] = {}
            for query in queries:
                print(query)
                result = llm.invoke(query, temperature=temp).content
                results[model_name][f"temperature={temp}"][query] = result
    
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
task1_results = run_experiments(models, temperatures, queries_task1)

# Save Task 1 results to a file
write_results_to_file("task1_results.json", task1_results)

# Running experiments for Task 2
task2_results = {}
print("Running experiments for Task 2")
task2_results = run_experiments(models, temperatures, queries_task2)

# Save Task 2 results to a file
write_results_to_file("task2_results.json", task2_results)

print("Results have been written to task1_results.json and task2_results.json")
