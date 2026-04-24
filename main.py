import os
import asyncio
import json
import random
from fastapi import FastAPI, BackgroundTasks
from twitter_client import TwitterClient
from ai_orchestrator import generate_engagement, generate_startup_tweet
from datetime import datetime

# ... (previous code)

# Live Logging System
logs = []

def log_action(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    print(full_message)
    logs.append(full_message)
    # Keep only the last 100 logs
    if len(logs) > 100:
        logs.pop(0)

async def bot_loop():
    global processed_ids
    log_action("Engagement loop initialized.")
    
    # Startup Action: Find and Retweet a relevant post immediately
    try:
        startup_keyword = random.choice(KEYWORDS)
        log_action(f"Startup: Looking for a tweet to retweet about {startup_keyword}...")
        startup_tweets = twitter.search_tweets(startup_keyword, max_results=1)
        if startup_tweets:
            target = startup_tweets[0]
            if twitter.retweet(target.id):
                log_action(f"Startup retweet successful: {target.text[:50]}...")
                processed_ids.add(target.id)
                save_processed_tweets(processed_ids)
        else:
            log_action("Startup: No tweets found to retweet.")
    except Exception as e:
        log_action(f"Failed startup retweet: {e}")

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
            
            action_roll = random.random()
            
            if action_roll < 0.6:
                response = generate_engagement(tweet.text, author_name, "reply")
                if twitter.reply(tweet.id, response):
                    log_action(f"Replied: {response}")
            elif action_roll < 0.9:
                response = generate_engagement(tweet.text, author_name, "quote")
                if twitter.quote(tweet.id, response):
                    log_action(f"Quoted: {response}")
            else:
                if twitter.retweet(tweet.id):
                    log_action("Retweeted successfully.")
                
            processed_ids.add(tweet.id)
            save_processed_tweets(processed_ids)
            
            wait_time = random.randint(30, 90)
            log_action(f"Sleeping for {wait_time}s between actions...")
            await asyncio.sleep(wait_time)
            
        log_action(f"Loop finished. Sleeping for {POLL_INTERVAL//60} minutes...")
        await asyncio.sleep(POLL_INTERVAL)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot_loop())

@app.get("/")
def read_root():
    # Show the latest 50 logs on the homepage
    log_html = "<br>".join(reversed(logs))
    return {
        "bot_status": "Active",
        "processed_total": len(processed_ids),
        "recent_activity": logs[-20:] # Return as JSON for easy reading
    }

@app.get("/logs")
def get_all_logs():
    return {"logs": logs}

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
