# INFO-5940
Assignmen One Instructions and Changes

## Changes made to environment:
1. To decode the PDF files i have included and made use of the library PyPDF2, I have updated the configurations in the pyproject file to include this configuration.
    #### About the Library: 
    - This library is a free and open-source pure-python PDF library capable of splitting, merging, cropping, and transforming the pages of PDF files. You can find more about the library at the following link:
        - `https://pypi.org/project/PyPDF2/`
    #### Changes made to incorporate library: 
    -  Specificaly I added the following `PyPDF2 = "^3.0.1"` to the `pyproject.toml` file under the [tool.poetry.dependencies]  portion
    - Your pyproject[tool.poetry.dependencies]  portion should read as follows, feel to copy and past bellow to update:

    
            [tool.poetry.dependencies]
                python = "^3.11"
                aioboto3 = "^12"
                fsspec = "*"
                openai = "^1.14"
                pandas = "^2"
                poetry = "^1.7"
                pydantic = "^2"
                s3fs = "*"
                streamlit = "^1.0"
                tiktoken = "^0.7.0"
                langchain-community = "^0.2.15"
                langchain = "^0.2.15"
                langchain_core = "^0.2.15"
                langchain-openai = "^0.1.23"
                pydub = "^0.25.1"
                scipy = "^1.14.1"
                langchain-chroma = "^0.1.4"
                pypdf = "^4.3.1"
                Markdown = "^3.7"
                protobuf = "3.20.0"
                PyPDF2 = "^3.0.1"

        
## Instructions to RUN:
1. Please update the [pyproject.toml] file to include the configurations above, specifally the PyPFF2, feel free to copy and paste the [tool.poetry.dependecies] into the corresponding spot in the `pyproject.toml` file.
1. Please update the [docker-compose.yml] to contain your API keys and corresponding secrets to run the application
    - Please change the following on the `docker-compose.yml` file to include your secrets: 
        ```
        environment:
        AWS_PROFILE: aaii
        AZURE_OPENAI_API_KEY: <API_KEY>
        AZURE_OPENAI_ENDPOINT: <ENDPOINT>
        AZURE_OPENAI_MODEL_DEPLOYMENT: gpt-4
        OPENAI_API_KEY: <API_KEY>

2. Please save the docker-compose.yml and rebuild the container: 
    - click on the bottom left corner of your VS code. Then select "Rebuild Container"
3. In the docker container please open the terminal and in the terminal run `streamlit run chat_upload.py`
    - this should provide you with a link to the chatbot upload file interface
    - hit command and click the Local URL link in the terminal this will bring you straight to the chatbot application
4. Enjoy! Upload files and conversate with the chatbot AI User Interface.
    - please note that my code currently contains two versions and feel free to try both!!
        1. The default version is chunking AFTER the prompt
        2. To switch the version to chunking BEFORE the prompt I have detailed comment instructions in the `chat_upload.py` file follow the steps detailed there!
            - simply comment out the portion/version you don't want to run and uncomment the version you do want to run
            - note that the the default version AFTER the prompt is the code currently uncommented
            - [IMPORTANT!] Make sure to leave the begining code for client, llm, and title as mentioned in the comments. DO NOT ALTER this code!
5. Have fun! 


## Overview:

This application has many features which include a file upload chat interface. The files available for decipher and upload include pdfs and txt files. You can upload your files and ask the AI chatbot questions regarding files uploaded (note you CAN upload multiple files).
- to upload files click on upload icon and select desired pdf and txt files
- Interact with chatbot using prompts
- This application also has various versions to run:
        1. RAG before use prompt
        2. RAG after prompt
        - to run each one use the instructions provided above as well as instructions detailed in the `chat_upload.py file`
