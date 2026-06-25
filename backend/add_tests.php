<?php
$dbFile = __DIR__ . '/ai_kanban.db';
$pdo = new PDO('sqlite:' . $dbFile);
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$prefix = 'taipo_';

$desc = "User story: As a Teacher, I want to enter grades for my courses.

Acceptance criteria:
- Teacher only sees assigned courses.
- Teacher can enter valid grades (1-5).
- Changes are saved immediately.

**TAIPO-generated Test Checklist:**
- [ ] Positive: Teacher logs in, sees only their assigned course in the roster.
- [ ] Positive: Teacher enters a grade '5', saves, reloads page, grade persists.
- [ ] Negative (Role): Student attempts to access the grade entry route. Should be blocked.
- [ ] Negative (Boundary): Teacher attempts to enter grade '6' or 'A'. Should show validation error.
- [ ] Negative (Access): Teacher attempts to modify grades for a course assigned to another teacher.
";

$stmt = $pdo->prepare("UPDATE {$prefix}tasks SET description = :desc WHERE title = 'MN-06 Teacher course roster and grade entry'");
$stmt->execute([':desc' => $desc]);
echo "Updated MN-06 with test checklist";
?>
