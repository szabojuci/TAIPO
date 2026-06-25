<?php
$file = 'C:/wamp64/www/AIKanbanLatest/AIKanban/app.py';
if (file_exists($file)) {
    $content = file_get_contents($file);
    
    // Replace the specific mojibake sequences
    $replacements = [
        'Ă˘â€ â€™' => '->',
        'Ă˘Ĺ›ĹąÄŹÂ¸Ĺą' => '(Edit)',
        'Ă˘â€ťâ‚¬' => '-',
        'Ă˘Ĺ›â€¦' => '[Save]',
        'Ă˘ĹĄĹš' => '[X]',
        'Ă˘Ĺ›â€ś' => '[OK]',
        '€ťâ‚¬' => '-',
        'Ă˘' => '' // Catch-all for remaining stray mojibake starting with Ă˘
    ];
    
    $content = str_replace(array_keys($replacements), array_values($replacements), $content);
    
    // Also remove any remaining strange characters outside standard ASCII + Hungarian
    // This regex keeps ASCII (32-126), newlines/tabs, and Hungarian letters
    // Actually, str_replace should be enough to clean the specific ones.
    
    file_put_contents($file, $content);
    echo "Fixed emojis/icons in app.py\n";
} else {
    echo "app.py not found.\n";
}
?>
