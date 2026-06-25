<?php
$file = 'C:/wamp64/www/AIKanbanLatest/AIKanban/app.py';
if (!file_exists($file)) {
    die("app.py not found.");
}

$content = file_get_contents($file);

// 1. Exact replacements based on what we see in the screenshot
$replacements = [
    'Ă˘â‚¬â€ś' => '-',
    'Ă˘â€ťâ‚¬' => '-',
    '€ťâ‚¬' => '-',
    'Ä\'ĹşĹ”â€ś' => '🎓',
    'Ä\'ĹşĹ”â€šĂ©Ĺ›' => '🎓',
    'Ă˘â€ â€™' => '->',
    'Ă˘Ĺ›ĹąÄŹÂ¸Ĺą' => '(Edit)',
    'Ă˘Ĺ›â€¦' => '[Save]',
    'Ă˘ĹĄĹš' => '[X]',
    'Ă˘Ĺ›â€ś' => '[OK]'
];
$content = str_replace(array_keys($replacements), array_values($replacements), $content);

// 2. Deep clean: Keep only ASCII (32-126), tabs/newlines (9, 10, 13), 
//    Hungarian chars, and standard emojis. Strip everything else.
$clean = '';
$length = mb_strlen($content, 'UTF-8');
for ($i = 0; $i < $length; $i++) {
    $char = mb_substr($content, $i, 1, 'UTF-8');
    $ord = mb_ord($char, 'UTF-8');
    
    if ($ord === false) { continue; }
    
    // ASCII
    if (($ord >= 32 && $ord <= 126) || in_array($ord, [9, 10, 13])) {
        $clean .= $char;
    }
    // Hungarian
    elseif (in_array($ord, [225, 233, 237, 243, 246, 337, 250, 252, 369, 193, 201, 205, 211, 214, 336, 218, 220, 368])) {
        $clean .= $char;
    }
    // Safe emojis
    elseif ($char === '🎓' || $char === '❌' || $char === '✅' || $char === '✏️' || $char === '💾' || $char === '🚨') {
        $clean .= $char;
    }
}

file_put_contents($file, $clean);
echo "Sanitized app.py in place.\n";
?>
