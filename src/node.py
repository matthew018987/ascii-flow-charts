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
Manage the structure of nodes and the parsing of text data into structures 

A node is a structure that contains the details of a box in the chart.
The node list is a structure that contains the nodes and parsers for all elements


                                       |                                         
                             _______________________                             
                            |                       |                            
                            |   parse string list   |                            
                            |                       |                            
                             -----------------------                             
             __________________________|__________________________               
            |                          |                          |              
  _______________________    _______________________    _______________________  
 |                       |  |                       |  |                       | 
 |       string 1        |  |       string 2        |  |       string n        | 
 |                       |  |                       |  |                       | 
  -----------------------    -----------------------    -----------------------  
            |__________________________|__________________________|              
                                       |                                         
                             _______________________                             
                            |                       |                            
                            | string validity check |                            
                            |                       |                            
                             -----------------------                             
             __________________________|__________________________               
            |                          |                          |              
  _______________________    _______________________    _______________________  
 |                       |  |                       |  |                       | 
 | string 1 valid check  |  | string 2 valid check  |  | string n valid check  | 
 |                       |  |                       |  |                       | 
  -----------------------    -----------------------    -----------------------  
            |__________________________|__________________________|              
                                       |                                         
                             _______________________                             
                            |                       |                            
                            |   create structures   |                            
                            |                       |                            
                             -----------------------                             
                                       |                                         
                                       |                                         
                             _______________________                             
                            |                       |                            
                            |         nodes         |                            
                            |                       |                            
                             -----------------------                             
             __________________________|__________________________               
            |                          |                          |              
  _______________________    _______________________    _______________________  
 |                       |  |                       |  |                       | 
 |        node 1         |  |        node 2         |  |        node n         | 
 |                       |  |                       |  |                       | 
  -----------------------    -----------------------    -----------------------  
            |                          |                          |      

This chart was generated by this program, note this is not strictly representative of the program
'''


class Node:

    def __init__(self, name, text):
        """
        set node name & text
        calculate size of node based on amount of text

        Args:
            name: string containing the identifier of the name: character in range a..z
            text: string containing the words to display in the box

        Returns:
            none
        """
        self.name = name
        self.text = text
        text_lines = text.split('\\n')
        max_height = len(text_lines)
        max_width = 0
        # calc required width of node based on the text length
        for line in text_lines:
            max_width = max(max_width, len(line))
        self.width = max_width
        self.height = max_height
         
        # these fields will be set when processing coordinates and vertices
        self.column = 0
        self.row = 0
        self.vertices = []

    def add_coordinate(self, column, row):
        """ 
        configure the nodes coordindates (each node can be in one particular row/column)
     
        Args:
            column: int, 0 index column number
            row: int, 0 index row number
        """
        self.column = column
        self.row = row
        return

    def add_vertice(self, node):
        """
        each node can have a list of other nodes that it connects to, add a node to that list

        Args:
            node: object type node
   
        Retuns:
            none
        """
        self.vertices.append(node)
        return


class NodeList:

    def __init__(self):
        self.nodes = []

    def get_node(self, name):
        """
        get the node from the list of nodes that has matching name

        Args:
            name: string containing name of node to search for

        Returns:
            node: object type node
        """
        for node in self.nodes:
            if node.name == name:
                return node
        return

    #######################################################################################
    # check string validity
    #######################################################################################

    def node_str_valid(self, node_str):
        # test validity of string
        has_delimiter = '=' in node_str
        has_name = ord(node_str[0]) in range(97, 122)  # character between a..z
        has_text = len(node_str) > 2
    
        if not has_delimiter:
            print('node string does not contain valid delimiter: ', node_str)
        if not has_name:
            print('node string does not have a valid name\nname must be a character in the alphabet between a & z: ', node_str)
        if not has_text:
            print('node text label was not found: ', node_str)
        
        return has_delimiter & has_name & has_text 

    def coordinate_str_valid(self, coord_str):
        # test validity of string
        print(coord_str)
        has_delimiter = '=' in coord_str
        has_start_node = False
        if len(coord_str) > 0:
            has_start_node = ord(coord_str[0]) in range(97, 122)  # character between a..z
        has_y_coord = False
        if len(coord_str) > 2:
            has_y_coord = ord(coord_str[2]) in range(65, 90)   # character between A..Z
        has_x_coord = False
        if len(coord_str) > 3:
            has_x_coord = ord(coord_str[3]) in range(48, 57)   # number between 0-9
    
        if not has_delimiter:
            print('coordinate string does not contain valid delimiter: ', coord_str)
        if not has_start_node:
            print('coordinate string does not start with a valid node name: ', coord_str)
        if not has_x_coord:
            print('coordinate string does not have a valid column name: ', coord_str)
        if not has_y_coord:
            print('coordinate string does not have a valid row number: ', coord_str)
       
        return has_delimiter & has_start_node & has_x_coord & has_y_coord

    def vertices_str_valid(self, node_str):
        # test validity of string
        has_delimiter = ',' in node_str
        # nodes must be in range a..z
        has_start_node = ord(node_str[0]) in range(97, 122)
        has_end_node = ord(node_str[2]) in range(97, 122)
    
        if not has_delimiter:
            print('vertice string does not contain valid delimiter')
        if not has_start_node:
            print('vertice string does not start with a valid node name')
        if not has_end_node:
            print('vertice string does not end with a valid node name')
        
        return has_delimiter & has_start_node & has_end_node 

    #######################################################################################
    # parsers
    #######################################################################################

    def parse_node_str(self, node_str):
        """
        Populate this nodes parameters with the information from string

        Args:
            node_str: string containing the definition of this node
                format required: <node name>=<text to display in node>
                for example: "a=bootloader"
                node name is "a"
                node text is "bootloader"

        Returns:
            node: newly created Node

        Raises:
            node string parser error
        """
        if self.node_str_valid(node_str):
            try:
                terms = node_str.split('=')
                name = terms[0]
                text = terms[1]
                # create new node
                node = Node(name, text)
            except:
                raise Exception('node string parser error')

        return node  

    def parse_nodes_str(self, nodes_str):
        """
        process the list of strings containing all information about the nodes

        Args:
            node_str: list of strings, each string defined a node

        Returns:
            node
        """
        for node_str in nodes_str:
            node = self.parse_node_str(node_str)
            self.nodes.append(node)
        return

    def parse_coordinate(self, coordinate_str):
        """  
        process a coordinate string 

        Args:
            coordinate_str: string containing the coordinate definition
                format required: <node name>=<row name><column number>
                for example: "a=B2"
                node name is "a"
                coordinate is "B2"
                    B2 represents row 2 (B) column 2

        Return:
            none
        """
        if self.coordinate_str_valid(coordinate_str):
            try:
                terms = coordinate_str.split('=')
                # convert the string ie B2 into 0 indexed numbers
                row_num = ord(terms[1][0]) - 65
                col_num = int(terms[1][1]) - 1
            except:
                raise Excpetion('coordinate string parser error')

            # add the 0 indexed numbers to the node
            node = self.get_node(terms[0])
            node.add_coordinate(col_num, row_num)
        return

    def parse_coordinates_str(self, coordinates_str):
        """
        process the list of strings containing all information about the nodes coordindates

        Args:
            coordinate_str: list of strings, each string defines a coordindate of a node

        Returns:
            none
        """
        for coordinate in coordinates_str:
            self.parse_coordinate(coordinate)   
        return

    def parse_vertice(self, vertice):
        """
        process the string containing the vertice definition

        Args:
            vertice: string, containing vertice definition

        Returns:
            none

        Raises:
            vertice string parsing error
        """
        if self.vertices_str_valid(vertice):
            try:
                points = vertice.split(',')
                # get the nodes by name 
                node_start = self.get_node(points[0])
                node_end = self.get_node(points[1])
                # add the second node the list of the first
                node_start.add_vertice(node_end)
            except:
                raise Exception('vertice string parsing error')

        return

    def parse_vertices_str(self, vertices_str):
        """
        process the list of strings containing all information about the lines that join the nodes

        Args:
            vertice_str: list of strings, each string defines a vertice between 2 nodes

        Returns:
            none
        """
        for vertice in vertices_str:
            self.parse_vertice(vertice)
        return
 
