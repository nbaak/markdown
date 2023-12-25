from markdown import Markdown


def main():
    document = Markdown('../README.md', new=True)
    section = document.add_node('', title='Markdown Editor')
    section.add_text('My attempt to crreate a Markdown Editor.')
    
    subsection = section.subsection('How 2 use', 'Example:')
    
    code_block = """
                document = Markdown('README.md')
                document.add_node('', title='headline')
                document.add_text('hello world')
                document.write()
                """ 
    
    subsection.add_code_block(code_block, 'python')
    
    document.write()



if __name__ == "__main__":
    main()