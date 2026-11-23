<?php
/**
 * NCAH theme setup.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action( 'after_setup_theme', function () {
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'responsive-embeds' );
	add_theme_support( 'editor-styles' );
	add_editor_style( 'style.css' );
	add_post_type_support( 'page', 'excerpt' ); // page summary used as the search description
} );

// Motion layer: one small stylesheet and one small script, no libraries.
add_action( 'wp_enqueue_scripts', function () {
	$dir = get_template_directory();
	$uri = get_template_directory_uri();

	// Theme stylesheet: design tokens, header, team cards, galleries.
	wp_enqueue_style(
		'ncah-style',
		get_stylesheet_uri(),
		array(),
		(string) filemtime( $dir . '/style.css' )
	);
	wp_enqueue_style(
		'ncah-motion',
		$uri . '/assets/css/motion.css',
		array( 'ncah-style' ),
		(string) filemtime( $dir . '/assets/css/motion.css' )
	);
	wp_enqueue_script(
		'ncah-motion',
		$uri . '/assets/js/motion.js',
		array(),
		(string) filemtime( $dir . '/assets/js/motion.js' ),
		array( 'in_footer' => true, 'strategy' => 'defer' )
	);
	// Photo lightbox for galleries and photos in news posts.
	if ( is_singular( 'post' ) ) {
		wp_enqueue_script(
			'ncah-lightbox',
			$uri . '/assets/js/lightbox.js',
			array(),
			(string) filemtime( $dir . '/assets/js/lightbox.js' ),
			array( 'in_footer' => true, 'strategy' => 'defer' )
		);
	}
} );

// Search and sharing basics (meta description, link previews, structured data, llms.txt).
require_once get_template_directory() . '/inc/seo.php';
require_once get_template_directory() . '/inc/migrate.php';
require_once get_template_directory() . '/inc/programs.php';
require_once get_template_directory() . '/inc/subdir.php';
require_once get_template_directory() . '/inc/event-gallery.php';

/**
 * The MailPoet form prints its own <style> block. The Shortcode block runs
 * wpautop over it, which breaks that CSS with stray <p> tags. Render the
 * MailPoet shortcode cleanly instead.
 */
add_filter( 'render_block', function ( $html, $block ) {
	if ( 'core/shortcode' === ( $block['blockName'] ?? '' ) && ( false !== strpos( $block['innerHTML'] ?? '', 'mailpoet_form' ) || false !== strpos( $block['innerHTML'] ?? '', 'instagram-feed' ) ) ) {
		$code = trim( $block['innerHTML'] );
		// Instagram Feed (Smash Balloon): use the first saved feed when none is named.
		if ( false !== strpos( $code, 'instagram-feed' ) && false === strpos( $code, 'feed=' ) ) {
			global $wpdb;
			$suppress = $wpdb->suppress_errors( true );
			$feed_id  = (int) $wpdb->get_var( "SELECT id FROM {$wpdb->prefix}sbi_feeds ORDER BY id ASC LIMIT 1" );
			$wpdb->suppress_errors( $suppress );
			if ( $feed_id ) {
				$code = '[instagram-feed feed=' . $feed_id . ']';
			}
		}
		return do_shortcode( $code );
	}
	return $html;
}, 10, 2 );


/**
 * Home page: the "Updates" news section now lives in the theme (parts/updates.html),
 * after "Our mission". Hide the older copy that is still saved inside the Home page content.
 */
add_filter( 'render_block', function ( $html, $block ) {
	if ( is_front_page() && 'core/group' === ( $block['blockName'] ?? '' ) ) {
		$raw = serialize_block( $block );
		if ( false !== strpos( $raw, '>Updates<' ) && false !== strpos( $raw, 'wp:query' ) && false === strpos( $raw, 'ncah-updates' ) ) {
			return '';
		}
	}
	return $html;
}, 11, 2 );


/** Instagram section: only shown when the Instagram Feed plugin is active and has posts to show. */
add_filter( 'render_block', function ( $html, $block ) {
	if ( 'core/group' === ( $block['blockName'] ?? '' ) && preg_match( '/class="[^"]*\bhb-insta[\s"]/', $html ) ) {
		if ( ! shortcode_exists( 'instagram-feed' ) || false === strpos( $html, 'sb_instagram' ) ) {
			return '';
		}
	}
	return $html;
}, 12, 2 );

/**
 * Footer newsletter signup. Uses the existing MailPoet plugin: set the form with
 * wp option update ncah_mailpoet_form_id <id> (or in Tools > NCAH migrate). Until set, shows a mail link.
 */
add_shortcode('ncah_newsletter', function () {
    $id = (int) get_option('ncah_mailpoet_form_id', 1);
    if ($id && shortcode_exists('mailpoet_form')) return do_shortcode('[mailpoet_form id="' . $id . '"]');
    return '<p class="has-small-font-size">Newsletter signup coming soon. Email <a href="mailto:info@ncahamilton.ca?subject=Newsletter">info@ncahamilton.ca</a> to be added.</p>';
});

/** Annual Gala hero slide: shown until the end of December 5, 2026 (site time), then removed so the photo hero takes over. */
add_filter( 'render_block', function ( $html, $block ) {
	if ( 'core/group' === ( $block['blockName'] ?? '' ) && preg_match( '/^\s*<div class="[^"]*\bncah-gala-slide\b/', $html ) ) {
		if ( current_time( 'Y-m-d' ) > '2026-12-05' ) {
			return '';
		}
	}
	return $html;
}, 12, 2 );
