# Medical Chatbot

## Initial Setup

### Prerequisites

- Windows with PowerShell
- Python 3.12
- uv

Verify the installed tools:

```
py --version
uv --version
```

### 1. Create the Project Directory

```
mkdir D:\projects\medical_chatbot
cd D:\projects\medical_chatbot
```

If the project directory already exists, navigate to it:

```
cd D:\projects\medical_chatbot
```

### 2. Initialize the Python Project

```
uv init --python 3.12
```

This initializes the project and creates the basic project files, including `pyproject.toml` and `main.py`.

### 3. Create a Virtual Environment

```
uv venv
```

This creates a project-local `.venv` directory.

### 4. Activate the Virtual Environment

```
.\.venv\Scripts\Activate.ps1
```

### 5. Install Project Dependencies

-- add a dependency
uv add fastapi

This adds the dependencies to `pyproject.toml`, resolves compatible package versions, installs the dependencies into the project environment, and creates or updates `uv.lock`.

-- Check a specific dependency already installed 
uv pip show dependency_name

### 6. Synchronize Dependencies

To install dependencies for an existing checkout of the project using its configuration and lockfile, run:

```
uv sync
```

Keep `pyproject.toml` and `uv.lock` in version control so other developers can reproduce the project environment. Do not commit the `.venv` directory.

### 7. Run Streamlit
uv run streamlit run app.py

