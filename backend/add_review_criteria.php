<?php
$dbFile = __DIR__ . '/ai_kanban.db';
$pdo = new PDO('sqlite:' . $dbFile);
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$prefix = 'taipo_';

$desc = "User story: As an Admin, I want to manage courses.

**TAIPO Review:**
Acceptance criteria:
- [PASS] Create and edit courses works correctly.
- [FAIL] Delete courses (Bug: Enrolled students still have ghost grades after course deletion).
- [PASS] Assign teacher to course successfully updates the database.

Decision log:
- Status: Returned to Implementation.
- Reason: The deletion cascade is missing. Needs a confirmation dialog and data cleanup.
";

$stmt = $pdo->prepare("UPDATE {$prefix}tasks SET description = :desc WHERE title = 'MN-05 Admin course management'");
$stmt->execute([':desc' => $desc]);
echo "Updated MN-05 with PASS/FAIL criteria";
?>
