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

echo "=== TABLES ===\n";
$tables = $pdo->query("SELECT name FROM sqlite_master WHERE type='table'")->fetchAll(PDO::FETCH_COLUMN);
print_r($tables);

echo "=== USERS ===\n";
$users = $pdo->query("SELECT * FROM {$prefix}users")->fetchAll(PDO::FETCH_ASSOC);
print_r($users);

echo "=== PROJECTS ===\n";
$projects = $pdo->query("SELECT * FROM {$prefix}projects")->fetchAll(PDO::FETCH_ASSOC);
print_r($projects);
