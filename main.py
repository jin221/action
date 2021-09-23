import os
from datetime import datetime
from pytz import timezone
from crawling import parsing_beautifulsoup, extract_book_data
from github_utils import get_github_repo, upload_github_issue


if __name__ == "__main__":
    access_token = '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'
    repository_name = "action"

    seoul_timezone = timezone('America/Indiana/Indianapolis')
    today = datetime.now(seoul_timezone)
    today_data = today.strftime("%m/ %d/ %Y")

    new_product_url = "https://www.barnesandnoble.com/b/books/_/N-1fZ29Z8q8"
    
    soup = parsing_beautifulsoup(new_product_url)
    
    issue_title = f"B&N Top 100({today_data})"
    upload_contents = extract_book_data(soup)
    repo = get_github_repo(access_token, repository_name)
    upload_github_issue(repo, issue_title, upload_contents)
    print("Upload Github Issue Success!")