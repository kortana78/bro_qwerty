import os
import asyncio
import json
import random
from fastapi import FastAPI
from twitter_client import TwitterClient
from ai_orchestrator import generate_engagement, generate_startup_tweet
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
twitter = TwitterClient()

# Configuration
# Focusing on Science, Philosophy, Tech, and Malawi as requested
KEYWORDS = ["science", "philosophy", "tech", "Malawi", "quantum physics", "biotechnology", "Malawi tech", "philosophy of mind"]
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL_MINUTES", 5)) * 60
PROCESSED_TWEETS_FILE = "processed_tweets.json"

# Live Logging System
logs = []

def log_action(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    print(full_message)
    logs.append(full_message)
    if len(logs) > 100:
        logs.pop(0)

def load_processed_tweets():
    if os.path.exists(PROCESSED_TWEETS_FILE):
        try:
            with open(PROCESSED_TWEETS_FILE, "r") as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def save_processed_tweets(processed_ids):
    try:
        with open(PROCESSED_TWEETS_FILE, "w") as f:
            json.dump(list(processed_ids), f)
    except Exception as e:
        log_action(f"Error saving processed tweets: {e}")

processed_ids = load_processed_tweets()

async def bot_loop():
    global processed_ids
    log_action("Engagement loop initialized.")
    
    # Startup Action: Post a startup tweet
    try:
        startup_text = generate_startup_tweet()
        if twitter.post_tweet(startup_text):
            log_action(f"Startup tweet posted: {startup_text}")
    except Exception as e:
        log_action(f"Failed startup action: {e}")

    while True:
        keyword = random.choice(KEYWORDS)
        log_action(f"Searching for tweets with keyword: {keyword}")
        
        tweets = twitter.search_tweets(keyword, max_results=5)
        
        if not tweets:
            log_action("No new tweets found for this keyword.")

        for tweet in tweets:
            if tweet.id in processed_ids:
                continue
                
            author_name = twitter.get_user_name(tweet.author_id)
            log_action(f"Processing tweet from @{author_name}: {tweet.text[:50]}...")
            
            # The user requested: "quote, repost and comment, do it"
            # We will do all three actions for the tweet.
            
            # 1. Quote
            quote_text = generate_engagement(tweet.text, author_name, "quote")
            if twitter.quote(tweet.id, quote_text):
                log_action(f"Quoted: {quote_text}")
            
            await asyncio.sleep(5) # Small gap
            
            # 2. Repost (Retweet)
            if twitter.retweet(tweet.id):
                log_action("Retweeted successfully.")
            
            await asyncio.sleep(5) # Small gap
            
            # 3. Comment (Reply)
            reply_text = generate_engagement(tweet.text, author_name, "reply")
            if twitter.reply(tweet.id, reply_text):
                log_action(f"Replied: {reply_text}")
                
            processed_ids.add(tweet.id)
            save_processed_tweets(processed_ids)
            
            wait_time = random.randint(60, 120)
            log_action(f"Sleeping for {wait_time}s between tweet batches...")
            await asyncio.sleep(wait_time)
            
        log_action(f"Loop finished. Sleeping for {POLL_INTERVAL//60} minutes...")
        await asyncio.sleep(POLL_INTERVAL)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot_loop())

@app.get("/")
def read_root():
    return {
        "bot_status": "Active",
        "processed_total": len(processed_ids),
        "recent_activity": logs[-20:]
    }

@app.get("/logs")
def get_all_logs():
    return {"logs": logs}

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
