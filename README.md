# Static HTML Page Generator

## Quick Start
### Installation
for now shpg is available through GitHub. You can install by cloning the project and renning setup.py:
```shell
git clone https://github.com/BastienCagna/shpg.git
cd shpg
python setup.py install
```
N.B: replace "install" by "develop" if you want to contribute to development or customize the package.
N.B2: use --user to install the package only for you (might be mandatory depending of the rights you have)

### Basic example
```python
import shpg

# Create the HTML Page
page = shpg.Page(title="My Page")
page.content.append(shpg.Heading1("Hello world!"))
page.content.append(shpg.Paragraph('This is my first page using SHPG.'))

# Generate the HTML page
report_path = "/tmp/my_page.html"
page.save(report_path, portable=True)
```

### Documentation
No documentation is available for now.
