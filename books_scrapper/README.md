# Books Scrapper

## Features

- Grabs book data from website.
- Allows users to query the script for books in a particular genre with an optional rating e.g. "Romance 5".
- Returns max of 10 books that meet that criteria, sorted by price in descending order.
- Each item in the returned list of books must have a title property, description, price and rating.


### Implementation

I have to create a dictionary that matches a user's query to the correct URL. A sample of the dictionary would be

Python
```
{
    travel: "...url",
    romance: "...url".
    etc: "..."
}



```