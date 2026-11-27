/**
 * NCAH photo lightbox.
 * Click any photo in a news post to view it large. Photos in the same gallery
 * can be browsed with the arrows, the keyboard (left, right, Escape) or a swipe.
 */
( function () {
	'use strict';

	var SCOPE = '.wp-block-post-content';
	var EXCLUDE = '.ncah-member-logos, .ncah-logos, .ncah-person__photo';

	function fullSrc( img ) {
		var best = img.currentSrc || img.src, bestW = 0;
		( img.getAttribute( 'srcset' ) || '' ).split( ',' ).forEach( function ( part ) {
			var bits = part.trim().split( /\s+/ ), w = parseInt( bits[ 1 ], 10 ) || 0;
			if ( bits[ 0 ] && w > bestW ) { bestW = w; best = bits[ 0 ]; }
		} );
		if ( ! bestW ) { best = best.replace( /-\d+x\d+(\.[a-z]+)(\?.*)?$/i, '$1' ); }
		return best;
	}

	// A photo is enlargeable when it has no link, or links straight to an image file.
	function plain( img ) {
		var a = img.closest( 'a' );
		return ! a || /\.(webp|jpe?g|png|gif|avif)(\?.*)?$/i.test( a.getAttribute( 'href' ) || '' );
	}

	function groups() {
		var root = document.querySelector( SCOPE );
		if ( ! root ) { return []; }
		var sets = [];
		var hasGallery = !! root.querySelector( '.wp-block-gallery' );
		// In a post with galleries, the first loose photo is its master (cover) image and is not enlarged.
		// In a post made only of loose photos, every photo belongs to the viewer.
		var master = hasGallery ? root.querySelector( '.wp-block-image img' ) : null;
		if ( master && master.closest( '.wp-block-gallery' ) ) { master = null; }
		root.querySelectorAll( '.wp-block-gallery' ).forEach( function ( g ) {
			if ( g.matches( EXCLUDE ) ) { return; }
			var imgs = [].slice.call( g.querySelectorAll( 'img' ) ).filter( plain );
			if ( imgs.length ) { sets.push( imgs ); }
		} );
		// Loose photos in one post are browsed together, so previous and next always work.
		var loose = [];
		root.querySelectorAll( '.wp-block-image img' ).forEach( function ( i ) {
			if ( i === master || i.closest( '.wp-block-gallery' ) || ! plain( i ) || i.closest( EXCLUDE ) ) { return; }
			loose.push( i );
		} );
		if ( loose.length ) { sets.push( loose ); }
		return sets;
	}

	var box, imgEl, capEl, countEl, prevBtn, nextBtn, current = [], index = 0, lastFocus = null;

	function build() {
		box = document.createElement( 'div' );
		box.className = 'ncah-lb';
		box.setAttribute( 'role', 'dialog' );
		box.setAttribute( 'aria-modal', 'true' );
		box.setAttribute( 'aria-label', 'Photo viewer' );
		box.innerHTML =
			'<button type="button" class="ncah-lb__close" aria-label="Close photo viewer">&times;</button>' +
			'<button type="button" class="ncah-lb__nav ncah-lb__prev" aria-label="Previous photo">&#8249;</button>' +
			'<figure class="ncah-lb__stage"><img class="ncah-lb__img" alt=""><figcaption class="ncah-lb__cap"></figcaption></figure>' +
			'<button type="button" class="ncah-lb__nav ncah-lb__next" aria-label="Next photo">&#8250;</button>' +
			'<div class="ncah-lb__count" aria-live="polite"></div>';
		document.body.appendChild( box );
		imgEl = box.querySelector( '.ncah-lb__img' );
		capEl = box.querySelector( '.ncah-lb__cap' );
		countEl = box.querySelector( '.ncah-lb__count' );
		prevBtn = box.querySelector( '.ncah-lb__prev' );
		nextBtn = box.querySelector( '.ncah-lb__next' );
		box.querySelector( '.ncah-lb__close' ).addEventListener( 'click', close );
		prevBtn.addEventListener( 'click', function () { go( -1 ); } );
		nextBtn.addEventListener( 'click', function () { go( 1 ); } );
		box.addEventListener( 'click', function ( e ) { if ( e.target === box || e.target.classList.contains( 'ncah-lb__stage' ) ) { close(); } } );
		var x0 = null;
		box.addEventListener( 'touchstart', function ( e ) { x0 = e.touches[ 0 ].clientX; }, { passive: true } );
		box.addEventListener( 'touchend', function ( e ) {
			if ( x0 === null ) { return; }
			var dx = e.changedTouches[ 0 ].clientX - x0;
			if ( Math.abs( dx ) > 45 ) { go( dx < 0 ? 1 : -1 ); }
			x0 = null;
		} );
		document.addEventListener( 'keydown', function ( e ) {
			if ( ! box.classList.contains( 'is-open' ) ) { return; }
			if ( e.key === 'Escape' ) { close(); }
			else if ( e.key === 'ArrowRight' ) { go( 1 ); }
			else if ( e.key === 'ArrowLeft' ) { go( -1 ); }
			else if ( e.key === 'Tab' ) {
				var f = [].slice.call( box.querySelectorAll( 'button' ) ).filter( function ( b ) { return b.offsetParent !== null; } );
				var i = f.indexOf( document.activeElement );
				e.preventDefault();
				f[ ( i + ( e.shiftKey ? -1 : 1 ) + f.length ) % f.length ].focus();
			}
		} );
	}

	function show() {
		var src = current[ index ];
		imgEl.classList.remove( 'is-loaded' );
		imgEl.onload = function () { imgEl.classList.add( 'is-loaded' ); };
		imgEl.src = fullSrc( src );
		imgEl.alt = src.alt || '';
		capEl.textContent = src.alt || '';
		capEl.hidden = ! src.alt;
		var many = current.length > 1;
		prevBtn.hidden = nextBtn.hidden = countEl.hidden = ! many;
		countEl.textContent = ( index + 1 ) + ' / ' + current.length;
		if ( many ) {
			[ index - 1, index + 1 ].forEach( function ( n ) {
				var t = current[ ( n + current.length ) % current.length ];
				( new Image() ).src = fullSrc( t );
			} );
		}
	}

	function go( step ) {
		if ( current.length < 2 ) { return; }
		index = ( index + step + current.length ) % current.length;
		show();
	}

	function open( set, i ) {
		if ( ! box ) { build(); }
		current = set; index = i; lastFocus = document.activeElement;
		show();
		box.classList.add( 'is-open' );
		document.documentElement.classList.add( 'ncah-lb-open' );
		box.querySelector( '.ncah-lb__close' ).focus();
	}

	function close() {
		box.classList.remove( 'is-open' );
		document.documentElement.classList.remove( 'ncah-lb-open' );
		imgEl.removeAttribute( 'src' );
		if ( lastFocus && lastFocus.focus ) { lastFocus.focus(); }
	}

	function init() {
		groups().forEach( function ( set ) {
			set.forEach( function ( img, i ) {
				img.classList.add( 'ncah-lb-thumb' );
				img.setAttribute( 'tabindex', '0' );
				img.setAttribute( 'role', 'button' );
				img.setAttribute( 'aria-label', 'Enlarge photo' + ( img.alt ? ': ' + img.alt : '' ) );
				img.addEventListener( 'click', function ( e ) { e.preventDefault(); open( set, i ); } );
				var link = img.closest( 'a' );
				if ( link ) { link.addEventListener( 'click', function ( e ) { e.preventDefault(); } ); }
				img.addEventListener( 'keydown', function ( e ) {
					if ( e.key === 'Enter' || e.key === ' ' ) { e.preventDefault(); open( set, i ); }
				} );
			} );
		} );
	}

	if ( document.readyState === 'loading' ) { document.addEventListener( 'DOMContentLoaded', init ); } else { init(); }
} )();
