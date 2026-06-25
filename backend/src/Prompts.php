<?php

namespace App;

class Prompts
{
    public static function getLanguagePrompt(string $language): string
    {
        $lang = htmlspecialchars($language);
        return "Plan a project named {{PROJECT_NAME}}! We demonstrate a simulated project: a weather forecast webpage with a zoom-in / zoom-out style map, a time slider bar, and the introduction of unforeseen requirement changes. This project should be primarily written in {$lang}. Generate at least 10 tasks for the Kanban board covering these core features, basic development steps, and UI/UX. Provide each task on a new line without any prefix (e.g. [SPRINT BACKLOG]:) so they all go into the **SPRINT BACKLOG** column. CRITICAL: Please mention '({$lang})' at the end of each task title so that developers know what language to write the code in. Do not include introductory text.";
    }
}
