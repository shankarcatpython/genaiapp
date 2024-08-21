import openai

import generative_ai.app.config as config

openai.api_key = config.config.OPENAI_API_KEY  # Ensure you set your API key

prompt = (
    "Generate a detailed and insightful summary based on the following data:\n"
    "Feature: TestFeature\n"
    "Mean: 5.0\n"
    "Median: 5.5\n"
    "Standard Deviation: 1.2\n"
    "Minimum Value: 3.0\n"
    "Maximum Value: 7.0\n"
    "Anomaly Count: 2"
)

try:
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    )
    print(response.choices[0].text.strip())
except Exception as e:
    print(f"Error: {e}")
