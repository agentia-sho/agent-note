from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging
import random
import time
import json
from playwright.sync_api import sync_playwright
import agentql
from agentql.ext.playwright.sync_api import Page

# Set up logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = FastAPI(
    title="Note.com Search API",
    description="API for searching articles on Note.com",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Author(BaseModel):
    name: str
    url: str

class NoteCard(BaseModel):
    title: str
    url: str
    author: Author
    price: Optional[int]
    createdAt: str
    likeCount: int
    thumbnailUrl: Optional[str]
    remainingCount: Optional[int]

class SearchResponse(BaseModel):
    results: List[NoteCard]

def key_press_end_scroll(page: Page):
    page.keyboard.press("End")
    page.wait_for_page_ready_state()
    time.sleep(random.uniform(0.5, 1.0))

def get_note_data(page: Page):
    query = """
    {
      noteCard[] {
        title
        url
        author {
          name
          url
        }
        price
        createdAt
        likeCount
        thumbnailUrl
        remainingCount
      }
    }
    """
    return page.query_data(query, mode="standard")

@app.get("/search", response_model=SearchResponse)
async def search_notes(
    q: str = Query(..., description="検索キーワード"),
    sort: str = Query("like", description="ソート方法: like, popular, or new"),
    num_scrolls: int = Query(3, description="スクロール回数（1回につき約20件の記事を取得）", ge=1, le=10)
):
    url = f"https://note.com/search?context=note_for_sale&q={q}&sort={sort}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = agentql.wrap(browser.new_page())
            page.goto(url)

            # Load more content by scrolling
            for i in range(num_scrolls):
                log.info(f"Scrolling to load more content... ({i+1}/{num_scrolls})")
                key_press_end_scroll(page)

            response = get_note_data(page)
            return {"results": response["noteCard"]}
        
        finally:
            browser.close()

@app.get("/")
async def root():
    return {"message": "Welcome to Note.com Search API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 