<?php
$dir = 'C:/Users/szjud/.gemini/antigravity/brain/1789015c-e5ac-4c3a-88e7-dc6d64d3f58e/';
foreach(glob($dir . '*.*') as $file) {
    if (is_file($file)) {
        $content = file_get_contents($file);
        // Replace UTF-8 en-dash, em-dash, and smart quotes with ASCII equivalents
        $content = str_replace(
            ['–', '—', '”', '“', '’', '‘'],
            ['-', '-', '"', '"', "'", "'"],
            $content
        );
        file_put_contents($file, $content);
    }
}
echo "Fixed characters in artifacts.\n";
?>
