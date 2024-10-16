# Y-Tables: html table parser & color-coder
Extract key-value pairs from table entries and display as individual columns with color gradient. Support multi-keyword searching and row highlight.

## System setup
1. Python Flask is required
2. Clone the code to your local repository
3. Run app.py and launch the web application at localhost:5002 with a web browser

## Application usage
1. Right click to [Inspect] the website that contains the table to be processed (e.g., "Active project proposals")
2. Find the "tbody" section, right click, and select "Edit as HTML"
3. Ctrl A + Ctrl C, Copy the HTML of "tbody" to the input box of this application
4. Enter a list of keywords to be found within the "Title" section of each table row; Case insensitive (Abc=ABC=abc); Partial match ("Reinforcement learning": "reinforce", "inforc", "ment lear", ...)
5. Click "Create table", and the processed table will be displayed below

## Output format
A table displaying popularity values of every attribute (e.g., 1,2,..,SNR,) in color gradient (darker color means more popular). Rows containing any of the keywords supplied will be highlighted in green color. Hover mouse on the "Title" column, all matching keywords will be displayed.

## Disclaimer
This web application is not collecting any personal information. No login or sign up required.
