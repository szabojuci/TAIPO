<?php
$dbFile = __DIR__ . '/ai_kanban.db';
$pdo = new PDO('sqlite:' . $dbFile);
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$prefix = 'taipo_';
$projectName = 'Mini neptun';

// Clear existing tasks for this project
$stmt = $pdo->prepare("DELETE FROM {$prefix}tasks WHERE project_name = :project_name");
$stmt->execute([':project_name' => $projectName]);

// 2. Define the tasks
$tasks = [
    [
        'title' => 'MN-01 Project skeleton and Streamlit setup',
        'description' => "User story: As a Developer, I want a running Streamlit app skeleton so that we have a foundation.\nContext: Mini-Neptun, Streamlit, single app.py.\n\nAcceptance criteria:\n- App runs without errors.\n- Basic page config is set.\n- Placeholder UI for login exists.",
        'status' => 'DONE',
        'po_comments' => null
    ],
    [
        'title' => 'MN-02 JSON persistence and seed data',
        'description' => "User story: As an Admin, I want data persistence so that records survive restarts.\nContext: JSON persistence in data.json.\n\nAcceptance criteria:\n- Data is saved to data.json.\n- Seed users (admin, teacher, student) are created on first run.\n- Read/write functions exist.\n\nDecision log:\n- TAIPO suggestions accepted: Use simple dict to JSON mapping.\n- Linked commit: abc1234",
        'status' => 'DONE',
        'po_comments' => null
    ],
    [
        'title' => 'MN-03 Authentication and role-based routing',
        'description' => "User story: As a User, I want to log in so that I see my specific dashboard.\nContext: Role-based access control.\n\nAcceptance criteria:\n- Admin logs in with admin/a.\n- Incorrect login shows error.\n- Route changes based on role.",
        'status' => 'DONE',
        'po_comments' => null
    ],
    [
        'title' => 'MN-04 Admin user management',
        'description' => "User story: As an Admin, I want to manage users.\n\nAcceptance criteria:\n- Admin can create students and teachers.\n- Admin cannot delete the last admin.\n- Admin cannot delete themselves.",
        'status' => 'DONE',
        'po_comments' => null
    ],
    [
        'title' => 'MN-05 Admin course management',
        'description' => "User story: As an Admin, I want to manage courses.\n\nAcceptance criteria:\n- Create, edit, delete courses.\n- Assign teacher to course.",
        'status' => 'REVIEW WIP:2',
        'po_comments' => "**PO Feedback:** Please verify what happens to enrolled students when a course is deleted. Do their grades disappear? Add a confirmation dialog."
    ],
    [
        'title' => 'MN-06 Teacher course roster and grade entry',
        'description' => "User story: As a Teacher, I want to enter grades for my courses.\n\nAcceptance criteria:\n- Teacher only sees assigned courses.\n- Teacher can enter valid grades (1-5).\n- Changes are saved immediately.",
        'status' => 'TESTING WIP:2',
        'po_comments' => null
    ],
    [
        'title' => 'MN-07 Student course enrollment and drop',
        'description' => "User story: As a Student, I want to enroll in courses.\n\nAcceptance criteria:\n- Can see available courses.\n- Can enroll if not full.\n- Can drop enrolled courses.",
        'status' => 'IMPLEMENTATION WIP:3',
        'po_comments' => null
    ],
    [
        'title' => 'MN-08 Transcript and GPA calculation',
        'description' => "User story: As a Student, I want to see my GPA.\n\nAcceptance criteria:\n- GPA is calculated correctly.\n- Shows all finished courses.",
        'status' => 'SPRINT BACKLOG',
        'po_comments' => null
    ],
    [
        'title' => 'MN-09 Role-based access-control tests',
        'description' => "User story: As a Security Auditor, I want negative tests for roles.\n\nTests:\n- Teacher trying to edit another teacher's grades.\n- Student trying to access Admin panel.",
        'status' => 'TESTING WIP:2',
        'po_comments' => null
    ],
    [
        'title' => 'CR-01: Prevent enrollment in full courses with UI indicator',
        'description' => "**Change Request**\nUser story: As a Student, I should clearly see if a course is full and be prevented from enrolling.\n\nAcceptance criteria:\n- UI shows 'FULL' badge in red.\n- Enroll button is disabled.\n\nAffected cards: MN-07",
        'status' => 'SPRINT BACKLOG',
        'po_comments' => null
    ]
];

$stmt = $pdo->prepare("INSERT INTO {$prefix}tasks (project_name, title, description, status, position) VALUES (:project_name, :title, :description, :status, :position)");

$pos = 0;
foreach ($tasks as $task) {
    $stmt->execute([
        ':project_name' => $projectName,
        ':title' => $task['title'],
        ':description' => $task['description'],
        ':status' => $task['status'],
        ':position' => $pos++
    ]);
    
    if ($task['po_comments']) {
        $id = $pdo->lastInsertId();
        $upd = $pdo->prepare("UPDATE {$prefix}tasks SET po_comments = :comments WHERE id = :id");
        $upd->execute([':comments' => $task['po_comments'], ':id' => $id]);
    }
}

echo "Successfully replaced tasks for project: " . $projectName . "\n";
?>
