# AI Plant Monitor

The AI Plant Monitor is an innovative project that integrates Raspberry Pi with the Adafruit STEMMA soil sensor to provide real-time soil condition monitoring through a Chat GPT-based model. This tool is perfect for gardening enthusiasts, educators, or anyone interested in plant care and technology.

## Prerequisites

Before you begin, ensure you have the following:
- A Raspberry Pi set up with internet access.
- An Adafruit STEMMA soil sensor connected to your Raspberry Pi.
- An OpenAI API key, Assistant ID, and Thread ID. You can obtain these from your OpenAI account on the [OpenAI Platform](https://platform.openai.com/assistants).

## Installation

1. **Clone the Repository**

   Open a terminal on your Raspberry Pi and run the following command to clone the repository:

   git clone https://github.com/Concept-Bytes/ai_plant.git

   Navigate into the project directory:

2. **Install Dependencies**

    Install the required Python packages:

3. **Configuration**

    Open `assist.py` in a text editor of your choice. Fill in your OpenAI API key, Assistant ID, and Thread ID in the designated spots. This information is critical for the AI functionality of the project and can be         obtained from your OpenAI account.
    
    ```python
    # Example placeholder in assist.py
    openai.api_key = "your_openai_api_key_here"
    assistant_id = "your_assistant_id_here"
    thread_id = "your_thread_id_here"

    
## Running the Application

After completing the setup and configuration, run the application with:

```python plant.py```

This script will initiate monitoring and interaction with the Chat GPT-based model to analyze and report on your plant's soil conditions.

## Contributing
Contributions to the AI Plant Monitor are welcome! Please feel free to fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file in the repository for details.
