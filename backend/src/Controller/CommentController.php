<?php
namespace App\Controller;

use App\Service\CommentService;
use App\Config;
use Exception;

class CommentController
{
    private CommentService $commentService;

    public function __construct(CommentService $commentService)
    {
        $this->commentService = $commentService;
    }

    public function handleGetComments()
    {
        $taskId = filter_var($_GET['task_id'] ?? $_POST['task_id'] ?? null, FILTER_VALIDATE_INT);
        if (!$taskId) {
            http_response_code(400);
            echo json_encode(['success' => false, 'error' => 'task_id is required']);
            return;
        }

        try {
            $userId = $_SESSION['user_id'] ?? 0;
            $isInstructor = $_SESSION['is_instructor'] ?? false;
            $comments = $this->commentService->getComments($taskId, $userId, $isInstructor);
            header(Config::APP_JSON);
            echo json_encode(['success' => true, 'comments' => $comments]);
        } catch (Exception $e) {
            http_response_code(403);
            echo json_encode(['success' => false, 'error' => $e->getMessage()]);
        }
    }

    public function handleAddComment()
    {
        $taskId = filter_var($_POST['task_id'] ?? null, FILTER_VALIDATE_INT);
        $content = trim($_POST['content'] ?? '');

        if (!$taskId || empty($content)) {
            http_response_code(400);
            echo json_encode(['success' => false, 'error' => 'task_id and content are required']);
            return;
        }

        try {
            $userId = $_SESSION['user_id'] ?? 0;
            $isInstructor = $_SESSION['is_instructor'] ?? false;
            $comment = $this->commentService->addComment($taskId, $userId, $content, $isInstructor);
            header(Config::APP_JSON);
            echo json_encode(['success' => true, 'comment' => $comment]);
        } catch (Exception $e) {
            http_response_code(403);
            echo json_encode(['success' => false, 'error' => $e->getMessage()]);
        }
    }
}
