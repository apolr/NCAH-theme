<?php
/**
 * [ncah_videos]: a responsive grid of every video on the NCAH YouTube channel.
 * Reads the channel's public feed (cached for six hours), opens each video in an accessible
 * privacy-friendly player (youtube-nocookie) and falls back to a short list if the feed is unreachable.
 */

const NCAH_YT_CHANNEL_ID  = 'UCeir27VO9uFUOfSS5dL5e8Q';
const NCAH_YT_CHANNEL_URL = 'https://www.youtube.com/@NCAHamilton';

/** @return array<int,array{id:string,title:string,date:string}> */
function ncah_youtube_videos() {
	$cached = get_transient( 'ncah_yt_videos' );
	if ( is_array( $cached ) && $cached ) {
		return $cached;
	}
	$out = array();
	$res = wp_remote_get( 'https://www.youtube.com/feeds/videos.xml?channel_id=' . NCAH_YT_CHANNEL_ID, array( 'timeout' => 8 ) );
	if ( ! is_wp_error( $res ) && 200 === wp_remote_retrieve_response_code( $res ) ) {
		$xml = wp_remote_retrieve_body( $res );
		if ( preg_match_all( '#<entry>(.*?)</entry>#s', $xml, $entries ) ) {
			foreach ( $entries[1] as $e ) {
				if ( preg_match( '#<yt:videoId>([\w-]{11})</yt:videoId>#', $e, $id ) && preg_match( '#<title>(.*?)</title>#s', $e, $t ) ) {
					preg_match( '#<published>([^<]+)</published>#', $e, $d );
					$out[] = array( 'id' => $id[1], 'title' => html_entity_decode( $t[1], ENT_QUOTES, 'UTF-8' ), 'date' => $d[1] ?? '' );
				}
			}
		}
	}
	if ( $out ) {
		set_transient( 'ncah_yt_videos', $out, 6 * HOUR_IN_SECONDS );
		return $out;
	}
	// Fallback: videos already featured on the previous site.
	$fallback = array(
		'2C_wG8mLvjU' => 'Recap of the 2024 End of Year Multicultural Gala',
		're8Eo57vFz4' => 'Recap of the 2023 End of Year Gala',
		'kRSui43Jt0Y' => 'Games at the 2023 NCAH End of the Year Gala Nite',
		'MoHHh-VlVIk' => 'NCAH video',
		'wIr1ipqrP1g' => 'NCAH video',
		'OnTW_Swx1r0' => 'NCAH video',
	);
	foreach ( $fallback as $id => $title ) {
		$out[] = array( 'id' => $id, 'title' => $title, 'date' => '' );
	}
	return $out;
}

add_shortcode( 'ncah_videos', function () {
	$videos = ncah_youtube_videos();
	if ( ! $videos ) {
		return '';
	}
	ob_start();
	?>
	<div class="ncah-videos">
		<ul class="ncah-videos__grid">
			<?php foreach ( $videos as $v ) : ?>
				<li>
					<button type="button" class="ncah-video" data-video="<?php echo esc_attr( $v['id'] ); ?>" aria-label="<?php echo esc_attr( 'Play video: ' . $v['title'] ); ?>">
						<span class="ncah-video__thumb"><img src="<?php echo esc_url( 'https://i.ytimg.com/vi/' . $v['id'] . '/hqdefault.jpg' ); ?>" alt="" loading="lazy" decoding="async" width="480" height="360"><span class="ncah-video__play" aria-hidden="true"><svg viewBox="0 0 24 24" focusable="false"><path d="M8 5v14l11-7z"/></svg></span></span>
						<span class="ncah-video__title"><?php echo esc_html( $v['title'] ); ?></span>
						<?php if ( $v['date'] ) : ?><span class="ncah-video__date"><?php echo esc_html( wp_date( 'F j, Y', strtotime( $v['date'] ) ) ); ?></span><?php endif; ?>
					</button>
				</li>
			<?php endforeach; ?>
		</ul>
		<p class="ncah-videos__more"><a class="wp-block-button__link wp-element-button" href="<?php echo esc_url( NCAH_YT_CHANNEL_URL ); ?>" target="_blank" rel="noopener">Visit our YouTube channel</a></p>
		<dialog class="ncah-video-dialog" aria-label="Video player">
			<button type="button" class="ncah-video-dialog__close" aria-label="Close video">&times;</button>
			<div class="ncah-video-dialog__frame"></div>
		</dialog>
	</div>
	<script>
	( function () {
		var root = document.currentScript.previousElementSibling; if ( ! root ) { return; }
		var dlg = root.querySelector( 'dialog' ), frame = root.querySelector( '.ncah-video-dialog__frame' ), last = null;
		if ( ! dlg || typeof dlg.showModal !== 'function' ) { root.querySelectorAll( '.ncah-video' ).forEach( function ( b ) { b.addEventListener( 'click', function () { window.open( 'https://www.youtube.com/watch?v=' + b.dataset.video, '_blank', 'noopener' ); } ); } ); return; }
		function close() { dlg.close(); }
		root.querySelectorAll( '.ncah-video' ).forEach( function ( b ) {
			b.addEventListener( 'click', function () {
				last = b;
				frame.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + encodeURIComponent( b.dataset.video ) + '?autoplay=1&rel=0" title="' + ( b.querySelector( '.ncah-video__title' ).textContent || 'Video' ).replace( /"/g, '' ) + '" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>';
				dlg.showModal();
			} );
		} );
		dlg.addEventListener( 'close', function () { frame.innerHTML = ''; if ( last ) { last.focus(); } } );
		dlg.addEventListener( 'click', function ( e ) { if ( e.target === dlg ) { close(); } } );
		dlg.querySelector( '.ncah-video-dialog__close' ).addEventListener( 'click', close );
	} )();
	</script>
	<?php
	return ob_get_clean();
} );
