# MUJChat

MUJbot is the official AI assistant for Manipal University Jaipur (MUJ).

## Properties
- **Frontend**: React, Vite
- **Backend**: FastAPI, Python
- **AI Model**: Gemini 2.0 Flash

## How to Run Locally

### Prerequisites
- Node.js installed
- Python 3.8+ installed
- API Key for Gemini (in `backend/.env`)

### Quick Start
1.  **Configure Environment**:
    -   Create `backend/.env` file.
    -   Add your API key: `GENAI_API_KEY=your_key_here`

2.  **Run the App**:
    ```bash
    chmod +x run_app.sh
    ./run_app.sh
    ```

3.  **Access**:
    -   Frontend: `http://localhost:5173`
    -   Backend Docs: `http://localhost:8000/docs`

## Deployment (GitHub Pages)
The frontend is deployed at: [https://ayankhancodes.github.io/MUJChat/](https://ayankhancodes.github.io/MUJChat/)

> **Note**: The deployed version interacts with `localhost:8000`. You MUST have the backend running locally for the online frontend to work, OR deploy the backend to a cloud provider.
