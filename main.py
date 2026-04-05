import os
import argparse
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function





def main():
        parser = argparse.ArgumentParser(description="AI Code Assistant")
        parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
        parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
        args = parser.parse_args()

        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY environment variable not set")

        client = genai.Client(api_key=api_key)
        messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
        if args.verbose:
            print(f"User prompt: {args.user_prompt}\n")

        for _ in range(20):

            result = generate_content(client, messages, args.verbose)
            if result:
                print("Final response:")
                print(result)
                return
        
        print("Max iterations reached")
        sys.exit(1)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
             tools=[available_functions],
             system_instruction=system_prompt, 
             temperature= 0)
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    for i in response.candidates:
        messages.append(i.content)

    if response.function_calls is not None:
         for i in response.function_calls:
              print(f"Calling function: {i.name}({i.args})")
    else:
        return response.text
    
    

    function_responses = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose)

        if not function_call_result.parts:
            raise Exception("This should not be empty")
        
        if not function_call_result.parts[0].function_response:
            raise Exception("Function response empty")
        
        if not function_call_result.parts[0].function_response.response:
            raise Exception("Result should not be empty")
        
        
        function_responses.append(function_call_result.parts[0])

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

    messages.append(types.Content(role="user", parts=function_responses))



    


if __name__ == "__main__":
    main()
