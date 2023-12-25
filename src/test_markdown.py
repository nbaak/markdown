from markdown import Markdown


def test_create():
    # Example usage
    md = Markdown()

    # Adding sections and text
    section1 = md.add_node('', title='1st Section #1', content='This is Section 1 content.')
    section1.add_text('Additional text for Section 1.')
    ss1 = section1.add_node(title="1st Subsection", content="A sub section!")
    
    ss2 = ss1.add_node(title="SubSubSection", content="a sub sub section.. let's see.")

    sec2 = md.add_node('', title="2nd Section!", content="woooooooot")
    sec2.add_text('woohoo')
    # Save to file
    md.save_to_file('example.md')

    print(md.document)


def test_read():
    md = Markdown()
    md.load_from_file('example.md')
    md.show()

    print('#################')
    node = md.get_node('SubSubSection')
    
    print(md.document)


def test_read_edit_write():
    md = Markdown()
    md.load_from_file('example.md')

    node = md.get_node('1st Subsection')
    node.add_text("meow!")
    
    node2 = md.get_node('SubSubSection')
    node2.add_text('more text')
    
    subsection = node.subsection('How 2 use', 'Example:')
    
    code_block = """
                document = Markdown('README.md')
                document.add_node('', title='headline')
                document.add_text('hello world')
                document.write()
                """
    subsection.add_code_block(code_block, 'python')

    md.save_to_file('example.md')
    
    print(md.document)
    md.show()


if __name__ == "__main__":
    test_create()
    test_read()
    test_read_edit_write()

