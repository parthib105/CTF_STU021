import pandas as pd
import hashlib

# generate hash
myId = "STU021"
hash_obj = hashlib.sha256(myId.encode())
hash_hex = hash_obj.hexdigest()
myHash = hash_hex[:8].upper()

print(f"Target Hash to find: {myHash}")

# get the data frame
df_reviews = pd.read_csv("reviews.csv")
# print(df1.dtypes, "\n")

df_books = pd.read_csv("books.csv")
# print(df2.dtypes)

# Find books with rating_number = 1234 AND average_rating = 5.0
candidate_books = df_books[(df_books['rating_number'] == 1234) & (df_books['average_rating'] == 5.0)]

# parent_asin : it exists in both CSV files and is unique
candidate_asins = candidate_books['parent_asin'].tolist()

# Filter reviews to only look at the candidate books we identified above
filtered_reviews = df_reviews[df_reviews['parent_asin'].isin(candidate_asins)]

match = filtered_reviews[filtered_reviews['text'].str.contains(myHash, case=False, na=False)]

if not match.empty:
    found_asin = match.iloc[0]['parent_asin']

    found_book = df_books[df_books['parent_asin'] == found_asin].iloc[0]
    full_title = str(found_book['title'])
    
    print(f"Book Identified: {full_title}")

    # Replace all spaces with empty strings
    title_no_spaces = full_title.replace(" ", "")
    
    # Slice the first 8 characters
    target_string = title_no_spaces[:8]
    
    # 2. Compute SHA256 of that string
    flag_hash = hashlib.sha256(target_string.encode()).hexdigest()
    
    print(f"FLAG1: {flag_hash}")
    
else:
    print("No reviews found containing the target hash.")