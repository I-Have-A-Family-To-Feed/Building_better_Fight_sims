# Building_better_Fight_sims
This tool extracts data from Warcraftlogs reports, and uses it to generate a Script to model that enounter in Simulationcraft
This script can then be used in Simulationcraft or in Raidbots. 

### Prerequisites

## Installation Instructions

### Linux

- **Arch Linux**:
  1. Update your package list:
     ```bash
     sudo pacman -Syu
     ```
  2. Install Python and pip:
     ```bash
     sudo pacman -S python python-pip
     ```

- **Debian**:
  1. Update your package list:
     ```bash
     sudo apt update
     ```
  2. Install Python and pip:
     ```bash
     sudo apt install python3 python3-pip
     ```

- **Fedora**:
  1. Update your package list:
     ```bash
     sudo dnf update
     ```
  2. Install Python and pip:
     ```bash
     sudo dnf install python3 python3-pip
     ```

- **Ubuntu** (and other Ubuntu-based derivatives):
  1. Update your package list:
     ```bash
     sudo apt update
     ```
  2. Install Python and pip:
     ```bash
     sudo apt install python3 python3-pip
     ```

- **Other Linux distributions**:
  - Consult your distribution’s documentation to install Python and pip.

### macOS

- **Homebrew**:
  1. Install Homebrew:
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
  2. Install Python:
     ```bash
     brew install python
     ```

- **App Store**:
  1. Open the App Store, search for "Python", and install the latest version.

### Windows

- **Winget**:
  1. Open terminal/powershell prompt as administrator.
  2. Install Python:
     ```bash
     winget install Python.Python.3
     ```

- **Chocolatey**:
  1. Open terminal/powershell prompt as administrator.
  2. Install Chocolatey:
     ```bash
     Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
     ```
  3. Install Python:
     ```bash
     choco install python
     ```

### Cloning the Repository

1. Open your terminal or command prompt.
2. Navigate to the directory where you want to clone the project.
3. Run the following command to clone the repository:
   ```
   git clone https://github.com/CautexWoW/Building_better_Fight_sims.git
   ```
4. Navigate into the project directory:
   ```
   cd Building_better_Fight_sims
   ```

### Setting up the Virtual Environment

1. Create a virtual environment:
   ```
   python -m venv venv
   ```
2. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

### Creating the `header.py` File with Bearer Token

1. Obtain your Warcraft Logs API key by following the instructions on the [Warcraft Logs API documentation](https://www.warcraftlogs.com/v2-api-docs/).
2. Create a new file named `header.py` in the project directory.
3. Add the following content to the `header.py` file, replacing `YOUR_BEARER_TOKEN` with your actual API key:
   ```python
   headers = {
       'Authorization': 'Bearer YOUR_BEARER_TOKEN',
   }
   ```

### Using the Project

1. Run the main script:
   ```
   python Main.py
   ```
2. Follow the on-screen instructions to input the necessary data and generate the Simulationcraft script.

### Reporting Issues

If you encounter any issues or have questions, please report them on the project's GitHub Issues page. Provide as much detail as possible, including error messages and steps to reproduce the issue.

### Troubleshooting

If you encounter any issues while using the project, here are some steps to help you troubleshoot and resolve them:

1. **Check the Python version**: Ensure you are using a compatible version of Python. This project requires Python 3.x. You can check your Python version by running `python --version` or `python3 --version` in your terminal or command prompt.

2. **Verify dependencies**: Make sure all required dependencies are installed. You can check the `requirements.txt` file for the list of dependencies and install them using `pip install -r requirements.txt`.

3. **Check for typos**: Double-check your code and configuration files for any typos or syntax errors. Even a small mistake can cause issues.

4. **Review error messages**: If you encounter an error, carefully read the error message. It often provides valuable information about the cause of the issue and potential solutions.

5. **Update dependencies**: Ensure you are using the latest versions of the required dependencies. You can update them by running `pip install --upgrade -r requirements.txt`.

6. **Check for known issues**: Visit the project's GitHub repository and check the Issues section for any known issues or bug reports. You may find that your issue has already been reported and a solution is available.

### Submitting a Bug Report

If you encounter a bug while using the project, please follow these steps to submit a bug report:

1. **Check for existing issues**: Before submitting a new bug report, check the project's GitHub Issues page to see if the issue has already been reported. If it has, you can add any additional information you have to the existing issue.

2. **Create a new issue**: If the issue has not been reported, create a new issue on the project's GitHub Issues page. Provide a clear and descriptive title for the issue.

3. **Describe the bug**: In the issue description, provide a detailed explanation of the bug. Include the following information:
   - A clear and concise description of what the bug is.
   - Steps to reproduce the bug. Include any relevant code snippets, configuration files, or commands.
   - Expected behavior. Describe what you expected to happen.
   - Actual behavior. Describe what actually happened.
   - Screenshots or error messages, if applicable.

4. **Provide environment details**: Include information about your environment, such as:
   - Operating system and version.
   - Python version.
   - List of installed dependencies and their versions. You can obtain this information by running `pip freeze` in your terminal or command prompt.

5. **Additional context**: If there is any other information that might help in diagnosing and fixing the issue, include it in the bug report.
