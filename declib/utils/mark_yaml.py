"""
MarkYaml is a formanteau, parsing Markdown-style headers into
a data structure, with content parsed as YAML

This is to improve readability over YAML and allows for managing
data documents comfortably in a Markdown editor

"""
from collections import OrderedDict

import yaml


class MarkYamlDataLoader:
    """
    Load data from a MarkYaml file

    `data = MarkYamlDataLoader(data_path).data`

    Args:
        data_path (str OR os.PathLike): 

    """
    def __init__(self, data_path):

        with open(data_path) as fh:
            doc_lines = fh.read().splitlines()

        self.data = {
            'name': 'root',
            'data_path': [],
            'header_depth': 0,
            'content': None,
            'children': OrderedDict(),
            'render_children_as_list': False
        }

        self.prev = self.data
        self.block_lines = []

        for line in doc_lines:
            self.read_line(line)

        # Load content into last element
        self.prev['content'] = yaml.safe_load('\n'.join(self.block_lines))

        self.data = self.restructure_data(self.data)


    def read_line(self, line):

        # Skip if comment line
        if line.startswith("//"):
            return

        # If not a header line, add to block and move on to next line
        if not line.startswith("#"):
            self.block_lines.append(line)
            return

        # Load previous block lines into content 
        self.prev['content'] = yaml.safe_load('\n'.join(self.block_lines))


        # Parse header line
        split_line = line.split()
        header_depth = len(split_line.pop(0))
        render_children_as_list = False
        if split_line and split_line[0] == "-":
            render_children_as_list = True
            split_line.pop(0)

        element_name = ' '.join(split_line)

        if header_depth > self.prev['header_depth']:
            # Going deeper - entry is child of previous
            parent = self.prev

        else:
            # Moving up or sibling
            # Start from root and follow path of children to find parent
            parent = self.data
            for node_name in self.prev['data_path']:
                node = parent['children'][node_name]
                if header_depth <= node['header_depth']:
                    break
                parent = node

        parent['children'][element_name] = {
            'name': element_name,
            'data_path': [ *parent['data_path'], element_name ],
            'header_depth': header_depth,
            'content': None,
            'children': OrderedDict(),
            'render_children_as_list': render_children_as_list
        }

        self.block_lines = []
        self.prev = parent['children'][element_name]


    def restructure_data(self, data):

        content = data['content']
        children = data['children']

        if type(content) is dict:
            content['name'] = data['name']

        if not children:
            return content

        cleaned_data = OrderedDict()
        if content:
            if type(content) is dict:
                cleaned_data.update(content)
            else:
                cleaned_data['content'] = content

        for child in children.values():
            child_data = self.restructure_data(child)

            cleaned_data[child['name']] = child_data

        if data['render_children_as_list']:
            cleaned_data = [ *cleaned_data.values() ]

        return cleaned_data
