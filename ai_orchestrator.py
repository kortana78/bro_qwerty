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
            content = f.read()
            # Strip out secondary persona sections if they exist
            if "## Secondary Persona" in content:
                content = content.split("## Secondary Persona")[0]
            return content
    except Exception as e:
        print(f"Error loading persona: {e}")
        return "You are Isaac, a Malawian intellectual interested in Science, Philosophy, and Tech."

def generate_engagement(tweet_text, author_name, action_type="reply"):
    persona = load_persona()
    
    system_prompt = f"""
{persona}

Your task is to {action_type} to a tweet. 
Tweet Content: "{tweet_text}"
Author: {author_name}

Rules:
1. Stay strictly in character.
2. If the tweet is about Malawi, be insightful or slightly witty.
3. If it's about science, philosophy or tech, be deep, curious, or analytical.
4. Do NOT mention any other bot accounts or specific handles like @bro_isaac, @bot_isaac, @bot_qwerty, or qwerty.
5. Keep the response under 250 characters.
6. Determine if the context is positive or negative and respond accordingly.
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Generate a {action_type} to this tweet: {tweet_text}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating AI response: {e}")
        return f"Interesting point by {author_name}! Science and philosophy always have more to uncover."

def generate_startup_tweet():
    persona = load_persona()
    
    system_prompt = f"""
{persona}

Your task is to write a short tweet (under 280 characters) announcing that you are online. 
Focus on science, philosophy, tech or Malawi. Do NOT mention other bots.
"""
    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Generate your first tweet."}
            ]
        )
        return response.choices[0].message.content
    except:
        return "Isaac is online. Exploring the intersections of science, philosophy, and our beautiful Malawi."
