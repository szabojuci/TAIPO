<?php
namespace App\Service;

use PDO;
use App\Config;
use App\Service\ProjectAccessTrait;

class CommentService
{
    use ProjectAccessTrait;

    public function __construct(PDO $pdo)
    {
        $this->pdo = $pdo;
    }

    public function addComment(int $taskId, int $userId, string $content, bool $isInstructor = false): array
    {
        // Check authorization
        $prefix = Config::getTablePrefix();
        $stmt = $this->pdo->prepare("SELECT project_name FROM {$prefix}tasks WHERE id = :task_id");
        $stmt->execute([':task_id' => $taskId]);
        $projectName = $stmt->fetchColumn();

        if (!$projectName || !$this->isAuthorized($projectName, $userId, $isInstructor)) {
            throw new \Exception("Unauthorized or task not found");
        }

        $stmt = $this->pdo->prepare("INSERT INTO {$prefix}task_comments (task_id, user_id, content) VALUES (:task_id, :user_id, :content)");
        $stmt->execute([
            ':task_id' => $taskId,
            ':user_id' => $userId,
            ':content' => $content
        ]);
        
        $commentId = $this->pdo->lastInsertId();
        
        // Fetch it back
        return $this->getComment($commentId);
    }

    public function getComments(int $taskId, int $userId, bool $isInstructor = false): array
    {
        $prefix = Config::getTablePrefix();
        $stmt = $this->pdo->prepare("SELECT project_name FROM {$prefix}tasks WHERE id = :task_id");
        $stmt->execute([':task_id' => $taskId]);
        $projectName = $stmt->fetchColumn();

        if (!$projectName || !$this->isAuthorized($projectName, $userId, $isInstructor)) {
            throw new \Exception("Unauthorized or task not found");
        }

        $stmt = $this->pdo->prepare("SELECT c.id, c.content, c.created_at, c.user_id, u.username FROM {$prefix}task_comments c JOIN {$prefix}users u ON c.user_id = u.id WHERE c.task_id = :task_id ORDER BY c.created_at ASC");
        $stmt->execute([':task_id' => $taskId]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    private function getComment(int $id): array
    {
        $prefix = Config::getTablePrefix();
        $stmt = $this->pdo->prepare("SELECT c.id, c.content, c.created_at, c.user_id, u.username FROM {$prefix}task_comments c JOIN {$prefix}users u ON c.user_id = u.id WHERE c.id = :id");
        $stmt->execute([':id' => $id]);
        return $stmt->fetch(PDO::FETCH_ASSOC);
    }
}
