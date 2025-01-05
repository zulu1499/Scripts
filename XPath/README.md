# XML Extraction Tools Using Oracle-Based Techniques

This repository contains two Python scripts designed to interact with vulnerable web applications and extract XML data or schemas. These tools leverage blind oracle attacks, payload crafting, and recursive exploration to reveal hidden data structures.

---

## Script 1: `xml_schema_extractor.py`

### Overview

The `xml_schema_extractor.py` script extracts the schema of an XML document through blind SQL/XML injection techniques. It recursively explores nodes, determines their names, child counts, and text content.

### Features

- **Recursive Schema Extraction**: Traverses XML hierarchies to construct a full schema.
- **Binary Search Optimization**: Efficiently determines node lengths and child counts.
- **Visualization**: Outputs the extracted schema in a structured format.
- **Flexible Integration**: Ready for visualization or extended analysis.

### Usage

1. **Prerequisites**:
   - Install the required dependencies:
     ```bash
     pip install requests lxml termcolor
     ```

2. **Execution**:
   - Update the `url` variable with the target application URL.
   - Run the script:
     ```bash
     python xml_schema_extractor.py
     ```

3. **Output**:
   - The extracted schema is displayed in the terminal or optionally saved as a formatted XML file.

---

## Script 2: `xml_data_extractor.py`

### Overview

The `xml_data_extractor.py` script extracts XML content by exploring nodes up to a specified depth. It uses crafted payloads to identify and retrieve data from web application responses.

### Features

- **Payload-Based Extraction**: Extracts data using custom query strings.
- **Depth Exploration**: Dynamically explores XML content at increasing depths.
- **Looping Over Nodes**: Iterates through potential child nodes at each depth to retrieve all data.

### Usage

1. **Prerequisites**:
   - Install the required dependencies:
     ```bash
     pip install requests lxml
     ```

2. **Execution**:
   - Update the `url` variable with the target application URL.
   - Run the script:
     ```bash
     python xml_data_extractor.py
     ```

3. **Output**:
   - Extracted XML content is stored in the `xml_document` list and displayed in the terminal.

---

## Sample Workflow

### Extracting XML Schema

1. **Define Target**: Update the URL for the vulnerable application.
2. **Run the Schema Extractor**: Launch `xml_schema_extractor.py` to retrieve and visualize the XML structure.

   Example schema output:
   ```python
   {
       'name': 'accounts',
       'path_parts': ('accounts',),
       'children_count': 2,
       'children': [
           {
               'name': 'user[1]',
               'path_parts': ('accounts', 'user[1]'),
               'children_count': 0,
               'text_content': 'John Doe'
           },
           {
               'name': 'user[2]',
               'path_parts': ('accounts', 'user[2]'),
               'children_count': 0,
               'text_content': 'Jane Smith'
           }
       ]
   }
