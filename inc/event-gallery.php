<?php
/**
 * Event Gallery: year navigation (2023, 2024, ...) for the event posts, plus a redirect from the old /events/ page.
 */

/** Years that have published posts, oldest first. */
function ncah_event_years() {
	global $wpdb;
	$years = $wpdb->get_col( "SELECT DISTINCT YEAR(post_date) FROM {$wpdb->posts} WHERE post_type = 'post' AND post_status = 'publish' ORDER BY 1 ASC" );
	return array_map( 'intval', $years );
}

/** The year being viewed: ?event_year=YYYY, otherwise the newest year with posts. */
function ncah_event_year() {
	$years = ncah_event_years();
	$want  = isset( $_GET['event_year'] ) ? (int) $_GET['event_year'] : 0;
	if ( $want && in_array( $want, $years, true ) ) {
		return $want;
	}
	return $years ? end( $years ) : (int) gmdate( 'Y' );
}

/** [ncah_year_tabs] prints the year links. */
add_shortcode( 'ncah_year_tabs', function () {
	$years = ncah_event_years();
	if ( ! $years ) {
		return '';
	}
	$cur  = ncah_event_year();
	$base = get_permalink() ?: home_url( '/event-gallery/' );
	$out  = '<nav class="ncah-year-tabs" aria-label="Event Gallery years"><ul>';
	foreach ( $years as $y ) {
		$on   = ( $y === $cur );
		$out .= '<li><a href="' . esc_url( add_query_arg( 'event_year', $y, $base ) ) . '"' . ( $on ? ' class="is-active" aria-current="page"' : '' ) . '>' . (int) $y . '</a></li>';
	}
	return $out . '</ul></nav>';
} );

/** Filter the gallery grid to the chosen year. */
add_filter( 'query_loop_block_query_vars', function ( $vars, $block ) {
	if ( is_page( 'event-gallery' ) && isset( $vars['post_type'] ) && 'post' === $vars['post_type'] ) {
		$vars['date_query'] = array( array( 'year' => ncah_event_year() ) );
	}
	return $vars;
}, 10, 2 );

/** Old /events/ address goes to the Event Gallery. */
add_action( 'template_redirect', function () {
	$path = untrailingslashit( (string) wp_parse_url( home_url(), PHP_URL_PATH ) );
	$req  = isset( $_SERVER['REQUEST_URI'] ) ? strtok( $_SERVER['REQUEST_URI'], '?' ) : '';
	if ( trailingslashit( $path . '/events' ) === trailingslashit( $req ) ) {
		wp_safe_redirect( home_url( '/event-gallery/' ), 301 );
		exit;
	}
}, 1 );
