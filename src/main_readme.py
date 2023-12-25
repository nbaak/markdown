from markdown import Markdown


def main():
    document = Markdown('../README.md', new=True)
    section = document.add_node('', title='Markdown Editor')
    section.add_text('My attempt to crreate a Markdown Editor.')
    
    subsection = section.subsection('How 2 use', 'Example:')
    subsection.add_text('''```python\n
                        document = Markdown('README.md')\n
                        document.add_node('', title='headline')\n
                        document.add_text('hello world')\n
                        document.write()\n
                        ```\n
                        ''')
    
    document.write()



if __name__ == "__main__":
    main()