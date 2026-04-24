import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def load_persona():
    try:
        with open("isaac_persona.md", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error loading persona: {e}")
        return "You are Isaac, a Malawian intellectual interested in Science, Philosophy, and Politics."

def generate_engagement(tweet_text, author_name, action_type="reply"):
    persona = load_persona()
    secondary_handle = os.getenv("SECONDARY_BOT_HANDLE", "@bot_isaac")
    
    system_prompt = f"""
{persona}

Your task is to {action_type} to a tweet. 
Tweet Content: "{tweet_text}"
Author: {author_name}

Rules:
1. Stay strictly in character as Isaac.
2. If the tweet is about Malawian politics, be insightful or slightly witty.
3. If it's about science or philosophy, be deep and curious.
4. If it's gossip, be playful.
5. You MUST mention {secondary_handle} in your response to 'bring them into the conversation'.
6. Keep the response under 250 characters (including the mention).
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo", # Or any other model available on OpenRouter
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Generate a {action_type} to this tweet: {tweet_text}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating AI response: {e}")
        return f"Interesting point by {author_name}! What do you think {secondary_handle}?"

if __name__ == "__main__":
    # Test
    print(generate_engagement("The quantum entanglement of particles is fascinating.", "Alice"))
