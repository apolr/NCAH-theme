<?php
/** Programs: a "Program" content type grouped by Directorate, with a Status field. */
if (!defined('ABSPATH')) exit;
add_action('init', function () {
    register_post_type('program', [
        'labels' => ['name' => 'Programs', 'singular_name' => 'Program', 'add_new_item' => 'Add program'],
        'public' => true, 'show_in_rest' => true, 'has_archive' => false, 'menu_icon' => 'dashicons-groups',
        'rewrite' => ['slug' => 'programs'], 'supports' => ['title', 'editor', 'excerpt', 'thumbnail', 'custom-fields'],
    ]);
    register_taxonomy('directorate', 'program', [
        'labels' => ['name' => 'Directorates', 'singular_name' => 'Directorate'],
        'public' => true, 'hierarchical' => true, 'show_in_rest' => true, 'rewrite' => ['slug' => 'directorate'],
    ]);
    register_post_meta('program', 'ncah_status', [
        'type' => 'string', 'single' => true, 'show_in_rest' => true, 'default' => 'running',
        'sanitize_callback' => function ($v) { return in_array($v, ['running', 'proposed', 'past'], true) ? $v : 'running'; },
    ]);
});
