# MIT License
#
# Copyright (c) 2022 matthew018987@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
Process the input file

Process input fields into lists, parse each list into their respective data structures,
render the chart from the data structures.



           |
  _____________________
 |                     |
 | load data from file |
 |                     |
  ---------------------
           |
           |
  _____________________
 |                     |
 |     parse nodes     |
 |                     |
  ---------------------
           |
           |
  _____________________
 |                     |
 |  parse coordinates  |
 |                     |
  ---------------------
           |
           |
  _____________________
 |                     |
 |   parse vertices    |
 |                     |
  ---------------------
           |
           |
  _____________________
 |                     |
 |       render        |
 |                     |
  ---------------------
           |

This flow chart was creared by this program
'''

from node import NodeList
from renderer import Renderer


class FileProcessor:
    """
    A class to manage the loading of the input file and execution of processing and
    plotting function

    Attributes:
        nodes_strings: list of strings
            contains strings from nodes section of input file
        coordinates_strings: list of strings
            contains strings from coordinates section of input file
        vertices_strings: list of strings
            contains strings from vertices section of input file

    Methods:
        load_input_file(file_path):
            load strings from input file into string lists
            print the number of lines found in each of the 3 sections
        plot_chart():
            call functions to load strings from lists into structures
            call functions to print output to stdout
    """

    def __init__(self):
        self.nodes_strings = []
        self.coordinates_strings = []
        self.vertices_strings = []

    def load_input_file(self, file_path):
        """
        we are expecting 3 sections in a file (nodes, coordinates, vertices)
        create a list of the lines from the file under each header

        Args:
            file_path: string containing the path to the input file

        Returns:
            none
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as chart:
                line = chart.readline().strip()
                while line:
                    # once we have found the nodes header
                    # process all following lines until we hit an empty line
                    if line == 'nodes':
                        line = chart.readline().strip()
                        while line != '':
                            self.nodes_strings.append(line)
                            line = chart.readline().strip()

                    # once we have found the coordinates header
                    # process all following lines until we hit an empty line
                    if line == 'coordinates':
                        line = chart.readline().strip()
                        while line != '':
                            self.coordinates_strings.append(line)
                            line = chart.readline().strip()

                    # once we have found the verticess header
                    # process all following lines until we hit an empty line
                    if line == 'vertices':
                        line = chart.readline().strip()
                        while line != '':
                            self.vertices_strings.append(line)
                            line = chart.readline().strip()

                    line = chart.readline().strip()
        except Exception as error:
            raise Exception('file format error occured') from error

        chart.close()

        print('number of nodes found: ', len(self.nodes_strings))
        print('number of coordinates found: ', len(self.coordinates_strings))
        print('number of vertices found: ', len(self.vertices_strings))
        print('')

    def plot_chart(self):
        """
        check that we have a list of the necessary information from the input file
        parse each set of information, then execute plotting of chart

        Args:
            none

        Returne:
            none
        """
        has_graph = self.nodes_strings and self.coordinates_strings and self.vertices_strings
        if has_graph:
            try:
                # process data structures
                nodes = NodeList()
                nodes.parse_nodes_str(self.nodes_strings)
                nodes.parse_coordinates_str(self.coordinates_strings)
                nodes.parse_vertices_str(self.vertices_strings)

                # render data structures
                renderer = Renderer()
                renderer.draw_chart(nodes)
            except Exception as error:
                raise Exception('error parsing input file') from error
        else:
            print('input file did not contain: nodes, coordinates and vertices')
