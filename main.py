import os
import asyncio
import json
import random
from fastapi import FastAPI, BackgroundTasks
from twitter_client import TwitterClient
from ai_orchestrator import generate_engagement
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
twitter = TwitterClient()

# Configuration
KEYWORDS = ["Malawian politics", "science", "philosophy", "quantum physics", "Malawi news", "MCP", "DPP", "UTM", "zikutheka"]
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL_MINUTES", 5)) * 60
PROCESSED_TWEETS_FILE = "processed_tweets.json"

def load_processed_tweets():
    if os.path.exists(PROCESSED_TWEETS_FILE):
        try:
            with open(PROCESSED_TWEETS_FILE, "r") as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def save_processed_tweets(processed_ids):
    with open(PROCESSED_TWEETS_FILE, "w") as f:
        json.dump(list(processed_ids), f)

processed_ids = load_processed_tweets()

async def bot_loop():
    global processed_ids
    while True:
        print("Starting engagement loop...")
        keyword = random.choice(KEYWORDS)
        print(f"Searching for tweets with keyword: {keyword}")
        
        tweets = twitter.search_tweets(keyword, max_results=5)
        
        for tweet in tweets:
            if tweet.id in processed_ids:
                continue
                
            author_name = twitter.get_user_name(tweet.author_id)
            print(f"Processing tweet from {author_name}: {tweet.text[:50]}...")
            
            # Randomly decide on action: reply, quote, or retweet
            # Weighted: 60% reply, 30% quote, 10% retweet
            action_roll = random.random()
            
            if action_roll < 0.6:
                response = generate_engagement(tweet.text, author_name, "reply")
                twitter.reply(tweet.id, response)
            elif action_roll < 0.9:
                response = generate_engagement(tweet.text, author_name, "quote")
                twitter.quote(tweet.id, response)
            else:
                twitter.retweet(tweet.id)
                
            processed_ids.add(tweet.id)
            save_processed_tweets(processed_ids)
            
            # Wait a bit between actions to avoid being too "bot-like"
            await asyncio.sleep(random.randint(30, 90))
            
        print(f"Loop finished. Sleeping for {POLL_INTERVAL} seconds...")
        await asyncio.sleep(POLL_INTERVAL)

@app.on_event("startup")
async def startup_event():
    # Start the bot loop in the background
    asyncio.create_task(bot_loop())

@app.get("/")
def read_root():
    return {"status": "Isaac bot is running", "processed_count": len(processed_ids)}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
