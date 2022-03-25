import html_report as html
from html_report.page import Paragraph


book = html.Book('Example website')
subpage = html.Page(title="Subpage 1")
book.pages.append(subpage)

links = {"Home": book.index, "Sub page": subpage}
menu = html.HMenu(links)
header = html.Div(html.Heading1("Example website"), menu)
footer = html.Footer("Example footer", {'Links': links, 'Contact': Paragraph("E-Mail: bastien.cagna@cea.fr")})

subpage.content.append(header)
subpage.content.append(html.Heading2("Sub page 1"))
subpage.content.append(html.Paragraph("This is a sub page of the book."))
subpage.content.append(footer)

book.index.title = 'Example website | Home'
book.index.content.append(header)
book.index.content.append(html.Heading2("Welcome Home!"))
book.index.content.append(html.Paragraph("Follow this link to go to " + subpage.link("sub page")))
book.index.content.append(footer)

book.save("/tmp/example_book.html", portable=False)