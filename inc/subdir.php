<?php
/**
 * Subdirectory installs (for example a staging copy at /staging).
 * Theme content uses root-relative links such as /about-us/. When the site lives in a subdirectory,
 * prefix those links with the site path so navigation stays inside the same copy of the site.
 * On a site at the domain root this does nothing.
 */
add_filter( 'render_block', function ( $html, $block ) {
	$path = untrailingslashit( (string) wp_parse_url( home_url(), PHP_URL_PATH ) );
	if ( '' === $path || false === strpos( $html, 'href="/' ) ) {
		return $html;
	}
	$q = preg_quote( $path, '#' );
	return preg_replace( '#href="/(?!/|' . ltrim( $q, '/' ) . '(?:/|"))(?!wp-(?:content|admin|json|includes))#', 'href="' . $path . '/', $html );
}, 20, 2 );
