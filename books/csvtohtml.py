import csv
from datetime import datetime

# ===== CONFIG =====
INPUT_CSV = "goodreads_library_export.csv"  # your exported CSV
OUTPUT_HTML = "index.html"
PAGE_TITLE = "Charlie's Books"

# ===== HELPER FUNCTION FOR STARS =====
def rating_to_stars(rating):
    try:
        num = int(float(rating))
    except:
        num = 0
    return "★" * num + "☆" * (5 - num)

# ===== HELPER FUNCTION TO PARSE DATE READ =====
def parse_date(date_str):
    """Parse date in YYYY/MM/DD format. Return datetime or very old date if invalid."""
    date_str = date_str.strip()
    if not date_str:
        return datetime(1900, 1, 1)  # very old date for missing
    try:
        return datetime.strptime(date_str, "%Y/%m/%d")
    except:
        return datetime(1900, 1, 1)  # fallback for unparseable date

# ===== READ AND FILTER CSV =====
books = []

with open(INPUT_CSV, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        shelf = row.get("Exclusive Shelf", "").lower()
        if shelf != "read":
            continue  # skip non-read books

        review_text = row.get("My Review", "").strip()
        if not review_text:
            continue  # skip books without review

        title = row.get("Title", "Unknown Title")
        author = row.get("Author", "Unknown Author")
        rating = row.get("My Rating", "0")
        stars = rating_to_stars(rating)
        date_read = parse_date(row.get("Date Read", ""))

        books.append({
            "title": title,
            "author": author,
            "review_text": review_text,
            "stars": stars,
            "date_read": date_read
        })

# ===== SORT BOOKS BY DATE READ DESCENDING =====
books.sort(key=lambda x: x["date_read"], reverse=True)

# ===== GENERATE HTML =====
html_head = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{PAGE_TITLE}</title>
    <link rel="icon" type="image/x-icon" href="../../favicon.ico">
    <link rel="stylesheet" href="../blog/blogstyles.css">
</head>
<body>
    <div class="topnav">
        <a href="/">Home</a>
        <a href="/blog/">Blog</a>
        <a class="active" href="/books/">Books</a>
    </div>
    <header>
        <h1>Recent Book Reviews</h1>
    </header>
    <div class="content">
        <div class="sidebar"></div>
        <div class="main">
"""

html_books = ""
for book in books:
    review_html = book["review_text"].replace('\n', '<br /><br />')
    html_books += f'''
<div class="bookbox">
    <strong>{book["title"]}</strong> by {book["author"]}<br/>
    My rating: {book["stars"]}<br /><br />
    {review_html}
</div>
'''

html_footer = f"""
<a href="https://www.goodreads.com/review/list/">View all my books</a>
        </div>
        <div class="sidebar"></div>
    </div>
</body>
</html>
"""

full_html = html_head + html_books + html_footer

# ===== SAVE HTML =====
with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(full_html)

print(f"HTML page generated successfully: {OUTPUT_HTML}")
