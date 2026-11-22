<?php
/**
 * One-off Elementor to blocks converter for NCAH posts. Run on switch-over day from
 * Tools > NCAH migrate (admin only). Dry run first; the real run keeps a backup of the
 * old content in post meta _ncah_pre_migrate_content so it can be undone.
 * Posts are uniform: image widget (featured photo) + gallery widget (lightbox photos).
 */
if (!defined('ABSPATH')) exit;

function ncah_migrate_walk($els, &$out) {
    foreach ((array) $els as $el) {
        if (($el['elType'] ?? '') === 'widget') $out[] = $el;
        if (!empty($el['elements'])) ncah_migrate_walk($el['elements'], $out);
    }
}

function ncah_migrate_blocks($post_id) {
    $raw = get_post_meta($post_id, '_elementor_data', true);
    $data = is_string($raw) ? json_decode($raw, true) : $raw;
    if (!is_array($data)) return null;
    $widgets = [];
    ncah_migrate_walk($data, $widgets);
    $blocks = [];
    $seen = [];
    foreach ($widgets as $w) {
        $s = $w['settings'] ?? [];
        switch ($w['widgetType'] ?? '') {
            case 'image':
                if (!empty($s['image']['url'])) {
                    $u = esc_url($s['image']['url']); $seen[$u] = 1;
                    $id = !empty($s['image']['id']) ? (int) $s['image']['id'] : 0;
                    $a = $id ? '{"id":' . $id . ',"sizeSlug":"large","linkDestination":"none"}' : '{"sizeSlug":"large","linkDestination":"none"}';
                    $blocks[] = "<!-- wp:image $a -->\n<figure class=\"wp-block-image size-large\"><img src=\"$u\" alt=\"\"" . ($id ? " class=\"wp-image-$id\"" : '') . "/></figure>\n<!-- /wp:image -->";
                }
                break;
            case 'gallery':
                $imgs = '';
                foreach ((array) ($s['gallery'] ?? []) as $g) {
                    if (empty($g['url'])) continue;
                    $u = esc_url($g['url']); $id = !empty($g['id']) ? (int) $g['id'] : 0;
                    $a = $id ? '{"id":' . $id . ',"sizeSlug":"large","linkDestination":"media"}' : '{"sizeSlug":"large","linkDestination":"media"}';
                    $imgs .= "<!-- wp:image $a -->\n<figure class=\"wp-block-image size-large\"><a href=\"$u\"><img src=\"$u\" alt=\"\"" . ($id ? " class=\"wp-image-$id\"" : '') . "/></a></figure>\n<!-- /wp:image -->\n\n";
                }
                if ($imgs) $blocks[] = "<!-- wp:gallery {\"columns\":3,\"linkTo\":\"media\",\"className\":\"ncah-gallery\"} -->\n<figure class=\"wp-block-gallery has-nested-images columns-3 is-cropped ncah-gallery\">\n" . trim($imgs) . "\n</figure>\n<!-- /wp:gallery -->";
                break;
            case 'text-editor':
                if (!empty($s['editor'])) $blocks[] = "<!-- wp:html -->\n" . wp_kses_post($s['editor']) . "\n<!-- /wp:html -->";
                break;
            case 'video':
                if (!empty($s['youtube_url'])) $blocks[] = '<!-- wp:embed {"url":"' . esc_url($s['youtube_url']) . '","providerNameSlug":"youtube"} -->' . "\n" . '<figure class="wp-block-embed is-provider-youtube wp-block-embed-youtube"><div class="wp-block-embed__wrapper">' . esc_url($s['youtube_url']) . "</div></figure>\n<!-- /wp:embed -->";
                break;
        }
    }
    return $blocks ? implode("\n\n", $blocks) : null;
}

add_action('admin_menu', function () {
    add_management_page('NCAH migrate', 'NCAH migrate', 'manage_options', 'ncah-migrate', 'ncah_migrate_page');
});

function ncah_migrate_page() {
    if (!current_user_can('manage_options')) return;
    $run = isset($_POST['ncah_run']) && check_admin_referer('ncah_migrate');
    $undo = isset($_POST['ncah_undo']) && check_admin_referer('ncah_migrate');
    $apply = $run && ($_POST['ncah_run'] === 'apply');
    echo '<div class="wrap"><h1>NCAH migrate</h1><form method="post">';
    wp_nonce_field('ncah_migrate');
    echo '<p><button class="button" name="ncah_run" value="dry">Dry run</button> <button class="button button-primary" name="ncah_run" value="apply">Convert posts</button> <button class="button" name="ncah_undo" value="1">Undo last conversion</button> <button class="button" name="ncah_seed" value="1">Create starter programs</button></p><p><label>MailPoet form ID for the footer signup: <input type="number" name="ncah_mp" value="'.(int) get_option("ncah_mailpoet_form_id").'" style="width:6em"></label> <button class="button" name="ncah_mpsave" value="1">Save</button></p></form>';
    if (isset($_POST["ncah_mpsave"]) && check_admin_referer("ncah_migrate")) { update_option("ncah_mailpoet_form_id", (int) ($_POST["ncah_mp"] ?? 0)); echo "<p><strong>Saved.</strong></p>"; }
    if (isset($_POST["ncah_seed"]) && check_admin_referer("ncah_migrate")) echo "<p><strong>Created " . (int) ncah_seed_programs() . " programs.</strong></p>";
    $ids = get_posts(['post_type' => 'post', 'post_status' => 'any', 'numberposts' => -1, 'fields' => 'ids']);
    if ($run || $undo) {
        echo '<table class="widefat"><tr><th>ID</th><th>Title</th><th>Result</th></tr>';
        foreach ($ids as $id) {
            $t = esc_html(get_the_title($id)); $res = '';
            if ($undo) {
                $old = get_post_meta($id, '_ncah_pre_migrate_content', true);
                if ($old !== '') {
                    wp_update_post(['ID' => $id, 'post_content' => wp_slash($old)]);
                    delete_post_meta($id, '_ncah_pre_migrate_content');
                    $m = get_post_meta($id, '_ncah_pre_migrate_meta', true);
                    if (is_array($m)) {
                        if (isset($m['template']) && $m['template'] !== '') update_post_meta($id, '_wp_page_template', $m['template']); else delete_post_meta($id, '_wp_page_template');
                        if (isset($m['mode']) && $m['mode'] !== '') update_post_meta($id, '_elementor_edit_mode', $m['mode']);
                        delete_post_meta($id, '_ncah_pre_migrate_meta');
                    }
                    $res = 'restored';
                } else $res = 'nothing to undo';
            } else {
                $b = ncah_migrate_blocks($id);
                if (!$b) $res = 'skipped (no Elementor data)';
                elseif (!$apply) $res = 'would convert (' . substr_count($b, '<!-- wp:image') . ' images)';
                else {
                    update_post_meta($id, '_ncah_pre_migrate_content', get_post_field('post_content', $id));
                    // Stop Elementor rendering the post (its Full Width template and builder flag), keep _elementor_data for undo.
                    update_post_meta($id, '_ncah_pre_migrate_meta', ['template' => get_post_meta($id, '_wp_page_template', true), 'mode' => get_post_meta($id, '_elementor_edit_mode', true)]);
                    delete_post_meta($id, '_wp_page_template');
                    delete_post_meta($id, '_elementor_edit_mode');
                    wp_update_post(['ID' => $id, 'post_content' => wp_slash($b)]);
                    $res = 'converted';
                }
            }
            echo "<tr><td>$id</td><td>$t</td><td>$res</td></tr>";
        }
        echo '</table>';
    }
    echo '</div>';
}
