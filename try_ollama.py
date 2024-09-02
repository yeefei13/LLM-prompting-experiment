from langchain_ollama import ChatOllama
import json

# Define the LLM models and temperature settings you want to experiment with
models = ["gemma2:2b", "deepseek-coder:1.3b", "qwen2:0.5b"]
temperatures = [1.5]

# Define the learning tasks (replace these with your actual tasks)
task1 = "Solve a math problem."
task2 = "Detect bug in given code."

# Define your queries/prompts for each task
queries_task1 = [
    # Zero-Shot Prompting 
    """Q: Solve the following math problem: 
      3*2+2-2/2*3-3+1
     A: """,  
    
    # One-Shot Prompting
    """Q: Solve the following math expression:
    1*4+1-1/1*2-1+2
    A: The correct order of operations gives us \( 4+1-2-1+2 = 4 \).
    Q: Solve the following math expression:
    3 * 2 + 2 - 2 / 2 * 3 - 3 + 1
    A: """,
    
    # gpt Prompting
    """Q: Solve the following math expression:
    3 * 2 + 2 - 2 / 2 * 3 - 3 + 1
    To solve this expression, let's break it down:
    1. First, identify and perform any multiplication or division operations from left to right.
    2. After performing each operation, simplify the expression step by step.
    3. Once all multiplication and division are handled, proceed to perform addition and subtraction, also from left to right.
    A: """,    

    # # Chain-of-Thought (CoT) Prompting
    """Q: Solve the following math expression:
    3 * 2 + 2 - 2 / 2 * 3 - 3 + 1
    Let's solve this step by step. First, identify and perform any multiplication or division from left to right.
    Then, update the expression with the results of these operations.
    After handling multiplication and division, move on to addition and subtraction, solving from left to right.
    Finally, simplify the expression to find the answer.
    A: """,    

    # # Tree-of-Thought (ToT) Prompting
    """Q: Solve the following math expression:
    3 * 2 + 2 - 2 / 2 * 3 - 3 + 1
    Let's explore different approaches:
    Scenario 1: Follow the standard order of operations (PEMDAS/BODMAS). 
    First, handle multiplication and division from left to right.
    Scenario 2: Consider simplifying the expression by grouping similar operations together.
    After exploring these scenarios, simplify the expression to find the final answer.
    A: """,

    """Q:solve the following math expression:
    3 * 2 + 2 - 2 / 2 * 3 - 3 + 1
    do division and multiplication first from left to right.
    do adding part step by step too.
    A:
    """,
    ]

queries_task2 = [
#     """Q: I have three piece of code rank them by time complexity Code: 
#     #include <iostream>

#     int sumArray(int arr[], int size) {
#         int sum = 0;
#         for (int i = 0; i < size; ++i) {
#             for (int j = 0; j <= i; ++j) {
#                 if (j == i) {
#                     sum += arr[i];
#                 }
#             }
#         }
#         return sum;
#     }

#     int main() {
#         int arr[] = {1, 2, 3, 4, 5};
#         int size = sizeof(arr) / sizeof(arr[0]);
#         std::cout << "Sum: " << sumArray(arr, size) << std::endl;
#         return 0;
#     }

#     #include <iostream>

#     int sumArray(int arr[], int size) {
#         int* sums = new int[size];
#         sums[0] = arr[0];

#         for (int i = 1; i < size; ++i) {
#             sums[i] = sums[i - 1] + arr[i];
#         }

#         int totalSum = sums[size - 1];
#         delete[] sums;  // Cleaning up allocated memory
#         return totalSum;
#     }

#     int main() {
#         int arr[] = {1, 2, 3, 4, 5};
#         int size = sizeof(arr) / sizeof(arr[0]);
#         std::cout << "Sum: " << sumArray(arr, size) << std::endl;
#         return 0;
#     }

#     #include <iostream>

#     int sumArray(int arr[], int size) {
#         int sum = 0;
#         for (int i = 0; i < size; ++i) {
#             sum += arr[i];
#         }
#         return sum;
#     }

#     int main() {
#         int arr[] = {1, 2, 3, 4, 5};
#         int size = sizeof(arr) / sizeof(arr[0]);
#         std::cout << "Sum: " << sumArray(arr, size) << std::endl;
#         return 0;
#     }
#     give me very short answer!
#     A:
#     """,  





#     """Q: I have three piece of code rank them by time complexity.
#     Code 1: 
#     #include <iostream>

#     int sumArray(int arr[], int size) {
#         int sum = 0;
#         for (int i = 0; i < size; ++i) {
#             for (int j = 0; j <= i; ++j) {
#                 if (j == i) {
#                     sum += arr[i];
#                 }
#             }
#         }
#         return sum;
#     }

#     int main() {
#         int arr[] = {1, 2, 3, 4, 5};
#         int size = sizeof(arr) / sizeof(arr[0]);
#         std::cout << "Sum: " << sumArray(arr, size) << std::endl;
#         return 0;
#     }

#     Code 2:
#     #include <iostream>

#     int sumArray(int arr[], int size) {
#         int* sums = new int[size];
#         sums[0] = arr[0];

#         for (int i = 1; i < size; ++i) {
#             sums[i] = sums[i - 1] + arr[i];
#         }

#         int totalSum = sums[size - 1];
#         delete[] sums;  // Cleaning up allocated memory
#         return totalSum;
#     }

#     int main() {
#         int arr[] = {1, 2, 3, 4, 5};
#         int size = sizeof(arr) / sizeof(arr[0]);
#         std::cout << "Sum: " << sumArray(arr, size) << std::endl;
#         return 0;
#     }

#     Code 3: 
#     #include <iostream>

#     int sumArray(int arr[], int size) {
#         int sum = 0;
#         for (int i = 0; i < size; ++i) {
#             sum += arr[i];
#         }
#         return sum;
#     }

#     int main() {
#         int arr[] = {1, 2, 3, 4, 5};
#         int size = sizeof(arr) / sizeof(arr[0]);
#         std::cout << "Sum: " << sumArray(arr, size) << std::endl;
#         return 0;
#     }
#     give me very short answer!
#     A:
#     """,  





#     """Q: I have three piece of code rank them by time complexity.
#     Code 1: 
#     #include <iostream>

#     int sumArray(int arr[], int size) {
#         int sum = 0;
#         for (int i = 0; i < size; ++i) {
#             for (int j = 0; j <= i; ++j) {
#                 if (j == i) {
#                     sum += arr[i];
#                 }
#             }
#         }
#         return sum;
#     }

#     int main() {
#         int arr[] = {1, 2, 3, 4, 5};
#         int size = sizeof(arr) / sizeof(arr[0]);
#         std::cout << "Sum: " << sumArray(arr, size) << std::endl;
#         return 0;
#     }

#     Code 2:
#     #include <iostream>

#     int sumArray(int arr[], int size) {
#         int* sums = new int[size];
#         sums[0] = arr[0];

#         for (int i = 1; i < size; ++i) {
#             sums[i] = sums[i - 1] + arr[i];
#         }

#         int totalSum = sums[size - 1];
#         delete[] sums;  // Cleaning up allocated memory
#         return totalSum;
#     }

#     int main() {
#         int arr[] = {1, 2, 3, 4, 5};
#         int size = sizeof(arr) / sizeof(arr[0]);
#         std::cout << "Sum: " << sumArray(arr, size) << std::endl;
#         return 0;
#     }

#     Code 3: 
#     #include <iostream>

#     int sumArray(int arr[], int size) {
#         int sum = 0;
#         for (int i = 0; i < size; ++i) {
#             sum += arr[i];
#         }
#         return sum;
#     }

#     int main() {
#         int arr[] = {1, 2, 3, 4, 5};
#         int size = sizeof(arr) / sizeof(arr[0]);
#         std::cout << "Sum: " << sumArray(arr, size) << std::endl;
#         return 0;
#     }


#     give me very short answer and rememberremember give me a rank(which one is the most efficient, which one is the second and which one is the most inefficient)!
#     A:
#     """,  






#     """Q: I have three piece of code rank them by time complexity.
#     Code 1: 
#     #include <iostream>

#     int sumArray(int arr[], int size) {
#         int sum = 0;
#         for (int i = 0; i < size; ++i) {
#             for (int j = 0; j <= i; ++j) {
#                 if (j == i) {
#                     sum += arr[i];
#                 }
#             }
#         }
#         return sum;
#     }

#     int main() {
#         int arr[] = {1, 2, 3, 4, 5};
#         int size = sizeof(arr) / sizeof(arr[0]);
#         std::cout << "Sum: " << sumArray(arr, size) << std::endl;
#         return 0;
#     }

#     Code 2:
#     #include <iostream>

#     int sumArray(int arr[], int size) {
#         int* sums = new int[size];
#         sums[0] = arr[0];

#         for (int i = 1; i < size; ++i) {
#             sums[i] = sums[i - 1] + arr[i];
#         }

#         int totalSum = sums[size - 1];
#         delete[] sums;  // Cleaning up allocated memory
#         return totalSum;
#     }

#     int main() {
#         int arr[] = {1, 2, 3, 4, 5};
#         int size = sizeof(arr) / sizeof(arr[0]);
#         std::cout << "Sum: " << sumArray(arr, size) << std::endl;
#         return 0;
#     }

#     Code 3: 
#     #include <iostream>

#     int sumArray(int arr[], int size) {
#         int sum = 0;
#         for (int i = 0; i < size; ++i) {
#             sum += arr[i];
#         }
#         return sum;
#     }

#     int main() {
#         int arr[] = {1, 2, 3, 4, 5};
#         int size = sizeof(arr) / sizeof(arr[0]);
#         std::cout << "Sum: " << sumArray(arr, size) << std::endl;
#         return 0;
#     }

#     remember give me a rank(which one is the most efficient, which one is the second and which one is the most inefficient)
#     give me very short answer!
#     A:
#     """,  










#     """Q: give me the efficiency of below code. Code: 
# class Solution {
# public:
#     vector<int> maxSlidingWindow(vector<int>& nums, int k) {
#         deque<int> cont;
#         vector<int> ans;
#         cont.push_back(nums[0]);
#         for(int i =1; i<k;i++){
#             while(cont.back()<nums[i]){
#                 cout<< "current rp: "<<nums[i]<<endl;
#                 cout<<" current deque:";
#                 for(auto j: cont){
#                     cout<< "  "<<j;
#                 }
#                 cout<<endl;
#                 cont.pop_back();
#                 if(cont.size()==0){
#                     break;
#                 }
#             }
#             cont.push_back(nums[i]);
#         }
#         ans.push_back(cont.front());
#         for( int rp = k; rp<nums.size();rp++){
#             if(nums[rp-k] == cont.front()){
#                 cont.pop_front();
#             }
#             if(cont.size()!=0){
#                 while(cont.back()<nums[rp]){
#                     cont.pop_back();
#                     if(cont.size()==0){
#                         break;
#                     }
#                 }
#             }
            
#             cont.push_back(nums[rp]);
#             cout<< "current rp: "<<nums[rp]<<endl;
#             cout<<" current deque:";
#             for(auto i: cont){
#                 cout<< "  "<<i;
#             }
#             cout<<endl;
#             ans.push_back(cont.front());
#         }
#         return ans;
#     }
# };

#     give me very short answer!
#     A:
#     """, 




#      """Q: give me the efficiency and big O notation of below code. Code: 
# class Solution {
# public:
#     vector<int> maxSlidingWindow(vector<int>& nums, int k) {
#         deque<int> cont;
#         vector<int> ans;
#         cont.push_back(nums[0]);
#         for(int i =1; i<k;i++){
#             while(cont.back()<nums[i]){
#                 cout<< "current rp: "<<nums[i]<<endl;
#                 cout<<" current deque:";
#                 for(auto j: cont){
#                     cout<< "  "<<j;
#                 }
#                 cout<<endl;
#                 cont.pop_back();
#                 if(cont.size()==0){
#                     break;
#                 }
#             }
#             cont.push_back(nums[i]);
#         }
#         ans.push_back(cont.front());
#         for( int rp = k; rp<nums.size();rp++){
#             if(nums[rp-k] == cont.front()){
#                 cont.pop_front();
#             }
#             if(cont.size()!=0){
#                 while(cont.back()<nums[rp]){
#                     cont.pop_back();
#                     if(cont.size()==0){
#                         break;
#                     }
#                 }
#             }
            
#             cont.push_back(nums[rp]);
#             cout<< "current rp: "<<nums[rp]<<endl;
#             cout<<" current deque:";
#             for(auto i: cont){
#                 cout<< "  "<<i;
#             }
#             cout<<endl;
#             ans.push_back(cont.front());
#         }
#         return ans;
#     }
# };

#     give me very short answer!
#     A:
#     """, 
]

# Function to run the queries with different models and temperatures
def run_experiments(models, temperatures, queries):
    results = {}
    
    for model_name in models:
        if model_name == "deepseek-coder:1.3b":
            llm = ChatOllama(
                model=model_name,
                temperature=1.5,  # Set initial temperature, it will be overridden
                max_tokens=200,
                repetition_penalty=1.2 
            )
        else:
            llm = ChatOllama(
                model=model_name,
                temperature=1.5,  # Set initial temperature, it will be overridden
                max_tokens=200,
            )
        print(model_name)
        results[model_name] = {}
        for temp in temperatures:
            results[model_name][f"temperature={temp}"] = {}
            some =0
            for query in queries:
                some+=1
                print(query)
                result = llm.invoke(query, temperature=temp, max_tokens=200).content
                results[model_name][f"temperature={temp}"][query] = result
                write_results_to_file(f"task1_results_{model_name}_{temp}_{some}.json", result)
    
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
