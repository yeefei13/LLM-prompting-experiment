from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="llama3.1",
    temperature=0,
)

result = llm.invoke(
    "Could you validate user 123? They previously lived at "
    "123 Fake St in Boston MA and 234 Pretend Boulevard in "
    "Houston TX."
)
print(result)