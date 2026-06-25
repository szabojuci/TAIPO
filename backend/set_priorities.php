<?php
$dbFile = __DIR__ . '/ai_kanban.db';
$pdo = new PDO('sqlite:' . $dbFile);
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$prefix = 'taipo_';
$projectName = 'Mini neptun';

$priorities = [
    'MN-01 Project skeleton and Streamlit setup' => 1,
    'MN-02 JSON persistence and seed data' => 2,
    'MN-03 Authentication and role-based routing' => 3,
    'MN-04 Admin user management' => 1,
    'MN-05 Admin course management' => 3,
    'MN-06 Teacher course roster and grade entry' => 2,
    'MN-07 Student course enrollment and drop' => 3,
    'MN-08 Transcript and GPA calculation' => 2,
    'MN-09 Role-based access-control tests' => 3,
    'CR-01: Prevent enrollment in full courses with UI indicator' => 3
];

$stmt = $pdo->prepare("UPDATE {$prefix}tasks SET is_important = :is_important WHERE project_name = :project_name AND title = :title");

foreach ($priorities as $title => $priority) {
    $stmt->execute([
        ':is_important' => $priority,
        ':project_name' => $projectName,
        ':title' => $title
    ]);
}

echo "Successfully updated priorities for project: " . $projectName . "\n";
?>
