# RNA-seq data analysis

A python-orianted code designed to analyze given RNA-seq data and visualize it easily

## Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Description
This project was developed as a final assigment in the Python for Neuroscientists course of Sagol School of Neuroscience, Tel Aviv University
Group Participants:
- Ziv Bentulila
- Dekel David
- Dana Greenberg
- Noa Strauss
- Ran Perelman

The main objective of this code is to clean raw RNA-seq data, visualize it, and detect possible pathways that are affected by the experimental conditions.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/DanaGrnbrg/HackathonGroup4.git
    ```

2. Navigate to the project directory:
    ```bash
    cd task-manager
    ```

3. Create and activate a virtual environment (recommended):
    - On macOS/Linux:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```
    - On Windows:
      ```bash
      python -m venv venv
      venv\Scripts\activate
      ```

4. Install the dependencies listed in `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

5. Run the project:
    ```bash
    python main.py
    ```



## Usage
Define parameters in the main.py file before running it.
These parameters will allow to tailor functions specifically for your analysis.

## Features
- Load RNA-seq data in the form of Excel file
- Clean the data from missing values
- Extract genes that are lower than specific statistical significance value (adjusted by user) from the main dataset.
- Responsive design to generate figures
- Clean, curated dataset for further analysis

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

1. Fork the repository
2. Create a new branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Create a new Pull Request

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
