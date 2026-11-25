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

/* Theme and upload images referenced with root-relative src (for example /wp-content/themes/ncah/...) stay inside the same copy of the site. */
add_filter( 'render_block', function ( $html ) {
	$path = untrailingslashit( (string) wp_parse_url( home_url(), PHP_URL_PATH ) );
	if ( '' === $path || false === strpos( $html, 'src="/wp-content/' ) ) {
		return $html;
	}
	return str_replace( 'src="/wp-content/', 'src="' . $path . '/wp-content/', $html );
}, 21 );
