<?php
$dir = 'C:/wamp64/www/AIKanbanLatest/AIKanban/';
// Let's fix .py and .md files in the root
$files = array_merge(glob($dir . '*.py'), glob($dir . '*.md'));

foreach($files as $file) {
    if (is_file($file)) {
        $content = file_get_contents($file);
        
        // Count before replacement to log if we changed anything
        $original_length = strlen($content);
        
        // Replace UTF-8 en-dash, em-dash, and smart quotes, and common mojibake strings directly
        $search = ['–', '—', '”', '“', '’', '‘', 'Ă˘â‚¬â€ś'];
        $replace = ['-', '-', '"', '"', "'", "'", '-'];
        $content = str_replace($search, $replace, $content);
        
        // Also fix the specific mojibake string if it got hardcoded
        $content = str_replace('Ă˘â‚¬â€ś', '-', $content);
        $content = str_replace('Ă˘â‚¬â€ť', '"', $content);
        $content = str_replace('Ă˘â‚¬Ĺ“', '"', $content);
        $content = str_replace('Ă˘â‚¬â„˘', "'", $content);
        $content = str_replace('Ă˘â‚¬', '-', $content); // fallback
        
        // Only write if changed
        if ($content !== file_get_contents($file)) {
            file_put_contents($file, $content);
            echo "Fixed: " . basename($file) . "\n";
        }
    }
}
echo "Done checking local files.\n";
?>
