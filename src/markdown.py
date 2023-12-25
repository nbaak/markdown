import re
import os


class MDNode:

    def __init__(self, title=None, content=None, parent=None):
        self.title = title
        self.content = [] if content is None else [content]
        self.children = []
        self.parent = parent  # Reference to the parent node
        
    def subsection(self, title, content=None):
        return self.add_node(title, content)

    def add_node(self, title, content=None):
        node = MDNode(title=title, content=content, parent=self)
        self.children.append(node)
        return node

    def add_text(self, text):
        self.content.append(text)
        
    def add_image(self, alt_text, image_url):
        image_markdown = f"![{alt_text}]({image_url})"
        self.content.append(image_markdown)

    def add_link(self, link_text, link_url):
        link_markdown = f"[{link_text}]({link_url})"
        self.content.append(link_markdown)
        
    def add_code_block(self, code, language=None):
        code = [line.strip() for line in code.strip().splitlines()]
        code = '\n'.join(code)
        if language:
            code_block_markdown = f"```{language}\n{code.strip()}\n```"
        else:
            code_block_markdown = f"```\n{code.strip()}\n```"
            
        self.content.append(code_block_markdown)

    def __str__(self, level=0):
        title_str = f"{self.title}" if self.title else ""
        text_content = '\n\n'.join(self.content)
        result = f"{'#' * (level + 1)} {title_str}\n\n{text_content}\n\n"
        for child in self.children:
            result += child.__str__(level + 1)
        return result

    def __repr__(self):
        return f"T:{self.title} {self.children}"


class Markdown:

    def __init__(self, file_path=None, new=False):
        self.file_path = file_path
        self.document = []
        if file_path and os.path.isfile(file_path) and not new:
            self.load_from_file(file_path)

    def load_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            md_content = file.readlines()

        self.document = []  # Clear existing document
        stack = []  # Stack to keep track of parent sections
        current_section = None

        for line in md_content:
            line = line.strip()
            if not line:
                # Skip empty lines
                continue

            if line.startswith('#'):
                left = line.split(' ')[0]
                # Determine the header level
                header_level = left.count('#')
                title = line.strip('# ').strip()
                new_section = MDNode(title=title)

                if not stack:
                    # Top-level header, append to the document
                    self.document.append(new_section)
                    current_section = new_section
                elif header_level == len(stack) + 1:
                    # Subsection, append to the current parent
                    stack[-1].add_node(title=new_section.title)
                    current_section = stack[-1].children[-1]
                else:
                    # Adjust the stack to the correct level
                    while len(stack) >= header_level:
                        stack.pop()
                    
                    if header_level == 1:
                        n = self.document.append(new_section)
                        current_section = new_section
                        

                stack.append(current_section)  # Push the new section onto the stack
            elif current_section:
                # If not a header line and there's a current_section, append the content
                current_section.add_text(line)
                
    def write(self):
        if self.file_path:
            self.save_to_file(self.file_path)

    def save_to_file(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            for node in self.document:
                file.write(str(node))
    
    def section(self, parent_title, title, content=None):
        return self.add_node(parent_title, title, content)

    def add_node(self, parent_title, title, content=None):
        parent = self._find_node(self.document, parent_title)
        if parent:
            return parent.add_node(title, content)
        else:
            if not parent_title:  # Adding to root
                node = MDNode(title=title, content=content)
                self.document.append(node)
                return node
            else:
                print(f"Parent node '{parent_title}' not found.")
                return None

    def add_text(self, title, text):
        node = self._find_node(self.document, title)
        if node:
            node.add_text(text)
        else:
            print(f"Node '{title}' not found.")

    def show(self):
        if self.document:
            for node in self.document:
                print(str(node))
        else:
            print("No Markdown content to display.")
            
    def get_node(self, title):
        return self._find_node(self.document, title)

    def _find_node(self, nodes, title):
        for node in nodes:
            if node.title == title:
                return node
            child_node = self._find_node(node.children, title)
            if child_node:
                return child_node
        return None

