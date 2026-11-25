/*
 * NCAH motion layer script. No dependencies.
 * Cycles hero slides, and reveals blocks as they scroll into view.
 */
( function () {
	'use strict';

	var root = document.documentElement;
	root.classList.add( 'ncah-js' );

	var reduce = window.matchMedia && window.matchMedia( '(prefers-reduced-motion: reduce)' ).matches;
	var INTERVAL = 7000;

	function initHero( hero ) {
		var slides = Array.prototype.slice.call( hero.querySelectorAll( ':scope > .ncah-hero__slide' ) );
		if ( slides.length === 0 ) {
			return;
		}
		var current = 0;
		var timer = null;

		slides[ 0 ].classList.add( 'is-active' );
		if ( slides.length === 1 ) {
			return;
		}

		var dots = document.createElement( 'div' );
		dots.className = 'ncah-hero__dots';
		var buttons = slides.map( function ( slide, i ) {
			var b = document.createElement( 'button' );
			b.type = 'button';
			b.setAttribute( 'aria-label', 'Show slide ' + ( i + 1 ) + ' of ' + slides.length );
			b.addEventListener( 'click', function () {
				show( i );
				restart();
			} );
			dots.appendChild( b );
			return b;
		} );
		hero.appendChild( dots );

		var paused = false;
		var pauseBtn = document.createElement( 'button' );
		pauseBtn.type = 'button';
		pauseBtn.className = 'ncah-hero__pause';
		pauseBtn.setAttribute( 'aria-label', 'Pause slideshow' );
		pauseBtn.setAttribute( 'aria-pressed', 'false' );
		pauseBtn.innerHTML = '<svg class="i-pause" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg><svg class="i-play" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg>';
		pauseBtn.addEventListener( 'click', function () {
			paused = ! paused;
			pauseBtn.setAttribute( 'aria-pressed', paused ? 'true' : 'false' );
			pauseBtn.setAttribute( 'aria-label', paused ? 'Play slideshow' : 'Pause slideshow' );
			if ( paused ) { stop(); } else { start(); }
		} );
		hero.appendChild( pauseBtn );

		function show( index ) {
			slides[ current ].classList.remove( 'is-active' );
			current = ( index + slides.length ) % slides.length;
			slides[ current ].classList.add( 'is-active' );
			buttons.forEach( function ( b, i ) {
				if ( i === current ) {
					b.setAttribute( 'aria-current', 'true' );
				} else {
					b.removeAttribute( 'aria-current' );
				}
			} );
		}

		function start() {
			if ( reduce || timer || paused ) {
				return;
			}
			timer = window.setInterval( function () {
				show( current + 1 );
			}, INTERVAL );
		}
		function stop() {
			window.clearInterval( timer );
			timer = null;
		}
		function restart() {
			stop();
			start();
		}

		show( 0 );
		start();

		hero.addEventListener( 'mouseenter', stop );
		hero.addEventListener( 'mouseleave', start );
		hero.addEventListener( 'focusin', stop );
		hero.addEventListener( 'focusout', start );
		document.addEventListener( 'visibilitychange', function () {
			if ( document.hidden ) {
				stop();
			} else {
				start();
			}
		} );
	}

	function initReveal() {
		var items = document.querySelectorAll( '.ncah-reveal' );
		if ( ! items.length ) {
			return;
		}
		if ( reduce || ! ( 'IntersectionObserver' in window ) ) {
			items.forEach( function ( el ) {
				el.classList.add( 'is-visible' );
			} );
			return;
		}
		var io = new IntersectionObserver(
			function ( entries ) {
				entries.forEach( function ( entry ) {
					if ( entry.isIntersecting ) {
						entry.target.classList.add( 'is-visible' );
						io.unobserve( entry.target );
					}
				} );
			},
			{ threshold: 0.15, rootMargin: '0px 0px -5% 0px' }
		);
		items.forEach( function ( el ) {
			io.observe( el );
		} );
	}

	// Decorative floating shapes in the hero and on full-width coloured bands.
	function addShapes( el ) {
		if ( el.querySelector( ':scope > .ncah-shapes' ) ) {
			return;
		}
		var wrap = document.createElement( 'div' );
		wrap.className = 'ncah-shapes';
		wrap.setAttribute( 'aria-hidden', 'true' );
		for ( var i = 1; i <= 5; i++ ) {
			var s = document.createElement( 'span' );
			s.className = 'ncah-shape ncah-shape--' + i;
			wrap.appendChild( s );
		}
		el.classList.add( 'ncah-has-shapes' );
		el.insertBefore( wrap, el.firstChild );
	}

	// Logo rows become a slow sideways scroller (content duplicated once for a seamless loop).
	function initMarquee( row ) {
		if ( row.closest( '.ncah-marquee' ) || row.children.length < 4 ) {
			return;
		}
		var outer = document.createElement( 'div' );
		outer.className = 'ncah-marquee';
		row.parentNode.insertBefore( outer, row );
		outer.appendChild( row );
		row.classList.add( 'ncah-marquee__track' );
		Array.prototype.slice.call( row.children ).forEach( function ( child ) {
			var copy = child.cloneNode( true );
			copy.setAttribute( 'aria-hidden', 'true' );
			copy.querySelectorAll( 'img' ).forEach( function ( img ) { img.alt = ''; } );
			row.appendChild( copy );
		} );
		row.style.setProperty( '--ncah-marquee', ( row.children.length * 3 ) + 's' );
	}

	/* Mobile menu: add the logo at the top and Donate plus Instagram at the bottom of the overlay. */
	function initMobileMenu() {
		document.querySelectorAll( '.ncah-nav .wp-block-navigation__responsive-container-content' ).forEach( function ( box ) {
			if ( box.querySelector( '.ncah-menu-extra' ) ) { return; }
			var header = box.closest( 'header' ) || document;
			var logo = header.querySelector( '.ncah-logo img' );
			if ( logo ) {
				var top = document.createElement( 'div' );
				top.className = 'ncah-menu-extra ncah-menu-logo';
				var a = document.createElement( 'a' );
				var homeLink = header.querySelector( '.ncah-logo a' );
				a.href = homeLink ? homeLink.getAttribute( 'href' ) : '/';
				a.setAttribute( 'aria-label', 'Home' );
				var img = logo.cloneNode( false );
				img.removeAttribute( 'srcset' );
				img.removeAttribute( 'width' );
				img.removeAttribute( 'height' );
				a.appendChild( img );
				top.appendChild( a );
				box.insertBefore( top, box.firstChild );
			}
			var foot = document.createElement( 'div' );
			foot.className = 'ncah-menu-extra ncah-menu-foot';
			var donate = header.querySelector( '.ncah-donate a' );
			if ( donate ) {
				var d = donate.cloneNode( true );
				d.className = 'ncah-menu-donate';
				foot.appendChild( d );
			}
			var socials = header.querySelectorAll( '.ncah-topsocial a' );
			if ( socials.length ) {
				var row = document.createElement( 'div' );
				row.className = 'ncah-menu-socials';
				socials.forEach( function ( src ) {
					var l = src.cloneNode( true );
					l.className = 'ncah-menu-social';
					l.setAttribute( 'target', '_blank' );
					l.setAttribute( 'rel', 'noopener' );
					var t = ( l.textContent || '' ).trim();
					l.setAttribute( 'aria-label', t || ( /facebook/.test( l.href ) ? 'Facebook' : /instagram/.test( l.href ) ? 'Instagram' : 'YouTube' ) );
					row.appendChild( l );
				} );
				foot.appendChild( row );
			}
			var mail = document.createElement( 'a' );
			mail.className = 'ncah-menu-mail';
			mail.href = 'mailto:info@ncahamilton.ca';
			mail.textContent = 'info@ncahamilton.ca';
			foot.appendChild( mail );
			box.appendChild( foot );
			var here = location.pathname.replace( /\/+$/, '' ) || '/';
			box.querySelectorAll( '.wp-block-navigation__container > .wp-block-navigation-item > a.wp-block-navigation-item__content' ).forEach( function ( a ) {
				var p;
				try { p = new URL( a.href, location.href ).pathname.replace( /\/+$/, '' ) || '/'; } catch ( e ) { return; }
				if ( p === here ) { a.setAttribute( 'aria-current', 'page' ); }
			} );
		} );
	}

	/* Point the newsletter form's "Privacy Policy" link at the real page. */
	function fixPrivacyLinks() {
		document.querySelectorAll( '.mailpoet_form a' ).forEach( function ( a ) {
			var h = a.getAttribute( 'href' );
			if ( ( ! h || h === '#' ) && /privacy/i.test( a.textContent ) ) { a.setAttribute( 'href', '/privacy-policy/' ); }
		} );
	}

	/* Floating back-to-top button, shown once the visitor has scrolled down. */
	function initBackToTop() {
		if ( document.querySelector( '.ncah-top' ) ) { return; }
		var btn = document.createElement( 'button' );
		btn.type = 'button';
		btn.className = 'ncah-top';
		btn.setAttribute( 'aria-label', 'Back to top' );
		btn.innerHTML = '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" focusable="false"><path d="M12 5l-7 7 1.4 1.4L11 8.8V20h2V8.8l4.6 4.6L19 12z" fill="currentColor"/></svg><span class="ncah-top__label">Top</span>';
		document.body.appendChild( btn );
		var ticking = false;
		function update() {
			btn.classList.toggle( 'is-shown', window.scrollY > 500 );
			ticking = false;
		}
		window.addEventListener( 'scroll', function () {
			if ( ! ticking ) { ticking = true; window.requestAnimationFrame( update ); }
		}, { passive: true } );
		btn.addEventListener( 'click', function () {
			var reduce = window.matchMedia && window.matchMedia( '(prefers-reduced-motion: reduce)' ).matches;
			window.scrollTo( { top: 0, behavior: reduce ? 'auto' : 'smooth' } );
			var target = document.querySelector( '.wp-site-blocks a, .wp-site-blocks button' );
			if ( target ) { target.focus( { preventScroll: true } ); }
		} );
		update();
	}

	/* Header tightens after scrolling; thin progress bar shows how far down the page you are. */
	function initScrollUI() {
		var header = document.querySelector( '.wp-site-blocks > header' );
		var bar = document.createElement( 'div' );
		bar.className = 'ncah-progress';
		bar.setAttribute( 'aria-hidden', 'true' );
		document.body.appendChild( bar );
		var ticking = false;
		function update() {
			var max = document.documentElement.scrollHeight - window.innerHeight;
			var y = window.scrollY;
			bar.style.setProperty( '--ncah-p', max > 0 ? Math.min( 1, y / max ).toFixed( 4 ) : 0 );
			if ( header ) { header.classList.toggle( 'is-scrolled', y > 60 ); }
			ticking = false;
		}
		window.addEventListener( 'scroll', function () {
			if ( ! ticking ) { ticking = true; window.requestAnimationFrame( update ); }
		}, { passive: true } );
		window.addEventListener( 'resize', update );
		update();
	}

	// Section blend: each band fades in from the colour of the band above it, so the seam flows instead of cutting.
	function initBlend() {
		var content = document.querySelector( '.wp-block-post-content' );
		if ( ! content ) { return; }
		function toRgb( el ) {
			var c = window.getComputedStyle( el ).backgroundColor, m = c.match( /rgba?\(([^)]+)\)/ );
			if ( ! m ) { return [ 255, 255, 255 ]; }
			var p = m[1].split( ',' ).map( parseFloat );
			if ( p.length > 3 && p[3] === 0 ) { return [ 255, 255, 255 ]; }
			return [ p[0], p[1], p[2] ];
		}
		function skip( prev ) {
			var cs = window.getComputedStyle( prev );
			return prev.classList.contains( 'wp-block-cover' ) || prev.classList.contains( 'ncah-hero' ) || cs.backgroundImage !== 'none' ||
				( cs.backgroundColor === 'rgba(0, 0, 0, 0)' && prev.querySelector( ':scope > .wp-block-cover, :scope > .ncah-tiles, .ncah-tile' ) );
		}
		function apply( el, prev ) {
			if ( ! prev || skip( prev ) ) { return; }
			var a = toRgb( prev ), b = toRgb( el );
			if ( a[0] === b[0] && a[1] === b[1] && a[2] === b[2] ) { return; }
			el.style.setProperty( '--ncah-self', 'rgb(' + b.join( ',' ) + ')' );
			el.classList.add( 'ncah-edge' );
		}
		var kids = Array.prototype.slice.call( content.children ).filter( function ( k ) { return k.classList.contains( 'alignfull' ); } );
		kids.forEach( function ( el, i ) {
			if ( el.classList.contains( 'wp-block-cover' ) || el.classList.contains( 'ncah-hero' ) || el.querySelector( ':scope > .wp-block-cover, :scope > .ncah-tiles' ) ) { return; }
			apply( el, kids[ i - 1 ] );
		} );
		var footer = document.querySelector( '.ncah-footer' ), last = kids[ kids.length - 1 ];
		if ( footer && last ) { apply( footer, last ); }
	}

	function init() {
		initScrollUI();
		initMobileMenu();
		initBackToTop();
		initBlend();
		fixPrivacyLinks();
		document.querySelectorAll( '.ncah-hero' ).forEach( function ( hero ) {
			initHero( hero );
			addShapes( hero );
		} );
		document.querySelectorAll( '.wp-block-post-content > .alignfull.has-background:not(.ncah-hero)' ).forEach( function ( band ) {
			band.classList.add( 'ncah-band' );
			addShapes( band );
		} );
		document.querySelectorAll( '.ncah-logos' ).forEach( function ( row ) {
			if ( ! row.closest( '.ncah-partners' ) ) {
				initMarquee( row );
			}
		} );
		initReveal();
	}

	if ( document.readyState === 'loading' ) {
		document.addEventListener( 'DOMContentLoaded', init );
	} else {
		init();
	}
} )();
