import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_for_pathway(gene_name: str) -> list:
    """
    Find the pathway a gene is part of in the reactome.org database using only requests and BeautifulSoup.

    Args:
        gene_name (string): The name of the gene.

    Returns:
        list: List of pathways that the gene is part of.

    Raises:
        TypeError: If input is not of type string.
    """
    
    # Raise TypeError if the input is not a string
    if not isinstance(gene_name, str):
        raise TypeError("Input must be of type string")

    # Step 1: Search for the gene using requests
    search_url = f"https://reactome.org/content/query?q={gene_name}"
    search_response = requests.get(search_url)

    # Check if the request was successful
    if search_response.status_code != 200:
        return []

    # Step 2: Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(search_response.text, 'html.parser')

    # Check if the page contains "No results found"
    if f"No results found for {gene_name}" in soup.get_text():
        return []  # Return an empty string immediately if no results found

    # Step 3: Find the specific div with class 'result-title'
    div = soup.find('div', class_='result-title')

    # Step 4: Extract the link within the div if present
    if div:
        a_tag = div.find('a')  # Find the first <a> tag within the div
        if a_tag:
            relative_link = a_tag['href']  # Get the href attribute (URL) from the <a> tag
            absolute_link = urljoin("https://reactome.org/content/", relative_link)  # Combine base URL with relative URL

            # Step 5: Use requests to load the pathway page
            pathway_response = requests.get(absolute_link)

            if pathway_response.status_code != 200:
                return []

            # Step 6: Parse the pathway page with BeautifulSoup
            pathway_soup = BeautifulSoup(pathway_response.text, 'html.parser')


            # Step 7: Find the fieldset with class 'fieldset-details'
            fieldset = pathway_soup.find('fieldset', class_='fieldset-details')

            if fieldset:
                # Find all the outermost <div> elements inside the fieldset
                outer_divs = fieldset.find_all('div', recursive=False)
                span_values = []  # To store the span values
                # Loop through each outermost div and find the first span inside it
                # Assuming you have already found the fieldset as fieldset
                # Initial layer is 1 for the outermost div
                layer = 1

                # Iterate through outer divs
                for outer_div in outer_divs:
                    # Create a stack to hold divs and their layer number
                    stack = [(outer_div, layer)]
                    # Process each div in the stack
                    while stack:
                        current_div, current_layer = stack.pop()
                        # Find and print all direct span elements in the current div
                        spans = current_div.find_all('span', recursive=False)
                        for span in spans:
                            span_values.append(span.text.strip())
                        
                        # Find all direct nested divs and add them to the stack with incremented layer number
                        nested_divs = current_div.find_all('div', recursive=False)
                        for nested_div in nested_divs:
                            stack.append((nested_div, current_layer + 1))

                if span_values:
                    return span_values # Return the span values separated by newlines
                else:
                    return []
            else:
                return []
    
    return []
