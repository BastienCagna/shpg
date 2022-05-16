"""
.. _page:

======================================
Render a page with basic HTML elements
======================================
"""

import shpg
import os.path as op
import webbrowser


# Create the HTML Page
page = shpg.Page(title="HTML Report Example")
# Define the list of HTML element composing the page
content = [
    shpg.Heading1("H1 Title"),
    shpg.Heading2("H2 Title"),
    shpg.Heading3("H3 Title"),
    shpg.Heading4("H4 Title"),
    shpg.Heading5("H5 Title"),
    shpg.Heading6("H6 Title"),
    shpg.Paragraph('This is the first paragraph of the generated SHPG page.'),
    shpg.Paragraph('This a second paragraph with a ', shpg.Link('./', 'link to this page'), '. Nothing more.')
]
# Add the element to the page content
page.content.extend(content)

# Save the html page with a local copy of the plot
report_path = "/tmp/html_report_example.html"
page.save(report_path, portable=True)

# Open it in the browser
webbrowser.open('file://' + op.realpath(report_path))
