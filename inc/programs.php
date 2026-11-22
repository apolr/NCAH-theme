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

/** Status badge: [ncah_status] prints Running / Proposed / Past for the current program. */
add_shortcode('ncah_status', function () {
    $v = get_post_meta(get_the_ID(), 'ncah_status', true) ?: 'running';
    $l = ['running' => 'Running', 'proposed' => 'Proposed', 'past' => 'Past'][$v] ?? 'Running';
    return '<span class="ncah-status' . ($v === 'proposed' ? ' ncah-status--proposed' : '') . '">' . esc_html($l) . '</span>';
});

/** Limit a Programs query block to one directorate: give the block the class ncah-dir-{slug}.
 *  The context filter runs for the query block's children, with the query block as parent. */
add_filter('render_block_context', function ($context, $parsed_block, $parent_block) {
    if ($parent_block && ($parent_block->name ?? '') === 'core/query') {
        $cls = $parent_block->attributes['className'] ?? '';
        if (preg_match('/ncah-dir-([a-z0-9-]+)/', $cls, $m) && isset($context['query'])) {
            $term = get_term_by('slug', $m[1], 'directorate');
            $context['query']['taxQuery'] = ['directorate' => [$term ? (int) $term->term_id : 0]];
        }
    }
    return $context;
}, 10, 3);

/** Starter programs, created from Tools > NCAH migrate. Proposed and unapproved items stay drafts. */
function ncah_seed_programs() {
    $set = [
        'youth-sports' => ['Youth and Sports Directorate', [
            ['Golden Eagles of Hamilton', 'running', 'publish', 'Our community soccer team, part of our youth development work through culturally relevant physical activity and mentorship. Visit soccer.ncahamilton.ca for news, fixtures and the squad.'],
            ['Jakada Youth Ambassador Programme', 'proposed', 'draft', '[Confirm description and launch date.]'],
            ['Tennis Club', 'proposed', 'draft', 'Proposed for 2027. [Confirm description.]'],
            ['Family Walk and Run', 'proposed', 'draft', 'Proposed for 2027. [Confirm description.]'],
            ['Indoor Activities for Adults and Seniors', 'proposed', 'draft', 'Proposed for 2027. [Confirm description.]'],
            ['Kulture Shock', 'proposed', 'draft', 'Draft until Board approval. [Confirm description.]'],
            ['BLK XLence (Black Excellence)', 'proposed', 'draft', 'Draft until Board approval. [Confirm description.]'],
        ]],
        'social' => ['Social Directorate', [
            ['Family Fun Festival', 'running', 'publish', 'A community celebration that promotes multicultural awareness and community integration.'],
            ['Annual Gala', 'running', 'publish', 'Our annual gala brings the community together and raises funds for our charitable programs. 2026 theme: 5v5.'],
            ['Ethnic Food Bank', 'running', 'publish', 'Food support and resource referrals for low-income individuals and families in Hamilton and surrounding areas.'],
        ]],
    ];
    $n = 0;
    foreach ($set as $slug => [$name, $items]) {
        $t = term_exists($slug, 'directorate') ?: wp_insert_term($name, 'directorate', ['slug' => $slug]);
        $tid = is_array($t) ? (int) $t['term_id'] : (int) $t;
        foreach ($items as [$title, $status, $post_status, $text]) {
            if (get_page_by_title($title, OBJECT, 'program')) continue;
            $id = wp_insert_post(['post_type' => 'program', 'post_title' => $title, 'post_status' => $post_status, 'post_excerpt' => $text, 'post_content' => $text]);
            if ($id && !is_wp_error($id)) { wp_set_object_terms($id, [$tid], 'directorate'); update_post_meta($id, 'ncah_status', $status); $n++; }
        }
    }
    return $n;
}
