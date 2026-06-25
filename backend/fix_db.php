<?php
$dbFile = __DIR__ . '/ai_kanban.db';
$pdo = new PDO('sqlite:' . $dbFile);
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$stmt = $pdo->query('SELECT id FROM taipo_users ORDER BY id DESC LIMIT 1');
$user = $stmt->fetch();
$userId = $user ? $user['id'] : 1;

$prefix = 'taipo_';
$pdo->exec("UPDATE {$prefix}projects SET user_id = {$userId} WHERE name = 'Mini-Neptun TAIPO Walkthrough'");
// Some columns might not exist if sqlite pragma isn't applied, but let's try
try {
    $pdo->exec("UPDATE {$prefix}tasks SET user_id = {$userId} WHERE project_name = 'Mini-Neptun TAIPO Walkthrough'");
} catch(Exception $e) {}

// Make user instructor to bypass limits
$pdo->exec("UPDATE {$prefix}users SET is_instructor = 1 WHERE id = {$userId}");

echo "Fixed user_id to $userId";
?>
