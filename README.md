# 🤖 TAIPO - The AI Product Owner (Kanban Board)

An intelligent, web-based **Agile Project Management Tool** that integrates **Generative AI** (Google Gemini) into the core of modern Agile workflows. This system not only visualizes tasks but acts as a virtual **Product Owner and Developer**, automating planning, refinement, coding, and code-review processes.

---

## 🌟 Overview

The **TAIPO (The AI Product Owner)** system is designed to simulate a complete software development lifecycle enhanced by AI. It enforces Agile discipline through **Work In Progress (WIP) limits** and takes over repetitive management and development tasks using the **Google Gemini API**.

### 🚀 Key AI Features
1. **AI Brainstorming (Project Generation)**: Automatically generates an initial project backlog based on a simple project idea.
2. **Auto-Refine Backlog**: The AI analyzes the backlog, estimates task complexity (Story Points), and assigns priorities dynamically.
3. **Generate Acceptance Criteria**: Instantly writes BDD-formatted (Given-When-Then) acceptance criteria for any draft task.
4. **Decompose Story**: Breaks down complex User Stories into smaller, actionable technical sub-tasks.
5. **Code Generation**: Acts as a developer to write functional code snippets for specific tasks.
6. **AI Review Workflow (PO Review)**: The AI acts as a strict Product Owner, generating a testing checklist. It automatically moves the task to "Done" if it passes, or fails it back to "WIP" with detailed feedback.
7. **Automated Status Reports**: Analyzes the entire Kanban board and generates a professional markdown report highlighting progress and bottlenecks.

---

## 🚀 How to Set Up (Step-by-Step)

### 1. Prepare Environment
* **Web Server:** On Windows, install [WAMP](https://www.wampserver.com/).
* **Project Files:** Place the project folder into your server's public directory (e.g., `C:\wamp64\www\TAIPO`).
* **Frontend:** The frontend is built with Vue 3. Run `npm install` and `npm run dev` in the `frontend` folder.

### 2. Obtain API Keys
* **Google Gemini API:** Visit [Google AI Studio](https://aistudio.google.com/) and click **"Get API Key"**.
* **GitHub PAT:** Go to your GitHub **Settings** > **Developer Settings** > **Personal Access Tokens**. Generate a new token with the `repo` scope to enable auto-committing.

### 3. Configuration
Copy the `.env.example` file to `.env` inside the `backend` directory.
```env
GEMINI_API_KEY="your_google_gemini_api_key_here"
GITHUB_USERNAME="your_github_username"
GITHUB_REPO="your_github_repository_name"
GITHUB_TOKEN="your_github_personal_access_token"
```

---

## 🎮 How to Use the App

### 🗂 Managing the Workflow
The board is divided into strict Agile stages: **SPRINT BACKLOG**, **IMPLEMENTATION (WIP: 3)**, **TESTING (WIP: 2)**, **REVIEW (WIP: 2)**, and **DONE**. Columns have strict WIP limits to prevent bottlenecks.

### 🪄 The AI Product Owner in Action
Click the **(...)** menu on any task card to access AI capabilities:
- **📝 Generate Acceptance Criteria**: Add professional criteria to your task.
- **✂️ Decompose**: Split the task into smaller sub-tasks.
- **💻 Generate Code**: Let the AI write the implementation.
- **🤖 Ask AI to Review**: Only available in the REVIEW column. The AI validates the code and decides if the task is DONE or if it needs to go back to IMPLEMENTATION.

### 📊 Project Management
- **🪄 Auto-Refine**: In the Sprint Backlog column, click this button to let the AI estimate story points and priorities for all tasks.
- **📊 Report**: In the top navigation bar, click Report to get an executive summary of the current project state.

### 🔗 Committing to GitHub
In the code preview window, click the **GitHub icon** to automatically push the AI-generated or manually written code directly to your connected GitHub repository.

---

## 🛠 Troubleshooting

* **Database Errors:** The app uses SQLite (`kanban.sqlite`). Ensure the backend folder has write permissions.
* **GitHub 403 Forbidden:** Ensure your PAT has `repo` scope and is correctly configured in `.env`.

---

## 📝 Academic Background

This project serves as a practical experiment and demonstration for the integration of Large Language Models into Agile methodologies, simulating the Product Owner role.

* **Author:** Judit Szabó *(Software Engineering Student)*  
* **Contributor:** Mihály Nyilas *(Software Engineering Student)*  
* **Supervisor:** Dr. Gábor Kusper  
* **Institution:** Eszterházy Károly Catholic University  
