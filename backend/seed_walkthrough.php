<?php
require_once __DIR__ . '/vendor/autoload.php';

// Load .env
if (file_exists(__DIR__ . '/.env')) {
    $dotenv = \Dotenv\Dotenv::createImmutable(__DIR__);
    $dotenv->safeLoad();
}

$db = new App\Database();
$pdo = $db->getPdo();
$prefix = App\Config::getTablePrefix();

$projectName = "Mini-Neptun TAIPO Walkthrough";

try {
    $pdo->beginTransaction();

    // 1. Delete project and associated tasks if they exist (clean slate)
    $stmt = $pdo->prepare("DELETE FROM {$prefix}tasks WHERE project_name = :name");
    $stmt->execute([':name' => $projectName]);

    $stmt = $pdo->prepare("DELETE FROM {$prefix}projects WHERE name = :name");
    $stmt->execute([':name' => $projectName]);

    // 2. Create the project
    $stmt = $pdo->prepare("INSERT INTO {$prefix}projects (name, user_id, is_archived) VALUES (:name, 1, 0)");
    $stmt->execute([':name' => $projectName]);
    
    echo "Project created successfully!\n";

    // 3. Define the tasks
    $tasks = [
        [
            'title' => 'MN-01: Project skeleton and Streamlit setup',
            'status' => 'DONE',
            'is_important' => 1,
            'description' => "User story:\nAs a Developer, I want to set up the basic Streamlit application skeleton, so that we have a running layout for different roles.\n\nContext:\nMini-Neptun, Streamlit, single app.py.\n\nAcceptance criteria:\n- Streamlit application runs without errors via `streamlit run app.py`.\n- Basic layout with a sidebar for login and navigation is visible.\n- Title shows \"Mini-Neptun Academic Management System\".\n\nImplementation notes:\n- Set up `app.py` with standard page configuration and sidebar layout.\n- Defined placeholder views for Admin, Teacher, and Student roles.\n\nTests:\n- Run app locally and verify page loads.\n- Verify layout responsiveness.\n\nDecision log:\n- TAIPO suggestions accepted: Single-file structure using function-based routing.\n- TAIPO suggestions rejected: Multiple pages via `pages/` directory (rejected to maintain single-file architecture).\n- Reason: Single-file layout is simpler for persistence checking.\n- Linked commit: 5c8f2a1",
            'po_comments' => "TAIPO: Verified skeleton. The UI structure is clean and correctly implements the side menu role selections."
        ],
        [
            'title' => 'MN-02: JSON persistence and seed data',
            'status' => 'DONE',
            'is_important' => 1,
            'description' => "User story:\nAs a System Administrator, I want the system to persist data in data.json and load seed data on startup, so that the application is pre-populated with users and courses.\n\nContext:\nMini-Neptun, data.json persistence.\n\nAcceptance criteria:\n- If `data.json` does not exist, a default file is created with seed data (1 Admin, 2 Teachers, 3 Students, 3 Courses).\n- `save_data()` saves the current state of users, courses, and grades after any modification.\n- `load_data()` loads data correctly on startup.\n\nImplementation notes:\n- Implemented `load_data()` and `save_data()` helper functions in `app.py`.\n- Created initial seed data containing default logins: Admin (`admin` / `a`), Teacher (`T01` / `t`), Student (`S01` / `s`).\n\nTests:\n- Check if `data.json` is created when running the app for the first time.\n- Modify a user, restart the app, and verify the modification persists.\n\nDecision log:\n- TAIPO suggestions accepted: Automated schema generation if the file is missing.\n- TAIPO suggestions rejected: Thread-safe locking on json file write.\n- Reason: Overkill for a simple local Streamlit walkthrough.\n- Linked commit: b7d9e1c",
            'po_comments' => "TAIPO: Persistence is robust. Tested file creation and structure on start."
        ],
        [
            'title' => 'MN-03: Authentication and role-based routing',
            'status' => 'DONE',
            'is_important' => 1,
            'description' => "User story:\nAs a User, I want to log in with my username/Neptun code and password, so that I see the features corresponding to my role.\n\nContext:\nRoles: Administrator, Teacher, Student.\n\nAcceptance criteria:\n- Login form accepts credentials and validates them against `data.json`.\n- Users are redirected to the view matching their role: Admin panel, Teacher panel, or Student portal.\n- Invalid credentials show a clear error message.\n\nImplementation notes:\n- Added session state tracking for `logged_in_user` and `user_role`.\n- Logout button resets the session state.\n\nTests:\n- Log in as `admin` (password: `a`) and verify Admin view is rendered.\n- Log in with invalid password and verify \"Invalid credentials\" error.\n\nDecision log:\n- TAIPO suggestions accepted: Use `st.session_state` to guard views from unauthorized access.\n- TAIPO suggestions rejected: JWT-based session tracking.\n- Reason: Native Streamlit session state is secure enough for local use.\n- Linked commit: f3a8e90",
            'po_comments' => "TAIPO: Authenticating correctly. Access limits prevent roles from reaching pages outside their scope."
        ],
        [
            'title' => 'MN-04: Admin user management',
            'status' => 'REVIEW WIP:2',
            'is_important' => 1,
            'description' => "User story:\nAs an Administrator, I want to create, update, and delete users, so that I can manage system members.\n\nContext:\nNeptun code auto-generation, role assignment.\n\nAcceptance criteria:\n- Admin can create Users (Admin, Teacher, Student) with unique Neptun codes.\n- Admin cannot delete themselves or the last administrator.\n- Password and username validation rules are enforced (Username >= 6 chars, Password >= 8 chars).\n\nImplementation notes:\n- Form controls in Admin dashboard for creating new records.\n- Logic to prevent self-deletion: checking `st.session_state.logged_in_user['id']`.\n\nTests:\n- Create a student user and log in as them.\n- Try to delete the active admin and check that it's blocked.\n\nDecision log:\n- TAIPO suggestions accepted: Enforcing a validation checks step to prevent deleting the last admin.\n- TAIPO suggestions rejected: Password strength complexity checks.\n- Reason: Not requested in product brief.",
            'po_comments' => "TAIPO: Self-deletion safety check works. User creation validations are functioning."
        ],
        [
            'title' => 'MN-05: Admin course management',
            'status' => 'REVIEW WIP:2',
            'is_important' => 1,
            'description' => "User story:\nAs an Administrator, I want to create courses and assign teachers to them, so that students can enroll in active classes.\n\nContext:\nCourse parameters: code, name, capacity, assigned teacher.\n\nAcceptance criteria:\n- Admin can add new courses with code, name, capacity, and a dropdown select for the teacher.\n- Capacity must be a positive integer.\n- UI shows a summary chart of course capacities (capacity diagram).\n\nImplementation notes:\n- Implemented course creation form.\n- Added capacity validation.\n- Used Streamlit's `st.bar_chart` to render capacity diagrams.\n\nTests:\n- Add a course with capacity -5 and verify error.\n- Verify bar chart displays correct values.\n\nDecision log:\n- TAIPO suggestions accepted: Use `st.bar_chart` for visual overview of course capacity.\n- TAIPO suggestions rejected: Auto-assigning courses based on teacher workload.\n- Reason: Too complex for current scope.",
            'po_comments' => "TAIPO: Visual graphs for capacity are set up. Re-rendering runs dynamically."
        ],
        [
            'title' => 'MN-06: Teacher course roster and grade entry',
            'status' => 'TESTING WIP:2',
            'is_important' => 1,
            'description' => "User story:\nAs a Teacher, I want to view the list of students in my courses and enter grades for them, so that they receive marks.\n\nContext:\nGrade modifications, teacher-course ownership check.\n\nAcceptance criteria:\n- Teachers can only view courses where they are assigned as the instructor.\n- Grades must be between 1 and 5.\n- Saving grades updates `data.json` immediately.\n\nImplementation notes:\n- Filter courses array by `course['teacher_id'] == current_user['neptun']`.\n- Added inline form inputs to submit/update grades.\n\nTests:\n- Log in as Teacher T01 and verify courses of T02 are hidden.\n- Enter grade 6 and verify it's blocked.",
            'po_comments' => "TAIPO: Roster is functional. Please verify how float values are rounded when computing GPAs."
        ],
        [
            'title' => 'MN-07: Student course enrollment and drop',
            'status' => 'IMPLEMENTATION WIP:3',
            'is_important' => 1,
            'description' => "User story:\nAs a Student, I want to view available courses, enroll in them, or drop them, so that I can configure my semester schedule.\n\nContext:\nWIP Implementation.\n\nAcceptance criteria:\n- Student can enroll in courses with vacant capacity.\n- Cannot enroll in the same course twice.\n- Cannot enroll in a course if capacity is full.\n\nImplementation notes:\n- Checking `len(course['enrolled_students']) < course['capacity']` before allowing enrollment.",
            'po_comments' => "TAIPO: Enrollment logic in progress. Working on the 'drop' mechanics."
        ],
        [
            'title' => 'MN-08: Transcript and GPA calculation',
            'status' => 'IMPLEMENTATION WIP:3',
            'is_important' => 1,
            'description' => "User story:\nAs a Student, I want to view my grade transcript and GPA, so that I can monitor my academic progress.\n\nContext:\nGPA formula = average of all grades.\n\nAcceptance criteria:\n- Displays list of enrolled courses with corresponding grades.\n- If no grade is entered, display \"No Grade\".\n- Correctly calculates GPA ignoring courses without grades.\n\nDecision log:\n- TAIPO suggestions accepted: Weighting is ignored (simple average).\n- TAIPO suggestions rejected: ECTS-based weighted average (no credits provided).",
            'po_comments' => "TAIPO: GPA formula defined. Integrating math operations into the view."
        ],
        [
            'title' => 'MN-09: Role-based access-control tests',
            'status' => 'SPRINT BACKLOG',
            'is_important' => 1,
            'description' => "User story:\nAs a QA Engineer, I want to test role-based access restrictions, so that no user can bypass security checks.\n\nAcceptance criteria:\n- Students cannot call Admin/Teacher backend handlers.\n- Unauthenticated users are strictly locked out of dashboard components.",
            'po_comments' => "TAIPO: Backlog item. Security checks will be validated in Sprint 3."
        ],
        [
            'title' => 'MN-10: UI consistency and theme responsiveness',
            'status' => 'SPRINT BACKLOG',
            'is_important' => 0,
            'description' => "User story:\nAs a User, I want a clean, responsive theme, so that I can use the tool on desktop and mobile.",
            'po_comments' => null
        ],
        [
            'title' => 'MN-11: User guide and run instructions',
            'status' => 'SPRINT BACKLOG',
            'is_important' => 0,
            'description' => "User story:\nAs a Developer, I want to write clear run instructions in README.md, so that the instructor can launch and evaluate the code.",
            'po_comments' => null
        ],
        [
            'title' => 'MN-12: CR-01: Course capacity indicators',
            'status' => 'SPRINT BACKLOG',
            'is_important' => 1,
            'description' => "User story:\nAs a Student, I want to see a \"Full\" badge next to courses that have reached maximum capacity, so that I know they are unavailable.\n\nContext:\nChange request requested by Product Owner.\n\nAcceptance criteria:\n- If course capacity is reached, show a red badge `[FULL]` in the UI.\n- Prevent clicking the register button.\n\nDecision log:\n- TAIPO suggestions accepted: Badge will render next to enrollment button.\n- TAIPO suggestions rejected: Sending email notifications on slot availability.",
            'po_comments' => "TAIPO: Added this change request to the backlog as per Sprint 4 goals."
        ]
    ];

    $stmtInsert = $pdo->prepare("
        INSERT INTO {$prefix}tasks 
        (project_name, title, description, status, is_important, po_comments) 
        VALUES 
        (:project_name, :title, :description, :status, :is_important, :po_comments)
    ");

    foreach ($tasks as $t) {
        $stmtInsert->execute([
            ':project_name' => $projectName,
            ':title' => $t['title'],
            ':description' => $t['description'],
            ':status' => $t['status'],
            ':is_important' => $t['is_important'],
            ':po_comments' => $t['po_comments']
        ]);
    }

    $pdo->commit();
    echo "Successfully seeded all 12 cards for the Mini-Neptun walkthrough!\n";
} catch (Exception $e) {
    if ($pdo->inTransaction()) {
        $pdo->rollBack();
    }
    echo "Error seeding: " . $e->getMessage() . "\n";
}
