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
functions to create a 2D grid that will be filled with lines and text

The sequence of steps:
 - a set of nodes must first be created
 - draw_chart is called passing in the nodes object
   - this determines the grid size required for the nodes
   - creates an empty grid for rendering in
   - fills the grid with boxes, text and lines joining the boxes
   - print the grid as ascii text


                                                          |
                                          ____________________________________
                                         |                                    |
                                         | iterate through nodes to get sizes |
                                         |                                    |
                                          ------------------------------------
                    _______________________________________|_______________________________________
                   |                                       |                                       |
  ____________________________________    ____________________________________    ____________________________________
 |                                    |  |                                    |  |                                    |
 |               size 1               |  |               size 2               |  |               size n               |
 |                                    |  |                                    |  |                                    |
  ------------------------------------    ------------------------------------    ------------------------------------
                   |_______________________________________|_______________________________________|
                                                           |
                                          ____________________________________
                                         |                                    |
                                         |       find the largest size        |
                                         |                                    |
                                          ------------------------------------
                                                           |
                                                           |
                                          ____________________________________
                                         |                                    |
                                         |            create grid             |
                                         |                                    |
                                          ------------------------------------
                    _______________________________________|_______________________________________
                   |                                       |                                       |
  ____________________________________    ____________________________________    ____________________________________
 |                                    |  |                                    |  |                                    |
 |             draw box 1             |  |             draw box 2             |  |             draw box n             |
 |                                    |  |                                    |  |                                    |
  ------------------------------------    ------------------------------------    ------------------------------------
                   |                                       |                                       |
                   |                                       |                                       |
  ____________________________________    ____________________________________    ____________________________________
 |                                    |  |                                    |  |                                    |
 |            draw text 1             |  |            draw text 2             |  |            draw text n             |
 |                                    |  |                                    |  |                                    |
  ------------------------------------    ------------------------------------    ------------------------------------
                   |_______________________________________|_______________________________________|
                                                           |
                                          ____________________________________
                                         |                                    |
                                         |    draw vertices between boxes     |
                                         |                                    |
                                          ------------------------------------
                                                           |
                                                           |
                                          ____________________________________
                                         |                                    |
                                         |         print ascii output         |
                                         |                                    |
                                          ------------------------------------
                                                           |


This chart was generated by this program, note this is not strictly representative of the program
'''


class Renderer:
    """
    Class to managed functions that process strcutures into a 2D array of characters then
    print to stdout

    Attributes:
        grid: array of characters
            used for populating characters that represent the chart
        max_col: int
            value of the highest column number used
        max_row: int
            value of the highest row number used
        max_width: int
            valud of the widest
    """
    def __init__(self):
        self.grid = []
        self.max_col = 0
        self.max_row = 0
        self.max_width = 0
        self.max_height = 0
        self.row_width = 0
        self.row_height = 0

    def create_grid(self, nodes):
        """
        create a 2D grid of whitespaces that is large enough to fill our nodes with
        defined text

        Agrs:
            nodes: array of type node

        Return:
            none
        """
        # find the widest column and longest row in the set of nodes
        # the grid spacing will be set to the size required by the max values
        for node in nodes:
            self.max_col = max(self.max_col, node.column)
            self.max_row = max(self.max_row, node.row)
            self.max_width = max(self.max_width, node.width)
            self.max_height = max(self.max_height, node.height)
        # set the height/width by finding the max text width and adding spacing and padding
        self.row_width = self.max_width + 6
        self.row_height = self.max_height + 6
        # define the grid area by finding the largest columns/row numbers and multiply
        # by the height/width
        grid_width = self.row_width * (self.max_col + 1)
        grid_height = self.row_height * (self.max_row + 1)
        # create a 2 dimensional array containing white spaces
        self.grid = [ [ ' ' for x in range( grid_width ) ] for y in range( grid_height ) ]

    def draw_node(self, node):
        """
        draw a single node by filling in the grid with borders and text

        Args:
            node: object node that we wish to draw
        """

        # find the position of node within the grid
        x_offset = (node.column * self.row_width)
        y_offset = (node.row * self.row_height)

        # draw top of box
        for i in range(2,self.max_width+4):
            self.grid[1 + y_offset][i + x_offset] = '_'
        # draw bottom of box
        for i in range(2,self.max_width+4):
            self.grid[self.max_height+4 + y_offset][i + x_offset] = '-'
        # draw left of box
        for i in range(2,self.max_height+4):
            self.grid[i + y_offset][1 + x_offset] = '|'
        # draw right of box
        for i in range(2,self.max_height+4):
            self.grid[i + y_offset][self.max_width+4 + x_offset] = '|'
        # draw text
        text_offset = (self.max_width - len(node.text)) // 2
        for i, character in enumerate(node.text):
            self.grid[3 + y_offset][i + x_offset + text_offset + 3] = character

    def draw_vertices(self, node):
        """
        draw the lines that join a node to all other nodes below it

        Args:
            node: object of type node

        Returns:
            none
        """

        # chart must flow from top to bottom
        # vertices can only exit a node from the bottom of the node
        # vertices can only enter a node from the top of the node

        # draw the exit nib from the start node
        x_coord_exit = (node.column * self.row_width) + (self.max_width // 2) + 2
        y_coord_exit = (node.row * self.row_height) + self.max_height + 5
        self.grid[y_coord_exit][x_coord_exit] = '|'

        # draw the entry nib to the end node
        x_coord_entry = (node.column * self.row_width) + (self.max_width // 2) + 2
        y_coord_entry = (node.row * self.row_height)
        self.grid[y_coord_entry][x_coord_entry] = '|'

        # draw horizontal line from start nib to end nib
        for vertice in node.vertices:
            if node.row < vertice.row:
                if node.column > vertice.column:
                    x_coord = (vertice.column * self.row_width) + (self.max_width // 2) + 2
                    for i in range(x_coord + 1, x_coord_exit):
                        self.grid[y_coord_exit][i] = '_'

                if node.column < vertice.column:
                    x_coord = (vertice.column * self.row_width) + (self.max_width // 2) + 2
                    for i in range(x_coord_exit + 1, x_coord):
                        self.grid[y_coord_exit][i] = '_'

    def print_grid(self):
        """
        print the contains of the 2D grid array as text to stdout

        Args:
            none

        Returns:
            none
        """

        for row in self.grid:
            row_str = ''
            print(row_str.join(row))

    def draw_chart(self, nodes):
        """
        create a 2D grid
        iterate over all nodes in the nodes list
        draw the node
        draw the lines between the nodes

        Args:
            nodes: list of type node

        Returns:
            none
        """
        self.create_grid(nodes.nodes)
        for node in nodes.nodes:
            self.draw_node(node)
            self.draw_vertices(node)
        self.print_grid()
