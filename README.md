# 🤖 TAIPO - The AI Product Owner (Kanban Board)

An intelligent, web-based **Agile Project Management Tool** that integrates **Generative AI (Google Gemini)** deeply into the core of modern Agile workflows. 

Unlike traditional Kanban boards that only track the status of tasks, **TAIPO** acts as an active participant in your team. It functions as a virtual **Product Owner**, **Agile Coach**, and **Developer**, automating planning, backlog refinement, coding, and code-review processes.

---

## 🌟 Comprehensive Overview

The **TAIPO** system is designed to simulate a complete software development lifecycle enhanced by Large Language Models (LLMs). It enforces Agile discipline through strict **Work In Progress (WIP) limits** and takes over repetitive management and development tasks.

### 🏗 Architecture
- **Backend:** PHP 8+ with lightweight custom routing (`Application.php`). Uses SQLite for zero-configuration persistent storage.
- **Frontend:** Vue.js 3 with Vite, styled with Tailwind CSS and DaisyUI components.
- **AI Integration:** Google Gemini API (`gemini-3-flash-preview` primary with `gemini-2.5-flash` fallback capability via environment variables).
- **Version Control:** Direct integration with GitHub API for seamless code committing.

---

## 🚀 Key AI & Advanced Features in Detail

The system is packed with major AI capabilities and management tools that guide a project from an idea to production-ready code:

### 1. 🧠 AI Brainstorming (Project Generation)
When creating a new project, instead of manually writing tasks, you provide a simple prompt (e.g., *"An e-commerce website with a shopping cart and Stripe payment integration"*). The AI generates a complete initial project backlog, creating technical tasks with descriptive titles and inserting them directly into your Kanban board.

### 2. 🪄 Auto-Refine Backlog (Estimation & Priority)
A traditional Product Owner spends hours estimating tasks and ordering the backlog. 
- By clicking the **Auto-Refine** button in the Sprint Backlog column, the AI reads all pending tasks.
- It calculates complexity in **Story Points** (e.g., 3 SP, 5 SP) and prepends them to the task description.
- It evaluates importance and automatically applies priority flags (Low, Medium, High) to the cards.

### 3. 📝 Generate Acceptance Criteria
If a team member drops a bare-bones task into the board (e.g., "Add login page"), the AI can instantly generate detailed, BDD-formatted (**Given-When-Then**) acceptance criteria with a single click from the card's menu.

### 4. ✂️ Decompose Story
Large User Stories can bottleneck a Sprint. If a task is too complex, the **Decompose** action allows the AI to break it down into 3-5 smaller, actionable technical sub-tasks, replacing the original epic.

### 5. 💻 Code Generation (Developer Role)
TAIPO doesn't just manage tasks; it executes them. 
- By selecting **Generate Code**, the AI writes functional code (e.g., Java, PHP, Python) based on the task's title, description, and acceptance criteria.
- The generated code is displayed in a built-in code editor modal for human review.

### 6. 🤖 AI Review Workflow (PO QA & Validation)
Before a task is considered "Done", it must be verified. 
- When a task is moved to the **REVIEW (WIP: 2)** column, the user can trigger an **AI Review**.
- The AI analyzes the task and generates a strict testing checklist.
- If the criteria are met, it passes the task and automatically moves it to **DONE**.
- If it fails, the AI moves the card back to the **IMPLEMENTATION** column and appends detailed failure reasons to the description.

### 7. 📊 Automated Status Reports & Cost Tracking
- **Executive Summaries:** By clicking the **Report** button, the AI analyzes the entire Kanban board (reading all columns, tasks, and bottlenecks) and generates a professional summary in Markdown format for stakeholders.
- **Token & Cost Metrics:** Built-in API tracking monitors token consumption (input/output) and estimates actual API usage costs, ensuring transparency in LLM operations.

---

## 🗂 Managing the Workflow & WIP Limits

The board is divided into strict Agile stages to optimize flow and prevent multitasking:

1. **SPRINT BACKLOG (No Limit)** - Unstarted tasks waiting to be pulled.
2. **IMPLEMENTATION (WIP: 3)** - Active development. The system physically prevents moving more than 3 tasks here.
3. **TESTING (WIP: 2)** - Manual or automated QA.
4. **REVIEW (WIP: 2)** - Code review and Product Owner validation.
5. **DONE (No Limit)** - Completed and committed work.

---

## 🚀 Installation & Setup

### 1. Environment Preparation
* **Web Server:** Install a local server environment (e.g., [WAMP](https://www.wampserver.com/) for Windows, XAMPP, or Laravel Valet).
* **Project Directory:** Clone this repository into your server's public document root (e.g., `C:\wamp64\www\TAIPO`).
* **Frontend Setup:** Open a terminal in the `frontend` folder. Since the project utilizes `pnpm`, run:
  ```bash
  pnpm install
  pnpm dev
  ```
  *(This starts the Vite development server).*

### 2. Obtain API Keys
* **Google Gemini API:** Visit [Google AI Studio](https://aistudio.google.com/) to generate an API key.
* **GitHub PAT:** Go to GitHub **Settings** > **Developer Settings** > **Personal Access Tokens**. Generate a token with the `repo` scope to enable the app's auto-commit feature.

### 3. Backend Configuration
Copy the `.env.example` file to `.env` inside the `backend` directory and populate your credentials:

```env
JWT_SECRET="your_secure_jwt_secret_here"
GEMINI_API_KEY="your_google_gemini_api_key_here"
GEMINI_BASE_MODEL="gemini-3-flash-preview"
GEMINI_FALLBACK_MODEL="gemini-2.5-flash"
GITHUB_USERNAME="your_github_username"
GITHUB_REPO="your_github_repository_name"
GITHUB_TOKEN="your_github_personal_access_token"
```

The app will automatically create the `ai_kanban.db` SQLite database file on its first run. Ensure the backend folder has write permissions.

---

## 🔗 Committing Directly to GitHub

TAIPO eliminates context switching. When you generate code via the AI, you can click the **GitHub icon** in the code editor window. The application uses the GitHub REST API to automatically commit and push the new file directly to the repository specified in your `.env` file, and instantly moves the Kanban card to **DONE**.

---

## 📝 Academic Background

This software project was developed as a practical experiment for a Scientific Students' Associations (TDK) paper and the Óbuda University Mini Symposium. It investigates the feasibility and efficiency of integrating Large Language Models into Agile project management methodologies, specifically focusing on simulating the roles of a Product Owner and Agile Coach.

* **Author:** Judit Szabó *(Software Engineering Student)*
* **Contributor:** Mihály Nyilas *(Software Engineering Student)*
* **Supervisor:** Dr. Gábor Kusper  
* **Institution:** Eszterházy Károly Catholic University
